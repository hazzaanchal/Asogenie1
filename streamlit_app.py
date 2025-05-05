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

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.image("5A4057F4-07C9-499A-9951-14D4A196B088.png", width=160)
st.title("🔮 ASOGenie")
st.caption("AI-powered ASO keyword magic. Built for Indian apps.")

# 🔍 STEP 0: App Selector
st.markdown("### 🔍 Search a Play Store App")
query = st.text_input("Enter app name", placeholder="e.g. Cred, Amazon, Nykaa")
selected_app_info, selected_package = None, None
autofill_theme, autofill_keywords = "", []

if query:
    results = search(query, lang="en", country="in", count=10)
    app_titles = [f"{r['title']} ({r['appId']})" for r in results]
    app_selected = st.selectbox("Select your app", options=app_titles)

    if app_selected:
        selected_package = re.search(r'\((.*?)\)', app_selected).group(1)
        selected_app_info = fetch_app(selected_package, lang="en", country="in")
        st.image(selected_app_info['icon'], width=64, caption=selected_app_info['title'])
        st.success(f"Fetched data for: {selected_app_info['title']}")
        st.markdown(f"**Category:** {selected_app_info['genre']}")
        st.markdown(f"**Description Preview:** {selected_app_info['description'][:300]}...")

        # Autofill app theme
        autofill_theme = selected_app_info['description']
        autofill_keywords = selected_app_info['description'].lower().split()[:15]

# 🧠 App Theme Autofilled
st.markdown("### 💡 App Theme (Auto-filled from Play Store)")
st.info(autofill_theme[:500])

# 🔍 Competitor App Selector
st.markdown("### 🧑‍🤝‍🧑 Add Competitor Apps")
comp_query = st.text_input("Search competitor app", key="competitor_search")
comp_selected = []
if comp_query:
    comp_results = search(comp_query, lang="en", country="in", count=10)
    comp_titles = [f"{r['title']} ({r['appId']})" for r in comp_results]
    comp_selected = st.multiselect("Select competitor apps", options=comp_titles, key="competitor_multiselect")

# 📝 User Keyword Input
st.markdown("### ✍️ Already have keyword ideas?")
user_keywords = st.text_area("Paste your keywords (comma separated)", placeholder="e.g. credit card tracker, loan calculator")

# ⏳ Keyword generation
final_keywords = []

if st.button("Generate Keyword Suggestions"):
    st.info("Genie is working its magic...")
    base_theme = autofill_theme
    full_competitor_text = ""

    # Fetch competitor descriptions
    if comp_selected:
        for entry in comp_selected:
            pkg = re.search(r'\((.*?)\)', entry).group(1)
            try:
                app_info = fetch_app(pkg, lang="en", country="in")
                full_competitor_text += " " + app_info['description']
            except Exception as e:
                st.warning(f"Could not fetch data for {pkg}")

    # 1. AI-generated keywords
    ai_keywords = generate_ai_keywords(base_theme + " " + full_competitor_text, "", include_hindi=False)
    validated_ai = validate_keywords(ai_keywords)
    final_keywords.extend(validated_ai)

    # 2. User keywords
    if user_keywords:
        base = [kw.strip() for kw in user_keywords.split(",") if kw.strip()]
        expanded = expand_user_keywords(base)
        validated_expanded = validate_keywords(expanded)
        final_keywords.extend(validated_expanded)

    # 3. Metadata based fallback
    validated_meta = validate_keywords(autofill_keywords)
    final_keywords.extend(validated_meta)

# 📊 Output
if final_keywords:
    try:
        final_df = pd.DataFrame(final_keywords)
        required_cols = ["Keyword", "Volume (Est)", "Difficulty", "Efficiency", "In Autocomplete?", "Language"]
        if not all(col in final_df.columns for col in required_cols):
            st.warning("Some fields missing in output. Please check keyword_utils.py.")
        else:
            st.markdown("### 📈 Keyword Suggestions")
            st.dataframe(final_df)
            st.download_button("📥 Download CSV", final_df.to_csv(index=False), "asogenie_keywords.csv")
    except Exception as e:
        st.error(f"Something went wrong while displaying the keywords: {e}")
else:
    st.warning("No keywords generated. Try adjusting your inputs.")
