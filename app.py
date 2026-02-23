import os
import datetime
import streamlit as st
import pandas as pd
import re
from dotenv import load_dotenv
import google.generativeai as genai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 1. SETUP
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/calendar.readonly'
]

TARGET_FOLDER_ID = "1HJzlxkUgZ6ooAAoHYp7MPvotLpQtVUAV"

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'full_context' not in st.session_state:
    st.session_state.full_context = ""

def get_google_services():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return (
        build('gmail', 'v1', credentials=creds),
        build('sheets', 'v4', credentials=creds),
        build('drive', 'v3', credentials=creds),
        build('calendar', 'v3', credentials=creds)
    )

def parse_and_sort_logic(markdown_text):
    lines = [line.strip() for line in markdown_text.strip().split('\n') if '|' in line]
    if len(lines) < 2: return []
    data_rows = []
    headers = ["Task/Event", "Date", "Priority", "Category"]
    for line in lines:
        if '---|' in line or 'Task/Event' in line: continue
        cells = [re.sub(r'[()]', '', cell.strip()) for cell in line.split('|') if cell.strip()]
        if cells:
            while len(cells) < 4: cells.append("Normal")
            data_rows.append(cells[:4])
    data_rows.sort(key=lambda x: x[1], reverse=True)
    return [headers] + data_rows

# 2. UI
st.set_page_config(page_title="FocusFlow Pro", page_icon="⚡", layout="wide")
st.title("⚡ FocusFlow: Personal Chief of Staff")

# 3. SIDEBAR
with st.sidebar:
    st.header("📅 Data Window")
    preset = st.selectbox("Quick Select", ["Last 7 Days", "Last 30 Days", "Last 100 Days"])
    today = datetime.date.today()
    days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 100 Days": 100}
    start_date = today - datetime.timedelta(days=days_map[preset])
    if st.button("🚀 Sync & Analyze Live Data"):
        st.session_state.trigger_fetch = True

# 4. FETCH & ANALYZE
if st.session_state.get('trigger_fetch'):
    gmail_service, _, _, cal_service = get_google_services()
    date_query = start_date.strftime('%Y/%m/%d')
    with st.spinner("🧠 Scanning for Payments, Orders, and Winnings..."):
        gmail_res = gmail_service.users().messages().list(userId='me', q=f"after:{date_query}", maxResults=60).execute()
        messages = gmail_res.get('messages', [])
        email_data = ""
        for m in messages:
            msg = gmail_service.users().messages().get(userId='me', id=m['id']).execute()
            snippet = msg.get('snippet', '')
            lower_snippet = snippet.lower()
            if any(k in lower_snippet for k in ["payment", "due", "bill", "statement", "temu", "order"]):
                snippet = f"CRITICAL_FINANCE: {snippet}"
            email_data += f"- {snippet}\n"
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        cal_res = cal_service.events().list(calendarId='primary', timeMin=now, maxResults=20, singleEvents=True, orderBy='startTime').execute()
        cal_data = "".join([f"- Event: {e['summary']} at {e['start'].get('dateTime', e['start'].get('date'))}\n" for e in cal_res.get('items', [])])
        st.session_state.full_context = email_data + "\n" + cal_data

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Extract interviews, purchase orders (Temu/Amazon), upcoming bill payments, and winnings.
        RULES:
        1. UPCOMING PAYMENTS: Find any mention of bills, statements, or payments due. Label as "Upcoming Payment".
        2. CONSOLIDATION: Group all lottery/gambling winnings into ONE item: "Total Lottery Winnings $XX.XX".
        3. ORDERS: Identify Temu or retail orders as "Order Confirmed".
        4. DATE: Use YYYY-MM-DD. No parentheses.
        Return ONLY a Markdown Table: | Task/Event | Date | Priority | Category |
        Data Context: {st.session_state.full_context}
        """
        response = model.generate_content(prompt)
        st.session_state.analysis_results = parse_and_sort_logic(response.text)
        st.session_state.trigger_fetch = False

# 5. DASHBOARD & MASTER LOG LINK
if st.session_state.analysis_results and len(st.session_state.analysis_results) > 1:
    st.subheader("📋 Your Actionable Dashboard")
    df = pd.DataFrame(st.session_state.analysis_results[1:], columns=st.session_state.analysis_results[0])
    st.table(df)
    
    if st.button("📊 Sync to Project Master Sheet"):
        _, sheets_service, drive_service, _ = get_google_services()
        query = f"'{TARGET_FOLDER_ID}' in parents and name='FocusFlow Master Log' and trashed=false"
        files = drive_service.files().list(q=query).execute().get('files', [])
        
        target_tab_name = f"Log {datetime.datetime.now().strftime('%m-%d %H%M')}"
        if files:
            sheet_id = files[0]['id']
            sheets_service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={'requests': [{'addSheet': {'properties': {'title': target_tab_name}}}]}).execute()
        else:
            file_metadata = {'name': "FocusFlow Master Log", 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [TARGET_FOLDER_ID]}
            sheet_id = drive_service.files().create(body=file_metadata, fields='id').execute().get('id')
            target_tab_name = "Sheet1"

        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=f"'{target_tab_name}'!A1",
            valueInputOption="USER_ENTERED", body={'values': st.session_state.analysis_results}
        ).execute()
        
        st.success("✅ Master Log Updated!")
        # NEW: Clickable link directly to the Spreadsheet file
        st.link_button("🚀 Open Master Log Sheet", f"https://docs.google.com/spreadsheets/d/{sheet_id}")

# 6. CHAT
st.divider()
st.subheader("💬 Query your Life Data")
user_query = st.text_input("Ask about payments, orders, or winnings:")
if user_query and st.session_state.full_context:
    model = genai.GenerativeModel('gemini-2.5-flash')
    chat_prompt = f"Data: {st.session_state.full_context}\nQuestion: {user_query}"
    answer = model.generate_content(chat_prompt)
    st.write(f"**Agent:** {answer.text}")