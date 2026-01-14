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
# IMAGE RECOMMENDER
# ==============================================================================
class ImageRecommender:
    @staticmethod
    def recommend(gender, styles, colors, max_images=3):
        base_dir = "ai_images"
        gender_dir = "male" if gender == "male" else "female"

        candidates = []

        for style in styles:
            for color in colors:
                path = os.path.join(base_dir, gender_dir, style, color)
                if os.path.exists(path):
                    for file in os.listdir(path):
                        if file.lower().endswith((".png", ".jpg", ".jpeg")):
                            candidates.append({
                                "path": os.path.join(path, file),
                                "style": style,
                                "color": color
                            })

        if not candidates:
            return []

        return random.sample(candidates, min(max_images, len(candidates)))

# ==============================================================================
# SIDEBAR
# ==============================================================================
def sidebar_controls():
    with st.sidebar:
        st.header("⚙️ Preferences")

        gender = st.selectbox("Gender", ["male", "female"])

        st.divider()

        styles = st.multiselect(
            "Select Styles (multiple)",
            StyleConfig.GENRES,
            default=["casual"]
        )

        colors = st.multiselect(
            "Select Colors (multiple)",
            StyleConfig.COLORS,
            default=["black", "beige"]
        )

        st.divider()

        generate = st.button("✨ Recommend Outfits")

    return gender, styles, colors, generate

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.caption("Choose gender, styles, and colors to get AI-generated outfit images.")

    gender, styles, colors, generate = sidebar_controls()

    if "images" not in st.session_state:
        st.session_state["images"] = []

    if generate:
        st.session_state["images"] = ImageRecommender.recommend(
            gender=gender,
            styles=styles if styles else StyleConfig.GENRES,
            colors=colors if colors else StyleConfig.COLORS,
            max_images=3
        )

    if st.session_state["images"]:
        cols = st.columns(3)

        for col, img in zip(cols, st.session_state["images"]):
            with col:
                st.image(img["path"], use_container_width=True)

                st.markdown(f"### {img['style']}")
                st.caption(f"Color: {img['color']}")

                with st.expander("Why this image was recommended", expanded=True):
                    st.markdown(f"""
                    - Selected gender matches  
                    - Style **{img['style']}** selected  
                    - Color **{img['color']}** selected  
                    - Image found in AI-generated dataset  
                    """)
    else:
        st.info("👈 Select your preferences and click **Recommend Outfits**")

# ==============================================================================
# RUN
# ==============================================================================
if __name__ == "__main__":
    main()
