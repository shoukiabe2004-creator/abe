import streamlit as st
import random
import os
from PIL import Image, ImageDraw

# ==============================================================================
# CONFIG & STYLES
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Premium Outfit Recommendations",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Arial', sans-serif;
}
.stApp {
    background-color: #FAFAFA;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA DEFINITIONS
# ==============================================================================
class StyleConfig:
    GENRES = ["streetwear", "casual", "Minimal", "Techwear", "Vintage", "Formal"]
    COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

# ==============================================================================
# AVATAR (Fallback)
# ==============================================================================
class AvatarRenderer:
    @staticmethod
    def render():
        img = Image.new("RGB", (250, 450), (240, 240, 240))
        draw = ImageDraw.Draw(img)

        # Head
        draw.ellipse([90, 20, 160, 90], fill=(235, 215, 200))
        # Body
        draw.rectangle([80, 90, 170, 300], fill=(120, 120, 120))
        # Legs
        draw.rectangle([90, 300, 120, 420], fill=(80, 80, 80))
        draw.rectangle([130, 300, 160, 420], fill=(80, 80, 80))

        return img

# ==============================================================================
# SIDEBAR
# ==============================================================================
def sidebar_controls():
    with st.sidebar:
        st.header("⚙️ Configure Persona")

        gender = st.selectbox("Gender", ["male", "female"])
        genres = st.multiselect(
            "Favorite Styles",
            StyleConfig.GENRES,
            default=["casual"]
        )

        if st.button("✨ Generate Collection"):
            return {
                "gender": gender,
                "genres": genres,
                "trigger": True
            }
    return {"trigger": False}

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    st.title("AI Personal Stylist")
    st.markdown("AI生成画像 × スタイリング推薦デモ")

    config = sidebar_controls()

    if config["trigger"]:
        gender = config["gender"]

        # ===============================
        # ★ AI画像フォルダ切り替え部分
        # ===============================
        image_root = "ai_images"
        gender_folder = "male" if gender == "male" else "female"
        image_path = os.path.join(image_root, gender_folder)

        st.subheader("Recommended Outfit")

        if os.path.exists(image_path):
            image_files = [
                f for f in os.listdir(image_path)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ]

            if image_files:
                selected_image = random.choice(image_files)
                img = Image.open(os.path.join(image_path, selected_image))
                st.image(img, use_container_width=True)
            else:
                st.warning("画像がありません。アバター表示に切り替えます。")
                st.image(AvatarRenderer.render())
        else:
            st.warning("画像フォルダが見つかりません。")
            st.image(AvatarRenderer.render())

if __name__ == "__main__":
    main()
