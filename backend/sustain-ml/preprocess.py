import gzip, json, os, csv

# Path to metadata folder
metadata_path = r"C:\Users\SHRIRAKSHA P ACHARYA\Downloads\abo-listings\listings\metadata"

POSITIVE_KEYWORDS = ["eco", "organic", "bamboo", "recycled", "sustainable", "biodegradable", "compostable", "renewable"]
NEGATIVE_KEYWORDS = ["plastic", "synthetic", "disposable", "single-use", "petroleum", "non-recyclable"]

def score_text(text):
    text = text.lower()
    score = 50
    for kw in POSITIVE_KEYWORDS:
        if kw in text:
            score += 10
    for kw in NEGATIVE_KEYWORDS:
        if kw in text:
            score -= 10
    return max(0, min(100, score))

def process_all_files(out_csv, limit_per_file=5000):
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "text", "score"])  # header

        for file in os.listdir(metadata_path):
            if file.endswith(".json.gz"):
                path = os.path.join(metadata_path, file)
                print(f"Processing {file}...")
                with gzip.open(path, "rt", encoding="utf-8") as fin:
                    for i, line in enumerate(fin):
                        if i >= limit_per_file: break
                        record = json.loads(line)

                        name = " ".join([x["value"] for x in record.get("item_name", [])])
                        bullets = " ".join([x["value"] for x in record.get("bullet_point", [])])
                        keywords = " ".join([x["value"] for x in record.get("item_keywords", [])])
                        text = f"{name} {bullets} {keywords}"

                        score = score_text(text)
                        writer.writerow([record.get("item_id"), name, text, score])

    print(f"✅ Done! Saved dataset to {out_csv}")

# Run
process_all_files("sustainability_dataset.csv", limit_per_file=2000)
