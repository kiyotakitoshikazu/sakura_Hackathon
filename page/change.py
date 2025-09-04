import streamlit as st
import csv
### セッションの初期化 ###
#並び順はcsvの並び順の通り
csv_file = "data.csv"

if "section" not in st.session_state:
    st.session_state.section = ""
if "emp_status" not in st.session_state:
    st.session_state.emp_status = ""
if "name" not in st.session_state:
    st.session_state.name = ""
if "work_content" not in st.session_state:
    st.session_state.work_content = ""
if "work_progress" not in st.session_state:
    st.session_state.work_progress = ""
if "work_place" not in st.session_state:
    st.session_state.work_place = ""
if "work_deadline" not in st.session_state:
    st.session_state.work_time = ""
if "update_time" not in st.session_state:
    st.session_state.update_time = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "password" not in st.session_state:
    st.session_state.password = ""
### セッションの初期化 ###
### 入力UI ###
st.session_state.section=st.selectbox("勤務状態",["勤務中","休日","休憩中",""])

### 入力UI ###