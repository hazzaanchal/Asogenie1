from google_play_scraper import search, app as fetch_app
import pandas as pd
import re
import streamlit as st
from keyword_utils import (
    generate_ai_keywords,
    validate_keywords,
    expand_user_keywords,
    extract_keywords_from_playstore_results
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

# 🔍 STEP 0: App Search
st.markdown("### 🔍 Search a Play Store App")
query = st.text_input("Enter your app name", placeholder="e.g. Cred, Amazon, Nykaa")
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

        autofill_theme = selected_app_info['description']
        autofill_keywords = selected_app_info['description'].lower().split()[:15]

# 🧠 App Theme Display
st.markdown("### 💡 App Theme (Auto-filled from Play Store)")
st.info(autofill_theme[:500])

# 🧑‍🤝‍🧑 Competitor App Search
st.markdown("### 🔄 Add Competitor Apps")
comp_query = st.text_input("Search competitor apps")
comp_selected = []
if comp_query:
    comp_results = search(comp_query, lang="en", country="in", count=10)
    comp_titles = [f"{r['title']} ({r['appId']})" for r in comp_results]
    comp_selected = st.multiselect("Select competitor apps", options=comp_titles, key="multi")

# ✍️ User Keyword Input
st.markdown("### ✍️ Already have keyword ideas?")
user_keywords = st.text_area("Paste your keywords (comma separated)", placeholder="e.g. credit card tracker, loan calculator")

# 🔮 Keyword Generation
final_keywords = []

if st.button("Generate Keyword Suggestions"):
    st.info("Genie is working...")

    # Collect app + competitor metadata
    full_theme = autofill_theme
    comp_text = ""

    for c in comp_selected:
        pkg = re.search(r'\((.*?)\)', c).group(1)
        try:
            app_info = fetch_app(pkg, lang="en", country="in")
            comp_text += app_info['description']
        except Exception:
            pass

    # Generate AI keywords
    ai_keywords = generate_ai_keywords(full_theme + " " + comp_text)
    validated_ai = validate_keywords(ai_keywords)
    final_keywords.extend(validated_ai)

    # Expand user keywords
    if user_keywords:
        base = [kw.strip() for kw in user_keywords.split(",") if kw.strip()]
        expanded = expand_user_keywords(base)
        validated_expanded = validate_keywords(expanded)
        final_keywords.extend(validated_expanded)

    # Extract keywords from live Play Store search
    dynamic_kw = extract_keywords_from_playstore_results(query)
    validated_dynamic = validate_keywords(dynamic_kw)
    final_keywords.extend(validated_dynamic)

# 📈 Output
if final_keywords:
    df = pd.DataFrame(final_keywords)
    st.markdown("### 📊 Keyword Suggestions")
    st.dataframe(df)
    st.download_button("📥 Download CSV", df.to_csv(index=False), "asogenie_keywords.csv")
else:
    st.warning("No keywords generated yet.")
