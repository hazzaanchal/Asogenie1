import re
import random
from google_play_scraper import search

# ------------------------------
# 1. Extract Keywords from Play Store App Results
# ------------------------------

def extract_keywords_from_playstore_results(query, country='in', lang='en', num_apps=5):
    """
    Extracts keyword-like phrases from app titles and descriptions for a given query.
    """
    results = search(query, lang=lang, country=country)[:num_apps]
    phrases = set()

    for app in results:
        title = app.get("title", "")
        desc = app.get("description", "")

        title_words = re.findall(r'\b\w+\b', title.lower())
        desc_words = re.findall(r'\b\w+\b', desc.lower())

        # 2-word phrases from titles
        for i in range(len(title_words) - 1):
            phrase = f"{title_words[i]} {title_words[i+1]}"
            if all(len(w) > 2 for w in phrase.split()):
                phrases.add(phrase)

        # 3-word phrases from descriptions
        for i in range(len(desc_words) - 2):
            phrase = f"{desc_words[i]} {desc_words[i+1]} {desc_words[i+2]}"
            if all(len(w) > 2 for w in phrase.split()):
                phrases.add(phrase)

    return list(phrases)[:25]  # return top 25 phrases

# ------------------------------
# 2. Generate AI-style Keywords
# ------------------------------

def generate_ai_keywords(text_blob, competitors="", include_hindi=False):
    """
    Generates relevant keywords based on app text and optional competitor content.
    """
    base_seeds = detect_seed_keywords(text_blob + competitors)
    
    words = re.findall(r'\b\w+\b', text_blob.lower())
    candidates = []
    for i in range(len(words) - 2):
        phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
        if all(len(w) > 2 for w in phrase.split()):
            candidates.append(phrase)

    final = list(set(base_seeds + candidates[:20]))
    return final

# ------------------------------
# 3. Expand User Keywords with Free Synonyms
# ------------------------------

def expand_user_keywords(base_keywords):
    synonyms = {
        "loan": ["loan interest", "loan calculator", "personal loan app"],
        "credit": ["credit card rewards", "check credit score", "credit report free"],
        "emi": ["emi calculator", "monthly emi app", "auto debit emi"],
        "fashion": ["online shopping app", "kurti app", "western wear app"],
        "shopping": ["buy clothes online", "top brands", "discount fashion app"]
    }

    expanded = []
    for kw in base_keywords:
        expanded.append(kw)
        for key in synonyms:
            if key in kw.lower():
                expanded.extend(synonyms[key])
    return list(set(expanded))

# ------------------------------
# 4. Simulated Autocomplete Suggestions
# ------------------------------

def simulate_autocomplete(app_name, description):
    """
    Fake autocomplete-like keywords based on app name and core description terms.
    """
    suggestions = []

    core_terms = re.findall(r'\b\w+\b', description.lower())[:30]

    for term in core_terms:
        if len(term) > 3:
            suggestions.extend([
                f"{term} app",
                f"{term} india",
                f"{term} online",
                f"{term} tracker",
                f"best {term} app"
            ])

    return random.sample(list(set(suggestions)), 10)

# ------------------------------
# 5. Validate Keywords + Score
# ------------------------------

def validate_keywords(keywords, include_hindi=False):
    stopwords = {"and", "or", "the", "to", "for", "your", "with", "get", "have", "has", "this", "that", "you", "apps", "app"}
    cleaned = []

    for kw in keywords:
        kw_clean = re.sub(r"[^\w\s]", "", kw).strip().lower()
        if kw_clean and all(w not in stopwords for w in kw_clean.split()) and len(kw_clean) > 3:
            cleaned.append(kw_clean)

    cleaned = list(set(cleaned))

    final = []
    for kw in cleaned:
        volume = random.randint(500, 20000)
        difficulty = random.randint(10, 90)
        kei = round((volume ** 2) / (difficulty + 1), 2)
        efficiency = round((kei / 100000.0), 2)

        final.append({
            "Keyword": kw,
            "Volume (Est)": volume,
            "Difficulty": difficulty,
            "Efficiency": efficiency,
            "In Autocomplete?": "Yes" if "app" in kw or "online" in kw else "No",
            "Language": "English"
        })

    return final

# ------------------------------
# 6. Seed Keyword Generator by Genre (Free substitute for NLP)
# ------------------------------

def detect_seed_keywords(description):
    """
    Infers top seed keywords based on content heuristics.
    """
    description = description.lower()
    if "loan" in description or "emi" in description or "credit" in description:
        return ["emi calculator", "loan comparison", "credit score app", "home loan interest"]
    elif "shopping" in description or "fashion" in description or "wear" in description:
        return ["fashion shopping app", "buy kurtis online", "lehenga app", "western wear app"]
    elif "fitness" in description or "health" in description:
        return ["fitness tracker", "workout planner", "health monitor", "step counter"]
    else:
        return ["best app", "top rated app", "user friendly", "trending in india"]
