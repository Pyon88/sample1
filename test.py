import streamlit as st
import pandas as pd

# エクセルファイルを読み込む
file_path = 'アイラブ楽曲検索ツール ver2.xlsx'
df = pd.read_excel(file_path)

# ユーザーの入力を取得
st.title("アイラブ楽曲検索ツール")

# リリース日フィルター
release_date = st.date_input("リリース日を選択")

# 曲の長さフィルター（ミリ秒）
length_range = st.slider(
    "曲の長さの範囲を選択（ミリ秒）",
    min_value=0,
    max_value=int(df['length'].max()),
    value=(0, int(df['length'].max()))
)

# 気分フィルター
mood = st.text_input("気分を入力")

# フィルタリング処理
filtered_df = df[
    (df['リリース日'] == pd.to_datetime(release_date)) &
    (df['length'] >= length_range[0]) &
    (df['length'] <= length_range[1]) &
    (df['気分'].str.contains(mood, na=False))
]

# 結果を表示
st.write("検索結果:")
st.dataframe(filtered_df)
