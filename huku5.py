import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation")

# -----------------------------
# 0. Gender Selection
# -----------------------------

st.header("0️⃣ Select Gender")
gender = st.radio("Gender", ["Male", "Female"])

# -----------------------------
# 1. Genre & Color Definitions
# -----------------------------

GENRES = [
    "Streetwear",
    "Casual",
    "Minimal",
    "Techwear",
    "Vintage",
    "Formal"
]

COLORS = [
    "Black",
    "White",
    "Gray",
    "Navy",
    "Brown",
    "Beige",
    "Green",
    "Red"
]

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

st.header("1️⃣ Rate Your Style Preference (0–5)")

genre_scores = {}
for g in GENRES:
    genre_scores[g] = st.slider(g, 0, 5, 0)

st.header("2️⃣ Rate Your Color Preference (0–5)")

color_scores = {}
for c in COLORS:
    color_scores[c] = st.slider(c, 0, 5, 0)

# -----------------------------
# 3. Content-Based Completion
# -----------------------------

def complete_scores(scores: dict):
    avg = sum(scores.values()) / len(scores)
    return {k: (v if v > 0 else round(avg, 2)) for k, v in scores.items()}

genre_scores = complete_scores(genre_scores)
color_scores = complete_scores(color_scores)

# -----------------------------
# 4. Select Top Genres & Colors
# -----------------------------

top_genres = sorted(genre_scores, key=genre_scores.get, reverse=True)[:3]
top_colors = sorted(color_scores, key=color_scores.get, reverse=True)[:3]

# -----------------------------
# 5. Outfit Templates (Gender-based)
# -----------------------------

OUTFIT_LIBRARY = {
    "Male": {
        "Streetwear": {
            "inner": ["Graphic Tee", "Long Sleeve Tee"],
            "outer": ["Hoodie", "Zip Hoodie"],
            "bottom": ["Wide Pants", "Cargo Pants"]
        },
        "Casual": {
            "inner": ["Plain T-Shirt", "Knit"],
            "outer": ["Cardigan", "Light Jacket"],
            "bottom": ["Denim", "Chinos"]
        },
        "Minimal": {
            "inner": ["Plain Tee"],
            "outer": ["Tailored Jacket"],
            "bottom": ["Slim Slacks"]
        },
        "Techwear": {
            "inner": ["Functional Tee"],
            "outer": ["Shell Jacket"],
            "bottom": ["Tech Pants"]
        },
        "Vintage": {
            "inner": ["Retro Tee"],
            "outer": ["Denim Jacket"],
            "bottom": ["Straight Jeans"]
        },
        "Formal": {
            "inner": ["Dress Shirt"],
            "outer": ["Blazer"],
            "bottom": ["Slacks"]
        }
    },
    "Female": {
        "Streetwear": {
            "inner": ["Crop Tee", "Short Tee"],
            "outer": ["Short Hoodie", "Denim Jacket"],
            "bottom": ["High-Waist Pants", "Wide Pants"]
        },
        "Casual": {
            "inner": ["Blouse", "Knit Top"],
            "outer": ["Cardigan", "Light Jacket"],
            "bottom": ["Flared Pants", "Skirt"]
        },
        "Minimal": {
            "inner": ["Plain Blouse"],
            "outer": ["Tailored Jacket"],
            "bottom": ["Slim Pants"]
        },
        "Techwear": {
            "inner": ["Functional Top"],
            "outer": ["Shell Jacket"],
            "bottom": ["Tech Pants"]
        },
        "Vintage": {
            "inner": ["Retro Blouse"],
            "outer": ["Denim Jacket"],
            "bottom": ["Long Skirt"]
        },
        "Formal": {
            "inner": ["Blouse"],
            "outer": ["Blazer"],
            "bottom": ["Slacks", "Long Skirt"]
        }
    }
}

# -----------------------------
# 6. Outfit Generator
# -----------------------------

def generate_outfit(gender, genre, color):
    parts = OUTFIT_LIBRARY[gender][genre]
    return {
        "Gender": gender,
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {random.choice(parts['bottom'])}"
    }

# -----------------------------
# 7. Image Generator (Human Silhouette)
# -----------------------------

def generate_image(outfit):
    base_color = COLOR_RGB[outfit["Color Theme"]]

    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)
    inner_color = tuple(min(255, c + 35) for c in base_color)
    bottom_color = tuple(max(0, c - 50) for c in base_color)

    # Head
    d.ellipse([105, 20, 155, 70], fill=skin)

    # Neck
    d.rectangle([120, 70, 140, 95], fill=skin)

    # Outer
    d.polygon(
        [(70, 100), (190, 100), (210, 270), (50, 270)],
        fill=base_color
    )

    # Inner
    d.rectangle([95, 120, 165, 250], fill=inner_color)

    # Bottom
    d.rectangle([95, 270, 125, 400], fill=bottom_color)
    d.rectangle([135, 270, 165, 400], fill=bottom_color)

    return img

# -----------------------------
# 8. Generate 3 Outfits
# -----------------------------

st.header("👕 Recommended Outfits")

used_colors = []

for i, genre in enumerate(top_genres):
    color = random.choice(top_colors)

    if color in used_colors and len(top_colors) > 1:
        color = random.choice([c for c in top_colors if c not in used_colors])

    used_colors.append(color)

    outfit = generate_outfit(gender, genre, color)
    img = generate_image(outfit)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(img, caption=f"Outfit {i+1}")

    with col2:
        st.subheader(f"Outfit {i+1} Details")
        st.write(f"**Gender:** {outfit['Gender']}")
        st.write(f"**Genre:** {outfit['Genre']}")
        st.write(f"**Color Theme:** {outfit['Color Theme']}")
        st.write(f"👕 Inner: {outfit['Inner']}")
        st.write(f"🧥 Outer: {outfit['Outer']}")
        st.write(f"👖 Bottom: {outfit['Bottom']}")

# -----------------------------
# 9. Display Final Scores
# -----------------------------

st.header("📊 Final Recommendation Scores")
st.subheader("Genre Scores")
st.json(genre_scores)

st.subheader("Color Scores")
st.json(color_scores)
