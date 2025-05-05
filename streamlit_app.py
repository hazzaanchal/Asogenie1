from google_play_scraper import search, app as fetch_app
import pandas as pd
import re
import streamlit as st
from keyword_utils import (
    generate_ai_keywords,
    validate_keywords,
    expand_user_keywords
)

# Set up
st.set_page_config(page_title="ASOGenie", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.image("5A4057F4-07C9-499A-9951-14D4A196B088.png", width=160)
st.title("🔮 ASOGenie")
st.caption("AI-powered ASO keyword magic. Built for Indian apps.")

# --- Step 0: App search ---
st.subheader("🔍 Search a Play Store App")
query = st.text_input("Enter app name", placeholder="e.g. Cred, Amazon, Nykaa")

selected_app_info, selected_package = None, None
autofill_theme = ""
autofill_keywords = []

if query:
    results = search(query)
    app_titles = [f"{r['title']} ({r['appId']})" for r in results]
    app_selected = st.selectbox("Select your app", options=app_titles)

    if app_selected:
        selected_package = re.search(r'\((.*?)\)', app_selected).group(1)
        selected_app_info = fetch_app(selected_package, lang="en", country="in")

        st.image(selected_app_info['icon'], width=64, caption=selected_app_info['title'])
        st.success(f"Fetched data for: {selected_app_info['title']}")
        st.markdown(f"**Category:** {selected_app_info['genre']}")
        st.markdown(f"**Description Preview:** {selected_app_info['description'][:300]}...")

        autofill_theme = selected_app_info['description'][:400]
        # Extract auto-suggestions
        words = re.findall(r'\b\w+\b', selected_app_info['description'].lower())
        common_words = [w for w in words if w not in {"the", "and", "you", "with", "for", "are", "this", "get", "your", "that", "have", "has"} and len(w) > 2]
        autofill_keywords = list(dict.fromkeys(common_words))[:15]  # de-dupe and limit

# --- Step 1: Theme Display ---
if selected_app_info:
    st.subheader("📘 App Theme (Auto-filled from Play Store)")
    st.info(autofill_theme)

# --- Step 2: Competitor Apps ---
st.subheader("🤝 Add Competitor Apps")
comp_query = st.text_input("Search competitor app")
competitor_ids = []

if comp_query:
    comp_results = search(comp_query)
    comp_titles = [f"{r['title']} ({r['appId']})" for r in comp_results]
    comp_selected = st.multiselect("Select competitor apps", options=comp_titles)

    for item in comp_selected:
        pkg = re.search(r'\((.*?)\)', item)
        if pkg:
            competitor_ids.append(pkg.group(1))

# Hindi toggle
include_hindi = st.checkbox("Include Hindi keywords")

# --- Step 3: Keyword ideas ---
st.subheader("✍️ Already have keyword ideas?")
suggested = ", ".join(autofill_keywords)
user_keywords = st.text_area("Paste your keywords (comma separated)", value=suggested)

# --- Generate Keywords ---
final_keywords = []

if st.button("Generate Keyword Suggestions"):
    st.info("Genie is working its magic...")

    # 1. AI + theme + competitors
    theme_input = autofill_theme
    competitor_str = ", ".join(competitor_ids)
    if theme_input:
        ai_keywords = generate_ai_keywords(theme_input, competitor_str, include_hindi)
        validated_ai = validate_keywords(ai_keywords)
        final_keywords.extend(validated_ai)

    # 2. Expanded user keywords
    if user_keywords:
        base = [kw.strip() for kw in user_keywords.split(",") if kw.strip()]
        expanded = expand_user_keywords(base)
        validated_expanded = validate_keywords(expanded)
        final_keywords.extend(validated_expanded)

    # 3. Metadata extracted keywords
    validated_extracted = validate_keywords(autofill_keywords)
    final_keywords.extend(validated_extracted)

# --- Output Section ---
if final_keywords:
    try:
        final_df = pd.DataFrame(final_keywords)
        required_cols = ["Keyword", "Volume (Est)", "Difficulty", "Efficiency", "In Autocomplete?", "Language"]
        if not all(col in final_df.columns for col in required_cols):
            st.warning("Some data fields are missing in the output. Please check logic or keyword_utils.py.")
        else:
            st.subheader("📈 Keyword Suggestions")
            st.dataframe(final_df)
            st.download_button("📥 Download CSV", final_df.to_csv(index=False), "asogenie_keywords.csv")
    except Exception as e:
        st.error(f"Something went wrong while displaying the keywords: {e}")
else:
    st.warning("No keywords generated. Try adjusting your inputs.")
