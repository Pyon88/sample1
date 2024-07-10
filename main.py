import streamlit as st
import pandas as pd

# エクセルファイルのパス
EXCEL_FILE = 'アイラブ楽曲検索ツール.xlsx'

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

# 検索機能の追加
st.header('楽曲検索')

with st.form("search_form"):
    曲名_search = st.text_input("曲名で検索")
    作品シリーズ_search = st.selectbox("作品シリーズで検索", ["全て", "シャニマス", "学マス", "Liella!", "蓮ノ空"])

    col1, col2 = st.columns(2)
    with col1:
        リリース日_from_search = st.date_input("リリース日（開始）で検索")
    with col2:
        リリース日_to_search = st.date_input("リリース日（終了）で検索")

    歌唱メンバー_search = st.text_input("歌唱メンバーで検索")
    
    気分の選択肢 = ["全て", "喜び", "悲しみ", "期待", "怒り", "驚き", "恐れ", "信頼", "安心", "感謝", "興奮", "冷静", "不思議", "幸福", "リラックス", "尊敬", "勇気", "後悔", "恥", "嫉妬", "苦しみ", "感動", "悩み", "希望"]
    気分_search = st.selectbox("気分で検索", 気分の選択肢)
    
    歌詞の一部の単語_search = st.text_input("歌詞の一部の単語で検索")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        曲の長さ_以上_search = st.number_input("曲の長さ（何分以上）で検索", min_value=0, step=1)
    with col2:
        曲の長さ_以下_search = st.number_input("曲の長さ（何分以下）で検索", min_value=0, step=1)
    with col3:
        曲の長さ_分台_search = st.number_input("曲の長さ（何分台）で検索", min_value=0, step=1)
    
    # フォーム送信ボタン
    search_submitted = st.form_submit_button("検索")

    if search_submitted:
        search_conditions = {
            "曲名": 曲名_search,
            "作品シリーズ": 作品シリーズ_search,
            "リリース日（開始）": リリース日_from_search,
            "リリース日（終了）": リリース日_to_search,
            "歌唱メンバー": 歌唱メンバー_search,
            "気分": 気分_search,
            "歌詞の一部の単語": 歌詞の一部の単語_search,
            "曲の長さ（何分以上）": 曲の長さ_以上_search,
            "曲の長さ（何分以下）": 曲の長さ_以下_search,
            "曲の長さ（何分台）": 曲の長さ_分台_search
        }
        
        filtered_df = df
        
        for key, value in search_conditions.items():
            if value and value != "全て":
                if key in ["リリース日（開始）", "リリース日（終了）"]:
                    if key == "リリース日（開始）":
                        filtered_df = filtered_df[filtered_df['リリース日'] >= value]
                    else:
                        filtered_df = filtered_df[filtered_df['リリース日'] <= value]
                elif key in ["曲の長さ（何分以上）", "曲の長さ（何分以下）", "曲の長さ（何分台）"]:
                    if key == "曲の長さ（何分以上）":
                        filtered_df = filtered_df[filtered_df['曲の長さ'] >= value]
                    elif key == "曲の長さ（何分以下）":
                        filtered_df = filtered_df[filtered_df['曲の長さ'] <= value]
                    else:
                        filtered_df = filtered_df[filtered_df['曲の長さ'] == value]
                else:
                    filtered_df = filtered_df[filtered_df[key].str.contains(value, na=False)]
        
        st.write("検索結果：")
        st.dataframe(filtered_df)

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
