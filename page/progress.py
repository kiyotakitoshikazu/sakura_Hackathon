import streamlit as st
import csv
import datetime

data_csv = "data.csv"

st.title("進捗報告")
work_content = st.text_input("作業内容")
work_progress = st.text_input("進捗状況")
work_place = st.text_input("作業場所")
work_deadline = st.text_input("作業期限")
emp_status = st.selectbox("ステータス", ["勤務中", "休日", "休憩中"])
update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if st.button("進捗を登録"):
    # data.csvに保存
    with open(data_csv, "a", newline="", encoding="shift_jis") as f:
        writer = csv.writer(f)
        writer.writerow([
            st.session_state.get("name", ""),
            st.session_state.get("email", ""),
            st.session_state.get("department", ""),
            work_content,
            work_progress,
            work_place,
            work_deadline,
            emp_status,
            update_time
        ])
    st.success("進捗を登録しました")
    st.write("作業内容:", work_content)
    st.write("進捗状況:", work_progress)
    st.write("作業場所:", work_place)
    st.write("作業期限:", work_deadline)
    st.write("ステータス:", emp_status)