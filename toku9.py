import streamlit as st
import random

# =====================
# GitHub RAW URL
# =====================
GITHUB_IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/ユーザー名/リポジトリ名/main/images/"
)

# =====================
# 画像データベース
# =====================
IMAGE_DB = [
    {"style": "casual", "color": "navy", "file": "casual_navy_1.jpg"},
    {"style": "casual", "color": "gray", "file": "casual_gray_1.jpg"},
    {"style": "vintage", "color": "red", "file": "vintage_red_1.jpg"},
    {"style": "vintage", "color": "red", "file": "vintage_red_2.jpg"},
    {"style": "military", "color": "olive", "file": "military_olive_1.jpg"},
]

# =====================
# 相対評価で上位を取得
# =====================
def get_top_items(score_dict, top_n=3):
    sorted_items = sorted(
        score_dict.items(), key=lambda x: x[1], reverse=True
    )

    # 全部0点なら全候補を返す
    if sorted_items[0][1] == 0:
        return [k for k, _ in sorted_items]

    return [k for k, _ in sorted_items[:top_n]]

# =====================
# 画像推薦ロジック
# =====================
def recommend_images(style_scores, color_scores, n=3):
    top_styles = get_top_items(style_scores, top_n=3)
    top_colors = get_top_items(color_scores, top_n=3)

    candidates = [
        img for img in IMAGE_DB
        if img["style"] in top_styles and img["color"] in top_colors
    ]

    if not candidates:
        candidates = IMAGE_DB.copy()

    return random.sample(
        candidates, min(n, len(candidates))
    )

# =====================
# Streamlit UI
# =====================
st.title("👕 AI Fashion Recommendation")

st.subheader("スタイル評価（0〜10）")
style_scores = {
    "casual": st.slider("Casual", 0, 10, 5),
    "vintage": st.slider("Vintage", 0, 10, 5),
    "military": st.slider("Military", 0, 10, 5),
}

st.subheader("色の評価（0〜10）")
color_scores = {
    "navy": st.slider("Navy", 0, 10, 5),
    "gray": st.slider("Gray", 0, 10, 5),
    "red": st.slider("Red", 0, 10, 5),
    "olive": st.slider("Olive", 0, 10, 5),
}

if st.button("おすすめを見る"):
    results = recommend_images(style_scores, color_scores, n=3)

    st.subheader("✨ Recommended Outfits")
    cols = st.columns(3)

    for col, img in zip(cols, results):
        image_url = GITHUB_IMAGE_BASE_URL + img["file"]
        col.image(image_url, use_container_width=True)
        col.caption(
            f"Style: {img['style']} / Color: {img['color']}"
        )
