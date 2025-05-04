import random
import pandas as pd

def generate_ai_keywords(app_theme, competitors, include_hindi=False):
    base = []

    if "beauty" in app_theme.lower():
        base += [
            "beauty shopping app", "skincare deals", "makeup discounts",
            "hair care products", "lipstick sale", "cosmetic shopping app"
        ]

    if "loan" in app_theme.lower() or "credit" in app_theme.lower():
        base += [
            "credit score app", "loan interest checker", "emi calculator",
            "home loan tracker", "compare loan rates", "pay credit card bill"
        ]

    if include_hindi:
        base += ["ऋण कैलकुलेटर", "मेकअप ऐप", "त्वचा देखभाल ऐप"]

    return list(set(base))

def validate_keywords(keywords):
    results = []
    for kw in keywords:
        volume = random.randint(500, 12000)
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

    return results

def expand_user_keywords(base_keywords):
    expansions = []
    for kw in base_keywords:
        expansions.append(kw)
        expansions.append(f"best {kw}")
        expansions.append(f"{kw} app")
        if "credit" in kw: expansions.append("credit score checker")
        if "card" in kw: expansions.append("credit card reward app")
        if "bill" in kw: expansions.append("auto bill pay tracker")
    return list(set(expansions))
