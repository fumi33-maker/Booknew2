import streamlit as st
import pandas as pd

st.set_page_config(page_title="本のリサーチDB", layout="wide")

def check_password():
    if st.session_state.get("password_correct", False):
        return True
    st.title("🔒 ログイン")
    pwd = st.text_input("合言葉を入力してください", type="password")
    if st.button("ログイン"):
        if pwd == st.secrets.get("APP_PASSWORD", "33"):
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("合言葉が違います")
    return False

if check_password():
    st.title("📖 本のリサーチ・コレクション")
    url = st.secrets.get("SPREADSHEET_URL", "https://docs.google.com/spreadsheets/d/1egitl-X7YL_gQzMuWdwwk8cHo6obsIqVZTux4egYmRU/export?format=csv")

    @st.cache_data(ttl=60)
    def load_data(csv_url):
        return pd.read_csv(csv_url)

    try:
        df = load_data(url)
        q = st.text_input("🔍 キーワード検索", "")
        if q:
            df = df[df.astype(str).apply(lambda x: x.str.contains(q, case=False)).any(axis=1)]
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"データ取得エラー。スプレッドシートの共有設定を確認してください。")
        