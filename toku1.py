import streamlit as st
import random
from PIL import Image, ImageDraw

# ==============================================================================
# CONFIG
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Recommendation Demo",
    layout="wide"
)

# ==============================================================================
# STYLE DEFINITIONS
# ==============================================================================
GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

COLOR_MAP = {
    "Black": (25, 25, 25),
    "White": (245, 245, 245),
    "Gray": (130, 130, 130),
    "Navy": (35, 55, 95),
    "Brown": (105, 75, 55),
    "Beige": (225, 215, 190),
    "Green": (70, 110, 85),
    "Red": (160, 50, 50)
}

# ==============================================================================
# FAKE OUTFIT DATABASE (投稿コーデの代替)
# ==============================================================================
OUTFIT_DB = [
    {
        "id": 1,
        "gender": "Male",
        "genre": "Streetwear",
        "colors": ["Black", "White"],
        "items": ["Hoodie", "Cargo Pants"],
        "style_vector": {
            "Streetwear": 5, "Casual": 2, "Minimal": 1,
            "Techwear": 3, "Vintage": 1, "Formal": 0
        }
    },
    {
        "id": 2,
        "gender": "Female",
        "genre": "Minimal",
        "colors": ["Beige", "Brown"],
        "items": ["Coat", "Slacks"],
        "style_vector": {
            "Streetwear": 1, "Casual": 2, "Minimal": 5,
            "Techwear": 1, "Vintage": 2, "Formal": 3
        }
    },
    {
        "id": 3,
        "gender": "Male",
        "genre": "Techwear",
        "colors": ["Black", "Gray"],
        "items": ["Shell Jacket", "Tech Pants"],
        "style_vector": {
            "Streetwear": 2, "Casual": 1, "Minimal": 1,
            "Techwear": 5, "Vintage": 0, "Formal": 0
        }
    },
    {
        "id": 4,
        "gender": "Female",
        "genre": "Vintage",
        "colors": ["Red", "Brown"],
        "items": ["Denim Jacket", "Skirt"],
        "style_vector": {
            "Streetwear": 1, "Casual": 3, "Minimal": 1,
            "Techwear": 0, "Vintage": 5, "Formal": 1
        }
    }
]

# ==============================================================================
# SIMILARITY (推薦ロジック)
# ==============================================================================
def similarity(user_vec, outfit_vec):
    return sum(user_vec[g] * outfit_vec.get(g, 0) for g in GENRES)

# ==============================================================================
# AVATAR RENDERER
# ==============================================================================
def render_avatar(outfit):
    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    main_color = COLOR_MAP[outfit["colors"][0]]
    skin = (235, 215, 200)

    # Head
    d.ellipse([100, 20, 160, 80], fill=skin)
    # Eyes
    d.ellipse([115, 45, 122, 52], fill="black")
    d.ellipse([138, 45, 145, 52], fill="black")
    # Nose
    d.polygon([(130, 55), (125, 65), (135, 65)], fill=(200,180,160))

    # Body
    d.rectangle([80, 100, 180, 260], fill=main_color)
    # Arms
    d.rectangle([50, 120, 80, 260], fill=main_color)
    d.rectangle([180, 120, 210, 260], fill=main_color)

    # Legs
    d.rectangle([95, 260, 125, 400], fill=main_color)
    d.rectangle([135, 260, 165, 400], fill=main_color)

    return img

# ==============================================================================
# UI
# ==============================================================================
st.title("👗 AI Stylist – Recommendation System (Demo)")
st.markdown("**架空コーデDBを用いた推薦学習デモ**")

with st.sidebar:
    st.header("👤 User Preferences")

    gender = st.selectbox("Gender", ["Male", "Female"])

    st.subheader("Style Preference")
    user_vector = {}
    for g in GENRES:
        user_vector[g] = st.slider(g, 0, 5, 0)

    if st.button("✨ Recommend Outfits"):
        st.session_state["trigger"] = True
    else:
        st.session_state.setdefault("trigger", False)

# ==============================================================================
# RECOMMENDATION
# ==============================================================================
if st.session_state["trigger"]:
    candidates = []
    for o in OUTFIT_DB:
        if o["gender"] == gender:
            score = similarity(user_vector, o["style_vector"])
            candidates.append((score, o))

    top_outfits = sorted(candidates, reverse=True, key=lambda x: x[0])[:3]

    st.subheader("🎯 Recommended Looks")

    cols = st.columns(3)
    for col, (_, outfit) in zip(cols, top_outfits):
        with col:
            img = render_avatar(outfit)
            st.image(img)
            st.markdown(f"### {outfit['genre']}")
            st.caption(f"Colors: {', '.join(outfit['colors'])}")
            st.write("**Items**")
            for item in outfit["items"]:
                st.write(f"- {item}")

else:
    st.info("👈 サイドバーで嗜好を設定して推薦を実行してください")
