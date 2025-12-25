import streamlit as st
import random
from PIL import Image, ImageDraw

st.set_page_config(page_title="Outfit Recommendation", layout="wide")
st.title("Content-Based Outfit Recommendation")

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
    "Black": (40, 40, 40),
    "White": (235, 235, 235),
    "Gray": (160, 160, 160),
    "Navy": (45, 65, 110),
    "Brown": (120, 85, 55),
    "Beige": (215, 205, 175),
    "Green": (70, 130, 95),
    "Red": (165, 60, 60)
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
# 5. Outfit Templates
# -----------------------------

OUTFIT_LIBRARY = {
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
}

# -----------------------------
# 6. Outfit Generator
# -----------------------------

def generate_outfit(genre, color):
    parts = OUTFIT_LIBRARY[genre]
    return {
        "Genre": genre,
        "Color Theme": color,
        "Inner": f"{color} {random.choice(parts['inner'])}",
        "Outer": f"{color} {random.choice(parts['outer'])}",
        "Bottom": f"{color} {random.choice(parts['bottom'])}"
    }

# -----------------------------
# 7. REALISTIC ICON Image Generator
# -----------------------------

def generate_image(outfit):
    base = COLOR_RGB[outfit["Color Theme"]]

    img = Image.new("RGB", (260, 420), (245, 245, 245))
    d = ImageDraw.Draw(img)

    # Ground shadow
    d.ellipse([70, 360, 190, 400], fill=(210, 210, 210))

    # Head
    d.ellipse([105, 20, 155, 70], fill=(220, 200, 180))

    # Outer (gradient)
    for y in range(90, 250):
        ratio = (y - 90) / 160
        color = tuple(int(base[i] * (0.9 + ratio * 0.15)) for i in range(3))
        d.line([(70, y), (190, y)], fill=color)

    # Inner
    inner = tuple(min(255, c + 35) for c in base)
    d.rectangle([95, 115, 165, 235], fill=inner)

    # Collar
    d.polygon([(70,90),(105,90),(130,120),(95,120)], fill=base)
    d.polygon([(190,90),(155,90),(130,120),(165,120)], fill=base)

    # Bottom (gradient)
    bottom = tuple(max(0, c - 40) for c in base)
    for y in range(250, 360):
        ratio = (y - 250) / 110
        color = tuple(int(bottom[i] * (0.9 + ratio * 0.1)) for i in range(3))
        d.line([(100, y), (160, y)], fill=color)

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

    outfit = generate_outfit(genre, color)
    img = generate_image(outfit)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image(img, caption=f"Outfit {i+1}")

    with col2:
        st.subheader(f"Outfit {i+1} Details")
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
