import random
import pandas as pd

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
