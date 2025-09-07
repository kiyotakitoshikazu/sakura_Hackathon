import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random 
import csv
import datetime
import smtplib
import ssl
from email.mime.text import MIMEText

csv_file = "account.csv"

button_css = f"""
<style>
  div.stButton > button:first-child  {{
    font-weight  : bold                ;/* 文字：太字                   */
    /*border       :  5px solid #f36     ;/* 枠線：ピンク色で5ピクセルの実線 */
    /*border-radius: 10px 10px 10px 10px ;/* 枠線：半径10ピクセルの角丸     */
    /*background   :                 ;/* 背景色：薄いグレー            */
    text-align:center;
  }}
</style>
"""
st.markdown(button_css, unsafe_allow_html=True)

### csvが無いとき自動で作れたらいいね ###

### ページの書式設定 ###
st.set_page_config(
    page_title="スケジュール管理システム",
    layout="centered",
    initial_sidebar_state="collapsed",
)
### ページの書式設定 ###

### セッションの初期化 ###
if "email" not in st.session_state:
    st.session_state.email = ""
if "name" not in st.session_state:
    st.session_state.name = ""
if "section" not in st.session_state:
    st.session_state.section = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "page_control" not in st.session_state:
    st.session_state.page_control = "login"
### セッションの初期化 ###

### メインページ ###
def work():
    tf=False
    # ユーザの入力を受け取る 
    st.title("タスク表示")
    st.session_state.section=st.selectbox("部署",["フロントエンド","バックエンド","インフラ"])

    # button_css = f"""
    # <style>
    #   div.stButton > button:first-child  {{
    #     font-weight  : bold                ;/* 文字：太字                   */
    #     align:'center'
    #   }}
    # </style>
    # """
    # st.markdown(button_css, unsafe_allow_html=True)

    con1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        is_pressed = st.button("確認", "confirm")

    # 区切り線
    st.divider()

    if is_pressed:
        # CSVファイル読み込み処理
        with open ("account.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                print(row)

                #@ ログイン済みか確認
                is_login_account = False
                if row[9] == st.session_state.email and row[10] == st.session_state.password: 
                    is_login_account = True

                # 不正な行
                if len(row) < 6:
                    continue

                # 部署が異なる
                if st.session_state.section != row[0]:
                    continue

                # 名前表示
                if is_login_account:
                    st.write(f"<b style='font-size:35px; '>👤{row[2]} (MY)</b>", unsafe_allow_html=True)
                else:
                    st.write(f"<b style='font-size:35px; '>👤{row[2]}</b>", unsafe_allow_html=True)                    
                # 離席状態表示
                if row[1] == "勤務中":
                    st.markdown(":green-badge[勤務中]")
                elif row[1] == "休憩中":
                    st.markdown(":red-badge[休憩中]")
                else:
                    st.markdown(":black-badge[不明]")

                st.write(f"<b>📝仕事内容:</b> ", unsafe_allow_html=True)
                st.write(str(row[3]))
                st.write("")
                
                st.markdown(f"部署名 : {st.session_state.section}")
                st.markdown(f":gray[作業場所 : {row[5]}]")
                st.write("")

                # 開始日時表示
                st.markdown(f"🗓️:gray[開始 : {str(row[6])}]")
                st.markdown(f"🗓️:gray[期限 : {str(row[7])}]")

                # 進捗状況
                st.write(f"進捗 : <b>{str(row[4])}</b> %", unsafe_allow_html=True)
                st.progress(int(row[4]))

                # @支援要請ボタン
                # if st.button("支援要請"):
                    # pass

                #@ ログイン済みの場合ボタン表示
                if is_login_account:
                    col1,col2,col3=st.columns([1.4,1,1])
                    with col1:
                        st.write(" ")
                    with col2:        
                        st.page_link("pages/change.py",label="変更")
                    with col3:
                        st.write(" ")
                # 区切り線
                st.divider()
    if tf==True:
        st.session_state.page_control="change"
        st_autorefresh(interval=1,limit=3,key="work2change")
### メインページ ###

### ログインページ ###
def login():
    ### セッションの初期化 ###
    st.session_state.email = ""
    st.session_state.name = ""
    st.session_state.password = ""
    st.session_state.page_control = "login"
    ### セッションの初期化 ###
    ### 入力UI ###
    st.title("スケジュール管理システム")
    st.session_state.email=st.text_input("メールアドレス")
    st.session_state.password=st.text_input("パスワード",type="password")
    ### 入力UI ###
    
    ### ログインボタン ###
    col1,col2,col3,col4,col5=st.columns(5)
    tf=True
    with col1:
        st.write(" ")
    with col2:
        if st.button("ログイン"):
            tf=False
            with open(csv_file,"r",encoding="utf-8") as f:
                reader=csv.reader(f)
                #print("input_pass")
                #print(st.session_state.email,st.session_state.password)
                #print("csv_data")
                for row in reader:
                    #print(row[9],row[10])
                    if(tf==False and row[9]==st.session_state.email and row[10]==st.session_state.password):
                        tf=True
                        st.session_state.page_control="work"
                        ### ユーザの情報を一時保存 ###
                        st.session_state.department = row[0]
                        st.session_state.section = row[1]
                        st.session_state.name = row[2]
                        st.session_state.work_content = row[3]
                        st.session_state.work_progress = row[4]
                        st.session_state.work_place = row[5]
                        st.session_state.work_start = row[6]
                        st.session_state.work_deadline = row[7]
                        st.session_state.update_time = row[8]
                        st.session_state.email = row[9]
                        st.session_state.password = row[10]
                        ### ユーザの情報を一時保存 ###
                        #print(st.session_state)
                        notification_auto()
                        st_autorefresh(interval=1,limit=3,key="login2work")
    
    with col3:
        st.write(" ")
    with col4:
        if st.button("新規登録",type="primary"):
            st.session_state.page_control="register"
            st_autorefresh(interval=1,limit=3,key="login2register")
    with col5:
        st.write(" ")    
    if tf==False:
        st.write("<div style='text-align: center'>ログイン失敗<div>",unsafe_allow_html=True)
        st.write("<div style='text-align: center'>メールアドレスかパスワードが間違っています。<div>",unsafe_allow_html=True)

    #st.page_link("pages/register.py",label="新規登録")
### ログインページ ###

### 登録ページ ###
def register():
    ### 入力UI ###
    st.title("新規登録")
    st.session_state.email=st.text_input("e-mail")
    st.session_state.name=st.text_input("名前")
    st.session_state.section=st.selectbox("部署",["","フロントエンド","バックエンド","インフラ"])
    st.session_state.password=st.text_input("パスワード",type="password")
    ### 入力UI ###

    ### 確認ボタン ###
    col1,col2,col3,col5=st.columns([1,1,1,2])
    tf=True
    with col1:
        st.write(" ")
    with col2:
        st.write(" ")
    with col3:
        if st.button("確認"):
            if st.session_state.email!="" and st.session_state.name!="" and st.session_state.section!="" and st.session_state.password!="":
                st.session_state.page_control="register_confirm"
                st_autorefresh(interval=1,limit=3,key="register2confirm")
            else:
                tf=False
#    with col4:
 #       st.write(" ")
    with col5:
        if st.button("ログインページへ"):
            st.session_state.page_control="login"
            st_autorefresh(interval=1,limit=3,key="register2login")
    if tf==False:
        st.write("<div style='text-align: center'>入力内容が不足しています。</div>",unsafe_allow_html=True)
    #st.page_link("pages/register_confirm.py",label="確認",)
    ### 確認ボタン ###
### 登録ページ ###

### 登録確認 ###
def register_confirm():
    tf=False
    with open(csv_file,"r",encoding="utf-8") as f:
            reader=csv.reader(f)
            for row in reader:
                if(tf==False and row[9]==st.session_state.email):
                    tf=True
                    st.write("<div style='text-align: center'>すでに登録されています。</div>",unsafe_allow_html=True)
                    col1,col2,col3=st.columns(3)
                    with col1:
                        st.write(" ")
                    with col2:
                        if st.button("ログインへ戻る"):
                            st.session_state.page_control="login"
                            st_autorefresh(interval=1,limit=3,key="confirm2login")
                    with col3:
                        st.write(" ")
                    

    if tf==False:
        ###　確認UI ###
        st.title("登録フォーム")
        col1_email,col2_email=st.columns(2)
        with col1_email:
            st.write("e mail:")
        with col2_email:
            st.write(st.session_state.email)
        col1_name,col2_name=st.columns(2)
        with col1_name:
            st.write("名前:")
        with col2_name:
            st.write(st.session_state.name)
        col1_section,col2_section=st.columns(2)
        with col1_section:
            st.write("部署:")
        with col2_section:
            st.write(st.session_state.section)
        col1_password,col2_password=st.columns(2)
        with col1_password:
            st.write("パスワード:")
        with col2_password:
            st.write(st.session_state.password)

        st.write("<div style='text-align: center'>上記の内容で登録します。</div>",unsafe_allow_html=True)
        #st.page_link("pages/register_back.py", label="登録")
        col1,col2,col3=st.columns(3)
        with col1:
            st.write(" ")
        with col2:
            if st.button("登録"):
                st.session_state.page_control="register_back"
                print(st.session_state.page_control)
                st_autorefresh(interval=1,limit=3,key="confirm2back")
        with col3:
            st.write(" ")
        ### 確認UI###
### 登録確認 ###

### 登録認証 ###
def register_back():
    ###e-mailの送信###
    from email.mime.text import MIMEText
    import smtplib
    import ssl

    if "code" not in st.session_state:
        st.session_state.code = random.randrange(100)

    group_address="keitolv1@gmail.com"
    group_password="lcrm qgnw ohgg upsq"

    def createMIMEText(FROM, TO, MESSAGE, SUBJECT):
        # ===== 送信メールの作成 ===================================
        # メール本文
        msg = MIMEText("テストメール")
        # 送信元メールアドレス
        msg['From'] = group_address
        # 送信先メールアドレス
        msg['To'] = st.session_state.email
        # 件名
        msg['Subject'] = '確認メール'
        # ========================================================
        
        return msg

    def send_email():
        from_email =group_address#送信元
        to_email=st.session_state.email#宛先

        # ===== 送信メールの作成 ===================================
        # メール本文
        line1=st.session_state.name+"さん。\nこちらは進捗管理アプリの登録認証となります。\n"
        line2="認証コードは"+str(st.session_state.code)+"となります。\n"
        line3="確認画面に表示される入力欄に認証コードを入力してください。\n"

        message=line1+"\n"+line2+"\n"+line3
        msg = MIMEText(message, 'plain', 'utf-8')
        # 送信元メールアドレス
        msg['From'] = 'keitolv1@gmail.com'
        # 送信先メールアドレス
        msg['To'] = to_email
        # 件名
        msg['Subject'] = '確認メール'
        # ========================================================

        smtpserv = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        smtpserv.login('keitolv1@gmail.com', 'lcrm qgnw ohgg upsq')
        # メール送信
        smtpserv.send_message(msg)
        # サーバーから切断
        smtpserv.quit()

    #メール送信
    send_email()
    ### emailの送信 ###

    st.title("確認コード入力",)
    st.session_state.input_code=st.text_input("確認コードを入力してください")

    if st.session_state.input_code==str(st.session_state.code):
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([st.session_state.section,"勤務中", st.session_state.name,"",0,"","","",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), st.session_state.email, st.session_state.password])  
        print("登録完了")
        st.session_state.page_control="login"
        st.write("<div style='text-align: center'>登録完了\n3秒後にログイン画面に移行します。</div>",unsafe_allow_html=True)
        st_autorefresh(interval=1000,limit=3,key="back2login")
        #st.page_link("pages/login.py", label="ログインへ")
### 登録認証 ###

### 変更 ###
def change():
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
    col1_start,col2_start=st.columns(2)
    with col1_start:
        st.session_state.work_start = st.date_input("作業開始(年月日)")
    with col2_start:
        st.session_state.work_start_time = st.time_input("作業開始(時間)")
    col1_end,col2_end=st.columns(2)
    with col1_end:
        st.session_state.work_deadline_date = st.date_input("作業期限(年月日)")
    with col2_end:
        st.session_state.work_deadline_time = st.time_input("作業期限(時間)")
    st.session_state.email = st.text_input("メールアドレス")
    st.session_state.password = st.text_input("パスワード", type="password")

    # 進捗登録・上書き
    col1,col2,col3=st.columns([1.4,1,1])
    with col1:
        st.write(" ")
    with col2:
        select=0
        if st.button("変更"):
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
                    select=1

                else:
                    select=2

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
    with col3:
        st.write(" ")
    if select==1:
        st.success("<div style='text-align: center'>該当ユーザーの進捗を上書きしました</div>",unsafe_allow_html=True)
    if select==2:
        st.error("<div style='text-align: center'>メールアドレスまたはパスワードが違います</div>",unsafe_allow_html=True)
    
    col1_back,col2_back,col3_back=st.columns([1.4,1,1])
    with col1_back:
        st.write(" ")
    with col2_back:
        if st.button("戻る"):
            st.session_state.page_control="work"
            st_autorefresh(interval=1,limit=3,key="change2work")
    with col3_back:
        st.write(" ")
### 変更 ###

### 通知 ###
def notification_auto():
    help_message=""
    with open("account.csv","r",encoding="utf-8") as f:
        reader=csv.reader(f)
        #print(st.session_state.email,st.session_state.password)
        print("start")
        if(int(st.session_state.work_progress)>90):
            for row in reader:
                notification_select=False
                if row[4]=="作業進捗":#一行目のカラム名じゃないかの確認
                    notification_select=True
                    print("end1",row[4],row[7],row[8])
                if notification_select==False and (row[7]=="" or row[8]==""):#時間の部分が空白じゃないかの確認
                    notification_select=True
                    print("end2",row[4],row[7],row[8])
                if notification_select==False and int(row[4])>=40:#遅れてる人の確認
                    notification_select=True
                    print("end3",row[4],row[7],row[8])
                if notification_select==False and row[0]!=st.session_state.department:#自分の部署と同じかの確認
                    notification_select=True
                    print("end4",row[4],row[7],row[8])
                if notification_select==False and row[9]==st.session_state.email:#自分のアカウントじゃないかの確認
                    notification_select=True
                    print("end5",row[4],row[7],row[8])
                if notification_select==False and st.session_state.department=="勤務中":#自分が休暇なら通知を送らない。
                    notification_select=True
                    print("end6",row[4],row[7],row[8],st.session_state.department)
                if notification_select==False:
                    ### 時間の確認 ###
                    time_line_start=row[7].split(" ")
                    time_line_end=row[8].split(" ")
                    time_line_start=time_line_start[0].split("-")
                    time_line_end=time_line_end[0].split("-")
                    print(time_line_start,time_line_end)
                    ### 時間の確認 ###
                    year=int(time_line_start[0])-int(time_line_end[0])
                    month=int(time_line_start[1])-int(time_line_end[1])
                    day=int(time_line_start[2])-int(time_line_end[2])
                    if abs(year)==0 and abs(month)==0 and abs(day==0):
                        help_message=help_message+row[2]+"さん(mail: "+row[9]+")"+"の進捗が遅れています！\n\n"
    
    if help_message!="":
        help_message=st.session_state.name+"さん。\n進捗通知です\n\n"+help_message+"期日が近いので助けましょう!"

        ###e-mailの送信###
        group_address="keitolv1@gmail.com"
        group_password="lcrm qgnw ohgg upsq"
        from_email =group_address#送信元
        to_email=st.session_state.email#宛先

        # ===== 送信メールの作成 ===================================
        # メール本文
        msg = MIMEText(help_message, 'plain', 'utf-8')
        # 送信元メールアドレス
        msg['From'] = 'keitolv1@gmail.com'
        # 送信先メールアドレス
        msg['To'] = to_email
        # 件名
        msg['Subject'] = '進捗通知'
        # ========================================================

        smtpserv = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        smtpserv.login('keitolv1@gmail.com', 'lcrm qgnw ohgg upsq')
        # メール送信
        smtpserv.send_message(msg)
        # サーバーから切断
        smtpserv.quit()
        print("send_help_email")
### 通知 ###

### ページの切り替え ###
if st.session_state.page_control=="change":
    change() 
if st.session_state.page_control=="work":
    work()
if st.session_state.page_control=="register_back":
    register_back()
if st.session_state.page_control=="register_confirm":
    register_confirm()
if st.session_state.page_control=="register":
    register()
if st.session_state.page_control=="login":
    login()

### ページの切り替え ###