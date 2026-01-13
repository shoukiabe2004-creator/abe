import streamlit as st
import os
import random
from PIL import Image

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(page_title="AI Fashion Recommender", layout="wide")

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

def weighted_choice(weight_dict):
    weighted_list = []
    for k, v in weight_dict.items():
        weighted_list.extend([k] * v)
    return random.choice(weighted_list) if weighted_list else None

# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.header("🧍 User Preferences")

    gender = st.radio("Gender", ["male", "female"])

    st.divider()

    st.subheader("🎨 Style Preference (0–10)")
    style_scores = {}
    for style in STYLES:
        score = st.slider(style.capitalize(), 0, 10, 0)
        if score > 0:
            style_scores[style] = score

    st.divider()

    st.subheader("🎯 Color Preference (0–10)")
    color_scores = {}
    for color in COLORS:
        score = st.slider(color.capitalize(), 0, 10, 0)
        if score > 0:
            color_scores[color] = score

    st.divider()

    generate = st.button("✨ Recommend Outfits")

# ==================================================
# MAIN
# ==================================================
st.title("AI Outfit Recommendation")
st.caption("Images are loaded directly from your GitHub repository")

if generate:
    if not style_scores or not color_scores:
        st.warning("スタイルと色を1つ以上評価してください。")
    else:
        selected_images = []

        for _ in range(3):
            style = weighted_choice(style_scores)
            color = weighted_choice(color_scores)

            imgs = get_images(gender, style, color)
            if imgs:
                selected_images.append({
                    "path": random.choice(imgs),
                    "style": style,
                    "color": color
                })

        if not selected_images:
            st.error("該当する画像が見つかりません。フォルダ構成を確認してください。")
        else:
            cols = st.columns(3)

            for col, item in zip(cols, selected_images):
                with col:
                    img = Image.open(item["path"])
                    st.image(img, use_container_width=True)

                    st.markdown("**Why this outfit?**")
                    st.markdown(f"""
- Style: **{item['style']}** (Score {style_scores[item['style']]})
- Color: **{item['color']}** (Score {color_scores[item['color']]})
- Match: High preference combination
""")
else:
    st.info("左のサイドバーで好みを評価してください 👈")
