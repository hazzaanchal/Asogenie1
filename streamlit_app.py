from google_play_scraper import search, app as fetch_app
import pandas as pd
import re
import streamlit as st
from keyword_utils import (
    generate_ai_keywords,
    validate_keywords,
    expand_user_keywords
)

st.set_page_config(page_title="ASOGenie", layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.image("5A4057F4-07C9-499A-9951-14D4A196B088.png", width=160)

st.title("🔮 ASOGenie")
st.caption("AI-powered ASO keyword magic. Built for Indian apps.")

# 🔍 STEP 0: DYNAMIC APP SELECTOR
st.markdown("### 🔍 Search a Play Store App")
query = st.text_input("Enter app name", placeholder="e.g. Cred, Amazon, Nykaa")

selected_app_info = None
selected_package = None
autofill_theme = ""
autofill_keywords = []

if query:
    results = search(query)
    if results:
        app_titles = [f"{r['title']} ({r['appId']})" for r in results]
        app_selected = st.selectbox("Select your app", options=app_titles)

        if app_selected:
            selected_package = re.search(r'\((.*?)\)', app_selected).group(1)
            selected_app_info = fetch_app(selected_package, lang="en", country="in")

            st.image(selected_app_info['icon'], width=64, caption=selected_app_info['title'])
            st.success(f"Fetched data for: {selected_app_info['title']}")
            st.markdown(f"**Category:** {selected_app_info['genre']}")
            st.markdown(f"**Description Preview:** {selected_app_info['description'][:300]}...")

            autofill_theme = selected_app_info['description'][:300]
            autofill_keywords = selected_app_info['description'].lower().split()[:15]

            st.markdown("### 🧠 App Theme (Auto-filled from Play Store)")
            st.info(autofill_theme)
    else:
        st.warning("No app found. Try modifying your search term.")

# 🔍 STEP 1.5: COMPETITOR APP PICKER
st.markdown("### 🔄 Add Competitor Apps")
competitor_query = st.text_input("Search competitor app", placeholder="e.g. OneCard, PhonePe")
competitor_options = []
selected_competitors = []

if competitor_query:
    competitor_results = search(competitor_query)
    competitor_options = [f"{r['title']} ({r['appId']})" for r in competitor_results]
    selected_competitors = st.multiselect("Select competitor apps", options=competitor_options)

# 🔧 HINDI SWITCH
include_hindi = st.checkbox("Include Hindi keywords")

# 🔧 STEP 2: Expand User Keywords
st.markdown("### ✍️ Already have keyword ideas?")
suggested_keyword_base = ", ".join(autofill_keywords[:5]) if autofill_keywords else ""
user_keywords = st.text_area(
    "Paste your keywords (comma separated)",
    placeholder="e.g. credit card tracker, loan calculator",
    value=suggested_keyword_base
)

# ✅ INIT
final_keywords = []

if st.button("Generate Keyword Suggestions"):
    st.info("Genie is working its magic...")

    # 1. From app metadata
    full_theme = autofill_theme
    competitors_text = ", ".join([re.search(r'\((.*?)\)', c).group(1) for c in selected_competitors]) if selected_competitors else ""

    if full_theme:
        ai_keywords = generate_ai_keywords(full_theme, competitors_text, include_hindi)
        validated_ai = validate_keywords(ai_keywords)
        final_keywords.extend(validated_ai)

    # 2. From user keywords
    if user_keywords:
        base = [kw.strip() for kw in user_keywords.split(",") if kw.strip()]
        expanded = expand_user_keywords(base)
        validated_expanded = validate_keywords(expanded)
        final_keywords.extend(validated_expanded)

    # 3. From raw app description words
    if autofill_keywords:
        validated_extracted = validate_keywords(autofill_keywords)
        final_keywords.extend(validated_extracted)

# ✅ Output
if final_keywords:
    try:
        final_df = pd.DataFrame(final_keywords)
        required_cols = ["Keyword", "Volume (Est)", "Difficulty", "Efficiency", "In Autocomplete?", "Language"]
        if not all(col in final_df.columns for col in required_cols):
            st.warning("Some data fields are missing in the output. Please check logic or keyword_utils.py.")
        else:
            st.markdown("### 🧾 Keyword Suggestions")
            st.dataframe(final_df)
            st.download_button("📥 Download CSV", final_df.to_csv(index=False), "asogenie_keywords.csv")
    except Exception as e:
        st.error(f"Something went wrong while displaying the keywords: {e}")
else:
    st.warning("No keywords generated. Try adjusting your inputs.")
