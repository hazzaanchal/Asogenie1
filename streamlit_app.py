import streamlit as st
import pandas as pd
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

st.markdown("**Step 1: Describe your app**")
app_theme = st.text_input("What does your app do?", placeholder="e.g. Track and pay credit card bills for rewards")
competitors = st.text_input("Any competitor apps? (comma separated)", placeholder="e.g. Cred, OneCard")
include_hindi = st.checkbox("Include Hindi keywords")

st.markdown("---")
st.markdown("**Step 2: Already have keyword ideas? Expand them with ASOGenie**")
user_keywords = st.text_area("Paste your keywords (comma separated)", placeholder="e.g. credit card tracker, loan calculator")

# ✅ INIT this outside button block to avoid NameError
final_keywords = []

if st.button("Generate Keyword Suggestions"):
    st.info("Genie is working its magic...")

    # From app theme + competitors
    if app_theme:
        ai_keywords = generate_ai_keywords(app_theme, competitors, include_hindi)
        validated_ai = validate_keywords(ai_keywords)
        final_keywords.extend(validated_ai)

    # From user-entered keywords
    if user_keywords:
        base = [kw.strip() for kw in user_keywords.split(",") if kw.strip()]
        expanded = expand_user_keywords(base)
        validated_expanded = validate_keywords(expanded)
        final_keywords.extend(validated_expanded)

# ✅ Output section outside the button block
if final_keywords:
    try:
        final_df = pd.DataFrame(final_keywords)

        required_cols = ["Keyword", "Volume (Est)", "Difficulty", "Efficiency", "In Autocomplete?", "Language"]
        if not all(col in final_df.columns for col in required_cols):
            st.warning("Some data fields are missing in the output. Please check logic or keyword_utils.py.")
        else:
            st.dataframe(final_df)
            st.download_button("📥 Download CSV", final_df.to_csv(index=False), "asogenie_keywords.csv")
    except Exception as e:
        st.error(f"Something went wrong while displaying the keywords: {e}")
else:
    st.warning("No keywords generated. Try adjusting your inputs.")
