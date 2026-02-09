import streamlit as st
import pandas as pd

st.set_page_config(page_title="本のリサーチDB")

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

# --- ログアウトボタンを左上（サイドバー）に追加 ---
with st.sidebar:
    st.write(f"ユーザー: ログイン中")
    if st.button("ログアウト"):
        st.session_state.auth = False
        st.rerun()

# --- メイン ---
st.title("📖 データベース")

# Secretsが読み込めていない時のための予備URL
url = st.secrets.get("SPREADSHEET_URL", "https://docs.google.com/spreadsheets/d/1egitl-X7YL_gQzMuWdwwk8cHo6obsIqVZTux4egYmRU/export?format=csv")

try:
    # データを読み込む
    df = pd.read_csv(url)
    st.success("データの取得に成功しました！")
    st.dataframe(df)
except Exception as e:
    st.error("取得エラーが発生しました")
    st.warning(f"エラーの詳細: {e}")
    st.info(f"現在読み込もうとしているURL: {url}")
