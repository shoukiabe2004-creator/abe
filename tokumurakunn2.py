import streamlit as st
import random
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# CONFIG & STYLES
# ==============================================================================
st.set_page_config(
    page_title="AI Stylist | Premium Outfit Recommendations",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Global Background */
    .stApp {
        background-color: #FAFAFA;
        color: #333333;
    }
    
    /* Sidebar Styling */
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E0E0E0;
    }

    /* Fix: Force text colors in sidebar to ensure visibility against white background */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        color: #111111 !important;
    }

    /* Fix: Ensure Button Text is White (overriding the generic sidebar rule above) */
    section[data-testid="stSidebar"] button span,
    section[data-testid="stSidebar"] button p {
        color: #FFFFFF !important;
    }

    /* Fix: Ensure Selectbox Background is White so black text is visible */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #111111;
        font-weight: 600;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #111111;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        width: 100%;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #333333;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Cards (Custom Logic needed to wrap streamlits columns, but we simulate via clean layout) */
    .outfit-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #EAEAEA;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    
    /* Dividers */
    hr {
        margin: 2em 0;
        border-color: #EEEEEE;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA DEFINITIONS
# ==============================================================================
class StyleConfig:
    GENRES = ["Streetwear", "Casual", "Minimal", "Techwear", "Vintage", "Formal"]
    COLORS = ["Black", "White", "Gray", "Navy", "Brown", "Beige", "Green", "Red"]
    
    # Enhanced Palette (RGB)
    COLOR_MAP = {
        "Black": (20, 20, 20),
        "White": (245, 245, 245),
        "Gray": (120, 120, 125),
        "Navy": (30, 45, 80),
        "Brown": (100, 70, 50),
        "Beige": (220, 210, 190),
        "Green": (55, 90, 60),
        "Red": (160, 40, 40)
    }

    OUTFIT_LIBRARY = {
        "Streetwear": {
            "inner": ["Oversized Tee", "Graphic Hoodie"],
            "outer": ["Bomber Jacket", "Puffer Vest"],
            "bottom": ["Cargo Pants", "Joggers"],
            "skirt": ["Pleated Mini", "Sport Skirt"],
            "shoe": ["Chunky Sneakers", "High Tops"]
        },
        "Casual": {
            "inner": ["Cotton Tee", "Soft Knit"],
            "outer": ["Denim Jacket", "Cardigan"],
            "bottom": ["Straight Jeans", "Chinos"],
            "skirt": ["A-Line Skirt", "Long Denim Skirt"],
            "shoe": ["Low Sneakers", "Loafers"]
        },
        "Minimal": {
            "inner": ["Mock Neck", "Crisp Shirt"],
            "outer": ["Trench Coat", "Wool Coat"],
            "bottom": ["Tapered Slacks", "Wide Trousers"],
            "skirt": ["Silk Skirt", "Pencil Skirt"],
            "shoe": ["Leather Boots", "Minimal Sneakers"]
        },
        "Techwear": {
            "inner": ["Compression Top", "Tech Tee"],
            "outer": ["Hardshell Parka", "Utility Vest"],
            "bottom": ["Tech Cargo", "Nylon Pants"],
            "skirt": ["Box Pleat Skirt", "Utility Skirt"],
            "shoe": ["Tactical Boots", "Running Shoes"]
        },
        "Vintage": {
            "inner": ["Ringer Tee", "Flannel Shirt"],
            "outer": ["Corduroy Jacket", "Varsity Jacket"],
            "bottom": ["Washed Jeans", "Corduroy Pants"],
            "skirt": ["Checkered Skirt", "Midi Skirt"],
            "shoe": ["Retro Trainers", "Leather Shoes"]
        },
        "Formal": {
            "inner": ["Dress Shirt", "Silk Blouse"],
            "outer": ["Tailored Blazer", "Long Coat"],
            "bottom": ["Dress Trousers", "Pressed Slacks"],
            "skirt": ["Wait Skirt", "Formal Midi"],
            "shoe": ["Derby Shoes", "Heels"]
        }
    }

    # Similarity/Affinity Matrix for Content-Based Recommendation (0.0 - 1.0)
    GENRE_RELATIONS = {
        "Streetwear": {"Techwear": 0.9, "Casual": 0.6, "Vintage": 0.4},
        "Casual": {"Minimal": 0.7, "Vintage": 0.7, "Streetwear": 0.5, "Formal": 0.3},
        "Minimal": {"Casual": 0.7, "Formal": 0.8, "Techwear": 0.4, "Streetwear": 0.2},
        "Techwear": {"Streetwear": 0.9, "Minimal": 0.5},
        "Vintage": {"Casual": 0.7, "Streetwear": 0.4, "Formal": 0.2},
        "Formal": {"Minimal": 0.8, "Casual": 0.3}
    }

    COLOR_RELATIONS = {
        "Black": {"Gray": 0.9, "Navy": 0.8, "White": 0.6},
        "White": {"Beige": 0.8, "Gray": 0.7, "Black": 0.5},
        "Gray": {"Black": 0.9, "White": 0.8, "Navy": 0.7},
        "Navy": {"Black": 0.8, "Gray": 0.7, "Green": 0.4},
        "Brown": {"Beige": 0.9, "Green": 0.6},
        "Beige": {"Brown": 0.9, "White": 0.8, "Green": 0.5},
        "Green": {"Brown": 0.6, "Beige": 0.6, "Navy": 0.4},
        "Red": {"Brown": 0.3, "Black": 0.2}
    }

# ==============================================================================
# LOGIC CORE
# ==============================================================================
class RecommendationEngine:
    @staticmethod
    def infer_weights(user_scores, relations, all_keys):
        """
        If a user scores an item 0, try to infer a weight based on their positive scores
        and the relation matrix.
        NewWeight = Max( OtherScore * Affinity ) for all OtherItems
        """
        final_weights = []
        for key in all_keys:
            current_score = user_scores.get(key, 0)
            
            if current_score > 0:
                final_weights.append(current_score)
            else:
                # Inference Logic
                inferred_score = 0
                # Check all other items the user Liked
                for other_key, other_score in user_scores.items():
                    if other_score > 0 and other_key != key:
                        # Get affinity from other -> key or key -> other (undirected mostly)
                        affinity = relations.get(other_key, {}).get(key, 0)
                        # Also check reverse if not present (symmetry)
                        if affinity == 0:
                            affinity = relations.get(key, {}).get(other_key, 0)
                            
                        # Calculate potential score
                        impact = other_score * affinity
                        if impact > inferred_score:
                            inferred_score = impact
                
                # Apply a slight penalty to inferred scores so explicit choices usually win
                # But floor it at 0
                final_weights.append(max(0, inferred_score * 0.8))
        
        return final_weights

class OutfitGenerator:
    @staticmethod
    def get_complementary_color(base_color, color_scores):
        # Basic pairings for better harmony
        pairs = {
            "Black": ["White", "Gray", "Beige", "Red"],
            "White": ["Black", "Navy", "Beige", "Gray"],
            "Navy": ["White", "Beige", "Gray"],
            "Brown": ["Beige", "White", "Navy"],
            "Beige": ["Brown", "Navy", "Black", "White"],
            "Gray": ["Black", "White", "Navy"],
            "Green": ["Beige", "Black", "White"],
            "Red": ["Black", "White", "Denim"] # Denim handled as Navy visual often
        }
        # Get candidates list
        all_colors = list(color_scores.keys())
        candidates = pairs.get(base_color, all_colors)
        
        # Filter candidates to ensure they exist in user prefs, default weight 1 if missing for safety
        weights = [color_scores.get(c, 0) for c in candidates]
        
        # Fallback if weights are all 0
        if sum(weights) == 0:
            weights = [1] * len(candidates)
            
        return random.choices(candidates, weights=weights, k=1)[0]

    @staticmethod
    def create(genre, base_color, gender, use_outer, color_scores):
        lib = StyleConfig.OUTFIT_LIBRARY.get(genre, StyleConfig.OUTFIT_LIBRARY["Casual"])
        
        # Color Logic
        accent_color = OutfitGenerator.get_complementary_color(base_color, color_scores)
        
        # Item Selection
        is_skirt = (gender == "Female" and random.random() < 0.6)
        
        inner_item = random.choice(lib["inner"])
        outer_item = random.choice(lib["outer"]) if use_outer else None
        bottom_item = random.choice(lib["skirt"]) if is_skirt else random.choice(lib["bottom"])
        shoe_item = random.choice(lib["shoe"])

        return {
            "genre": genre,
            "main_color": base_color,
            "accent_color": accent_color,
            "items": {
                "inner": inner_item,
                "outer": outer_item,
                "bottom": bottom_item,
                "shoe": shoe_item
            },
            "meta": {
                "is_skirt": is_skirt,
                "has_outer": use_outer
            }
        }

class AvatarRenderer:
    @staticmethod
    def render(outfit):
        # High-res canvas for anti-aliasing (resize down later)
        W, H = 500, 900
        img = Image.new("RGB", (W, H), (250, 250, 250))
        draw = ImageDraw.Draw(img)

        # Colors
        c_main = StyleConfig.COLOR_MAP[outfit["main_color"]]
        c_accent = StyleConfig.COLOR_MAP[outfit["accent_color"]]
        c_skin = (235, 215, 200)
        c_hair = (40, 30, 30)
        
        # Helper to darken a color slightly for outlines/shading
        def shade(rgb, factor=0.85):
            return tuple(int(x * factor) for x in rgb)

        # --- DRAWING LAYERS ---
        
        # 1. Body/Head
        # Head
        draw.ellipse([200, 50, 300, 160], fill=c_skin)
        # Neck
        draw.rectangle([235, 150, 265, 190], fill=c_skin)
        
        meta = outfit["meta"]
        items = outfit["items"]

        # 2. Bottoms
        # If skirt, draw specialized shape
        pants_color = c_main # Monochromatic base usually looks good for bottoms
        
        if meta["is_skirt"]:
            # Skirt shape
            draw.polygon([
                (180, 450), (320, 450), # Waist
                (360, 650), (140, 650)  # Hem
            ], fill=pants_color)
            # Legs
            draw.rectangle([210, 650, 240, 800], fill=c_skin)
            draw.rectangle([260, 650, 290, 800], fill=c_skin)
        else:
            # Pants shape
            draw.rectangle([180, 450, 320, 800], fill=pants_color)
            # Gap between legs
            draw.polygon([(245, 450), (255, 450), (255, 800), (245, 800)], fill=(250,250,250)) 

        # 3. Inner Top
        inner_color = c_accent
        draw.rectangle([180, 180, 320, 460], fill=inner_color) # Torso
        draw.rectangle([150, 180, 190, 350], fill=inner_color) # Left Arm base
        draw.rectangle([310, 180, 350, 350], fill=inner_color) # Right Arm base
        
        # Hands
        draw.ellipse([140, 340, 190, 390], fill=c_skin)
        draw.ellipse([310, 340, 360, 390], fill=c_skin)

        # 4. Outerwear (if creates)
        if meta["has_outer"] and items["outer"]:
            outer_color = c_main
            # Open Jacket look
            draw.rectangle([140, 170, 210, 480], fill=outer_color) # Left panel
            draw.rectangle([290, 170, 360, 480], fill=outer_color) # Right panel
            # Sleeves
            draw.rectangle([120, 180, 170, 420], fill=outer_color)
            draw.rectangle([330, 180, 380, 420], fill=outer_color)

        # 5. Shoes
        shoe_color = (30,30,30)
        draw.rectangle([190, 800, 240, 850], fill=shoe_color)
        draw.rectangle([260, 800, 310, 850], fill=shoe_color)

        # Resize for better quality (Antialiasing hack)
        return img.resize((250, 450), resample=Image.LANCZOS)

# ==============================================================================
# UI COMPONENTS
# ==============================================================================
def sidebar_controls():
    with st.sidebar:
        st.header("⚙️ Configure Persona")
        
        st.subheader("Identity")
        gender = st.selectbox("Gender", ["Male", "Female"], index=1)
        use_outer = st.toggle("Include Outerwear", value=True)
        
        st.divider()
        
        st.subheader("Style Weights")
        # Weighted Style Input
        st.caption("Rate preferences (0 = Auto-infer from valid scores)")
        style_scores = {}
        
        # Create 2 columns for compact layout
        cols = st.columns(2)
        for i, genre in enumerate(StyleConfig.GENRES):
            with cols[i % 2]:
                # Default values: Casual/Minimal=8, others=4 to give some initial variety
                default_score = 8 if genre in ["Casual", "Minimal"] else 4
                style_scores[genre] = st.slider(f"{genre}", 0, 10, default_score, key=f"slider_{genre}")
        
        # Color Palette
        st.subheader("Color Preference (0-10)")
        color_scores = {}
        cols_c = st.columns(2)
        for i, color in enumerate(StyleConfig.COLORS):
            with cols_c[i % 2]:
                default_val = 8 if color in ["Black", "White", "Navy"] else 5
                color_scores[color] = st.slider(f"{color}", 0, 10, default_val, key=f"slider_color_{color}")
        
        st.divider()
        
        if st.button("✨ Generate Collection", type="primary"):
            return {
                "gender": gender,
                "use_outer": use_outer,
                "style_scores": style_scores,
                "color_scores": color_scores,
                "trigger": True
            }
            
    return {"trigger": False}

def main():
    # Session State
    if "outfits" not in st.session_state:
        st.session_state["outfits"] = []

    # Title
    st.title("AI Personal Stylist")
    st.markdown("Your curated daily rotation based on your preferences.")
    
    # Inputs
    config = sidebar_controls()
    
    # Generation Logic
    if config["trigger"]:
        new_outfits = []
        # Generate 3 looks
        style_scores = config["style_scores"]
        color_scores = config["color_scores"]
        
        # 1. Infer Style Weights
        all_genres = list(style_scores.keys())
        style_weights = RecommendationEngine.infer_weights(
            style_scores, 
            StyleConfig.GENRE_RELATIONS, 
            all_genres
        )
        
        # Safety fallback
        if sum(style_weights) == 0: 
            style_weights = [1] * len(all_genres)

        # 2. Infer Color Weights
        all_colors = list(color_scores.keys())
        color_weights = RecommendationEngine.infer_weights(
            color_scores, 
            StyleConfig.COLOR_RELATIONS, 
            all_colors
        )
        
        # Safety fallback
        if sum(color_weights) == 0: 
            color_weights = [1] * len(all_colors)

        # Store debug info for visualization
        st.session_state["debug_scores"] = {
            "styles": dict(zip(all_genres, style_weights)),
            "colors": dict(zip(all_colors, color_weights))
        }

        for _ in range(3):
            # Weighted selection for Genre
            # random.choices returns a list, we take [0]
            g = random.choices(all_genres, weights=style_weights, k=1)[0]
            # Weighted selection for Main Color
            c = random.choices(all_colors, weights=color_weights, k=1)[0]
            
            outfit = OutfitGenerator.create(g, c, config["gender"], config["use_outer"], color_scores)
            new_outfits.append(outfit)
            
        st.session_state["outfits"] = new_outfits

    # Display Gallery
    if st.session_state["outfits"]:
        cols = st.columns(3)
        
        for idx, (col, outfit) in enumerate(zip(cols, st.session_state["outfits"])):
            with col:
                # Custom container style via markdown hack or just clean layout
                img = AvatarRenderer.render(outfit)
                st.image(img, use_container_width=True)
                
                st.markdown(f"### {outfit['genre']}")
                st.caption(f"{outfit['main_color']} & {outfit['accent_color']}")
                
                with st.expander("View Details", expanded=True):
                    items = outfit['items']
                    st.markdown(f"""
                    - **Inner**: {items['inner']}
                    - **Outer**: {items['outer'] if items['outer'] else 'None'}
                    - **Bottom**: {items['bottom']}
                    - **Shoes**: {items['shoe']}
                    """)
        
        # Display Inferred Scores
        if "debug_scores" in st.session_state:
            st.divider()
            with st.expander("📊 Recommendation Engine Insights (Inferred Scores)", expanded=False):
                scores = st.session_state["debug_scores"]
                
                c1, c2 = st.columns(2)
                
                with c1:
                    st.markdown("#### Genre Weights")
                    # Normalize for display (0-10 scale approximation)
                    max_s = max(scores["styles"].values()) if scores["styles"].values() else 1
                    for k, v in scores["styles"].items():
                        norm_v = v / max_s
                        st.progress(norm_v, text=f"{k}: {v:.1f}")

                with c2:
                    st.markdown("#### Color Weights")
                    max_c = max(scores["colors"].values()) if scores["colors"].values() else 1
                    for k, v in scores["colors"].items():
                        norm_v = v / max_c
                        st.progress(norm_v, text=f"{k}: {v:.1f}")

    else:
        st.info("👈 Select your preferences in the sidebar and click 'Generate Collection' to start.")

if __name__ == "__main__":
    main()
