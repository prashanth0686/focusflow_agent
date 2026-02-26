🚀 Running the Agent
To launch the FocusFlow dashboard, use the Python launcher command. This method is recommended for Windows users to ensure the Streamlit module is called from the correct Python environment.

1. Standard Execution
Open your terminal in the project root and run:

Bash
py -m streamlit run app.py
2. Execution with Script Arguments
If you need to pass specific flags to your agent (e.g., to run in headless mode for a server), use:

Bash
py -m streamlit run app.py --server.headless true
3. What Happens Next?
Local Server: Streamlit will start a local web server (typically at http://localhost:8501).

Authentication: On your first run, a browser window will prompt you to authorize FocusFlow to access your Google Gmail and Calendar data.

Token Generation: After authorization, a token.json file will appear in your project folder. This stores your session so you don't have to log in every time.

💡 PM Troubleshooting Tip: Why use py -m?
As a Product Manager, you might handle multiple environments. Using the py -m prefix (the Python launcher) explicitly tells Windows to find the streamlit library inside the Python installation. This avoids the common " 'streamlit' is not recognized" error that happens when the Streamlit scripts folder isn't in your System PATH.
