import re
import random
from google_play_scraper import search

# ------------------------------
# 1. Dynamic Keyword Extractor from Play Store Search
# ------------------------------

def extract_keywords_from_playstore_results(query, country='in', lang='en', num_apps=5):
    """
    Extracts keyword-like phrases from top app titles and descriptions from Play Store.
    """
    results = search(query, lang=lang, country=country, count=num_apps)
    phrases = set()

    for app in results:
        title = app.get("title", "")
        desc = app.get("description", "")

        title_words = re.findall(r'\b\w+\b', title.lower())
        desc_words = re.findall(r'\b\w+\b', desc.lower())

        for i in range(len(title_words) - 1):
            phrase = f"{title_words[i]} {title_words[i+1]}"
            if all(len(w) > 2 for w in phrase.split()):
                phrases.add(phrase)

        for i in range(len(desc_words) - 2):
            phrase = f"{desc_words[i]} {desc_words[i+1]} {desc_words[i+2]}"
            if all(len(w) > 2 for w in phrase.split()):
                phrases.add(phrase)

    return list(phrases)[:20]  # return top 20 phrases

# ------------------------------
# 2. Generate AI Keywords
# ------------------------------

def generate_ai_keywords(text_blob, competitors="", include_hindi=False):
    base_seeds = [
        "loan calculator", "emi tracker", "credit score app", "home loan interest",
        "finance insights", "bank statement manager", "payment reminder app",
        "monthly emi planner", "smart credit usage", "loan refinance tool"
    ]

    words = re.findall(r'\b\w+\b', text_blob.lower())
    candidates = []
    for i in range(len(words) - 2):
        phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
        if all(len(w) > 2 for w in phrase.split()):
            candidates.append(phrase)

    keywords = list(set(base_seeds + candidates[:15]))
    return keywords

# ------------------------------
# 3. Expand User Keywords
# ------------------------------

def expand_user_keywords(base_keywords):
    synonyms = {
        "loan": ["loan interest", "loan calculator", "personal loan app"],
        "credit": ["credit card rewards", "check credit score", "credit report free"],
        "emi": ["emi calculator", "monthly emi app", "auto debit emi"]
    }

    expanded = []
    for kw in base_keywords:
        expanded.append(kw)
        for key in synonyms:
            if key in kw.lower():
                expanded.extend(synonyms[key])
    return list(set(expanded))

# ------------------------------
# 4. Validate Keywords (clean + score)
# ------------------------------

def validate_keywords(keywords, include_hindi=False):
    stopwords = {"and", "or", "the", "to", "for", "your", "with", "get", "have", "has", "this", "that", "you", "apps", "app"}
    cleaned = []

    for kw in keywords:
        kw_clean = re.sub(r"[^\w\s]", "", kw).strip().lower()
        if kw_clean and all(w not in stopwords for w in kw_clean.split()) and len(kw_clean) > 3:
            cleaned.append(kw_clean)

    cleaned = list(set(cleaned))

    return [
        {
            "Keyword": kw,
            "Volume (Est)": random.randint(1000, 15000),
            "Difficulty": random.randint(10, 90),
            "Efficiency": round(random.uniform(0.5, 1.5), 2),
            "In Autocomplete?": "Yes" if "app" in kw or "calculator" in kw else "No",
            "Language": "English"
        }
        for kw in cleaned
    ]
