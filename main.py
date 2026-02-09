import streamlit as st
import pandas as pd

st.set_page_config(page_title="本のリサーチDB", layout="wide")

# --- 認証 ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("合言葉(33)", type="password")
    if st.button("ログイン"):
        if pwd == st.secrets.get("APP_PASSWORD", "33"):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("違います")
    st.stop()

# --- 検索キーワードの保持用 ---
if "search_word" not in st.session_state:
    st.session_state.search_word = ""

# --- クリアボタンが押された時の処理 ---
def clear_search():
    st.session_state.search_word = ""

# --- サイドバー（左側メニュー） ---
with st.sidebar:
    st.title("🛠 操作パネル")
    
    # ログアウトボタン
    if st.button("ログアウト"):
        st.session_state.auth = False
        st.rerun()
    
    st.divider() # 区切り線
    
    # キーワード検索欄
    st.subheader("🔍 検索")
    search_query = st.text_input(
        "キーワードを入力", 
        value=st.session_state.search_word, # ここに保持された値をいれる
        key="search_input", # 一意のキー
        placeholder="例: ビジネス, 小説..."
    )
    
    # クリアボタン
    if st.button("検索をクリア", on_click=clear_search):
        st.rerun()

# --- メインコンテンツ ---
st.title("📖 データベース")

url = st.secrets.get("SPREADSHEET_URL", "https://docs.google.com/spreadsheets/d/1egitl-X7YL_gQzMuWdwwk8cHo6obsIqVZTux4egYmRU/export?format=csv")

try:
    df = pd.read_csv(url)

    # --- 検索処理（search_query を使用） ---
    if search_query:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        df_display = df[mask]
    else:
        df_display = df

    # 結果の表示
    if search_query:
        st.info(f"「{search_query}」での検索結果: {len(df_display)}件")
    else:
        st.success(f"全データを表示中: {len(df_display)}件")

    st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
