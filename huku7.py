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
        "Streetwear": {
            "inner": ["Graphic Tee"],
            "outer": ["Hoodie"],
            "bottom": ["Wide Pants"]
        },
        "Casual": {
            "inner": ["Plain T-Shirt"],
            "outer": ["Cardigan"],
            "bottom": ["Chinos"]
        },
        "Formal": {
            "inner": ["Dress Shirt"],
            "outer": ["Blazer"],
            "bottom": ["Slacks"]
        }
    },
    "Female": {
        "Streetwear": {
            "inner": ["Crop Tee"],
            "outer": ["Short Jacket"],
            "bottom": ["High Waist Pants"]
        },
        "Casual": {
            "inner": ["Blouse"],
            "outer": ["Light Cardigan"],
            "bottom": ["Flared Pants"]
        },
        "Formal": {
            "inner": ["Blouse"],
            "outer": ["Tailored Jacket"],
            "bottom": ["Skirt"]
        }
    }
}

# fallback
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
# 6. Image Generator (Face + Gender Difference)
# -----------------------------

def generate_image(outfit, gender):
    base = COLOR_RGB[outfit["Color"]]
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
    eye_size = 4 if gender == "Male" else 6
    d.ellipse([115, 45, 115 + eye_size, 45 + eye_size], fill="black")
    d.ellipse([140, 45, 140 + eye_size, 45 + eye_size], fill="black")

    # Nose
    d.line([130, 52, 130, 60], fill=(120, 90, 70), width=2)

    # Mouth
    mouth_y = 68 if gender == "Male" else 64
    d.arc([120, mouth_y, 150, mouth_y + 10], 0, 180, fill=(120, 60, 60), width=2)

    # Body shape
    if gender == "Male":
        body = [(60, 100), (200, 100), (215, 280]()
