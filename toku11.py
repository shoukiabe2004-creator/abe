import streamlit as st
import random
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# STYLE
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background-color: #FAFAFA;
}

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E0E0E0;
}

h1, h2, h3 {
    font-weight: 600;
}

div.stButton > button {
    background-color: #111111;
    color: white;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA
# ==============================================================================
class StyleConfig:
    GENRES = ["streetwear", "casual", "minimal", "vintage", "kireime"]
    COLORS = ["black", "white", "gray", "navy", "brown", "beige", "green", "red"]

# ==============================================================================
# IMAGE RECOMMENDER (評価ベース)
# ==============================================================================
class ImageRecommender:
    @staticmethod
    def recommend(gender, style_scores, color_scores, max_images=3):
        base_dir = "ai_images"
        gender_dir = "male" if gender == "male" else "female"

        candidates = []

        for style, s_score in style_scores.items():
            for color, c_score in color_scores.items():
                weight = s_score + c_score
                if weight <= 0:
                    continue

                path = os.path.join(base_dir, gender_dir, style, color)
                if os.path.exists(path):
                    for file in os.listdir(path):
                        if file.lower().endswith((".png", ".jpg", ".jpeg")):
                            candidates.append({
                                "path": os.path.join(path, file),
                                "style": style,
                                "color": color,
                                "weight": weight,
                                "style_score": s_score,
                                "color_score": c_score
                            })

        if not candidates:
            return []

        weights = [c["weight"] for c in candidates]
        selected = random.choices(candidates, weights=weights, k=min(max_images, len(candidates)))

        return selected

# ==============================================================================
# SIDEBAR
# ==============================================================================
def sidebar_controls():
    with st.sidebar:
        st.header("⚙️ Preferences")

        gender = st.selectbox("Gender", ["male", "female"])
        st.divider()

        st.subheader("🎨 Style Ratings (0–10)")
        style_scores = {}
        for style in StyleConfig.GENRES:
            style_scores[style] = st.slider(
                style.capitalize(),
                0, 10, 5
            )

        st.divider()

        st.subheader("🎯 Color Ratings (0–10)")
        color_scores = {}
        for color in StyleConfig.COLORS:
            color_scores[color] = st.slider(
                color.capitalize(),
                0, 10, 5
            )

        st.divider()
        generate = st.button("✨ Recommend Outfits")

    return gender, style_scores, color_scores, generate

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.caption("Rate styles and colors (0–10). Higher ratings are recommended more often.")

    gender, style_scores, color_scores, generate = sidebar_controls()

    if "images" not in st.session_state:
        st.session_state["images"] = []

    if generate:
        st.session_state["images"] = ImageRecommender.recommend(
            gender=gender,
            style_scores=style_scores,
            color_scores=color_scores,
            max_images=3
        )

    if st.session_state["images"]:
        cols = st.columns(3)

        for col, img in zip(cols, st.session_state["images"]):
            with col:
                st.image(img["path"], use_container_width=True)

                st.markdown(f"### {img['style'].capitalize()}")
                st.caption(f"Color: {img['color']}")

                with st.expander("Why this image was recommended", expanded=True):
                    st.markdown(f"""
                    - Gender matched: **{gender}**
                    - Style score (**{img['style']}**): **{img['style_score']} / 10**
                    - Color score (**{img['color']}**): **{img['color_score']} / 10**
                    - Total weight: **{img['weight']}**
                    """)

    else:
        st.info("👈 Rate styles & colors, then click **Recommend Outfits**")

# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
