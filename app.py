# import streamlit as st

# # 初期化
# if 'submitted' not in st.session_state:
#     st.session_state['submitted'] = False

# if not st.session_state['submitted']:
#     with st.form("my_form"):
#         st.write("以下の情報を入力してください")
#         name = st.text_input('名前')
#         email = st.text_input('メールアドレス')
#         password = st.text_input('パスワード', type='password')
#         department = st.selectbox(
#             '部署', 
#             ['部署を選択してください','フロントエンド', 'バックエンド', 'インフラ']
#         )
#         submitted = st.form_submit_button("登録")

#         if submitted:
#             st.session_state['name'] = name
#             st.session_state['email'] = email
#             st.session_state['password'] = password
#             st.session_state['department'] = department
#             st.session_state['submitted'] = True
#             st.rerun()  # ここで即時画面更新

# else:
#     st.title("登録内容")
#     st.write("名前:", st.session_state.get('name', '未入力'))
#     st.write("メールアドレス:", st.session_state.get('email', '未入力'))
#     st.write("パスワード:", st.session_state.get('password', '未入力'))
#     st.write("部署:", st.session_state.get('department', '未入力'))
#     if st.button("再入力"):
#         st.session_state['submitted'] = False
#         st.rerun()  # 再入力時も即時画面更新

import streamlit as st
import csv

acount_csv = "acount.csv"

st.title("ユーザー登録")
name = st.text_input("名前")
email = st.text_input("メールアドレス")
password = st.text_input("パスワード", type="password")
department = st.selectbox("部署", ["フロントエンド", "バックエンド", "インフラ"])

if st.button("登録"):
    # acount.csvに保存（文字化け対策: utf-8-sig推奨）
    with open(acount_csv, "a", newline="", encoding="shift_jis") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, password, department])
    st.success("ユーザー情報を登録しました")
    # セッションに保存して進捗画面へ
    st.session_state.name = name
    st.session_state.email = email
    st.session_state.password = password
    st.session_state.department = department
    st.switch_page("progress")