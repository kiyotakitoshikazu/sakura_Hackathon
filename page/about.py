import streamlit as st

# タブ名に表示される
st.set_page_config(page_title="About", page_icon="📈")

st.title("Aboutページ")
st.write("名前:", st.session_state.get('name', '未入力'))
st.write("メールアドレス:", st.session_state.get('email', '未入力'))
st.write("パスワード:", st.session_state.get('password', '未入力'))
st.write("部署:", st.session_state.get('department', '未入力'))