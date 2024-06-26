import streamlit as st
import pandas as pd

# エクセルファイルのパス
EXCEL_FILE = 'playlist_data.xlsx'

# エクセルファイルを読み込む関数
def load_data(file):
    df = pd.read_excel(file)
    return df

# アプリのタイトル
st.title('音楽プレイリスト作成')

# サイドバーにファイルアップローダーを追加
uploaded_file = st.sidebar.file_uploader("エクセルファイルをアップロードしてください", type=["xlsx"])

# エクセルファイルがアップロードされたらデータを読み込む
if uploaded_file:
    df = load_data(uploaded_file)
    st.write("読み込まれたデータ：")
    st.dataframe(df)
else:
    st.write("エクセルファイルをアップロードしてください。")

# 入力フォームを作成
st.header('新しい曲を追加')

with st.form("entry_form"):
    曲名 = st.text_input("曲名")
    作品シリーズ = st.selectbox("作品シリーズ", ["シャニマス", "学マス", "Liella!", "蓮ノ空"])

    col1, col2 = st.columns(2)
    with col1:
        リリース日_from = st.date_input("リリース日（開始）")
    with col2:
        リリース日_to = st.date_input("リリース日（終了）")

    歌唱メンバー = st.text_input("歌唱メンバー")
    
    気分の選択肢 = ["喜び", "悲しみ", "期待", "怒り", "驚き", "恐れ", "信頼", "安心", "感謝", "興奮", "冷静", "不思議", "幸福", "リラックス", "尊敬", "勇気", "後悔", "恥", "嫉妬", "苦しみ", "感動", "悩み", "希望"]
    気分 = None
    col1, col2 = st.columns(2)
    with col1:
        気分 = st.radio("気分", 気分の選択肢[:len(気分の選択肢)//2])
    with col2:
        if not 気分:
            気分 = st.radio("気分", 気分の選択肢[len(気分の選択肢)//2:])
    
    歌詞の一部の単語 = st.text_area("歌詞の一部の単語")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        曲の長さ_以上 = st.number_input("曲の長さ（何分以上）", min_value=0, step=1)
    with col2:
        曲の長さ_以下 = st.number_input("曲の長さ（何分以下）", min_value=0, step=1)
    with col3:
        曲の長さ_分台 = st.number_input("曲の長さ（何分台）", min_value=0, step=1)
    
    # フォーム送信ボタン
    submitted = st.form_submit_button("追加")

    if submitted:
        new_data = {
            "曲名": [曲名],
            "作品シリーズ": [作品シリーズ],
            "リリース日（開始）": [リリース日_from],
            "リリース日（終了）": [リリース日_to],
            "歌唱メンバー": [歌唱メンバー],
            "気分": [気分],
            "歌詞の一部の単語": [歌詞の一部の単語],
            "曲の長さ（何分以上）": [曲の長さ_以上],
            "曲の長さ（何分以下）": [曲の長さ_以下],
            "曲の長さ（何分台）": [曲の長さ_分台]
        }
        new_df = pd.DataFrame(new_data)
        
        if uploaded_file:
            df = df.append(new_df, ignore_index=True)
        else:
            df = new_df

        # エクセルファイルに保存
        df.to_excel(EXCEL_FILE, index=False)
        st.success('曲が追加されました！')
        st.write("更新されたデータ：")
        st.dataframe(df)
