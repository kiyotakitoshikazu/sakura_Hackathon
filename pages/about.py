# import streamlit as st

# # タブ名に表示される
# st.set_page_config(page_title="About", page_icon="📈")

# st.title("Aboutページ")
# st.write("名前:", st.session_state.get('name', '未入力'))
# st.write("メールアドレス:", st.session_state.get('email', '未入力'))
# st.write("パスワード:", st.session_state.get('password', '未入力'))
# st.write("部署:", st.session_state.get('department', '未入力'))

import streamlit as st
import csv

acount_csv = "acount.csv"

st.title("ユーザー情報一覧")
try:
    with open(acount_csv, "r", encoding="shift_jis") as f:
        reader = csv.reader(f)
        for row in reader:
            st.write(row)
except FileNotFoundError:
    st.info("ユーザー情報がありません。")