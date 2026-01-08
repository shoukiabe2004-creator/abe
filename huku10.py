import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation")

# -----------------------------
# 1. Definitions
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

PATTERNS = ["None", "Stripe", "Dot", "Check"]

# -----------------------------
# 2. User Input
# -----------------------------

st.header("0️⃣ Select Gender")
gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

st.header("1️⃣ Style Preference")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("2️⃣ Color Preference")
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# -----------------------------
# 3. Score Completion
# -----------------------------

def complete_scores(scores):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else avg) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# -----------------------------
# 4. Outfit Library
# -----------------------------

OUTFIT_LIBRARY = {
    "Streetwear": ["Graphic Tee", "Hoodie"],
    "Casual": ["Plain Tee", "Cardigan"],
    "Minimal": ["Plain Tee", "Jacket"],
    "Techwear": ["Functional Tee", "Shell Jacket"],
    "Vintage": ["Retro Tee", "Denim Jacket"],
    "Formal": ["Dress Shirt", "Blazer"]
}

# -----------------------------
# 5. Pattern Drawer
# -----------------------------

def draw_pattern(d, area, pattern, base_color):
    x1, y1, x2, y2 = area
    if pattern == "Stripe":
        for x in range(x1, x2, 8):
            d.line([(x, y1), (x, y2)], fill=(255, 255, 255, 60), width=2)

    elif pattern == "Dot":
        for x in range(x1, x2, 12):
            for y in range(y1, y2, 12):
                d.ellipse([x, y, x+3, y+3], fill=(255, 255, 255))

    elif pattern == "Check":
        for x in range(x1, x2, 12):
            d.line([(x, y1), (x, y2)], fill=(220, 220, 220), width=1)
        for y in range(y1, y2, 12):
            d.line([(x1, y), (x2, y)], fill=(220, 220, 220), width=1)

# -----------------------------
# 6. Image Generator
# -----------------------------

def generate_image(color_name, gender):
    base = COLOR_RGB[color_name]
    inner_pattern = random.choice(PATTERNS)
    outer_pattern = random.choice(PATTERNS)

    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)
    inner = tuple(min(255, c + 30) for c in base)
    bottom = tuple(max(0, c - 50) for c in base)

    # Head
    d.ellipse([105, 20, 155, 70], fill=skin, outline="black")

    # Face
    d.ellipse([118, 38, 124, 44], fill="black")
    d.ellipse([136, 38, 142, 44], fill="black")
    d.line([130, 44, 130, 52], fill="black", width=2)

    if gender == "Female":
        d.arc([122, 52, 138, 62], 0, 180, fill="black", width=2)
    else:
        d.line([122, 58, 138, 58], fill="black", width=2)

    # Neck
    d.rectangle([120, 70, 140, 95], fill=skin)

    # Outer
    outer_area = (60, 100, 200, 270)
    d.rectangle(outer_area, fill=base, outline="black")
    draw_pattern(d, outer_area, outer_pattern, base)

    # Zipper
    d.line([130, 100, 130, 270], fill=(200, 200, 200), width=2)

    # Inner
    inner_area = (95, 120, 165, 250)
    d.rectangle(inner_area, fill=inner, outline="black")
    draw_pattern(d, inner_area, inner_pattern, inner)

    # Logo
    d.rectangle([120, 170, 140, 190], fill=(255, 255, 255))

    # Pants
    d.rectangle([95, 270, 125, 400], fill=bottom, outline="black")
    d.rectangle([135, 270, 165, 400], fill=bottom, outline="black")
    d.line([110, 270, 110, 400], fill=(200, 200, 200))
    d.line([150, 270, 150, 400], fill=(200, 200, 200))

    # Shoes
    d.rectangle([90, 400, 130, 420], fill=(40, 40, 40))
    d.rectangle([130, 400, 170, 420], fill=(40, 40, 40))

    return img

# -----------------------------
# 7. Output
# -----------------------------

st.header("👕 Recommended Outfits")

for i, genre in enumerate(top_genres):
    color = random.choice(top_colors)
    img = generate_image(color, gender)
    st.image(img, caption=f"Outfit {i+1} | {genre} / {color}")
