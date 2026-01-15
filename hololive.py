import streamlit as st
import random
import os

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Hologram Edition",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# HOLOGRAM STYLE (BLUE / PINK / CYAN / PURPLE / RAINBOW)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ==============================
   BASE
============================== */
.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(110,203,255,0.18), transparent 40%),
        radial-gradient(circle at 80% 30%, rgba(255,122,217,0.16), transparent 45%),
        radial-gradient(circle at 50% 90%, rgba(199,184,255,0.14), transparent 40%),
        #0B0E14;
    color: #EEF1FF;
}

/* ==============================
   SIDEBAR
============================== */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            160deg,
            rgba(255,255,255,0.05),
            rgba(255,255,255,0.01)
        ),
        #0B0E14;
    border-right: 1px solid rgba(110,203,255,0.35);
    box-shadow: 4px 0 28px rgba(110,203,255,0.25);
    backdrop-filter: blur(10px);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    background: linear-gradient(
        90deg,
        #6ECBFF,
        #FF7AD9,
        #5AF2E8,
        #C7B8FF
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ==============================
   HEADERS
============================== */
h1, h2 {
    background: linear-gradient(
        90deg,
        #6ECBFF,
        #FF7AD9,
        #5AF2E8,
        #C7B8FF
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ==============================
   BUTTON
============================== */
div.stButton > button {
    background:
        linear-gradient(
            120deg,
            #6ECBFF,
            #FF7AD9,
            #5AF2E8,
            #C7B8FF
        );
    background-size: 300% 300%;
    color: #0B0E14;
    border: none;
    border-radius: 20px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    box-shadow:
        0 0 18px rgba(110,203,255,0.45),
        0 0 36px rgba(255,122,217,0.35);
    transition: all 0.3s ease;
    width: 100%;
}

div.stButton > button:hover {
    animation: holoShift 3s ease infinite;
    transform: translateY(-2px) scale(1.03);
}

/* ==============================
   SLIDER
============================== */
div[data-baseweb="slider"] > div {
    background-color: rgba(255,255,255,0.06);
}

div[data-baseweb="slider"] span {
    color: #5AF2E8;
}

/* ==============================
   IMAGE CARD
============================== */
img {
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.35);
    box-shadow:
        0 0 20px rgba(110,203,255,0.35),
        0 0 40px rgba(255,122,217,0.25);
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.15),
            rgba(255,255,255,0.03)
        );
}

/* ==============================
   EXPANDER
============================== */
details {
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.02)
        );
    border: 1px solid rgba(199,184,255,0.45);
    border-radius: 18px;
    padding: 0.6rem;
    box-shadow: 0 0 18px rgba(199,184,255,0.35);
    backdrop-filter: blur(12px);
}

summary {
    background: linear-gradient(
        90deg,
        #FF7AD9,
        #6ECBFF
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 600;
}

/* ==============================
   INFO BOX
============================== */
div[data-testid="stInfo"] {
    background:
        linear-gradient(
            120deg,
            rgba(110,203,255,0.12),
            rgba(255,122,217,0.12)
        );
    border: 1px solid rgba(110,203,255,0.5);
    color: #EEF1FF;
    box-shadow: 0 0 18px rgba(110,203,255,0.45);
}

/* ==============================
   ANIMATION
============================== */
@keyframes holoShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
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
        st.subheader("✨ Style Ratings (0–10)")
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
        generate = st.button("✨ Generate Hologram Outfit")

    return gender, style_scores, color_scores, generate

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.caption("Hologram Edition · Iridescent UI · Weight ≥ 12")

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

                with st.expander("Why this hologram outfit was selected", expanded=True):
                    st.markdown(f"""
- 🌈 Iridescent style & color harmony
- Total holo-weight: **{img['weight']}**
- Threshold passed (**≥12**)
- Gradient diversity applied
- No duplicate projections
""")
    else:
        st.info("👈 Adjust preferences and generate hologram fits")

# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
