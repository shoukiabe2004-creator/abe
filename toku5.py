import streamlit as st
import random
from PIL import Image, ImageDraw

# ==============================================================================
# PAGE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Outfit Recommendation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# STYLE (CSS)
# ==============================================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Arial', sans-serif;
}
.stApp {
    background-color: #FAFAFA;
}
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E0E0E0;
}
div.stButton > button {
    background-color: #111;
    color: white;
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA DEFINITIONS
# ==============================================================================
class StyleConfig:
    GENRES = ["streetwear", "casual", "minimal", "Techwear", "Vintage", "Formal"]
    COLORS = ["black", "white", "Gray", "Navy", "Brown", "beige", "green", "red"]

    COLOR_MAP = {
        "black": (30,30,30),
        "white": (245,245,245),
        "Gray": (140,140,140),
        "Navy": (30,50,90),
        "Brown": (120,80,50),
        "beige": (220,210,190),
        "green": (60,100,70),
        "red": (160,50,50)
    }

    OUTFITS = {
        "streetwear": ["Oversized Tee", "Hoodie", "Cargo Pants"],
        "casual": ["T-shirt", "Denim Jacket", "Chinos"],
        "minimal": ["Shirt", "Slacks", "Leather Shoes"],
        "Techwear": ["Utility Jacket", "Tech Pants"],
        "Vintage": ["Flannel Shirt", "Washed Denim"],
        "Formal": ["Blazer", "Dress Pants"]
    }

# ==============================================================================
# AVATAR RENDERER
# ==============================================================================
class AvatarRenderer:
    @staticmethod
    def render(main_color):
        img = Image.new("RGB", (250, 450), (250,250,250))
        d = ImageDraw.Draw(img)
        c = StyleConfig.COLOR_MAP[main_color]

        # Head
        d.ellipse([90,20,160,90], fill=(235,215,200))
        # Body
        d.rectangle([80,90,170,260], fill=c)
        # Legs
        d.rectangle([90,260,120,400], fill=c)
        d.rectangle([130,260,160,400], fill=c)

        return img

# ==============================================================================
# SIDEBAR
# ==============================================================================
def sidebar():
    with st.sidebar:
        st.header("👤 Persona")

        gender = st.selectbox("Gender", ["male", "female"])

        st.divider()
        st.subheader("🎨 Styles (select multiple)")
        styles = st.multiselect(
            "Preferred Sty
