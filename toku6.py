import streamlit as st
import os
import random
from PIL import Image

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Fashion Recommender",
    layout="wide"
)

# ==================================================
# CONSTANTS
# ==================================================
IMAGE_ROOT = "ai_images"

STYLES = ["streetwear", "casual", "minimal", "vintage"]
COLORS = ["black", "white", "gray", "beige", "navy", "green", "red", "olive"]

# ==================================================
# FUNCTIONS
# ==================================================
def get_images(gender, style, color):
    path = os.path.join(IMAGE_ROOT, gender, style, color)
    if not os.path.exists(path):
        return []
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

def recommend_images(gender, style, color, n=3):
    images = get_images(gender, style, color)
    if len(images) == 0:
        return []
    return random.sample(images, min(n, len(images)))

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.header("🧍 User Preference")

    gender = st.radio("Gender", ["male", "female"])

    style = st.selectbox("Style", STYLES)

    color = st.selectbox("Color", COLORS)

    recommend = st.button("✨ Recommend")

# ==================================================
# MAIN
# ==================================================
st.title("AI Outfit Recommendation")
st.caption("Images are loaded directly from GitHub repository")

if recommend:
    images = recommend_images(gender, style, color)

    if not images:
        st.error("該当する画像が見つかりません。フォルダ構成を確認してください。")
    else:
        cols = st.columns(3)

        for i, img_path in enumerate(images):
            with cols[i]:
                img = Image.open(img_path)
                st.image(img, use_container_width=True)

                st.markdown("**Why this outfit?**")
                st.markdown(f"""
- Gender: **{gender}**
- Style: **{style}**
- Color: **{color}**
- Match: User preference一致
""")
else:
    st.info("左のサイドバーから条件を選んでください 👈")
