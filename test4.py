import streamlit as st
import pandas as pd

# エクセルファイルを全シート読み込む
file_path = 'アイラブ楽曲検索ツール ver4.xlsx'
sheets = pd.read_excel(file_path, sheet_name=None)

# すべてのシートを一つのデータフレームに結合
df_list = []
for sheet_name, df in sheets.items():
    df['作品シリーズ'] = sheet_name  # シート名を新しい列として追加
    df_list.append(df)
all_data = pd.concat(df_list, ignore_index=True)

# リリース日列をdatetime型に変換
if 'リリース日' in all_data.columns:
    all_data['リリース日'] = pd.to_datetime(all_data['リリース日'], errors='coerce')
else:
    st.error("データフレームに 'リリース日' 列が存在しません。")

# ユーザーの入力を取得
st.title("アイラブ楽曲検索ツール")

# 作品シリーズフィルター
series_options = st.multiselect("作品シリーズを選択", options=all_data['作品シリーズ'].unique())

# リリース日フィルター（範囲指定のカレンダー）
if 'リリース日' in all_data.columns:
    release_date_range = st.date_input("リリース日の範囲を選択", value=[all_data['リリース日'].min(), all_data['リリース日'].max()])

# 曲の長さフィルター（ミリ秒）
length_range = st.slider(
    "曲の長さの範囲を選択（ミリ秒）",
    min_value=0,
    max_value=int(all_data['length'].max()),
    value=(0, int(all_data['length'].max()))
)

# 気分フィルター
moods = ["喜び", "悲しみ", "期待", "怒り", "驚き", "恐れ", "信頼", "安心", "感謝", "興奮", "冷静", "不思議",
         "幸福", "リラックス", "尊敬", "勇気", "後悔", "恥", "嫉妬", "苦しみ", "感動", "悩み", "希望"]

mood = st.selectbox("気分を選択", moods)

# フィルタリング処理
if 'リリース日' in all_data.columns:
    filtered_df = all_data[
        (all_data['作品シリーズ'].isin(series_options)) &
        (all_data['リリース日'] >= pd.to_datetime(release_date_range[0])) &
        (all_data['リリース日'] <= pd.to_datetime(release_date_range[1])) &
        (all_data['length'] >= length_range[0]) &
        (all_data['length'] <= length_range[1]) &
        (all_data['気分'].str.contains(mood, na=False))
    ]

    # 必要な列のみ表示
    result_df = filtered_df[['曲名', '歌唱メンバー']]

    # 結果を表示
    st.write("検索結果:")
    st.table(result_df)
