import streamlit as st
import pandas as pd
from src.scanner import ScannerAgent
from src.evaluator import EvaluatorAgent

# 1. Page Configuration
st.set_page_config(
    page_title="Knowledge Decay Detector",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# 2. Header & Styling
st.title("🕵️‍♂️ Internal Knowledge Decay Agent")
st.markdown("""
**Welcome, Engineer.**
This tool uses AI to scan your documentation (Local or GitHub) and detect "stale" or outdated knowledge.
""")

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    target_input = st.text_input(
        "Target Directory or GitHub Repo",
        value="mock_docs",
        help="Enter a local folder path (e.g., 'docs/') or a GitHub repo (e.g., 'owner/repo')."
    )
    
    start_btn = st.button("🚀 Start Scan", type="primary")

# 4. Main Logic Flow
if start_btn:
    # A. Validate Input
    if not target_input:
        st.error("Please enter a valid target!")
        st.stop()

    # B. Initialize Agents (Show a spinner while working)
    with st.spinner(f"Agents are scanning: {target_input}..."):
        try:
            # Initialize Scanner
            scanner = ScannerAgent(target_input)
            
            # --- PHASE 1: SCAN ---
            status_text = st.empty() # specific placeholder for updates
            status_text.text("📂 Scanning file system...")
            
            scanned_files = scanner.scan()
            
            if not scanned_files:
                st.warning("No Markdown (.md) files found in this location.")
                st.stop()
                
            st.success(f"✅ Found {len(scanned_files)} files. Analyzing content...")
            
            # --- PHASE 2: EVALUATE ---
            evaluator = EvaluatorAgent()
            results = []
            progress_bar = st.progress(0)
            
            for i, file in enumerate(scanned_files):
                # Update progress bar
                progress = (i + 1) / len(scanned_files)
                progress_bar.progress(progress)
                status_text.text(f"🧠 Reading: {file['path']}...")
                
                # AI Judgment
                analysis = evaluator.evaluate(file['path'], file['content'])
                
                # Store Result
                results.append({
                    "File Path": file['path'],
                    "Status": analysis['status'],
                    "Reason": analysis['reason']
                })
            
            # Clear progress indicators
            status_text.empty()
            progress_bar.empty()

            # --- PHASE 3: REPORT ---
            # Convert list of dicts to a Pandas DataFrame for a pretty table
            df = pd.DataFrame(results)
            
            # Separate Stale vs Fresh
            stale_docs = df[df["Status"] == "STALE"]
            fresh_docs = df[df["Status"] == "FRESH"]

            # Display Stale Docs (The "Bad" News)
            if not stale_docs.empty:
                st.error(f"🚨 Knowledge Decay Detected in {len(stale_docs)} files!")
                st.dataframe(
                    stale_docs, 
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("🎉 Excellent! No knowledge decay detected.")

            # Display Fresh Docs (Expandable)
            with st.expander("View Fresh Documents"):
                st.dataframe(
                    fresh_docs, 
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")