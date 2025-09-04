import streamlit as st
import csv
import datetime

csv_file = "data.csv"

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
st.session_state.department = st.selectbox("部署", ["フロントエンド", "バックエンド", "インフラ"])
st.session_state.section = st.selectbox("勤務状態", ["勤務中", "休日", "休憩中", ""])
st.session_state.name = st.text_input("名前")
st.session_state.work_content = st.text_input("仕事内容")
st.session_state.work_progress = st.slider("作業進捗（0～100）", min_value=0, max_value=100, step=1)
st.session_state.work_place = st.selectbox("作業場所", ["自宅", "職場", "その他"])
st.session_state.work_deadline_date = st.date_input("期限（日付）")
st.session_state.work_deadline_time = st.time_input("期限（時間）")
st.session_state.email = st.text_input("メールアドレス")
st.session_state.password = st.text_input("パスワード", type="password")

# 進捗登録・上書き
if st.button("進捗を登録"):
    # ボタンが押された時の日時の記録
    st.session_state.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 日付と時間を結合
    work_deadline = datetime.datetime.combine(
        st.session_state.work_deadline_date,
        st.session_state.work_deadline_time
    ).strftime("%Y-%m-%d %H:%M:%S")
    # csv書き込み
    try:
        with open(csv_file, "r", encoding="cp932") as f:
            rows = list(csv.reader(f))
        found = False
        for i, row in enumerate(rows):
            # 既存ユーザー（メールアドレス・パスワード一致）がいれば進捗を更新
            if len(row) >= 10 and row[8] == st.session_state.email and row[9] == st.session_state.password:
                rows[i] = [
                    st.session_state.department,
                    st.session_state.section,
                    st.session_state.name,
                    st.session_state.work_content,
                    str(st.session_state.work_progress),
                    st.session_state.work_place,
                    work_deadline,
                    st.session_state.update_time,
                    st.session_state.email,
                    st.session_state.password
                ]
                found = True
                break
        if found:
            with open(csv_file, "w", newline="", encoding="cp932") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            st.success("該当ユーザーの進捗を上書きしました")
        else:
            with open(csv_file, "a", newline="", encoding="cp932") as f:
                writer = csv.writer(f)
                writer.writerow([
                    st.session_state.department,
                    st.session_state.section,
                    st.session_state.name,
                    st.session_state.work_content,
                    str(st.session_state.work_progress),
                    st.session_state.work_place,
                    work_deadline,
                    st.session_state.update_time,
                    st.session_state.email,
                    st.session_state.password
                ])
            st.success("新規ユーザーの進捗を登録しました")
    except FileNotFoundError:
        with open(csv_file, "w", newline="", encoding="cp932") as f:
            writer = csv.writer(f)
            writer.writerow([
                st.session_state.department,
                st.session_state.section,
                st.session_state.name,
                st.session_state.work_content,
                str(st.session_state.work_progress),
                st.session_state.work_place,
                work_deadline,
                st.session_state.update_time,
                st.session_state.email,
                st.session_state.password
            ])
        st.success("新規ユーザーの進捗を登録しました")