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
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
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

# ==============================================================================
# LOGIC CORE
# ==============================================================================
class OutfitGenerator:
    @staticmethod
    def get_complementary_color(base_color, all_colors):
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
        candidates = pairs.get(base_color, all_colors)
        return random.choice(candidates)

    @staticmethod
    def create(genre, base_color, gender, use_outer, all_colors):
        lib = StyleConfig.OUTFIT_LIBRARY.get(genre, StyleConfig.OUTFIT_LIBRARY["Casual"])
        
        # Color Logic
        accent_color = OutfitGenerator.get_complementary_color(base_color, all_colors)
        
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
        # Simplify input using multiselect for primary genres instead of individual sliders
        genres = st.multiselect(
            "Favorite Styles (Select 1-3)", 
            StyleConfig.GENRES, 
            default=["Casual", "Minimal"]
        )
        
        # Color Palette
        colors = st.multiselect(
            "Preferred Colors", 
            StyleConfig.COLORS,
            default=["Black", "Beige", "Navy"]
        )
        
        st.divider()
        
        if st.button("✨ Generate Collection", type="primary"):
            return {
                "gender": gender,
                "use_outer": use_outer,
                "genres": genres if genres else StyleConfig.GENRES,
                "colors": colors if colors else StyleConfig.COLORS,
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
        possible_genres = config["genres"]
        possible_colors = config["colors"]
        
        for _ in range(3):
            g = random.choice(possible_genres)
            c = random.choice(possible_colors)
            outfit = OutfitGenerator.create(g, c, config["gender"], config["use_outer"], possible_colors)
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
    else:
        st.info("👈 Select your preferences in the sidebar and click 'Generate Collection' to start.")

if __name__ == "__main__":
    main()
