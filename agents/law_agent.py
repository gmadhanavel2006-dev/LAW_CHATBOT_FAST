import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAW_DIR = os.path.join(BASE_DIR, "law_data")


def load_law_data(country: str) -> list:
    try:
        path = os.path.join(LAW_DIR, f"{country.lower()}.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


def match_relevant_laws(issue_description: str, law_data: list) -> list:
    """
    SAFE dynamic matching.
    Skips invalid law entries.
    """
    results = []
    issue_lower = issue_description.lower()

    for law in law_data:
        if not isinstance(law, dict):
            continue  # 🔒 CRITICAL SAFETY

        explanation = law.get("explanation", "").lower()
        if any(word in explanation for word in issue_lower.split()):
            results.append(law)

    return results[:3]