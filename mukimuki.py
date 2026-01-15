import streamlit as st
import random
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Cyberpunk Edition",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CYBERPUNK STYLE (CYAN / MAGENTA / NEON GREEN / BLACK)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

/* ==============================
   BASE
============================== */
.stApp {
    background: radial-gradient(circle at top, #05070A 0%, #02030A 70%);
    color: #E5E7EB;
}

/* ==============================
   SIDEBAR
============================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #02030A 0%, #05070A 100%);
    border-right: 1px solid rgba(0, 246, 255, 0.3);
    box-shadow: 4px 0 24px rgba(0, 246, 255, 0.2);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    color: #00F6FF;
    text-shadow: 0 0 6px rgba(0, 246, 255, 0.6);
}

/* ==============================
   HEADERS
============================== */
h1, h2 {
    color: #00F6FF;
    text-shadow:
        0 0 8px rgba(0, 246, 255, 0.7),
        0 0 16px rgba(0, 246, 255, 0.4);
}

/* ==============================
   BUTTON
============================== */
div.stButton > button {
    background: linear-gradient(90deg, #00F6FF, #FF2A9D);
    color: #05070A;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.4rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    box-shadow:
        0 0 10px rgba(0, 246, 255, 0.6),
        0 0 22px rgba(255, 42, 157, 0.4);
    transition: all 0.25s ease-in-out;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow:
        0 0 14px rgba(57, 255, 20, 0.9),
        0 0 32px rgba(57, 255, 20, 0.6);
}

/* ==============================
   SLIDER
============================== */
div[data-baseweb="slider"] > div {
    background-color: #111827;
}

div[data-baseweb="slider"] span {
    color: #39FF14;
}

/* ==============================
   IMAGE CARD
============================== */
img {
    border-radius: 16px;
    border: 1px solid rgba(0, 246, 255, 0.45);
    box-shadow:
        0 0 18px rgba(0, 246, 255, 0.35),
        0 0 36px rgba(255, 42, 157, 0.2);
}

/* ==============================
   EXPANDER
============================== */
details {
    background-color: #02030A;
    border: 1px solid rgba(255, 42, 157, 0.35);
    border-radius: 12px;
    padding: 0.5rem;
    box-shadow: 0 0 14px rgba(255, 42, 157, 0.25);
}

summary {
    color: #FF2A9D;
    font-weight: 600;
}

/* ==============================
   INFO BOX
============================== */
div[data-testid="stInfo"] {
    background: rgba(0, 246, 255, 0.08);
    border: 1px solid #00F6FF;
    color: #00F6FF;
    box-shadow: 0 0 12px rgba(0, 246, 255, 0.4);
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
    st.caption("Cyberpunk Edition · Weight ≥ 12 · No duplicate images")

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
