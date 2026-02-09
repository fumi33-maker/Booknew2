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

# --- クリアボタン用の関数 ---
def clear_search():
    # 入力欄の値を直接「空」に上書きする
    st.session_state["search_input"] = ""

# --- サイドバー（左側メニュー） ---
with st.sidebar:
    st.title("🛠 操作パネル")
    
    if st.button("ログアウト"):
        st.session_state.auth = False
        st.rerun()
    
    st.divider()
    
    st.subheader("🔍 検索")
    
    # 検索窓（keyを指定するのがポイントです！）
    search_query = st.text_input(
        "キーワードを入力", 
        key="search_input", 
        placeholder="例: ビジネス, 小説..."
    )
    
    # クリアボタン
    st.button("検索をクリア", on_click=clear_search)

# --- メインコンテンツ ---
st.title("📖 データベース")

url = st.secrets.get("SPREADSHEET_URL", "https://docs.google.com/spreadsheets/d/1egitl-X7YL_gQzMuWdwwk8cHo6obsIqVZTux4egYmRU/export?format=csv")

try:
    df = pd.read_csv(url)

    # 検索処理
    if search_query:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        df_display = df[mask]
    else:
        df_display = df

    # 表示
    if search_query:
        st.info(f"「{search_query}」での検索結果: {len(df_display)}件")
    else:
        st.success(f"全データを表示中: {len(df_display)}件")

    st.dataframe(df_display, use_container_width=True)

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
