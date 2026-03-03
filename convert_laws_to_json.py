import json
import os

INPUT_FILE = "laws.txt"            # your raw text file
OUTPUT_FILE = "law_data/india.json"

os.makedirs("law_data", exist_ok=True)

laws = []
line_number = 0

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        line_number += 1
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        parts = [p.strip() for p in line.split("|")]

        # We expect at least 4 columns
        if len(parts) < 4:
            print(f"⚠️ Skipped invalid line {line_number}: {line}")
            continue

        issue = parts[0]
        section = parts[1]
        punishment = parts[2]
        description = parts[3]

        laws.append({
            "issue": issue,
            "section": section,
            "punishment": punishment,
            "description": description,
            "jurisdiction": "central"   # you can change later
        })

output_data = {
    "country": "india",
    "last_updated": "2025-02-01",
    "total_laws": len(laws),
    "laws": laws
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(output_data, out, indent=2, ensure_ascii=False)

print(f"✅ Conversion complete!")
print(f"📁 Output file: {OUTPUT_FILE}")
print(f"📊 Total laws converted: {len(laws)}")