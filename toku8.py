import streamlit as st
import random
import os
from PIL import Image

# =====================================================
# BASIC CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Stylist",
    layout="wide"
)

BASE_DIR = "ai_images"

STYLES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

# =====================================================
# UTIL FUNCTIONS
# =====================================================
def weighted_choice(score_dict):
    keys = list(score_dict.keys())
    weights = list(score_dict.values())
    return random.choices(keys, weights=weights, k=1)[0]

def get_images(gender, style, color):
    path = os.path.join(BASE_DIR, gender.lower(), style, color)
    if not os.path.exists(path):
        return []
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.header("🧍‍♂️ Select Gender")
    gender = st.selectbox("Gender", ["male", "female"])

    st.divider()

    st.header("🎨 Style Preference (0–10)")
    style_scores = {}
    for style in STYLES:
        style_scores[style] = st.slider(
            style, 0, 10, 5, key=f"style_{style}"
        )

    st.divider()

    st.header("🌈 Color Preference (0–10)")
    color_scores = {}
    for color in COLORS:
        color_scores[color] = st.slider(
            color, 0, 10, 5, key=f"color_{color}"
        )

    st.divider()

    generate = st.button("✨ Generate Outfit")

# =====================================================
# MAIN
# =====================================================
st.title("AI Outfit Recommendation")
st.caption("Based on your preferences, 3 outfits are selected.")

if generate:
    results = []
    max_trials = 40
    trials = 0

    while len(results) < 3 and trials < max_trials:
        trials += 1

        style = weighted_choice(style_scores)
        color = weighted_choice(color_scores)

        images = get_images(gender, style, color)
        if not images:
            continue

        img_path = random.choice(images)

        if img_path in [r["path"] for r in results]:
            continue

        results.append({
            "path": img_path,
            "style": style,
            "color": color
        })

    if len(results) < 3:
        st.warning("⚠️ Not enough matching images. Please add more images.")

    cols = st.columns(3)
    for col, item in zip(cols, results):
        with col:
            img = Image.open(item["path"])
            st.image(img, use_container_width=True)

            st.markdown("### Why this outfit?")
            st.markdown(f"""
- **Style**: {item['style']} (Score {style_scores[item['style']]})
- **Color**: {item['color']} (Score {color_scores[item['color']]})
""")
else:
    st.info("👈 Select preferences and click **Generate Outfit**")
