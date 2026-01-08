import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation")

# -----------------------------
# 1. Genre & Color Definitions
# -----------------------------

GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]

COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]

COLOR_RGB = {
    "Black": (30, 30, 30),
    "White": (240, 240, 240),
    "Gray": (160, 160, 160),
    "Navy": (40, 60, 100),
    "Brown": (120, 80, 50),
    "Beige": (210, 200, 170),
    "Green": (60, 120, 80),
    "Red": (160, 50, 50)
}

# -----------------------------
# 2. User Input
# -----------------------------

st.header("👤 Select Gender")
gender = st.radio("Gender", ["Male", "Female"])

st.header("1️⃣ Rate Your Style Preference (0–5)")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("2️⃣ Rate Your Color Preference (0–5)")
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# -----------------------------
# 3. Score Completion
# -----------------------------

def complete_scores(scores):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# -----------------------------
# 4. Outfit Library
# -----------------------------

OUTFIT_LIBRARY = {
    "Streetwear": {"inner": ["Graphic Tee"], "outer": ["Hoodie"], "bottom": ["Wide Pants"]},
    "Casual": {"inner": ["Plain Tee"], "outer": ["Cardigan"], "bottom": ["Denim"]},
    "Minimal": {"inner": ["Plain Tee"], "outer": ["Jacket"], "bottom": ["Slacks"]},
    "Techwear": {"inner": ["Functional Tee"], "outer": ["Shell Jacket"], "bottom": ["Tech Pants"]},
    "Vintage": {"inner": ["Retro Tee"], "outer": ["Denim Jacket"], "bottom": ["Straight Jeans"]},
    "Formal": {"inner": ["Shirt"], "outer": ["Blazer"], "bottom": ["Slacks"]}
}

def generate_outfit(genre, color):
    p = OUTFIT_LIBRARY[genre]
    return {
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(p['inner'])}",
        "Outer": f"{color} {random.choice(p['outer'])}",
        "Bottom": f"{color} {random.choice(p['bottom'])}"
    }

# -----------------------------
# 5. Gender-Aware Image Generator
# -----------------------------

def generate_image(outfit, gender):
    base = COLOR_RGB[outfit["Color Theme"]]
    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (230, 200, 180)

    # ---- HEAD ----
    d.ellipse([100, 20, 160, 80], fill=skin, outline="black")

    # Hair
    if gender == "Male":
        d.rectangle([100, 20, 160, 45], fill=(50, 30, 20))
    else:
        d.ellipse([90, 15, 170, 110], outline=(60, 40, 20), width=4)

    # ---- BODY SHAPE ----
    if gender == "Male":
        body = [(60, 100), (200, 100), (215, 280), (45, 280)]
    else:
        body = [(80, 100), (180, 100), (200, 280), (60, 280)]

    d.polygon(body, fill=base, outline="black")

    # ---- INNER ----
    d.rectangle([105, 120, 155, 260], fill=(min(255, base[0]+40),)*3)

    # ---- ARMS ----
    d.rectangle([35, 120, 60, 260], fill=base)
    d.rectangle([200, 120, 225, 260], fill=base)

    # ---- BOTTOM ----
    if gender == "Female":
        d.polygon([(90, 280), (170, 280), (200, 360), (60, 360)], fill=(base[0]-30,)*3)
    else:
        d.rectangle([95, 280, 125, 400], fill=(base[0]-50,)*3)
        d.rectangle([135, 280, 165, 400], fill=(base[0]-50,)*3)

    # Shoes
    d.rectangle([90, 400, 130, 420], fill=(40, 40, 40))
    d.rectangle([130, 400, 170, 420], fill=(40, 40, 40))

    return img

# -----------------------------
# 6. Display Results
# -----------------------------

st.header("👕 Recommended Outfits")

for i, g in enumerate(top_genres):
    c = random.choice(top_colors)
    outfit = generate_outfit(g, c)
    img = generate_image(outfit, gender)

    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.image(img, caption=f"{gender} Outfit {i+1}")
    with col2:
        st.write(outfit)
