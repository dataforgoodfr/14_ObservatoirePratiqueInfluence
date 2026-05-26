import re
import csv
import argparse
import unicodedata
from pathlib import Path

_DEFAULT_BRANDS_CSV = (
    Path(__file__).resolve().parent / "Labelisation - Brand (Default View).csv"
)


def resolve_brands_csv_path(cli_path: str | None, no_brands: bool) -> str | None:
    """Chemin effectif du catalogue marques (None = passe 2 désactivée)."""
    if no_brands:
        return None
    if cli_path and str(cli_path).strip():
        return str(cli_path).strip()
    if _DEFAULT_BRANDS_CSV.is_file():
        return str(_DEFAULT_BRANDS_CSV)
    return None

# ============================================
# ALGORITHME YOUTUBE - Détection de Partenariats
# ============================================


# --- Regex compilées pour chaque règle ---
RE_COLLAB_COMM    = re.compile(r'collaboration commerciale', re.I)
RE_PUBLICITE      = re.compile(r'publicit[eéè]', re.I)
RE_SPONSORISE     = re.compile(r'sponsoris[eéè]', re.I)
RE_MERCI_SPONSOR  = re.compile(r"merci à\s+(.+?)\s+d'avoir\s+sponsoris", re.I)
RE_MERCI_ACCOMP   = re.compile(r'merci à\s+(.+?)\s+de nous avoir accompagn', re.I)
RE_PRESENTE_PAR   = re.compile(r'présenté(?:e)?\s+par', re.I)
RE_EN_PARTENARIAT = re.compile(r'en partenariat avec', re.I)
RE_PRODUITS_OFF   = re.compile(r'produits?\s+offerts?', re.I)

# --- Regex additionnelles pour extraction partenaire (niveau B) ---
RE_MERCI_SPONSOR_EXACT = re.compile(
    r"merci\s+(?:beaucoup\s+)?à\s+(?:la\s+marque\s+)?(.+?)\s+d[’']avoir\s+sponsoris",
    re.I,
)
RE_MERCI_ACCOMP_EXACT = re.compile(
    r"merci\s+à\s+(?:la\s+marque\s+)?(.+?)\s+de\s+nous\s+avoir\s+accompagn",
    re.I,
)
RE_EN_PARTENARIAT_WITH_BRAND = re.compile(
    r"en\s+partenariat\s+avec\s+(.+?)(?:[\n\r\.\!\?,;]|https?://|$)",
    re.I,
)
RE_COLLAB_AVEC_BRAND = re.compile(
    r"(?:en\s+)?collaboration\s+commerciale\s+avec\s+(.+?)(?:[\n\r\.\!\?,;]|https?://|$)",
    re.I,
)
RE_AVEC_BRAND_PROMO = re.compile(
    r"avec\s+(.+?)\s*,?\s*(?:profitez|b[ée]n[ée]ficiez)\s+de",
    re.I,
)
RE_CODE_CHEZ_BRAND = re.compile(
    r"(?:sur|chez)\s+(.+?)\s+avec\s+le\s+code",
    re.I,
)
RE_TELECHARGEZ_BRAND = re.compile(
    r"t[ée]l[ée]chargez\s+(?:l['’]application\s+)?(.+?)(?:\s+(?:gratuitement|via|ici)\b|\s+avec\s+(?:ce|mon)\s+lien\b|\s+avec\s+le\s+code\b|https?://|[\n\r\.\!\?,;]|$)",
    re.I,
)
RE_SITE_BRAND = re.compile(
    r"(?:sur\s+tout\s+le\s+site|sur\s+le\s+site|le\s+site\s+de)\s+(.+?)(?:\s+avec\s+le\s+code\b|\s+via\s+ce\s+lien\b|https?://|[\n\r\.\!\?,;]|$)",
    re.I,
)
RE_CODE_AFTER_BRAND = re.compile(
    r"(.+?)\s+avec\s+le\s+code\b",
    re.I,
)

# Expressions non exploitables comme nom de partenaire
BAD_PARTNER_TOKENS = {
    "la video", "la vidéo", "cette video", "cette vidéo", "youtube",
    "mon code", "votre commande", "l’ukraine", "ukraine", "la france", "france",
    "eux", "nous", "vous", "leur", "ils", "elles",
}


def _as_text(value) -> str:
    if value is None:
        return ""
    text = str(value)
    return "" if text == "nan" else text


def _clean_partner_candidate(value: str) -> str:
    text = " ".join((value or "").replace("\n", " ").split())
    text = text.strip(" -|,.;:!?)([]{}\"'")
    text = re.sub(r"^(la\s+marque)\s+", "", text, flags=re.I)
    text = re.sub(r"^(?:le|la)\s+site\s+de\s+", "", text, flags=re.I)
    text = re.sub(r"^sur\s+(?:tout\s+)?le\s+site\s+", "", text, flags=re.I)
    text = re.sub(r"^votre\s+esim\s+", "", text, flags=re.I)
    text = re.sub(r"^(?:les?\s+offres?\s+en\s+cours|les?\s+produits?\s+en\s+promotion)\s+", "", text, flags=re.I)
    text = re.sub(r"^(?:l['’]offre|offre)\s+", "", text, flags=re.I)
    text = re.sub(r"\s+(?:avec\s+mon\s+code|avec\s+le\s+code|profitez|b[ée]n[ée]ficiez|jusqu['’]a|jusqu['’]à|voir\s+conditions?).*$", "", text, flags=re.I)
    text = re.sub(r"\s*[-–]\s*(?:avec\s+mon\s+code|avec\s+le\s+code).*$", "", text, flags=re.I)
    text = text.strip(" -|,.;:!?)([]{}\"'")
    return text


def _valid_partner_candidate(value: str) -> bool:
    if not value:
        return False
    lowered = value.lower()
    if lowered in BAD_PARTNER_TOKENS:
        return False
    if lowered.startswith("mon code "):
        return False
    if lowered.startswith("votre commande"):
        return False
    if any(token in lowered for token in ("http://", "https://", "%", "commande", "reduction", "réduction", "offre", "offerts", "profitez", "beneficiez", "bénéficiez")):
        return False
    if len(value.split()) > 5:
        return False
    return 1 < len(value) <= 50


def _normalize_for_brand_search(text: str) -> str:
    s = _as_text(text).lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = " ".join(s.split())
    return s


def _brand_pattern_from_canonical(canonical: str) -> re.Pattern | None:
    raw = (canonical or "").strip()
    if not raw:
        return None
    norm = _normalize_for_brand_search(raw)
    if not norm:
        return None
    parts = [p for p in re.split(r"[\s-]+", norm) if p]
    if not parts:
        return None
    escaped = [re.escape(p) for p in parts]
    core = escaped[0] if len(escaped) == 1 else r"[\s-]+".join(escaped)
    return re.compile(rf"(?<![a-z0-9]){core}(?![a-z0-9])")


def load_brand_catalog(csv_path: str | None) -> list[tuple[re.Pattern, str]]:
    """
    Lit la colonne Name du CSV de marques ; ignore les lignes sans nom.
    Retourne des paires (pattern compilé, nom canonique) triées par longueur
    du nom normalisé décroissante.
    """
    if not csv_path or not str(csv_path).strip():
        return []
    path = Path(csv_path)
    if not path.is_file():
        return []

    names: list[str] = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = _as_text(row.get("Name", "")).strip()
            if name:
                names.append(name)

    names.sort(key=lambda n: len(_normalize_for_brand_search(n)), reverse=True)
    matchers: list[tuple[re.Pattern, str]] = []
    seen_upper: set[str] = set()
    for canonical in names:
        key = canonical.upper()
        if key in seen_upper:
            continue
        seen_upper.add(key)
        pat = _brand_pattern_from_canonical(canonical)
        if pat is not None:
            matchers.append((pat, canonical))
    return matchers


def find_all_brand_hits(normalized_haystack: str, matchers: list[tuple[re.Pattern, str]]) -> list[str]:
    if not normalized_haystack or not matchers:
        return []
    found: list[str] = []
    seen: set[str] = set()
    for pattern, canonical in matchers:
        if pattern.search(normalized_haystack):
            k = canonical.upper()
            if k not in seen:
                seen.add(k)
                found.append(canonical)
    return sorted(found, key=str.upper)


def _manual_brand_from_row(row: dict) -> str:
    manual_col = _as_text(row.get("Brand - Ajout Manuel", "")).strip()
    brand_col = _as_text(row.get("Brand", "")).strip()
    raw = manual_col if manual_col else brand_col
    return _clean_partner_candidate(raw)


def _row_value(row: dict, *keys: str) -> str:
    for key in keys:
        if key in row:
            return _as_text(row.get(key, ""))
    return ""


def _normalize_partner_label(value: str) -> str:
    return _normalize_for_brand_search(_clean_partner_candidate(value))


def _is_empty_brand_value(value: str) -> bool:
    lowered = _as_text(value).strip().lower()
    return lowered in ("", "-", "none", "nan", "null")


def _split_brand_values(value: str) -> list[str]:
    if _is_empty_brand_value(value):
        return []
    raw = _as_text(value).replace("\n", ";")
    parts = re.split(r"[;|,/]+", raw)
    cleaned = [_clean_partner_candidate(p) for p in parts]
    return [c for c in cleaned if c and not _is_empty_brand_value(c)]


def _parse_manual_brand_ground_truth(row: dict) -> tuple[str, set[str], dict[str, str]]:
    main_raw = _row_value(row, "Manuel - Collab Commerciale")
    others_raw = _row_value(row, "Manuel - Autres marques")

    gt_main_norm = ""
    norm_to_display: dict[str, str] = {}
    gt_set: set[str] = set()

    for brand in _split_brand_values(main_raw):
        norm = _normalize_partner_label(brand)
        if not norm:
            continue
        if not gt_main_norm:
            gt_main_norm = norm
        if norm not in norm_to_display:
            norm_to_display[norm] = brand
        gt_set.add(norm)
        break

    for brand in _split_brand_values(others_raw):
        norm = _normalize_partner_label(brand)
        if not norm:
            continue
        if norm not in norm_to_display:
            norm_to_display[norm] = brand
        gt_set.add(norm)

    return gt_main_norm, gt_set, norm_to_display


def _parse_predicted_brand_set(partner_final: str) -> tuple[str, set[str], dict[str, str]]:
    pred_main_norm = ""
    norm_to_display: dict[str, str] = {}
    pred_set: set[str] = set()

    for brand in _split_brand_values(partner_final):
        norm = _normalize_partner_label(brand)
        if not norm:
            continue
        if not pred_main_norm:
            pred_main_norm = norm
        if norm not in norm_to_display:
            norm_to_display[norm] = brand
        pred_set.add(norm)

    return pred_main_norm, pred_set, norm_to_display


def _display_label(norm_value: str, norm_to_display: dict[str, str]) -> str:
    if not norm_value:
        return "(vide)"
    return norm_to_display.get(norm_value, norm_value)


def _merge_partners(partner_pass1: str, list_hits: list[str]) -> str:
    merged: dict[str, str] = {}
    for p in partner_pass1.split(";"):
        p = p.strip()
        if not p:
            continue
        k = p.upper()
        if k not in merged:
            merged[k] = p
    for h in list_hits:
        merged[h.upper()] = h
    return "; ".join(sorted(merged.values(), key=str.upper))


def extract_partner_level_b(description: str) -> str:
    """
    Niveau B: extraction stricte d'une marque depuis le texte description.
    """
    desc = _as_text(description)
    patterns = (
        RE_MERCI_SPONSOR_EXACT,
        RE_MERCI_ACCOMP_EXACT,
        RE_COLLAB_AVEC_BRAND,
        RE_EN_PARTENARIAT_WITH_BRAND,
        RE_SITE_BRAND,
        RE_TELECHARGEZ_BRAND,
        RE_AVEC_BRAND_PROMO,
        RE_CODE_CHEZ_BRAND,
    )
    for pattern in patterns:
        match = pattern.search(desc)
        if not match:
            continue
        candidate = _clean_partner_candidate(match.group(1))
        if _valid_partner_candidate(candidate):
            return candidate
        # Fallback spécifique aux captures longues de type "... avec le code ..."
        if pattern in (RE_SITE_BRAND, RE_TELECHARGEZ_BRAND, RE_AVEC_BRAND_PROMO):
            sub = RE_CODE_AFTER_BRAND.search(candidate)
            if sub:
                recut = _clean_partner_candidate(sub.group(1))
                if _valid_partner_candidate(recut):
                    return recut
    return ""


def detect_youtube_partnership(title: str, description: str, paid_placement: bool) -> dict:
    """
    Détecte si une vidéo YouTube contient un partenariat commercial.

    Paramètres
    ----------
    title : str           – Titre de la vidéo
    description : str     – Description complète de la vidéo
    paid_placement : bool – Flag YouTube "SN Has Paid Placement"

    Retourne
    --------
    dict avec :
        detected : bool        – Partenariat détecté oui/non
        brands   : list[str]   – Marques identifiées
        rules    : list[str]   – Règles ayant déclenché la détection
    """
    desc = (description or "").lower()
    detected = False
    brands = set()
    rules = []

    # RÈGLE 1 : Flag YouTube "Paid Placement"
    if paid_placement is True:
        detected = True
        rules.append("PAID_PLACEMENT")

    # RÈGLE 2 : "Collaboration commerciale"
    if RE_COLLAB_COMM.search(desc):
        detected = True
        rules.append("COLLAB_COMMERCIALE")

    # RÈGLE 3 : "Publicité"
    if RE_PUBLICITE.search(desc):
        detected = True
        rules.append("PUBLICITE")

    # RÈGLE 4 : "sponsorisé / sponsoriser"
    if RE_SPONSORISE.search(desc):
        detected = True
        rules.append("SPONSORISE")

    # RÈGLE 5 : "Merci à [MARQUE] d'avoir sponsorisé"
    m = RE_MERCI_SPONSOR.search(desc)
    if m:
        detected = True
        rules.append("MERCI_SPONSOR")
        brand = m.group(1).strip()
        brand = re.sub(r'^la marque\s+', '', brand, flags=re.I)
        if 1 < len(brand) < 40:
            brands.add(brand)

    # RÈGLE 6 : "Merci à [MARQUE] de nous avoir accompagné"
    m = RE_MERCI_ACCOMP.search(desc)
    if m:
        detected = True
        rules.append("MERCI_ACCOMPAGNE")
        brand = m.group(1).strip()
        brand = re.sub(r'^la marque\s+', '', brand, flags=re.I)
        if 1 < len(brand) < 40:
            brands.add(brand)

    # RÈGLE 8 : "présenté par"
    if RE_PRESENTE_PAR.search(desc):
        detected = True
        rules.append("PRESENTE_PAR")

    # RÈGLE 9 : "en partenariat avec"
    if RE_EN_PARTENARIAT.search(desc):
        detected = True
        rules.append("EN_PARTENARIAT")

    # RÈGLE 10 : "produits offerts"
    if RE_PRODUITS_OFF.search(desc):
        detected = True
        rules.append("PRODUITS_OFFERTS")

    return {"detected": detected, "brands": list(brands), "rules": rules}


def compute_final_annotation(
    title: str,
    description: str,
    paid_placement: bool,
    manual_brand: str,
    brand_matchers: list[tuple[re.Pattern, str]],
) -> dict:
    """
    Passe 1 (regex + A/B) puis passe 2 (liste marques sur titre + description).

    Retourne notamment :
        pass1_detected, rules, partner_pass1, partner_source,
        list_hits, detected_final, partner_final, marqueur_texte
    """
    result = detect_youtube_partnership(title, description, paid_placement)
    pass1_detected = result["detected"]
    rules = list(result["rules"])
    brands_from_detector = sorted(set(result["brands"]))

    partner_pass1 = ""
    partner_source = ""

    cleaned_manual = _clean_partner_candidate(manual_brand)
    if pass1_detected and _valid_partner_candidate(cleaned_manual):
        partner_pass1 = cleaned_manual
        partner_source = "A"
    elif pass1_detected and brands_from_detector:
        partner_pass1 = "; ".join(brands_from_detector)
        partner_source = "B"
    elif pass1_detected:
        extracted = extract_partner_level_b(description)
        if _valid_partner_candidate(extracted):
            partner_pass1 = extracted
            partner_source = "B"

    haystack = _normalize_for_brand_search(f"{title}\n{description}")
    list_hits = find_all_brand_hits(haystack, brand_matchers) if brand_matchers else []

    partner_final = _merge_partners(partner_pass1, list_hits)
    detected_final = pass1_detected or bool(list_hits)

    marqueur_parts = list(rules)
    if list_hits:
        marqueur_parts.append(
            "LISTE_MARQUE:" + "|".join(sorted(list_hits, key=str.upper))
        )
    marqueur_texte = " | ".join(marqueur_parts) if marqueur_parts else ""

    pass1_names_upper = {p.strip().upper() for p in partner_pass1.split(";") if p.strip()}
    list_only_upper = {h.upper() for h in list_hits} - pass1_names_upper

    return {
        "pass1_detected": pass1_detected,
        "rules": rules,
        "partner_pass1": partner_pass1,
        "partner_source": partner_source,
        "list_hits": list_hits,
        "detected_final": detected_final,
        "partner_final": partner_final if detected_final else "",
        "marqueur_texte": marqueur_texte,
        "list_only_upper": list_only_upper,
    }


def annotate_youtube_csv(
    input_csv_path: str,
    output_csv_path: str,
    brands_csv_path: str | None = None,
):
    """
    Annote toutes les lignes d'un CSV YouTube avec les colonnes:
    - Partenariat_Détecté
    - Partenaire(s)
    - Type_Partenariat
    - Marqueur_Texte

    Règles de remplissage Partenaire(s):
    - Passe 1 — Niveau A: Brand - Ajout Manuel ou colonne Brand
    - Passe 1 — Niveau B: marques regex + extraction stricte
    - Passe 2: union avec les noms présents dans le CSV catalogue marques
    """
    brand_matchers = load_brand_catalog(brands_csv_path)

    with open(input_csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV sans en-têtes")
        rows = list(reader)
        fieldnames = list(reader.fieldnames)

    for col in ("Partenariat_Détecté", "Partenaire(s)", "Type_Partenariat", "Marqueur_Texte"):
        if col not in fieldnames:
            fieldnames.append(col)

    total_rows = len(rows)
    detected_count = 0
    detected_partner_filled = 0
    level_a_fills = 0
    level_b_fills = 0
    unresolved_detected = 0
    before_empty_detected = 0
    fixed_from_empty = 0
    inferred_list_only = 0
    list_filled_empty_partner = 0
    list_added_to_existing = 0

    for row in rows:
        title = _as_text(row.get("Title", ""))
        description = _as_text(row.get("Description", ""))
        paid_raw = _as_text(row.get("SN Has Paid Placement", ""))
        paid = paid_raw.strip().upper() in ("TRUE", "1", "VRAI")

        previous_partner = _as_text(row.get("Partenaire(s)", "")).strip()

        manual_brand = _manual_brand_from_row(row)
        ann = compute_final_annotation(
            title, description, paid, manual_brand, brand_matchers
        )
        detected_final = ann["detected_final"]
        partner = ann["partner_final"]
        partner_source = ann["partner_source"]
        pass1_detected = ann["pass1_detected"]
        partner_pass1 = ann["partner_pass1"]
        list_hits = ann["list_hits"]
        list_only_upper = ann["list_only_upper"]

        row["Partenariat_Détecté"] = "Oui" if detected_final else "Non"
        row["Partenaire(s)"] = partner
        row["Type_Partenariat"] = "Commercial" if detected_final else ""
        row["Marqueur_Texte"] = ann["marqueur_texte"]

        if not pass1_detected and list_hits:
            inferred_list_only += 1
        if pass1_detected and not partner_pass1.strip() and list_hits:
            list_filled_empty_partner += 1
        if partner_pass1.strip() and list_only_upper:
            list_added_to_existing += 1

        if detected_final:
            detected_count += 1
            if not previous_partner:
                before_empty_detected += 1
            if partner:
                detected_partner_filled += 1
                if not previous_partner:
                    fixed_from_empty += 1
                if partner_source == "A":
                    level_a_fills += 1
                elif partner_source == "B":
                    level_b_fills += 1
            else:
                unresolved_detected += 1

    with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    brands_display = brands_csv_path if brands_csv_path else "(désactivé)"
    print("=" * 60)
    print("  YOUTUBE — Annotation (regex + liste marques)")
    print("=" * 60)
    print(f"  Fichier source                 : {input_csv_path}")
    print(f"  Fichier annoté                 : {output_csv_path}")
    print(f"  CSV marques (passe 2)          : {brands_display}")
    print(f"  Marques chargées               : {len(brand_matchers)}")
    print(f"  Lignes totales                 : {total_rows}")
    print(f"  Lignes détectées (Oui)         : {detected_count}")
    print(f"  Partenaires remplis (Oui)      : {detected_partner_filled}")
    print(f"  Partenaires vides (Oui)        : {unresolved_detected}")
    print("-" * 60)
    print(f"  Remplissages Niveau A          : {level_a_fills}")
    print(f"  Remplissages Niveau B          : {level_b_fills}")
    print("-" * 60)
    print(f"  'Oui' grâce à la liste seule   : {inferred_list_only}")
    print(f"  Liste complète partenaire vide : {list_filled_empty_partner}")
    print(f"  Liste ajoute marque(s) en plus : {list_added_to_existing}")
    print("-" * 60)
    print(f"  'Oui' avec partenaire vide AVANT : {before_empty_detected}")
    print(f"  Vides corrigés après traitement   : {fixed_from_empty}")
    print(f"  'Oui' encore vide APRÈS           : {before_empty_detected - fixed_from_empty}")
    print("=" * 60)


# ============================================
# ÉVALUATION
# ============================================
def evaluate_youtube(
    csv_path: str,
    brands_csv_path: str | None = None,
):
    """
    Lit le CSV exporté de la feuille 'YouTube - Vidéos' et évalue l'algorithme.

    Utilise la même logique que l'annotation : regex (passe 1) puis catalogue
    marques (passe 2) si brands_csv_path est fourni et chargeable.

    Le CSV doit avoir les colonnes :
        Title, Description, SN Brand, SN Has Paid Placement,
        Brand - Ajout Manuel, Account Name, Social Network,
        Post Url, Post Type, Partenariat_Détecté, Partenaire(s),
        Type_Partenariat, Marqueur_Texte
    """
    brand_matchers = load_brand_catalog(brands_csv_path)
    TP = FP = FN = TN = 0
    fn_details = []
    fp_details = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # start=2 car ligne 1 = header
            title       = _as_text(row.get("Title", ""))
            description = _as_text(row.get("Description", ""))
            paid_raw    = _as_text(row.get("SN Has Paid Placement", ""))
            paid        = paid_raw.strip().upper() in ("TRUE", "1", "VRAI")
            gt          = row.get("Partenariat_Détecté", "").strip()
            gt_partner  = row.get("Partenaire(s)", "")

            # Ignorer les lignes non annotées
            if gt not in ("Oui", "Non"):
                continue

            manual = _manual_brand_from_row(row)
            ann = compute_final_annotation(
                title, description, paid, manual, brand_matchers
            )
            predicted = ann["detected_final"]

            if gt == "Oui":
                if predicted:
                    TP += 1
                else:
                    FN += 1
                    fn_details.append({
                        "row": i,
                        "title": title[:60],
                        "partner": gt_partner,
                    })
            elif gt == "Non":
                if predicted:
                    FP += 1
                    fp_details.append({
                        "row": i,
                        "title": title[:60],
                        "marqueur": ann["marqueur_texte"],
                    })
                else:
                    TN += 1

    total = TP + FP + FN + TN
    recall    = TP / (TP + FN) if (TP + FN) else 0
    fpr       = FP / (FP + TN) if (FP + TN) else 0
    miss_rate = FN / (FN + TP) if (FN + TP) else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print("=" * 55)
    print("  YOUTUBE — Résultats de l'algorithme")
    print("=" * 55)
    print(f"  Passe 2 (CSV marques) : {brands_csv_path or '(désactivé)'} — {len(brand_matchers)} marques")
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
        print(f"\n  Faux Positifs ({len(fp_details)}) :")
        for d in fp_details[:10]:
            print(f"    Ligne {d['row']} | {d['title']} | Marqueur: {d['marqueur']}")


def evaluate_dash_admin_youtube(
    csv_path: str,
    brands_csv_path: str | None = None,
    debug_csv_path: str | None = None,
):
    """
    Évalue sur le CSV Dash Admin avec la vérité terrain:
        DA - Manuel Collab Brand
    Convention GT:
        '-' / vide / 'None' => Non
        autre valeur => Oui, avec marque principale = valeur du champ
    """
    brand_matchers = load_brand_catalog(brands_csv_path)
    TP = FP = FN = TN = 0
    fn_details = []
    fp_details = []
    debug_rows = []
    # Multi-label (micro)
    brand_tp = brand_fp = brand_fn = 0
    gt_brand_positive_rows = 0
    pred_brand_non_empty_on_gt = 0
    # Main brand (mono-label)
    main_total = 0
    main_correct = 0
    main_missed = 0
    main_wrong = 0
    main_confusions: dict[tuple[str, str], int] = {}

    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            title = _row_value(row, "Title")
            description = _row_value(row, "Description")
            paid_raw = _row_value(row, "SN Has Paid Placement", "Scrappé - SN Has Paid Placement")
            paid = paid_raw.strip().upper() in ("TRUE", "1", "VRAI")

            gt_da_raw = _row_value(row, "DA - Manuel Collab Brand")
            gt_detected = not _is_empty_brand_value(gt_da_raw)
            gt_main_display = _clean_partner_candidate(gt_da_raw) if gt_detected else ""
            gt_main_norm = _normalize_partner_label(gt_main_display) if gt_detected else ""
            gt_brand_set = {gt_main_norm} if gt_main_norm else set()
            gt_display = {gt_main_norm: gt_main_display} if gt_main_norm else {}

            manual = _manual_brand_from_row(row)
            ann = compute_final_annotation(
                title, description, paid, manual, brand_matchers
            )
            predicted = ann["detected_final"]
            predicted_partner = ann["partner_final"].strip()
            pred_main_norm, pred_brand_set, pred_display = _parse_predicted_brand_set(predicted_partner)

            # Multi-label brand metrics (micro aggregation)
            if gt_brand_set:
                gt_brand_positive_rows += 1
                if pred_brand_set:
                    pred_brand_non_empty_on_gt += 1
            brand_tp += len(gt_brand_set & pred_brand_set)
            brand_fp += len(pred_brand_set - gt_brand_set)
            brand_fn += len(gt_brand_set - pred_brand_set)

            # Main brand metrics (only rows with GT main brand from DA)
            if gt_main_norm:
                main_total += 1
                if pred_main_norm == gt_main_norm:
                    main_correct += 1
                    main_status = "MAIN_MATCH"
                elif not pred_main_norm:
                    main_missed += 1
                    main_status = "MAIN_MISSED"
                    key = (gt_main_norm, "")
                    main_confusions[key] = main_confusions.get(key, 0) + 1
                else:
                    main_wrong += 1
                    main_status = "MAIN_WRONG"
                    key = (gt_main_norm, pred_main_norm)
                    main_confusions[key] = main_confusions.get(key, 0) + 1
            else:
                main_status = "MAIN_NA"

            if gt_detected:
                if predicted:
                    TP += 1
                    status = "TP"
                else:
                    FN += 1
                    status = "FN"
                    fn_details.append({
                        "row": i,
                        "title": title[:60],
                        "partner": gt_main_display,
                    })
            else:
                if predicted:
                    FP += 1
                    status = "FP"
                    fp_details.append({
                        "row": i,
                        "title": title[:60],
                        "marqueur": ann["marqueur_texte"],
                    })
                else:
                    TN += 1
                    status = "TN"

            if gt_brand_set and pred_brand_set:
                if pred_brand_set == gt_brand_set:
                    brand_match_status = "BRAND_EXACT_SET"
                elif gt_brand_set & pred_brand_set:
                    brand_match_status = "BRAND_PARTIAL_SET"
                else:
                    brand_match_status = "BRAND_WRONG_SET"
            elif gt_brand_set and not pred_brand_set:
                brand_match_status = "BRAND_MISSED_SET"
            elif not gt_brand_set and pred_brand_set:
                brand_match_status = "BRAND_SPURIOUS_SET"
            else:
                brand_match_status = "BRAND_NONE_SET"

            if debug_csv_path:
                debug_rows.append({
                    "row_number": i,
                    "post_url": _row_value(row, "Post Url"),
                    "gt_da_manual_brand": gt_main_display,
                    "gt_main_brand": _display_label(gt_main_norm, gt_display) if gt_main_norm else "",
                    "gt_brand_set": "; ".join(sorted(_display_label(k, gt_display) for k in gt_brand_set)),
                    "gt_detected": "Oui" if gt_detected else "Non",
                    "pred_detected": "Oui" if predicted else "Non",
                    "pred_main_brand": _display_label(pred_main_norm, pred_display) if pred_main_norm else "",
                    "pred_brand_set": "; ".join(sorted(_display_label(k, pred_display) for k in pred_brand_set)),
                    "pred_partner_raw": predicted_partner,
                    "detect_status": status,
                    "brand_match_status": brand_match_status,
                    "main_brand_detected": "Oui" if (gt_main_norm and pred_main_norm == gt_main_norm) else "Non",
                    "main_brand_status": main_status,
                    "paid_placement_raw": paid_raw,
                    "marqueur_texte": ann["marqueur_texte"],
                })

    total = TP + FP + FN + TN
    recall = TP / (TP + FN) if (TP + FN) else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    specificity = TN / (TN + FP) if (TN + FP) else 0
    accuracy = (TP + TN) / total if total else 0
    fpr = FP / (FP + TN) if (FP + TN) else 0
    miss_rate = FN / (FN + TP) if (FN + TP) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    brand_precision = brand_tp / (brand_tp + brand_fp) if (brand_tp + brand_fp) else 0
    brand_recall = brand_tp / (brand_tp + brand_fn) if (brand_tp + brand_fn) else 0
    brand_f1 = (
        2 * brand_precision * brand_recall / (brand_precision + brand_recall)
        if (brand_precision + brand_recall)
        else 0
    )
    brand_fill_rate = (
        pred_brand_non_empty_on_gt / gt_brand_positive_rows
        if gt_brand_positive_rows
        else 0
    )

    main_accuracy = main_correct / main_total if main_total else 0
    main_missed_rate = main_missed / main_total if main_total else 0
    main_wrong_rate = main_wrong / main_total if main_total else 0

    print("=" * 65)
    print("  YOUTUBE DASH ADMIN — Évaluation (GT DA - Manuel Collab Brand)")
    print("=" * 65)
    print(f"  CSV évalué                 : {csv_path}")
    print(f"  Passe 2 (CSV marques)      : {brands_csv_path or '(désactivé)'}")
    print(f"  Marques chargées           : {len(brand_matchers)}")
    print(f"  Total lignes évaluées      : {total}")
    print(f"  GT positifs (détection)    : {TP + FN}")
    print("-" * 65)
    print(f"  Vrais Positifs  (TP)       : {TP}")
    print(f"  Faux Positifs   (FP)       : {FP}")
    print(f"  Faux Négatifs   (FN)       : {FN}")
    print(f"  Vrais Négatifs  (TN)       : {TN}")
    print("-" * 65)
    print(f"  Exactitude                : {accuracy:.1%}")
    print(f"  Précision                 : {precision:.1%}")
    print(f"  Rappel                    : {recall:.1%}")
    print(f"  Spécificité               : {specificity:.1%}")
    print(f"  % Faux Positifs           : {fpr:.1%}")
    print(f"  % Loupés                  : {miss_rate:.1%}")
    print(f"  F1-Score                  : {f1:.1%}")
    print("-" * 65)
    print("  Marques (multi-label, micro)")
    print(f"    TP / FP / FN            : {brand_tp} / {brand_fp} / {brand_fn}")
    print(f"    Précision marque        : {brand_precision:.1%}")
    print(f"    Rappel marque           : {brand_recall:.1%}")
    print(f"    F1 marque               : {brand_f1:.1%}")
    print(f"    Complétion set (GT+)    : {brand_fill_rate:.1%}")
    print("-" * 65)
    print("  Marque principale (mono-label, GT DA)")
    print(f"    Lignes évaluées         : {main_total}")
    print(f"    Main brand detected     : {main_correct} ({main_accuracy:.1%})")
    print(f"    Main brand missed       : {main_missed} ({main_missed_rate:.1%})")
    print(f"    Main brand incorrecte   : {main_wrong} ({main_wrong_rate:.1%})")
    print("=" * 65)

    if fn_details:
        print(f"\n  Faux Négatifs ({len(fn_details)}) :")
        for d in fn_details[:10]:
            print(f"    Ligne {d['row']} | {d['title']} | GT marque: {d['partner']}")

    if fp_details:
        print(f"\n  Faux Positifs ({len(fp_details)}) :")
        for d in fp_details[:10]:
            print(f"    Ligne {d['row']} | {d['title']} | Marqueur: {d['marqueur']}")

    if main_confusions:
        sorted_confusions = sorted(main_confusions.items(), key=lambda x: x[1], reverse=True)
        print("\n  Top confusions marque principale :")
        for (gt_norm, pred_norm), count in sorted_confusions[:10]:
            gt_name = _display_label(gt_norm, {})
            pred_name = _display_label(pred_norm, {}) if pred_norm else "(vide)"
            print(f"    {gt_name} -> {pred_name} : {count}")

    if debug_csv_path:
        debug_fields = [
            "row_number",
            "post_url",
            "gt_da_manual_brand",
            "gt_main_brand",
            "gt_brand_set",
            "gt_detected",
            "pred_detected",
            "pred_main_brand",
            "pred_brand_set",
            "pred_partner_raw",
            "detect_status",
            "brand_match_status",
            "main_brand_detected",
            "main_brand_status",
            "paid_placement_raw",
            "marqueur_texte",
        ]
        with open(debug_csv_path, "w", encoding="utf-8", newline="") as debug_file:
            writer = csv.DictWriter(debug_file, fieldnames=debug_fields)
            writer.writeheader()
            writer.writerows(debug_rows)
        print(f"\n  Export debug écrit dans   : {debug_csv_path}")


# --- Point d'entrée ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Outils YouTube (évaluation / annotation).")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_eval = subparsers.add_parser("evaluate", help="Évaluer l'algorithme sur un CSV annoté")
    p_eval.add_argument("--csv", default="youtube_videos.csv", help="Chemin du CSV à évaluer")
    p_eval.add_argument(
        "--brands-csv",
        default=None,
        help="CSV catalogue marques (passe 2). Défaut: Labelisation - Brand... à côté du script.",
    )
    p_eval.add_argument(
        "--no-brands-csv",
        action="store_true",
        help="N'utiliser que la passe 1 (regex), sans liste de marques.",
    )

    p_eval_dash = subparsers.add_parser(
        "evaluate-da",
        help="Évaluer sur CSV Dash Admin (GT: DA - Manuel Collab Brand)",
    )
    p_eval_dash.add_argument("--csv", default="youtube_videos.csv", help="Chemin du CSV à évaluer")
    p_eval_dash.add_argument(
        "--brands-csv",
        default=None,
        help="CSV catalogue marques (passe 2). Défaut: Labelisation - Brand... à côté du script.",
    )
    p_eval_dash.add_argument(
        "--no-brands-csv",
        action="store_true",
        help="N'utiliser que la passe 1 (regex), sans liste de marques.",
    )
    p_eval_dash.add_argument(
        "--debug-output",
        default=None,
        help="Chemin d'export debug CSV (statut TP/FP/TN/FN par ligne).",
    )

    p_annotate = subparsers.add_parser("annotate", help="Annoter toutes les lignes (regex + liste)")
    p_annotate.add_argument("--input", default="youtube_videos.csv", help="CSV source")
    p_annotate.add_argument("--output", default="youtube_videos_annotated.csv", help="CSV de sortie")
    p_annotate.add_argument(
        "--brands-csv",
        default=None,
        help="CSV catalogue marques (passe 2). Défaut: Labelisation - Brand... à côté du script.",
    )
    p_annotate.add_argument(
        "--no-brands-csv",
        action="store_true",
        help="Désactive la passe 2 (aucun scan sur la liste de marques).",
    )

    args = parser.parse_args()

    if args.command == "evaluate":
        brands_path = resolve_brands_csv_path(args.brands_csv, args.no_brands_csv)
        evaluate_youtube(args.csv, brands_path)
    elif args.command == "evaluate-da":
        brands_path = resolve_brands_csv_path(args.brands_csv, args.no_brands_csv)
        evaluate_dash_admin_youtube(args.csv, brands_path, args.debug_output)
    else:
        brands_path = resolve_brands_csv_path(args.brands_csv, args.no_brands_csv)
        annotate_youtube_csv(args.input, args.output, brands_path)