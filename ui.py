# ui_fixed.py - With better error handling
import streamlit as st
import requests
import os
import shutil
from pathlib import Path
import json
import time

# API URL
API_URL = "http://localhost:8000"
WORKSPACE = "agent_workspace"

st.set_page_config(
    page_title="AI File Organizer",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# Title
st.title("🤖 AI File Organizer Agent")
st.markdown("---")

# Create workspace
os.makedirs(WORKSPACE, exist_ok=True)

# === API CONNECTION TEST ===
# This runs every time the UI loads
try:
    response = requests.get(f"{API_URL}/status", timeout=3)
    if response.status_code == 200:
        api_status = "🟢 CONNECTED"
        api_working = True
        status_data = response.json()
    else:
        api_status = "🟡 ERROR"
        api_working = False
        status_data = None
except requests.exceptions.ConnectionError:
    api_status = "🔴 NOT RUNNING"
    api_working = False
    status_data = None
except Exception as e:
    api_status = f"🔴 ERROR: {str(e)[:50]}"
    api_working = False
    status_data = None

# Show API status at the top
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("API Status", api_status)
with col2:
    if api_working and status_data:
        st.metric("Files in Workspace", status_data.get('total_files', 0))
with col3:
    if api_working and status_data:
        st.metric("Folders Created", status_data.get('folders_created', 0))

if not api_working:
    st.error("⚠️ **API IS NOT RUNNING!** Please start it with: `python api.py` in a terminal")
    st.code("""
    # In a new terminal:
    cd my_ai_agent
    python api.py
    """)
    st.stop()  # Stop the UI here if API not running

# Rest of your UI code...
st.success("✅ API is connected! Ready to organize files.")

# Function to get file structure
def get_file_structure():
    structure = {
        'unorganized': [],
        'organized': {}
    }
    
    workspace = Path(WORKSPACE)
    
    for item in workspace.iterdir():
        if item.is_file() and item.name != "memory.json":
            structure['unorganized'].append(item.name)
        elif item.is_dir() and item.name not in ["__pycache__", ".ipynb_checkpoints"]:
            files = [f.name for f in item.iterdir() if f.is_file()]
            if files:
                structure['organized'][item.name] = files
    
    return structure

# Sidebar
with st.sidebar:
    st.header("🎮 Control Panel")
    
    if st.button("📊 Refresh Status", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.subheader("API Info")
    st.write(f"URL: {API_URL}")
    st.write(f"Status: {api_status}")
    
    if st.button("📁 TEST ORGANIZE", type="primary", use_container_width=True):
        with st.spinner("🤖 Agent organizing..."):
            try:
                response = requests.post(f"{API_URL}/organize", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ Organized {result['total']} files!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Failed: {e}")
    
    st.markdown("---")
    if st.button("🧠 Show Memory", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/memory")
            memory = response.json()
            st.write("**Learned:**", memory.get('learned', {}))
            st.write("**Recent:**", memory.get('history', [])[-3:])
        except:
            st.error("Could not fetch memory")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload", "📁 Files", "🧠 Memory"])

with tab1:
    st.header("Upload Files")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"📦 {len(uploaded_files)} files selected")
        
        for file in uploaded_files:
            st.write(f"• {file.name}")
        
        if st.button("📤 Upload to Workspace", use_container_width=True):
            for file in uploaded_files:
                file_path = Path(WORKSPACE) / file.name
                with open(file_path, 'wb') as f:
                    f.write(file.getbuffer())
            st.success(f"✅ Uploaded {len(uploaded_files)} files!")
            st.info("👉 Go to 'Files' tab and click ORGANIZE")
            time.sleep(1)
            st.rerun()

with tab2:
    st.header("📁 File Organization")
    
    structure = get_file_structure()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📄 Unorganized ({len(structure['unorganized'])})")
        if structure['unorganized']:
            for f in sorted(structure['unorganized']):
                st.write(f"📄 {f}")
            
            if st.button("🚀 ORGANIZE FILES NOW", use_container_width=True):
                with st.spinner("🤖 Agent working..."):
                    try:
                        response = requests.post(f"{API_URL}/organize", timeout=10)
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ Organized {result['total']} files!")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.success("No files to organize!")
    
    with col2:
        st.subheader(f"📁 Organized ({sum(len(f) for f in structure['organized'].values())})")
        if structure['organized']:
            for folder, files in structure['organized'].items():
                with st.expander(f"📁 {folder} ({len(files)})"):
                    for f in sorted(files):
                        st.write(f"📄 {f}")
        else:
            st.info("No organized files yet")

with tab3:
    st.header("🧠 Agent Memory")
    
    try:
        response = requests.get(f"{API_URL}/memory")
        memory = response.json()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Learned Patterns")
            if memory.get('learned'):
                for ext, folder in memory['learned'].items():
                    st.write(f"• {ext} → **{folder}**")
            else:
                st.info("No learned patterns yet")
        
        with col2:
            st.subheader("Recent Actions")
            if memory.get('history'):
                for action in memory['history'][-5:]:
                    st.write(f"• {action.get('file', '')} → **{action.get('to', '')}**")
            else:
                st.info("No actions yet")
        
        # Teaching section
        st.markdown("---")
        st.subheader("🎓 Teach Agent")
        with st.form("teach_form"):
            ext = st.text_input("Extension", ".txt")
            folder = st.text_input("Folder", "Documents")
            if st.form_submit_button("🤝 Teach"):
                try:
                    r = requests.post(f"{API_URL}/learn/{ext}/{folder}")
                    st.success(f"✅ Learned: {ext} → {folder}")
                    time.sleep(1)
                    st.rerun()
                except:
                    st.error("❌ Failed")
    
    except:
        st.error("Cannot connect to API")

# Auto-refresh
time.sleep(5)
st.rerun()
