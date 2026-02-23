# ⚡ FocusFlow: Personal AI Chief of Staff

FocusFlow is an intelligent personal assistant agent that bridges the gap between unstructured life data (Gmail/Calendar) and structured productivity tools (Google Sheets). It uses LLM reasoning to synthesize emails and events into a prioritized, actionable dashboard.

## 🚀 Core Features
* **Deep Life-Data Sync**: Scans Gmail and Google Calendar for critical commitments, interviews, and orders.
* **Intelligent Extraction**: Uses Gemini 2.5 Flash to identify purchase confirmations (Temu/Amazon) and upcoming payments.
* **Financial Consolidation**: Automatically groups fragmented lottery/gambling winnings into a single "Net Position" line item.
* **Master Log Integration**: Syncs the daily dashboard to a specific Google Drive folder, appending a new timestamped tab to a master spreadsheet.
* **Deterministic Sorting**: Implements Python-level post-processing to ensure data is strictly sorted in descending order by date.
* **Real-time Querying**: A conversational agent that allows users to ask natural language questions about their fetched data.

## 🛠️ Tech Stack
* **Frontend**: Streamlit
* **AI Engine**: Google Gemini 2.5 Flash
* **APIs**: Google Gmail API, Google Calendar API, Google Sheets API, Google Drive API
* **Data Handling**: Pandas & Regex for data normalization

## 📋 Prerequisites
* Python 3.10+
* A Google Cloud Project with Gmail, Sheets, Drive, and Calendar APIs enabled.
* `credentials.json` from your Google Cloud Console.

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/prashanth0686/focusflow_agent.git](https://github.com/prashanth0686/focusflow_agent.git)
   cd focusflow_agent
