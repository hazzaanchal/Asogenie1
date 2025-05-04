import random
import pandas as pd

# Placeholder AI logic
def generate_ai_keywords(app_theme, competitors, include_hindi=False):
    base = [
        "emi calculator", "loan interest checker", "home loan tracker", 
        "credit score monitor", "bill payment app", "finance manager",
        "loan savings app", "compare interest rates", "loan emi planner"
    ]

    if include_hindi:
        base += ["ऋण कैलकुलेटर", "क्रेडिट स्कोर ऐप", "होम लोन प्लानर"]

    return list(set(base))

# Fake validation logic
def validate_keywords(keywords):
    results = []
    for kw in keywords:
        volume = random.randint(500, 10000)
        difficulty = random.randint(20, 80)
        efficiency = round(volume / difficulty, 2)
        autocomplete = random.choice(["Yes", "No"])
        language = "Hindi" if any(ord(c) > 2000 for c in kw) else "English"
        results.append({
            "Keyword": kw,
            "Volume (Est)": volume,
            "Difficulty": difficulty,
            "Efficiency": efficiency,
            "In Autocomplete?": autocomplete,
            "Language": language
        })
    return pd.DataFrame(results)

# Expand user keywords
def expand_user_keywords(base_keywords):
    expansions = []
    for kw in base_keywords:
        expansions.append(kw)
        if "loan" in kw: expansions.append(f"{kw} tracker")
        if "credit" in kw: expansions.append(f"{kw} score app")
        if "bill" in kw: expansions.append(f"auto {kw} payment")
        expansions.append(f"best {kw} app")
    return list(set(expansions))
