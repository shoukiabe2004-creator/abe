import streamlit as st
import random

# =====================
# GitHub RAW URL（要変更）
# =====================
GITHUB_BASE_URL = "https://raw.githubusercontent.com/ユーザー名/リポジトリ名/main/images/"

# =====================
# 選択肢
# =====================
STYLES = ["street", "casual", "minimal", "formal", "vintage"]
COLORS = ["black", "white", "brown", "beige", "green", "gray", "red"]

# =====================
# 画像DB（例）
# =====================
IMAGE_DB = [
    {"gender": "male", "style": "street", "color": "black", "file": "street_black_1.jpg"},
    {"gender": "male", "style": "casual", "color": "white", "file": "casual_white_1.jpg"},
    {"gender": "male", "style": "vintage", "color": "red", "file": "vintage_red_1.jpg"},
    {"gender": "male", "style": "minimal", "color": "beige", "file": "minimal_beige_1.jpg"},
    {"gender": "female", "style": "street", "color": "black", "file": "street_black_1.jpg"},
    {"gender": "female", "style": "formal", "color": "gray", "file": "formal_gray_1.jpg"},
]

# =====================
# 相対評価（順位）取得
# =====================
def get_top_items(score_dict, top_n=3):
    sorted_items = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    if sorted_items[0][1] == 0:
        return [k for k, _ in sorted_items]

    return [k for k, _ in sorted_items[:top_n]]

# =====================
# 推薦ロジック
# =====================
def recommend_images(gender, style_scores, color_scores, n=3):
    top_styles = get_top_items(style_scores)
    top_colors = get_top_items(color_scores)

    candidates = [
        img for img in IMAGE_DB
        if img["gender"] == gender
        and img["style"] in top_styles
        and img["color"] in top_colors
    ]

    if not candidates:
        candidates = [img for img in IMAGE_DB if img["gender"] == gender]

    return random.sample(candidates, min(n, len(candidates)))

# =====================
# Streamlit UI
# =====================
st.title("👗 AI Fashion Recommendation")

# 性別選択
gender = st.radio("性別を選択", ["male", "female"])

st.subheader("👕 スタイル評価（0〜10）")
style_scores = {
    "street": st.slider("ストリート", 0, 10, 5),
    "casual": st.slider("カジュアル", 0, 10, 5),
    "minimal": st.slider("ミニマル", 0, 10, 5),
    "formal": st.slider("フォーマル", 0, 10, 5),
    "vintage": st.slider("ヴィンテージ", 0, 10, 5),
}

st.subheader("🎨 色の評価（0〜10）")
color_scores = {
    "black": st.slider("黒", 0, 10, 5),
    "white": st.slider("白", 0, 10, 5),
    "brown": st.slider("茶色", 0, 10, 5),
    "beige": st.slider("ベージュ", 0, 10, 5),
    "green": st.slider("緑", 0, 10, 5),
    "gray": st.slider("グレー", 0, 10, 5),
    "red": st.slider("赤", 0, 10, 5),
}

if st.button("おすすめを見る"):
    results = recommend_images(gender, style_scores, color_scores, n=3)

    st.subheader("✨ Recommended Outfits")
    cols = st.columns(3)

    for col, img in zip(cols, results):
        image_url = f"{GITHUB_BASE_URL}{img['gender']}/{img['file']}"
        col.image(image_url, use_container_width=True)
        col.caption(
            f"スタイル: {img['style']} / 色: {img['color']}"
        )
