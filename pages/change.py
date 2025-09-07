import streamlit as st
import csv
import datetime

csv_file = "account.csv"

# セッションの初期化
if "department" not in st.session_state:
    st.session_state.department = ""
if "section" not in st.session_state:
    st.session_state.section = ""
if "name" not in st.session_state:
    st.session_state.name = ""
if "work_content" not in st.session_state:
    st.session_state.work_content = ""
if "work_progress" not in st.session_state:
    st.session_state.work_progress = 0
if "work_place" not in st.session_state:
    st.session_state.work_place = ""
if "work_deadline_date" not in st.session_state:
    st.session_state.work_deadline_date = datetime.date.today()
if "work_deadline_time" not in st.session_state:
    st.session_state.work_deadline_time = datetime.datetime.now().time()
if "update_time" not in st.session_state:
    st.session_state.update_time = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "password" not in st.session_state:
    st.session_state.password = ""

# 入力UI
st.session_state.department = st.selectbox("部署", ["","フロントエンド", "バックエンド", "インフラ"])
st.session_state.section = st.selectbox("勤務状態", ["","勤務中", "休日", "休憩中"])
st.session_state.name = st.text_input("名前")
st.session_state.work_content = st.text_input("仕事内容")
st.session_state.work_progress = st.slider("作業進捗（0～100）", min_value=0, max_value=100, step=1)
st.session_state.work_place = st.text_input("作業場所")
# st.session_state.work_start = st.time_input("作業開始", value=datetime.datetime.now().time())
st.session_state.work_start = st.date_input("作業開始(年月日)")
st.session_state.work_start_time = st.time_input("作業開始(時間)")
st.session_state.work_deadline_date = st.date_input("作業期限(年月日)")
st.session_state.work_deadline_time = st.time_input("作業期限(時間)")
st.session_state.email = st.text_input("メールアドレス")
st.session_state.password = st.text_input("パスワード", type="password")

# 進捗登録・上書き
if st.button("進捗を登録"):
    st.session_state.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    work_start_str = datetime.datetime.combine(
        st.session_state.work_start,
        st.session_state.work_start_time
    ).strftime("%Y-%m-%d %H:%M:%S")
    work_deadline = datetime.datetime.combine(
        st.session_state.work_deadline_date,
        st.session_state.work_deadline_time
    ).strftime("%Y-%m-%d %H:%M:%S")
    # csv書き込み
    # [部署, 勤務状態, 名前, 仕事内容, 作業進捗, 作業場所, 作業開始, 作業期限(年月日), 作業期限(時間), メールアドレス, パスワード]
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        found = False
        email_exists = False
        for i, row in enumerate(rows):
            # メールアドレスが一致するか判定
            if len(row) >= 11 and row[9] == st.session_state.email:
                email_exists = True
                # パスワードも一致した場合のみ上書き
                if row[10] == st.session_state.password:
                    #　ここから上書き部分
                    rows[i] = [
                        st.session_state.department,
                        st.session_state.section,
                        st.session_state.name,
                        st.session_state.work_content,
                        str(st.session_state.work_progress),
                        st.session_state.work_place,
                        work_start_str,
                        work_deadline,
                        st.session_state.update_time,
                        st.session_state.email,
                        st.session_state.password
                    ]
                    found = True
                break
        if found:
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            st.success("該当ユーザーの進捗を上書きしました")
        else:
            st.error("メールアドレスまたはパスワードが違います")
    # account.csvが存在しない場合はファイルが新規作成されます
    except FileNotFoundError:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                st.session_state.department,
                st.session_state.section,
                st.session_state.name,
                st.session_state.work_content,
                str(st.session_state.work_progress),
                st.session_state.work_place,
                work_start_str,
                work_deadline,
                st.session_state.update_time,
                st.session_state.email,
                st.session_state.password
            ])
        st.success("新規ユーザーの進捗を登録しました")