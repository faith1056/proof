import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.connection import init_db

# Initialize database on startup
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

# Page configuration
st.set_page_config(
    page_title="FixNaija Intelligence",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        color: #1a472a;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subtitle {
        color: #27663b;
        font-size: 1.2em;
        margin-bottom: 1.5em;
    }
    .info-box {
        background-color: #f0f8f5;
        border-left: 4px solid #27663b;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🇳🇬 FixNaija Intelligence")
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Report Problem", "Dashboard", "Authority Portal", "Settings"]
)

if page == "Home":
    st.markdown('<div class="main-header">FixNaija Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Transform citizen reports into community intelligence</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("""
    ### Welcome to FixNaija Intelligence
    
    FixNaija Intelligence helps your community detect, analyze, and solve recurring civic problems.
    
    **What we do:**
    - 🔍 **Detect** similar problems reported by different citizens
    - 📊 **Analyze** patterns, hotspots, and trends
    - 🎯 **Prioritize** the most urgent issues
    - 📍 **Route** problems to the right authorities
    - ✅ **Track** whether solutions actually work
    - 📈 **Learn** what works and what doesn't
    
    ### Get Started
    
    Use the menu on the left to:
    - **Report a Problem** - Submit evidence of a civic issue
    - **View Dashboard** - See community intelligence and hotspots
    - **Authority Portal** - Track case status and resolutions
    """)
    
    st.markdown(
        '<div class="info-box">'
        '<strong>ℹ️ Note:</strong> FixNaija Intelligence does NOT solve problems itself. '
        'We help organize citizen reports into actionable information for authorities.'
        '</div>',
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reports", "0", delta=None)
    with col2:
        st.metric("Active Cases", "0", delta=None)
    with col3:
        st.metric("Hotspots Detected", "0", delta=None)

elif page == "Report Problem":
    st.title("📝 Report a Civic Problem")
    st.write("Help us understand what's happening in your community.")
    st.info("Your report will be analyzed alongside others to identify patterns and hotspots.")
    st.write("*Coming soon - Report submission form*")

elif page == "Dashboard":
    st.title("📊 Community Intelligence Dashboard")
    st.write("View trends, hotspots, and problem analysis.")
    st.write("*Coming soon - Dashboard with maps and charts*")

elif page == "Authority Portal":
    st.title("👮 Authority Portal")
    st.write("Track cases and manage resolutions.")
    st.write("*Coming soon - Authority dashboard*")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Configure notification preferences and authority contacts.")
    st.write("*Coming soon*")

st.sidebar.markdown("---")
st.sidebar.markdown("**FixNaija Intelligence** | Civic Tech Platform")
st.sidebar.markdown("🇳🇬 Built for Nigerian communities")
