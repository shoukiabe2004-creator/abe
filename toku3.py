import streamlit as st
import random
import os
from PIL import Image, ImageDraw

# ==============================================================================
# CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist",
    layout="wide"
)

# ==============================================================================
# DATA
# ==============================================================================
STYLES = ["Streetwear", "Casual", "Minimal"]
COLORS = ["Black", "White", "Green", "Beige", "Gray", "Navy"]

# ==============================================================================
# FALLBACK AVATAR
# ==============================================================================
class AvatarRenderer:
    @staticmethod
    def render():
        img = Image.new("RGB", (250, 450), (240, 240, 240))
        draw = ImageDraw.Draw(img)
        draw.ellipse([90, 20, 160, 90], fill=(235, 215, 200))
        draw.rectangle([80, 90, 170, 300], fill=(120, 120, 120))
        draw.rectangle([90, 300, 120, 420], fill=(80, 80, 80))
        draw.rectangle([130, 300, 160, 420], fill=(80, 80, 80))
        return img

# ==============================================================================
# SIDEBAR
# ==============================================================================
def sidebar_controls():
    with st.sidebar:
        st.header("⚙️ Preferences")

        gender = st.selectbox("Gender", ["Male", "Female"])
        styles = st.multiselect("Style", STYLES, default=["Casual"])
        colors = st.multiselect("Color", COLORS, default=["Black"])

        if st.button("✨ Recommend"):
            return {
                "gender": gender,
                "styles": styles,
                "colors": colors,
                "trigger": True
            }
    return {"trigger": False}

# ==============================================================================
# IMAGE SEARCH LOGIC
# ==============================================================================
def find_images(gender, style, color):
    base = "ai_images"
    path = os.path.join(base, gender.lower(), style.lower(), color.lower())

    if os.path.exists(path):
        files = [f for f in os.listdir(path) if f.endswith((".png", ".jpg"))]
        if files:
            return [os.path.join(path, f) for f in files]

    return []

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.markdown("あなたの好みに基づいたコーデ推薦")

    config = sidebar_controls()

    if config["trigger"]:
        gender = config["gender"]
        styles = config["styles"]
        colors = config["colors"]

        st.subheader("Recommended Outfits")

        cols = st.columns(3)
        shown = 0

        for col in cols:
            if shown >= 3:
                break

            style = random.choice(styles)
            color = random.choice(colors)

            images = find_images(gender, style, color)

            with col:
                if images:
                    img_path = random.choice(images)
                    img = Image.open(img_path)
                    st.image(img, use_container_width=True)
                else:
                    st.image(AvatarRenderer.render())

                # ===============================
                # Recommendation Reason
                # ===============================
                st.markdown("**Why this outfit?**")
                st.markdown(f"""
                - Gender: **{gender}**
                - Style: **{style}**
                - Color: **{color}**
                - Matches your selected preferences
                """)

            shown += 1

if __name__ == "__main__":
    main()
