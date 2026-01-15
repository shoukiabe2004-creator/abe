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
# STYLE（未来風・ネオンUI）
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top, #0f2027, #05080d);
    color: #E6F1FF;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #05080d, #0b1320);
    border-right: 1px solid rgba(0,255,255,0.25);
    box-shadow: 4px 0 20px rgba(0,255,255,0.15);
}

/* Headings */
h1, h2, h3 {
    color: #7df9ff;
    text-shadow: 0 0 8px rgba(125,249,255,0.6);
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #00f5ff, #7f00ff);
    color: #05080d;
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    width: 100%;
    font-weight: 600;
    border: none;
    box-shadow: 0 0 15px rgba(0,245,255,0.7);
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(127,0,255,0.9);
}

/* Images */
img {
    border-radius: 14px;
    box-shadow: 0 0 25px rgba(0,245,255,0.35);
}

/* Expander */
details {
    background: rgba(10,20,40,0.85);
    border: 1px solid rgba(0,255,255,0.3);
    border-radius: 12px;
    padding: 0.5rem;
    box-shadow: inset 0 0 15px rgba(0,255,255,0.15);
}

/* Sliders */
div[data-baseweb="slider"] > div {
    color: #7df9ff;
}

/* Captions */
.stCaption {
    color: #9adfff;
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
# IMAGE RECOMMENDER
# ==============================================================================
class ImageRecommender:
    @staticmethod
    def recommend(gender, style_scores, color_scores, max_images=3, min_weight=12):
        base_dir = "ai_images"
        gender_dir = "male" if gender == "male" else "female"

        candidates = []

        for style, s_score in style_scores.items():
            for color, c_score in color_scores.items():
                total_weight = s_score + c_score

                if total_weight < min_weight:
                    continue

                path = os.path.join(base_dir, gender_dir, style, color)
                if os.path.exists(path):
                    for file in os.listdir(path):
                        if file.lower().endswith((".png", ".jpg", ".jpeg")):
                            candidates.append({
                                "path": os.path.join(path, file),
                                "style": style,
                                "color": color,
                                "weight": total_weight
                            })

        if not candidates:
            return []

        selected = []
        pool = candidates.copy()

        while pool and len(selected) < max_images:
            weights = [c["weight"] for c in pool]
            choice = random.choices(pool, weights=weights, k=1)[0]
            selected.append(choice)
            pool.remove(choice)

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

        style_scores = {
            style: st.slider(style, 0, 10, 5)
            for style in StyleConfig.GENRES
        }

        st.divider()
        st.subheader("🌈 Color Ratings (0–10)")

        color_scores = {
            color: st.slider(color, 0, 10, 5)
            for color in StyleConfig.COLORS
        }

        st.divider()
        generate = st.button("✨ Recommend Outfits")

    return gender, style_scores, color_scores, generate

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.caption("Only outfits with total weight ≥ 12 are recommended. No duplicate images.")

    gender, style_scores, color_scores, generate = sidebar_controls()

    if "images" not in st.session_state:
        st.session_state["images"] = []

    if generate:
        st.session_state["images"] = ImageRecommender.recommend(
            gender=gender,
            style_scores=style_scores,
            color_scores=color_scores,
            max_images=3,
            min_weight=12
        )

    if st.session_state["images"]:
        cols = st.columns(3)

        for col, img in zip(cols, st.session_state["images"]):
            with col:
                st.image(img["path"], use_container_width=True)

                st.markdown(f"### {img['style']}")
                st.caption(f"Color: {img['color']} | Total Weight: {img['weight']}")

                with st.expander("Why this image was recommended", expanded=True):
                    st.markdown(f"""
                    - Style score + Color score = **{img['weight']}**
                    - Meets minimum threshold (**≥12**)
                    - Higher weight → higher recommendation probability
                    - No duplicate images
                    """)
    else:
        st.info("👈 Set ratings and click **Recommend Outfits**")

# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
