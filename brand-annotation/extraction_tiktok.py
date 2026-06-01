import re
import csv

# ============================================
# ALGORITHME TIKTOK — Détection de Partenariats
# ============================================

RE_COLLAB_COMM = re.compile(r"collaboration\s+commerciale?", re.I)
RE_HASHTAG_AD = re.compile(r"#ad\b", re.I)
RE_PUBLICITE = re.compile(r"publicit[eéè]", re.I)  # optionnel (voir note)
RE_PROMO_SITE = re.compile(
    r"profitez de\s+(?:-|moins\s+)?\d+%\s+sur\s+(?:tout\s+le\s+site|le\s+site)\s+.{0,30}code",
    re.I,
)
RE_SPONSORED = re.compile(r"#sponsor(?:ed|is[eéè])", re.I)


def detect_tiktok_partnership(
    title: str,
    description: str,
    include_publicite: bool = False,
) -> dict:
    """
    Détecte si un post TikTok contient un partenariat commercial.

    Paramètres
    ----------
    title              : str  – Titre du post
    description        : str  – Description / légende du post
    include_publicite  : bool – Inclure la règle 'Publicité' (défaut False).
                                Active = +recall mais +FP sur certaines annotations.

    Retourne
    --------
    dict avec :
        detected : bool
        brands   : list[str]   – @mentions extraites si partenariat détecté
        rules    : list[str]
    """
    desc_lower = (description or "").lower()
    title_lower = (title or "").lower()
    full_text = desc_lower + " " + title_lower

    detected = False
    brands = set()
    rules = []

    # RÈGLE 1 : "Collaboration commerciale / commercial"
    if RE_COLLAB_COMM.search(full_text):
        detected = True
        rules.append("COLLAB_COMMERCIALE")

    # RÈGLE 2 : #ad
    if RE_HASHTAG_AD.search(full_text):
        detected = True
        rules.append("HASHTAG_AD")

    # RÈGLE 3 (optionnelle) : "Publicité"
    if include_publicite and RE_PUBLICITE.search(full_text):
        detected = True
        rules.append("PUBLICITE")

    # RÈGLE 4 : "Profitez de -X% sur tout le site avec le code"
    if RE_PROMO_SITE.search(full_text):
        detected = True
        rules.append("PROMO_SITE_CODE")

    # RÈGLE 5 : #sponsored / #sponsorisé
    if RE_SPONSORED.search(full_text):
        detected = True
        rules.append("HASHTAG_SPONSORED")

    # Extraction des @mentions si partenariat détecté
    if detected:
        mentions = re.findall(r"@([\w.\-]+)", full_text)
        for m in mentions:
            if len(m) > 2:
                brands.add(m)

    return {"detected": detected, "brands": list(brands), "rules": rules}


# ============================================
# ÉVALUATION
# ============================================
def evaluate_tiktok(csv_path: str, include_publicite: bool = False) -> None:
    """
    Lit le CSV exporté de la feuille 'TikTok' et évalue l'algorithme.

    Le CSV doit avoir les colonnes :
        Title, Description, SN Brand, SN Has Paid Placement,
        Brand - Ajout Manuel, Account Name, Social Network,
        Post Url, Post Type, Partenariat_Détecté, Partenaire(s),
        Marqueur_Regex
    """
    TP = FP = FN = TN = 0
    fn_details = []
    fp_details = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            title = row.get("Title", "")
            description = row.get("Description", "")
            gt = row.get("Partenariat_Détecté", "").strip()
            gt_partner = row.get("Partenaire(s)", "")

            if gt not in ("Oui", "Non"):
                continue

            result = detect_tiktok_partnership(
                title, description, include_publicite=include_publicite
            )

            if gt == "Oui":
                if result["detected"]:
                    TP += 1
                else:
                    FN += 1
                    fn_details.append(
                        {
                            "row": i,
                            "title": title[:60],
                            "partner": gt_partner,
                        }
                    )
            elif gt == "Non":
                if result["detected"]:
                    FP += 1
                    fp_details.append(
                        {
                            "row": i,
                            "title": title[:60],
                            "rules": result["rules"],
                            "account": row.get("Account Name", ""),
                        }
                    )
                else:
                    TN += 1

    total = TP + FP + FN + TN
    recall = TP / (TP + FN) if (TP + FN) else 0
    fpr = FP / (FP + TN) if (FP + TN) else 0
    miss_rate = FN / (FN + TP) if (FN + TP) else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    mode = "AVEC" if include_publicite else "SANS"
    print("=" * 55)
    print(f"  TIKTOK — Résultats ({mode} règle 'publicité')")
    print("=" * 55)
    print(f"  Total annotées        : {total}")
    print(f"  Vrais Positifs  (TP)  : {TP}")
    print(f"  Faux Positifs   (FP)  : {FP}")
    print(f"  Faux Négatifs   (FN)  : {FN}")
    print(f"  Vrais Négatifs  (TN)  : {TN}")
    print("-" * 55)
    print(f"  % Résultats Corrects  : {recall:.1%}")
    print(f"  % Faux Positifs       : {fpr:.1%}")
    print(f"  % Loupés              : {miss_rate:.1%}")
    print(f"  Précision             : {precision:.1%}")
    print(f"  F1-Score              : {f1:.1%}")
    print("=" * 55)

    if fn_details:
        print(f"\n  Faux Négatifs ({len(fn_details)}) :")
        for d in fn_details:
            print(f"    Ligne {d['row']} | {d['title']} | Partenaire: {d['partner']}")

    if fp_details:
        print(f"\n  Faux Positifs ({len(fp_details)}, top 15) :")
        for d in fp_details[:15]:
            print(f"    Ligne {d['row']} | @{d['account']} | Règles: {d['rules']}")


# --- Point d'entrée ---
if __name__ == "__main__":
    # Version recommandée (sans publicité) : 100% recall, 0.05% FPR
    evaluate_tiktok("tiktok.csv", include_publicite=False)

    print("\n")

    # Version avec publicité : 100% recall, 2.3% FPR
    # (les 271 FP sont probablement des erreurs d'annotation)
    evaluate_tiktok("tiktok.csv", include_publicite=True)
