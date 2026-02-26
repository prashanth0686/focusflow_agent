# ⚡ FocusFlow: Personal AI Chief of Staff

FocusFlow is an intelligent personal assistant agent that bridges the gap between unstructured life data (Gmail/Calendar) and structured productivity tools (Google Sheets). It uses LLM reasoning to synthesize emails and events into a prioritized, actionable dashboard.

---

## 🚀 Core Features
* **Deep Life-Data Sync**: Scans Gmail and Google Calendar for critical commitments, interviews, and orders.
* **Intelligent Extraction**: Uses **Gemini 2.5 Flash** to identify purchase confirmations (Temu/Amazon) and upcoming payments.
* **Financial Consolidation**: Automatically groups fragmented lottery/gambling winnings into a single "Net Position" line item.
* **Master Log Integration**: Syncs the daily dashboard to Google Drive, appending a new timestamped tab to a master spreadsheet.
* **Deterministic Sorting**: Implements Python-level post-processing to ensure data is strictly sorted in descending order by date.
* **Real-time Querying**: A conversational agent that allows users to ask natural language questions about their fetched data.

---

## 🛠️ Tech Stack
* **Frontend**: Streamlit
* **AI Engine**: Google Gemini 2.5 Flash (`google-genai` SDK)
* **APIs**: Google Gmail, Calendar, Sheets, and Drive APIs
* **Data Handling**: Pandas & Regex for data normalization

---

## ⚙️ Installation & Setup

### 1. Prerequisites
* **Python 3.10+** installed on your system.
* **Google Cloud Project**: Enable the Gmail, Calendar, Sheets, and Drive APIs.
* **Gemini API Key**: Obtain your key from [Google AI Studio](https://aistudio.google.com/).

### 2. Google Cloud Authentication (Essential)
To allow FocusFlow to read your data, you must set up OAuth:
1. Go to **APIs & Services > Credentials** in the [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Create Credentials > OAuth client ID**.
3. Select **Desktop App** as the application type.
4. Download the resulting JSON file, rename it to `credentials.json`, and place it in the project root directory.


# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

### 3. Environment Configuration
Create a file named `.env` in the root directory and add your specific keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SPREADSHEET_ID=your_google_sheet_id_here
DRIVE_FOLDER_ID=your_folder_id_here

4. Repository Setup
# Clone the repository
git clone [https://github.com/prashanth0686/focusflow_agent.git](https://github.com/prashanth0686/focusflow_agent.git)
cd focusflow_agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

🚀 Running the Agent
To start the dashboard on Windows, use the Python launcher to ensure Streamlit runs within your local environment's context:
py -m streamlit run app.py

Note: On the first run, a browser tab will open for Google Authorization. This will generate a token.json file locally to save your session. Do not commit token.json or credentials.json to GitHub.

📂 Project Structure
focusflow_agent/
├── app.py              # Main Streamlit dashboard & Agent logic
├── core/               # Data extraction & AI processing modules
├── utils/              # Google API helpers (Gmail, Calendar, Sheets)
├── credentials.json    # (User-provided) Google OAuth credentials
├── token.json          # (Auto-generated) User session token
├── .env                # (User-provided) API keys and IDs
└── requirements.txt    # Project dependencies

🛡️ Security & Privacy
FocusFlow processes your data locally. It only sends specific email/calendar snippets to the Gemini API for synthesis. Your credentials and tokens stay on your machine. Ensure your .gitignore includes credentials.json, token.json, and .env before pushing to any public repository.






FOLDER_ID=your_folder_id_here
