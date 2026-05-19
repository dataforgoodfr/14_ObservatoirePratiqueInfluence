import csv
import sys
import argparse
from pathlib import Path

# Import the core detection logic from your existing algorithm
try:
    from extraction_instagram import detect_instagram_partnership
except ImportError:
    print("Error: 'extraction_instagram.py' not found in the same directory.")
    sys.exit(1)

# Mapping to handle variations in input CSV column names (case-insensitive)
COLUMN_MAP = {
    "post_id": ["post-id", "id", "post id", "post_id"],
    "account": ["account", "da - key account", "author", "username", "handle"],
    "post_url": ["post url", "post_url", "url", "link"],
    "title": ["title", "titre"],
    "desc": ["description", "text", "caption", "legende"],
    "sn_brand": ["sn brand", "scrappé - sn brand", "branded_content", "brand"],
    "paid": [
        "sn has paid placement",
        "scrappé - sn has paid placement",
        "paid_placement",
        "paid",
    ],
}


def get_mapped_value(row: dict, field_keys: list[str]) -> str:
    """Helper to extract a value from the row using various possible column names."""
    row_lower = {k.lower().strip(): v for k, v in row.items() if k}

    for key in field_keys:
        if key in row_lower:
            return row_lower[key].strip()
    return ""


def process_dataset(input_csv: str, output_csv: str, social_network: str):
    print(f"Loading new dataset: {input_csv}")
    print(f"Social Network set to: {social_network}")

    # Define the exact output columns requested
    output_fields = [
        "post-id",
        "account",
        "post url",
        "title",
        "social network",
        "has_collab",
        "detected_brands",
    ]

    processed_count = 0
    detected_count = 0

    try:
        with (
            open(input_csv, "r", encoding="utf-8-sig") as f_in,
            open(output_csv, "w", encoding="utf-8", newline="") as f_out,
        ):
            reader = csv.DictReader(f_in)
            writer = csv.DictWriter(f_out, fieldnames=output_fields)
            writer.writeheader()

            for row in reader:
                # 1. Extract values from the input CSV
                post_id = get_mapped_value(row, COLUMN_MAP["post_id"])
                account = get_mapped_value(row, COLUMN_MAP["account"])
                post_url = get_mapped_value(row, COLUMN_MAP["post_url"])
                title = get_mapped_value(row, COLUMN_MAP["title"])
                desc = get_mapped_value(row, COLUMN_MAP["desc"])

                # Scraping signals (used by your algorithm)
                sn_brand = get_mapped_value(row, COLUMN_MAP["sn_brand"])
                paid_raw = get_mapped_value(row, COLUMN_MAP["paid"])
                paid_placement = paid_raw.lower() in ("true", "1", "vrai", "yes")

                # 2. Run your existing algorithm
                result = detect_instagram_partnership(
                    title=title,
                    description=desc,
                    sn_brand=sn_brand,
                    paid_placement=paid_placement,
                )

                # 3. Format and write the output
                has_collab = result["detected"]
                detected_brands = "|".join(result["brands"]) if result["brands"] else ""

                writer.writerow(
                    {
                        "post-id": post_id,
                        "account": account,
                        "post url": post_url,
                        "title": "",  # Set to blank as requested
                        "social network": social_network,  # Dynamically passed parameter
                        "has_collab": has_collab,
                        "detected_brands": detected_brands,
                    }
                )

                processed_count += 1
                if has_collab:
                    detected_count += 1

        print(f"✅ Extraction complete!")
        print(f"📊 Processed {processed_count} posts.")
        print(f"🎯 Detected {detected_count} collaborations.")
        print(f"📁 Output saved to: {output_csv}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract partnerships to a clean CSV.")
    parser.add_argument("input_csv", help="Path to the new raw dataset CSV.")
    parser.add_argument(
        "-o",
        "--output",
        help="Path for the output CSV. Defaults to 'extracted_<input_name>'",
        default=None,
    )
    parser.add_argument(
        "-n",
        "--network",
        help="Social network name to populate the column",
        default="Instagram",
    )

    args = (
        parser.ArgumentParser().parse_args()
        if len(sys.argv) == 1
        else parser.parse_args()
    )

    input_path = Path(args.input_csv)

    if args.output:
        output_path = args.output
    else:
        output_path = input_path.parent / f"extracted_{input_path.name}"

    process_dataset(str(input_path), str(output_path), args.network)
