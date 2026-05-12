import re
import csv
from collections import Counter
from difflib import SequenceMatcher

# ============================================
# ALGORITHME INSTAGRAM — Détection de Partenariats
# ============================================

# --- Regex compilées pour chaque règle ---
RE_PUBLICITE = re.compile(r"publicit[eéè]", re.I)
RE_COLLAB_COMM = re.compile(r"collaboration\s+commerciale?", re.I)
RE_HASHTAG_COLLAB = re.compile(r"#collab(?:oration)?\b", re.I)
RE_HASHTAG_AD = re.compile(r"#ad\b", re.I)
RE_HASHTAG_SPONSORED = re.compile(r"#sponsor(?:ed|is[eéè])\b", re.I)
RE_HASHTAG_PARTENARIAT = re.compile(r"#partenariat\b", re.I)
RE_EN_PARTENARIAT = re.compile(r"en partenariat avec", re.I)
RE_PRESENTE_PAR = re.compile(r"présenté(?:e)?\s+par", re.I)
RE_OFFERT_PAR = re.compile(r"offert(?:s|e|es)?\s+par", re.I)
RE_PRODUITS_OFF = re.compile(r"produits?\s+offerts?", re.I)
RE_SPONSORISE = re.compile(r"sponsoris[eéè]", re.I)
RE_CODE_PROMO = re.compile(
    r"(?:tapez|utilisez|avec)\s+(?:mon\s+)?code\s+[A-Z0-9]{3,}"
    r"|(?:mon\s+)?code\s+(?:promo|réduction|réduc|de\s+réduction)\s*:?\s*\*{0,2}[A-Z0-9]{3,}\*{0,2}",
    re.I,
)
RE_LIEN_BIO = re.compile(r"lien\s+en\s+bio", re.I)
RE_INVITATION = re.compile(r"\*?invitation\*?", re.I)
RE_COLLAB_COMM_HASH = re.compile(r"#collaborationcommerciale", re.I)
RE_COLLAB_ASTERISK = re.compile(r"collaboration\s*\*", re.I)
RE_OFFERT_ASTERISK = re.compile(r"\*offert\*?|\boffert\*", re.I)
RE_AMBASSADEUR = re.compile(r"\bambassad(?:eur[s]?|rice[s]?)\b", re.I)
RE_CONCOURS = re.compile(r"(?:grand\s+)?(?:jeu\s+)?concours", re.I)
RE_COLLAB_WORD = re.compile(r"\bcollab\b", re.I)
RE_GIFT = re.compile(r"\*?gift\*?", re.I)
# --- Nouvelles regex (signaux forts) ---
RE_PARTENARIAT_REMUNERE = re.compile(r"partenariat\s+r[eéè]mun[eéè]r[eéè]", re.I)
RE_PAID_PARTNERSHIP = re.compile(r"paid\s+partnership", re.I)
RE_HASHTAG_PUB = re.compile(r"#pub\b", re.I)
RE_HASHTAG_SPONSO = re.compile(r"#sponso\b", re.I)
RE_HASHTAG_GIFTED = re.compile(r"#gifted\b", re.I)
RE_HASHTAG_PR = re.compile(r"#pr\b", re.I)
RE_RECU_GRATUIT = re.compile(r"re[cç]u\s+(?:en\s+cadeau|gratuitement)", re.I)
RE_ENVOYE_PAR = re.compile(r"envoy[eéè]e?\s+par", re.I)
RE_AFFILIATION = re.compile(r"(?:lien|code)\s+d['\u2019]affiliation", re.I)
RE_COLLAB_REMUNEREE = re.compile(r"collaboration\s+r[eéè]mun[eéè]r[eéè]e?\*?", re.I)


# 1. Extraire si un post est considéré comme sponsorisé ou non:

# 2. Extraire les marques sponsorisées par influ:

# 3.

# collaboration rémunérée

# collaborationnonrémunérée

# ============================================
# EXTRACTION CONTEXTUELLE DE LA MARQUE
# ============================================
# Chaque pattern capture le @handle de la marque à proximité d'un signal de partenariat.
# Ordonnés du plus précis au plus générique — on s'arrête au premier match.
_PARTNERSHIP_SIGNALS = [
    re.compile(r"publicit[eéè]", re.I),
    re.compile(r"collaboration\s+commerciale?", re.I),
    re.compile(r"#collab(?:oration)?\b", re.I),
    re.compile(r"#ad\b", re.I),
    re.compile(r"#sponsor(?:ed|is[eéè])\b", re.I),
    re.compile(r"#partenariat\b", re.I),
    re.compile(r"en partenariat avec", re.I),
    re.compile(r"présenté(?:e)?\s+par", re.I),
    re.compile(r"offert(?:s|e|es)?\s+par", re.I),
    re.compile(r"produits?\s+offerts?", re.I),
    re.compile(r"sponsoris[eéè]", re.I),
    re.compile(r"\bambassad(?:eur[s]?|rice[s]?)\b", re.I),
    re.compile(r"\bcollab\b", re.I),
    re.compile(r"\*?gift\*?", re.I),
    re.compile(r"merci\s+(?:à|pour)\b", re.I),
]

_RE_MENTION = re.compile(r"@([\w.\-]{3,})")


def extract_primary_brand(description: str) -> str | None:
    mentions = [(m.start(), m.group(1)) for m in _RE_MENTION.finditer(description)]

    if not mentions:
        return None

    signal_positions = []
    for pat in _PARTNERSHIP_SIGNALS:
        for m in pat.finditer(description):
            signal_positions.append((m.start() + m.end()) // 2)

    if not signal_positions:
        return mentions[0][1]

    first_signal = min(signal_positions)
    mentions_before = [(pos, h) for pos, h in mentions if pos < first_signal]

    if mentions_before:
        _, handle = min(mentions_before, key=lambda t: first_signal - t[0])
        return handle

    def min_dist(pos: int) -> int:
        return min(abs(pos - sig) for sig in signal_positions)

    _, handle = min(mentions, key=lambda t: min_dist(t[0]))
    return handle


def detect_instagram_partnership(
    title: str,
    description: str,
    sn_brand: str,
    paid_placement: bool,
) -> dict:
    """
    Détecte si un post Instagram contient un partenariat commercial.

    Paramètres
    ----------
    title         : str  – Titre du post (souvent vide sur Instagram)
    description   : str  – Légende du post
    sn_brand      : str  – Compte marque tagué par Instagram (Scrappé - SN Brand)
    paid_placement: bool – Flag Instagram "Paid Partnership" (Scrappé - SN Has Paid Placement)

    Retourne
    --------
    dict avec :
        detected : bool
        brands   : list[str]  – Marques identifiées (@mentions si partenariat détecté)
        rules    : list[str]
    """
    full_text = ((description or "") + " " + (title or "")).lower()

    detected = False
    brands = set()
    rules = []

    # RÈGLE 1 : Flag Instagram "Paid Partnership"
    if paid_placement:
        detected = True
        rules.append("PAID_PLACEMENT")
        if sn_brand:
            brands.add(sn_brand)

    # RÈGLE 2 : Compte marque tagué par Instagram (SN Brand)
    if sn_brand:
        detected = True
        rules.append("SN_BRAND_TAG")
        brands.add(sn_brand)

    # RÈGLE 3 : "Publicité" dans la légende
    if RE_PUBLICITE.search(full_text):
        detected = True
        rules.append("PUBLICITE")

    # RÈGLE 4 : "Collaboration commerciale"
    if RE_COLLAB_COMM.search(full_text):
        detected = True
        rules.append("COLLAB_COMMERCIALE")

    # RÈGLE 5 : #collab / #collaboration
    if RE_HASHTAG_COLLAB.search(full_text):
        detected = True
        rules.append("HASHTAG_COLLAB")

    # RÈGLE 6 : #ad
    if RE_HASHTAG_AD.search(full_text):
        detected = True
        rules.append("HASHTAG_AD")

    # RÈGLE 7 : #sponsored / #sponsorisé
    if RE_HASHTAG_SPONSORED.search(full_text):
        detected = True
        rules.append("HASHTAG_SPONSORED")

    # RÈGLE 8 : #partenariat
    if RE_HASHTAG_PARTENARIAT.search(full_text):
        detected = True
        rules.append("HASHTAG_PARTENARIAT")

    # RÈGLE 9 : "en partenariat avec"
    if RE_EN_PARTENARIAT.search(full_text):
        detected = True
        rules.append("EN_PARTENARIAT")

    # RÈGLE 10 : "présenté par"
    if RE_PRESENTE_PAR.search(full_text):
        detected = True
        rules.append("PRESENTE_PAR")

    # RÈGLE 11 : "offert par" / "produits offerts"
    if RE_OFFERT_PAR.search(full_text) or RE_PRODUITS_OFF.search(full_text):
        detected = True
        rules.append("OFFERT_PAR")

    # RÈGLE 12 : "sponsorisé" (hors hashtag)
    if RE_SPONSORISE.search(full_text):
        detected = True
        rules.append("SPONSORISE")

    # RÈGLE 13 : Code promo ("tapez mon code XXXX", "code **XXXX**")
    if RE_CODE_PROMO.search(full_text):
        detected = True
        rules.append("CODE_PROMO")

    # RÈGLE 14 : "invitation" / "*invitation*" (événement offert)
    if RE_INVITATION.search(full_text):
        detected = True
        rules.append("INVITATION")

    # RÈGLE 15 : #collaborationcommerciale (sans espace)
    if RE_COLLAB_COMM_HASH.search(full_text):
        detected = True
        rules.append("HASH_COLLAB_COMM")

    # RÈGLE 16 : "collaboration*" (astérisque = disclosure implicite)
    if RE_COLLAB_ASTERISK.search(full_text):
        detected = True
        rules.append("COLLAB_ASTERISK")

    # RÈGLE 17 : "*offert*" (produit offert avec astérisque)
    if RE_OFFERT_ASTERISK.search(full_text):
        detected = True
        rules.append("OFFERT_ASTERISK")

    # RÈGLE 18 : "ambassadeur / ambassadeurs / ambassadrice / ambassadrices"
    if RE_AMBASSADEUR.search(full_text):
        detected = True
        rules.append("AMBASSADRICE")

    # RÈGLE 19 : "concours" / "jeu concours" (giveaway sponsorisé)
    if RE_CONCOURS.search(full_text):
        detected = True
        rules.append("CONCOURS")

    # RÈGLE 20 : "collab" (mot seul, hors hashtag)
    if RE_COLLAB_WORD.search(full_text):
        detected = True
        rules.append("COLLAB_WORD")

    # RÈGLE 21 : "*gift*" / "gift" (produit offert anglophone)
    if RE_GIFT.search(full_text):
        detected = True
        rules.append("GIFT")

    # RÈGLE 22 : "partenariat rémunéré" (label officiel Instagram FR)
    if RE_PARTENARIAT_REMUNERE.search(full_text):
        detected = True
        rules.append("PARTENARIAT_REMUNERE")

    # RÈGLE 23 : "paid partnership" (label officiel Instagram EN)
    if RE_PAID_PARTNERSHIP.search(full_text):
        detected = True
        rules.append("PAID_PARTNERSHIP")

    # RÈGLE 24 : #pub (marqueur de transparence FR très courant)
    if RE_HASHTAG_PUB.search(full_text):
        detected = True
        rules.append("HASHTAG_PUB")

    # RÈGLE 25 : #sponso (variante informelle FR)
    if RE_HASHTAG_SPONSO.search(full_text):
        detected = True
        rules.append("HASHTAG_SPONSO")

    # RÈGLE 26 : #gifted (produit offert, anglophone)
    if RE_HASHTAG_GIFTED.search(full_text):
        detected = True
        rules.append("HASHTAG_GIFTED")

    # RÈGLE 27 : #pr (envoi presse)
    if RE_HASHTAG_PR.search(full_text):
        detected = True
        rules.append("HASHTAG_PR")

    # RÈGLE 28 : "reçu en cadeau" / "reçu gratuitement"
    if RE_RECU_GRATUIT.search(full_text):
        detected = True
        rules.append("RECU_GRATUIT")

    # RÈGLE 29 : "envoyé par" (produit envoyé par une marque)
    if RE_ENVOYE_PAR.search(full_text):
        detected = True
        rules.append("ENVOYE_PAR")

    # RÈGLE 30 : "lien/code d'affiliation"
    if RE_AFFILIATION.search(full_text):
        detected = True
        rules.append("AFFILIATION")

    if RE_COLLAB_REMUNEREE.search(full_text):
        detected = True
        rules.append("COLLAB_REMUNEREE")

    # Extraction de la marque principale (contextuelle) + toutes les @mentions
    if detected:
        primary = extract_primary_brand(description or "")
        if primary:
            brands.add(primary)
        # Toutes les @mentions en complément
        for m in re.findall(r"@([\w.\-]+)", full_text):
            if len(m) > 2:
                brands.add(m)

    return {"detected": detected, "brands": list(brands), "rules": rules}


# ============================================
# HELPERS
# ============================================


def _normalize_brand(s: str) -> str:
    """
    Normalise un nom de marque pour la comparaison souple :
    - minuscules, supprime le @ initial
    - supprime espaces, points, tirets, underscores (ex. "MEMO PARIS" → "memoparis", "memo.paris" → "memoparis")
    - supprime les chiffres en fin de chaîne (ex. "kinesthetique13" → "kinesthetique")
    """
    s = s.lower().lstrip("@")
    s = re.sub(r"[\s.\-_]", "", s)
    s = re.sub(r"\d+$", "", s)
    return s


_FUZZY_THRESHOLD = 0.82  # ratio SequenceMatcher minimum pour un match flou


def _brands_match(gt: str, extracted: str) -> bool:
    """
    Retourne True si les deux noms de marque désignent probablement la même entité.
    Deux niveaux :
      1. Substring après normalisation  (ex. "BDK PARFUMS" ↔ "bdkparfumsparis")
      2. Similarité fuzzy via SequenceMatcher  (ex. "KINESTETIQUE" ↔ "kinesthetique")
    """
    gt_n = _normalize_brand(gt)
    ext_n = _normalize_brand(extracted)
    if not gt_n or not ext_n:
        return False
    if gt_n in ext_n or ext_n in gt_n:
        return True
    ratio = SequenceMatcher(None, gt_n, ext_n).ratio()
    return ratio >= _FUZZY_THRESHOLD


def _print_metrics(label: str, TP: int, FP: int, FN: int, TN: int):
    total = TP + FP + FN + TN
    recall = TP / (TP + FN) if (TP + FN) else 0
    fpr = FP / (FP + TN) if (FP + TN) else 0
    miss_rate = FN / (FN + TP) if (FN + TP) else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print("=" * 60)
    print(f"  {label}")
    print("=" * 60)
    print(f"  Total annotées          : {total}")
    print(f"  Vrais Positifs  (TP)    : {TP}")
    print(f"  Faux Positifs   (FP)    : {FP}")
    print(f"  Faux Négatifs   (FN)    : {FN}")
    print(f"  Vrais Négatifs  (TN)    : {TN}")
    print("-" * 60)
    print(f"  Recall (% détectés)     : {recall:.1%}")
    print(f"  Précision               : {precision:.1%}")
    print(f"  F1-Score                : {f1:.1%}")
    print(f"  Taux de faux positifs   : {fpr:.1%}")
    print(f"  Taux de loupés          : {miss_rate:.1%}")
    print("=" * 60)


# ============================================
# ÉVALUATION DU SCRAPING
# ============================================


def evaluate_scraping(csv_path: str):
    """
    Évalue la qualité du scraping Instagram :
    - Signal scrappé  : SN Brand non vide OU SN Has Paid Placement == true
    - Ground truth    : DA - Manuel Collab Brand non vide
    """
    TP = FP = FN = TN = 0
    fn_details = []
    fp_details = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            gt_brand = row.get("DA - Manuel Collab Brand", "").strip()
            sn_brand = row.get("Scrappé - SN Brand", "").strip()
            paid_raw = row.get("Scrappé - SN Has Paid Placement", "").strip()
            paid = paid_raw.lower() in ("true", "1", "vrai")
            desc = row.get("Description", "")
            account = row.get("DA - Key Account", "")

            gt_brand = gt_brand.replace("-", "")
            gt_positive = bool(gt_brand)  # ground truth
            scraped_hit = bool(sn_brand) or paid  # signal scrappé

            if gt_positive:
                if scraped_hit:
                    TP += 1
                else:
                    FN += 1
                    fn_details.append(
                        {
                            "row": i,
                            "account": account,
                            "gt_brand": gt_brand,
                            "desc": desc.replace("\n", " "),
                        }
                    )
            else:
                if scraped_hit:
                    FP += 1
                    fp_details.append(
                        {
                            "row": i,
                            "account": account,
                            "sn_brand": sn_brand,
                            "paid": paid,
                            "desc": desc.replace("\n", " "),
                        }
                    )
                else:
                    TN += 1

    _print_metrics(
        "INSTAGRAM — Qualité du Scraping (SN Brand / Paid Placement)", TP, FP, FN, TN
    )

    if fn_details:
        print(f"\n  Faux Négatifs — non scrappés ({len(fn_details)}, top 20) :")
        for d in fn_details[:20]:
            print(
                f"    Ligne {d['row']:4d} | @{d['account']:<25} | GT={d['gt_brand']:<20} | {d['desc']}"
            )

    if fp_details:
        print(f"\n  Faux Positifs — scrappés sans annotation ({len(fp_details)}) :")
        for d in fp_details[:10]:
            print(
                f"    Ligne {d['row']:4d} | @{d['account']:<25} | SN={d['sn_brand']:<20} Paid={d['paid']} | {d['desc']}"
            )

    # Règles qui ont couvert les TP
    print(f"\n  Distribution des signaux scrappés sur les TP :")
    tp_with_sn = sum(1 for d in [] if True)  # recompute inline
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    pos_rows = [r for r in rows if r.get("DA - Manuel Collab Brand", "").strip()]
    both = sum(
        1
        for r in pos_rows
        if r.get("Scrappé - SN Brand", "").strip()
        and r.get("Scrappé - SN Has Paid Placement", "").lower() in ("true", "1")
    )
    sn_only = sum(
        1
        for r in pos_rows
        if r.get("Scrappé - SN Brand", "").strip()
        and r.get("Scrappé - SN Has Paid Placement", "").lower() not in ("true", "1")
    )
    paid_only = sum(
        1
        for r in pos_rows
        if not r.get("Scrappé - SN Brand", "").strip()
        and r.get("Scrappé - SN Has Paid Placement", "").lower() in ("true", "1")
    )
    print(f"    SN Brand + Paid Placement : {both}")
    print(f"    SN Brand seul             : {sn_only}")
    print(f"    Paid Placement seul        : {paid_only}")


# ============================================
# ÉVALUATION DU REGEX
# ============================================


def evaluate_regex(csv_path: str):
    """
    Évalue la qualité de la détection par regex Instagram.
    Ground truth : DA - Manuel Collab Brand non vide = partenariat.
    """
    TP = FP = FN = TN = 0
    fn_details = []
    fp_details = []
    rule_counts = Counter()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            gt_brand = row.get("DA - Manuel Collab Brand", "").strip()
            title = row.get("Title", "")
            description = row.get("Description", "")
            sn_brand = row.get("Scrappé - SN Brand", "").strip()
            paid_raw = row.get("Scrappé - SN Has Paid Placement", "").strip()
            paid = paid_raw.lower() in ("true", "1", "vrai")
            account = row.get("DA - Key Account", "")

            gt_brand = gt_brand.replace("-", "")

            gt_positive = bool(gt_brand)
            result = detect_instagram_partnership(title, description, sn_brand, paid)

            for r in result["rules"]:
                rule_counts[r] += 1

            if gt_positive:
                if result["detected"]:
                    TP += 1
                else:
                    FN += 1
                    fn_details.append(
                        {
                            "row": i,
                            "account": account,
                            "gt_brand": gt_brand,
                            "desc": description.replace("\n", " "),
                        }
                    )
            else:
                if result["detected"]:
                    FP += 1
                    fp_details.append(
                        {
                            "row": i,
                            "account": account,
                            "rules": result["rules"],
                            "desc": description.replace("\n", " "),
                        }
                    )
                else:
                    TN += 1

    _print_metrics("INSTAGRAM — Qualité du Regex (toutes règles)", TP, FP, FN, TN)

    print(f"\n  Déclenchements par règle (sur l'ensemble du dataset) :")
    for rule, count in rule_counts.most_common():
        print(f"    {rule:<25} : {count}")

    if fn_details:
        print(f"\n  Faux Négatifs — non détectés par regex ({len(fn_details)}) :")
        for d in fn_details[:50]:
            print(
                f"    Ligne {d['row']:4d} | @{d['account']:<25} | GT={d['gt_brand']:<20} | {d['desc']}"
            )

    if fp_details:
        print(f"\n  Faux Positifs — détectés à tort ({len(fp_details)}, top 20) :")
        for d in fp_details:
            print(
                f"    Ligne {d['row']:4d} | @{d['account']:<25} | Règles={d['rules']} | {d['desc']}"
            )


# ============================================
# ÉVALUATION REGEX SANS SCRAPING
# ============================================


def evaluate_regex_only(csv_path: str):
    """
    Évalue uniquement les règles textuelles (sans SN Brand ni Paid Placement),
    pour mesurer la valeur ajoutée du regex indépendamment du scraping.
    """
    TP = FP = FN = TN = 0
    fn_details = []
    fp_details = []
    rule_counts = Counter()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            gt_brand = row.get("DA - Manuel Collab Brand", "").strip()
            title = row.get("Title", "")
            description = row.get("Description", "")
            account = row.get("DA - Key Account", "")

            gt_brand = gt_brand.replace("-", "")
            gt_positive = bool(gt_brand)
            # On passe sn_brand="" et paid=False pour isoler le regex pur
            result = detect_instagram_partnership(
                title, description, sn_brand="", paid_placement=False
            )

            for r in result["rules"]:
                rule_counts[r] += 1

            if gt_positive:
                if result["detected"]:
                    TP += 1
                else:
                    FN += 1
                    fn_details.append(
                        {
                            "row": i,
                            "account": account,
                            "gt_brand": gt_brand,
                            "desc": description.replace("\n", " "),
                        }
                    )
            else:
                if result["detected"]:
                    FP += 1
                    fp_details.append(
                        {
                            "row": i,
                            "account": account,
                            "rules": result["rules"],
                            "desc": description.replace("\n", " "),
                        }
                    )
                else:
                    TN += 1

    _print_metrics(
        "INSTAGRAM — Regex seul (sans SN Brand / Paid Placement)", TP, FP, FN, TN
    )

    print(f"\n  Déclenchements par règle :")
    for rule, count in rule_counts.most_common():
        print(f"    {rule:<25} : {count}")

    if fn_details:
        print(f"\n  Faux Négatifs ({len(fn_details)}) :")
        for d in fn_details[:20]:
            print(
                f"    Ligne {d['row']:4d} | @{d['account']:<25} | GT={d['gt_brand']:<20} | {d['desc']}"
            )

    if fp_details:
        print(f"\n  Faux Positifs ({len(fp_details)}, top 20) :")
        for d in fp_details[:20]:
            print(
                f"    Ligne {d['row']:4d} | @{d['account']:<25} | Règles={d['rules']} | {d['desc']}"
            )


# ============================================
# ÉVALUATION DE L'EXTRACTION DE MARQUE
# ============================================


def evaluate_brand_extraction(csv_path: str):
    """
    Évalue la précision de extract_primary_brand() sur les vrais positifs détectés
    par le regex.

    Pour chaque post correctement détecté comme partenariat (TP), compare le
    @handle extrait par extract_primary_brand() au compte de marque annoté manuellement
    (DA - Manuel Collab Brand).

    Méthode de comparaison : normalisation souple via _brands_match() —
    supprime espaces/points/tirets et chiffres terminaux avant comparaison,
    ce qui tolère "MEMO PARIS" ↔ "memo.paris", "BDK PARFUMS" ↔ "bdkparfumsparis", etc.
    """
    total_tp = 0
    exact = 0  # handle exact ou sous-chaîne matchée
    partial = 0  # au moins une @mention de la liste correspond
    no_mention = 0  # aucune @mention dans la description
    mismatch = 0  # @mention trouvée mais ne correspond pas au GT

    mismatch_details = []
    brand_counter: Counter = Counter()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            gt_brand = row.get("DA - Manuel Collab Brand", "").strip()
            title = row.get("Title", "")
            description = row.get("Description", "")
            sn_brand = row.get("Scrappé - SN Brand", "").strip()
            paid_raw = row.get("Scrappé - SN Has Paid Placement", "").strip()
            paid = paid_raw.lower() in ("true", "1", "vrai")
            account = row.get("DA - Key Account", "")

            gt_brand = gt_brand.replace("-", "")

            if not gt_brand:
                continue  # on ne s'intéresse qu'aux positifs

            result = detect_instagram_partnership(title, description, sn_brand, paid)
            if not result["detected"]:
                continue  # FN : on ignore (algo ne l'a pas détecté)

            total_tp += 1
            extracted = extract_primary_brand(description or "")

            if extracted is None:
                no_mention += 1
                mismatch_details.append(
                    {
                        "row": i,
                        "account": account,
                        "gt": gt_brand,
                        "extracted": "(aucune mention)",
                        "desc": description.replace("\n", " "),
                    }
                )
                continue

            if _brands_match(gt_brand, extracted):
                exact += 1
                brand_counter[extracted] += 1
            else:
                # Vérifier si au moins une autre @mention dans le texte coïncide
                all_mentions = re.findall(r"@([\w.\-]{3,})", description)
                if any(_brands_match(gt_brand, m) for m in all_mentions):
                    partial += 1
                mismatch += 1
                brand_counter[extracted] += 1
                mismatch_details.append(
                    {
                        "row": i,
                        "account": account,
                        "gt": gt_brand,
                        "extracted": extracted,
                        "desc": description.replace("\n", " "),
                    }
                )

    correct = exact
    print("=" * 65)
    print("  INSTAGRAM — Précision de l'extraction de marque")
    print("=" * 65)
    print(f"  Vrais Positifs analysés          : {total_tp}")
    print(
        f"  Handle exact / sous-chaîne       : {exact}  ({exact/total_tp:.1%})"
        if total_tp
        else ""
    )
    print(
        f"  Aucune @mention dans la desc.     : {no_mention}  ({no_mention/total_tp:.1%})"
        if total_tp
        else ""
    )
    print(
        f"  Mauvaise marque extraite          : {mismatch}  ({mismatch/total_tp:.1%})"
        f"  dont {partial} avec la bonne marque ailleurs dans le texte"
        if total_tp
        else ""
    )
    print("-" * 65)
    if total_tp:
        print(
            f"  Précision globale                 : {correct/total_tp:.1%}  ({correct}/{total_tp})"
        )
    print("=" * 65)

    print("\n  Marques extraites (liste complète) :")
    for brand, count in brand_counter.most_common()[:10]:
        print(f"    @{brand:<30} : {count}")

    if mismatch_details:
        print(
            f"\n  Mauvaises extractions / sans mention ({len(mismatch_details)}, top 20) :"
        )
        for d in mismatch_details:
            print(
                f"    Ligne {d['row']:4d} | @{d['account']:<22} | GT={d['gt']:<20} | Extrait={d['extracted']:<20} | {d['desc']}"
            )


# ============================================
# COMPARAISON DEUX DATASETS
# ============================================

try:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker

    _PLOT_AVAILABLE = True
except ImportError:
    _PLOT_AVAILABLE = False


def _analyse_dataset(csv_path: str, has_gt: bool) -> dict:
    """
    Applique l'algo sur un CSV et retourne un dict de stats.
    Si has_gt=True, calcule aussi précision/recall via DA - Manuel Collab Brand.
    """
    COLUMN_MAP = {
        "title": ["Title"],
        "desc": ["Description"],
        "sn_brand": ["SN Brand", "Scrappé - SN Brand"],
        "paid": ["SN Has Paid Placement", "Scrappé - SN Has Paid Placement"],
        "account": ["Account", "DA - Key Account"],
        "post_url": ["Post Url"],
        "gt": ["DA - Manuel Collab Brand"],
    }

    def _get(row, key):
        for col in COLUMN_MAP[key]:
            if col in row:
                return row[col].strip()
        return ""

    results = []
    TP = FP = FN = TN = 0
    rule_counts: Counter = Counter()
    brand_counts: Counter = Counter()

    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            title = _get(row, "title")
            desc = _get(row, "desc")
            sn = _get(row, "sn_brand")
            paid = _get(row, "paid").lower() in ("true", "1", "vrai")
            gt = _get(row, "gt") if has_gt else ""

            det = detect_instagram_partnership(title, desc, sn, paid)
            brand = extract_primary_brand(desc) if det["detected"] else None

            for r in det["rules"]:
                rule_counts[r] += 1
            if brand:
                brand_counts[brand] += 1

            results.append(
                {
                    "account": _get(row, "account"),
                    "post_url": _get(row, "post_url"),
                    "detected": det["detected"],
                    "brand": brand or "",
                    "all_brands": "|".join(det["brands"]),
                    "rules": "|".join(det["rules"]),
                    "gt": gt,
                    "description": desc[:200].replace("\n", " "),
                }
            )

            if has_gt:
                gp = bool(gt)
                if gp and det["detected"]:
                    TP += 1
                elif gp and not det["detected"]:
                    FN += 1
                elif not gp and det["detected"]:
                    FP += 1
                else:
                    TN += 1

    total = len(results)
    detected = sum(1 for r in results if r["detected"])

    metrics = None
    if has_gt:
        recall = TP / (TP + FN) if (TP + FN) else 0
        precision = TP / (TP + FP) if (TP + FP) else 0
        f1 = (
            2 * precision * recall / (precision + recall) if (precision + recall) else 0
        )
        metrics = dict(
            TP=TP, FP=FP, FN=FN, TN=TN, recall=recall, precision=precision, f1=f1
        )

    # Toutes les marques normalisées
    groups: dict = {}
    for brand, count in brand_counts.items():
        key = _normalize_brand(brand)
        if key not in groups:
            groups[key] = Counter()
        groups[key][brand] += count
    agg = Counter({k: sum(v.values()) for k, v in groups.items()})
    labels = {k: v.most_common(1)[0][0] for k, v in groups.items()}
    top_brands = [(labels[k], c) for k, c in agg.most_common()]

    return dict(
        path=csv_path,
        total=total,
        detected=detected,
        metrics=metrics,
        top_brands=top_brands,
        rule_counts=rule_counts,
        results=results,
    )


def compare_datasets(csv_labelled: str, csv_production: str):
    """
    Compare les résultats de l'algo sur deux CSV :
      - csv_labelled   : avec ground truth (DA - Manuel Collab Brand)
      - csv_production : sans ground truth
    Affiche un résumé console et génère un graphique de comparaison.
    """
    from pathlib import Path

    print(f"  Analyse A (labellisé) : {csv_labelled}")
    a = _analyse_dataset(csv_labelled, has_gt=True)
    print(f"  Analyse B (production): {csv_production}")
    b = _analyse_dataset(csv_production, has_gt=False)

    label_a = Path(csv_labelled).stem[:28]
    label_b = Path(csv_production).stem[:28]

    # ── Résumé console ──────────────────────────────────────────────
    ra = a["detected"] / a["total"] if a["total"] else 0
    rb = b["detected"] / b["total"] if b["total"] else 0

    print("\n" + "=" * 68)
    print("  COMPARAISON — Détection de partenariats Instagram")
    print("=" * 68)
    print(f"  {'':38} {'A':>12}  {'B':>12}")
    print(f"  {'':38} {label_a[:12]:>12}  {label_b[:12]:>12}")
    print("-" * 68)
    print(f"  {'Posts analysés':<38} {a['total']:>12}  {b['total']:>12}")
    print(f"  {'Partenariats détectés':<38} {a['detected']:>12}  {b['detected']:>12}")
    print(f"  {'Taux de détection':<38} {ra:>11.1%}  {rb:>11.1%}")

    if a["metrics"]:
        m = a["metrics"]
        print("\n  Métriques A (ground truth) :")
        print(f"    TP={m['TP']}  FP={m['FP']}  FN={m['FN']}  TN={m['TN']}")
        print(
            f"    Recall={m['recall']:.1%}  Précision={m['precision']:.1%}  F1={m['f1']:.1%}"
        )

    all_brands = {}
    for brand, count in a["top_brands"] + b["top_brands"]:
        key = _normalize_brand(brand)
        if key not in all_brands:
            all_brands[key] = (brand, 0, 0)
        _, ca, cb = all_brands[key]
        all_brands[key] = (brand, ca, cb)
    da = dict((_normalize_brand(b), c) for b, c in a["top_brands"])
    db = dict((_normalize_brand(b), c) for b, c in b["top_brands"])
    merged = sorted(set(da) | set(db), key=lambda k: -(da.get(k, 0) + db.get(k, 0)))
    brand_display = {
        _normalize_brand(b): b for b, _ in a["top_brands"] + b["top_brands"]
    }

    print(f"\n  {'Marques extraites (liste complète)':<32} {'A':>6}  {'B':>6}")
    print("  " + "-" * 48)
    for key in merged:
        print(
            f"  @{brand_display.get(key, key):<31} {da.get(key,0):>6}  {db.get(key,0):>6}"
        )

    all_rules = sorted(
        set(a["rule_counts"]) | set(b["rule_counts"]),
        key=lambda r: -(a["rule_counts"].get(r, 0) + b["rule_counts"].get(r, 0)),
    )
    print(f"\n  {'Règles':<32} {'A':>6}  {'B':>6}")
    print("  " + "-" * 48)
    for rule in all_rules:
        print(
            f"  {rule:<32} {a['rule_counts'].get(rule,0):>6}  {b['rule_counts'].get(rule,0):>6}"
        )
    print("=" * 68)

    # ── Export CSV ──────────────────────────────────────────────────
    out_dir = Path(csv_labelled).parent

    fields = [
        "account",
        "post_url",
        "detected",
        "brand",
        "all_brands",
        "rules",
        "gt",
        "description",
    ]

    """
    fields = [
        "post-id"
        "account",
        "post_url",


        "title", "social network", "has_collab", "detected_brands"


        "account",
        "post_url",
        "detected", has_collab
        "brand", detected_brands
        "title", 
      
        "gt", has_collab
        "description",
    ]
    """

    for dataset, suffix in [(a, "labelled"), (b, "production")]:
        out_path = out_dir / f"comparison_{suffix}.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(dataset["results"])
        print(f"  CSV exporté → {out_path}")

    if not _PLOT_AVAILABLE:
        print("  (matplotlib non disponible — graphique ignoré)")
        return

    # ── Graphiques ──────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(18, 13))
    fig.suptitle(
        "Comparaison de détection de partenariats Instagram",
        fontsize=14,
        fontweight="bold",
    )

    # 1. Taux de détection
    ax = axes[0, 0]
    bars = ax.bar(
        [label_a, label_b],
        [ra * 100, rb * 100],
        color=["#E8645A", "#6BAED6"],
        edgecolor="white",
        width=0.5,
    )
    for bar, rate, d in zip(bars, [ra, rb], [a, b]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{rate:.1%}\n({d['detected']}/{d['total']})",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    ax.set_ylabel("Taux de détection (%)")
    ax.set_ylim(0, max(ra, rb) * 100 * 1.4)
    ax.set_title("Taux de détection", fontweight="bold")
    ax.set_xticklabels([label_a, label_b], rotation=15, ha="right")

    # 2. Top 15 marques — triées par dataset B (production)
    ax = axes[0, 1]
    top15_keys = sorted(set(da) | set(db), key=lambda k: -db.get(k, 0))[:15]
    top15_labels = [brand_display.get(k, k) for k in top15_keys]
    vals_a = [da.get(k, 0) for k in top15_keys]
    vals_b = [db.get(k, 0) for k in top15_keys]
    y = np.arange(len(top15_keys))
    h = 0.35
    ax.barh(y + h / 2, vals_a, h, label=label_a, color="#E8645A", edgecolor="white")
    ax.barh(y - h / 2, vals_b, h, label=label_b, color="#6BAED6", edgecolor="white")
    ax.set_yticks(y)
    ax.set_yticklabels(top15_labels, fontsize=8)
    ax.set_xlabel("Nombre de posts")
    ax.set_title("Top 15 marques extraites", fontweight="bold")
    ax.legend(fontsize=8)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    # 3. Ranking influenceurs par % de collabs (dataset B = production)
    ax = axes[1, 0]
    account_total: Counter = Counter()
    account_detected: Counter = Counter()
    for r in b["results"]:
        account_total[r["account"]] += 1
        if r["detected"]:
            account_detected[r["account"]] += 1
    ranked = sorted(
        [
            (acc, account_detected[acc] / account_total[acc], account_total[acc])
            for acc in account_total
            if account_total[acc] >= 5
        ],
        key=lambda x: x[1],
        reverse=True,
    )[:20]
    if ranked:
        accs, rates, _ = zip(*ranked)
        bars = ax.barh(
            list(reversed(accs)),
            [r * 100 for r in reversed(rates)],
            color="#74C476",
            edgecolor="white",
        )
        for bar, (acc, rate, tot) in zip(bars, reversed(ranked)):
            ax.text(
                bar.get_width() + 0.5,
                bar.get_y() + bar.get_height() / 2,
                f"{rate:.0%} ({account_detected[acc]}/{tot})",
                va="center",
                fontsize=7,
            )
        ax.set_xlim(0, 120)
        ax.set_xlabel("% de posts avec partenariat")
        ax.set_title(
            f"Top 20 influenceurs — % collabs\n({label_b}, min. 5 posts)",
            fontweight="bold",
        )
        ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    else:
        ax.text(
            0.5,
            0.5,
            "Pas assez de données",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=12,
        )
        ax.set_title("Ranking influenceurs", fontweight="bold")

    # 4. Règles côte à côte
    ax = axes[1, 1]
    x = np.arange(len(all_rules))
    h = 0.35
    ax.bar(
        x - h / 2,
        [a["rule_counts"].get(r, 0) for r in all_rules],
        h,
        label=label_a,
        color="#E8645A",
        edgecolor="white",
    )
    ax.bar(
        x + h / 2,
        [b["rule_counts"].get(r, 0) for r in all_rules],
        h,
        label=label_b,
        color="#6BAED6",
        edgecolor="white",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(all_rules, rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Déclenchements")
    ax.set_title("Règles déclenchées", fontweight="bold")
    ax.legend(fontsize=8)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    plt.tight_layout()
    out = Path(csv_labelled).parent / "instagram_comparison.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\n  Graphique sauvegardé → {out}")
    plt.show()


# --- Point d'entrée ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        # Mode comparaison : python extraction_instagram.py <labelled.csv> <production.csv>
        compare_datasets(sys.argv[1], sys.argv[2])
    else:
        # Mode évaluation classique sur le CSV labellisé
        CSV = sys.argv[1]
        print("\n")
        evaluate_scraping(CSV)

        print("\n\n")
        evaluate_regex_only(CSV)

        print("\n\n")
        evaluate_regex(CSV)

        print("\n\n")
        evaluate_brand_extraction(CSV)
