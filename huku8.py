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
    "White": (235, 235, 235),
    "Gray": (150, 150, 150),
    "Navy": (40, 60, 100),
    "Brown": (120, 80, 50),
    "Beige": (210, 200, 170),
    "Green": (60, 120, 80),
    "Red": (160, 50, 50)
}

# -----------------------------
# 2. User Input
# -----------------------------

st.header("1️⃣ Select Gender")
gender = st.radio("Gender", ["Male", "Female"])

st.header("2️⃣ Rate Your Style Preference (0–5)")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("3️⃣ Rate Your Color Preference (0–5)")
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
# 4. Outfit Library (Gender-based)
# -----------------------------

OUTFIT_LIBRARY = {
    "Male": {
        "Streetwear": {"inner": ["Graphic Tee"], "outer": ["Hoodie"], "bottom": ["Wide Pants"]},
        "Casual": {"inner": ["Plain T-Shirt"], "outer": ["Cardigan"], "bottom": ["Chinos"]},
        "Formal": {"inner": ["Dress Shirt"], "outer": ["Blazer"], "bottom": ["Slacks"]}
    },
    "Female": {
        "Streetwear": {"inner": ["Crop Tee"], "outer": ["Short Jacket"], "bottom": ["High Waist Pants"]},
        "Casual": {"inner": ["Blouse"], "outer": ["Light Cardigan"], "bottom": ["Flared Pants"]},
        "Formal": {"inner": ["Blouse"], "outer": ["Tailored Jacket"], "bottom": ["Skirt"]}
    }
}

def get_outfit_parts(gender, genre):
    return OUTFIT_LIBRARY[gender].get(
        genre, list(OUTFIT_LIBRARY[gender].values())[0]
    )

# -----------------------------
# 5. Outfit Generator
# -----------------------------

def generate_outfit(genre, color):
    parts = get_outfit_parts(gender, genre)
    return {
        "Genre": genre,
        "Color": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {random.choice(parts['bottom'])}"
    }

# -----------------------------
# 6. Utility (RGB safety)
# -----------------------------

def safe_color(c):
    return tuple(max(0, min(255, int(x))) for x in c)

# -----------------------------
# 7. Image Generator
# -----------------------------

def generate_image(outfit, gender):
    base = safe_color(COLOR_RGB[outfit["Color"]])
    darker = safe_color((base[0]-40, base[1]-40, base[2]-40))

    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (230, 200, 180)
    hair = (60, 40, 25)

    # Head
    d.ellipse([100, 20, 160, 80], fill=skin, outline="black")

    # Hair
    if gender == "Male":
        d.rectangle([100, 20, 160, 45], fill=hair)
    else:
        d.ellipse([90, 15, 170, 120], outline=hair, width=4)

    # Eyes
    eye = 4 if gender == "Male" else 6
    d.ellipse([115, 45, 115 + eye, 45 + eye], fill="black")
    d.ellipse([140, 45, 140 + eye, 45 + eye], fill="black")

    # Nose
    d.line([130, 52, 130, 60], fill=(120, 90, 70), width=2)

    # Mouth
    my = 68 if gender == "Male" else 64
    d.arc([120, my, 150, my + 10], 0, 180, fill=(120, 60, 60), width=2)

    # Body
    if gender == "Male":
        body = [(60, 100), (200, 100), (215, 280), (45, 280)]
    else:
        body = [(80, 100), (180, 100), (200, 280), (60, 280)]

    d.polygon(body, fill=base, outline="black")

    # Arms
    d.rectangle([35, 120, 60, 260], fill=base)
    d.rectangle([200, 120, 225, 260], fill=base)

    # Bottom
    if gender == "Male":
        d.rectangle([95, 280, 125, 400], fill=darker, outline="black")
        d.rectangle([135, 280, 165, 400], fill=darker, outline="black")
    else:
        d.polygon([(90, 280), (170, 280), (200, 360), (60, 360)],
                  fill=darker, outline="black")

    # Shoes
    d.rectangle([90, 400, 130, 420], fill=(40, 40, 40))
    d.rectangle([130, 400, 170, 420], fill=(40, 40, 40))

    return img

# -----------------------------
# 8. Display Results
# -----------------------------

st.header("👕 Recommended Outfits")

for i, genre in enumerate(top_genres):
    color = random.choice(top_colors)
    outfit = generate_outfit(genre, color)
    img = generate_image(outfit, gender)

    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.image(img, caption=f"Outfit {i+1}")
    with col2:
        st.subheader(f"Outfit {i+1}")
        st.write(f"**Gender:** {gender}")
        st.write(f"**Genre:** {outfit['Genre']}")
        st.write(f"**Color:** {outfit['Color']}")
        st.write(f"👕 {outfit['Inner']}")
        st.write(f"🧥 {outfit['Outer']}")
        st.write(f"👖 {outfit['Bottom']}")
