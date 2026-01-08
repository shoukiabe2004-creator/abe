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

st.header("0️⃣ Select Gender")
gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

st.header("1️⃣ Rate Your Style Preference (0–5)")
genre_scores = {g: st.slider(g, 0, 5, 0) for g in GENRES}

st.header("2️⃣ Rate Your Color Preference (0–5)")
color_scores = {c: st.slider(c, 0, 5, 0) for c in COLORS}

# -----------------------------
# 3. Content-Based Completion
# -----------------------------

def complete_scores(scores):
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
# 7. Image Generator (Face Added)
# -----------------------------

def generate_image(outfit, gender):
    base_color = COLOR_RGB[outfit["Color Theme"]]

    img = Image.new("RGB", (260, 440), (245, 245, 245))
    d = ImageDraw.Draw(img)

    skin = (220, 200, 180)
    inner_color = tuple(min(255, c + 35) for c in base_color)
    bottom_color = tuple(max(0, c - 50) for c in base_color)

    # Head
    d.ellipse([105, 20, 155, 70], fill=skin, outline="black")

    # Eyes
    d.ellipse([118, 38, 124, 44], fill="black")
    d.ellipse([136, 38, 142, 44], fill="black")

    # Eyelashes / Eyebrows
    if gender == "Female":
        d.line([116, 36, 126, 36], fill="black", width=2)
        d.line([134, 36, 144, 36], fill="black", width=2)
    else:
        d.line([114, 34, 128, 34], fill="black", width=3)
        d.line([132, 34, 146, 34], fill="black", width=3)

    # Nose
    d.line([130, 44, 130, 52], fill="black", width=2)

    # Mouth
    if gender == "Female":
        d.arc([122, 52, 138, 62], start=0, end=180, fill="black", width=2)
    else:
        d.line([122, 58, 138, 58], fill="black", width=2)

    # Neck
    d.rectangle([120, 70, 140, 95], fill=skin)

    # Outer
    d.polygon([(70, 100), (190, 100), (210, 270), (50, 270)], fill=base_color, outline="black")

    # Inner
    d.rectangle([95, 120, 165, 250], fill=inner_color, outline="black")

    # Bottom
    d.rectangle([95, 270, 125, 400], fill=bottom_color, outline="black")
    d.rectangle([135, 270, 165, 400], fill=bottom_color, outline="black")

    # Shoes
    d.rectangle([90, 400, 130, 420], fill=(40, 40, 40))
    d.rectangle([130, 400, 170, 420], fill=(40, 40, 40))

    return img

# -----------------------------
# 8. Generate Outfits
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
        st.subheader(f"Outfit {i+1} Details")
        st.write(f"**Genre:** {outfit['Genre']}")
        st.write(f"**Color Theme:** {outfit['Color Theme']}")
        st.write(f"👕 Inner: {outfit['Inner']}")
        st.write(f"🧥 Outer: {outfit['Outer']}")
        st.write(f"👖 Bottom: {outfit['Bottom']}")

# -----------------------------
# 9. Scores
# -----------------------------

st.header("📊 Final Recommendation Scores")
st.json({"Genre": genre_scores, "Color": color_scores})
