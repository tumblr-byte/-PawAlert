import streamlit as st
from groq import Groq
import json
from datetime import datetime
import time
import base64
from PIL import Image

# Page config
st.set_page_config(
    page_title="PawAlert - Animal Rescue Platform",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'report_submitted' not in st.session_state:
    st.session_state.report_submitted = False

# Custom CSS with Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Global Font */
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Navigation Bar - Glassmorphism */
    .navbar {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nav-logo-img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .app-name {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .nav-icon {
        color: white;
        font-size: 1.4rem;
        cursor: pointer;
        transition: all 0.3s ease;
        padding: 0.7rem;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
    }
    
    .nav-icon:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    .user-profile-img {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid rgba(255, 255, 255, 0.5);
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .user-profile-img:hover {
        transform: scale(1.1);
        border-color: white;
    }
    
    /* Hero Section - Glassmorphism */
    .hero-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        text-align: center;
    }
    
    .hero-image-container {
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
    }
    
    .hero-image {
        width: 100%;
        height: auto;
        display: block;
        transition: transform 0.3s ease;
    }
    
    .hero-image:hover {
        transform: scale(1.02);
    }
    
    /* AI Chat Button - Floating */
    .ai-button-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    
    .ai-chat-button {
        width: 75px;
        height: 75px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    
    .ai-chat-button:hover {
        transform: scale(1.15);
        background: rgba(255, 255, 255, 0.3);
    }
    
    .ai-chat-button i {
        font-size: 2.2rem;
        color: white;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        50% {
            box-shadow: 0 8px 50px 0 rgba(31, 38, 135, 0.6);
        }
    }
    
    /* Chat Interface - Glassmorphism */
    .chat-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        max-width: 900px;
        margin: 2rem auto;
    }
    
    .chat-header {
        color: white;
        font-size: 1.6rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .chat-message {
        padding: 1.2rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .chat-message.user {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(5px);
        color: white;
        margin-left: 20%;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .chat-message.assistant {
        background: rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(5px);
        color: white;
        margin-right: 20%;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Report Form - Glassmorphism */
    .report-form {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 2rem 0;
    }
    
    .form-section-title {
        color: white;
        font-size: 1.4rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    /* Success Message - Glassmorphism */
    .success-message {
        background: rgba(76, 175, 80, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px solid rgba(76, 175, 80, 0.5);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px 0 rgba(76, 175, 80, 0.3);
    }
    
    .success-message h2 {
        font-size: 1.8rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .success-message h3 {
        font-size: 1.3rem;
        font-weight: 400;
        margin: 0.5rem 0;
    }
    
    /* Case Cards - Glassmorphism */
    .case-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border-left: 5px solid rgba(102, 126, 234, 0.8);
        color: white;
    }
    
    .case-id {
        color: white;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    .case-status {
        background: rgba(76, 175, 80, 0.3);
        backdrop-filter: blur(5px);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 1rem;
        border: 1px solid rgba(76, 175, 80, 0.5);
        font-weight: 500;
    }
    
    /* Vet Suggestions Styling */
    .vet-suggestions {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        color: white;
        line-height: 1.8;
    }
    
    .vet-suggestions h3 {
        color: white;
        font-size: 1.4rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* No Cases Container */
    .no-cases-container {
        text-align: center;
        padding: 3rem;
        color: white;
    }
    
    .no-cases-text {
        font-size: 1.3rem;
        font-weight: 400;
        margin-top: 1rem;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* Input Fields Styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stFileUploader label {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load images
def load_image(image_path):
    """Load and display image"""
    try:
        return Image.open(image_path)
    except:
        return None

# Navigation Bar
def render_navbar():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="nav-left">
            <img src="data:image/png;base64,{}" class="nav-logo-img" alt="Logo">
            <span class="app-name">PawAlert</span>
        </div>
        """.format(get_image_base64("logo.png") if get_image_base64("logo.png") else ""), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="nav-right">
            <div class="nav-icon" title="Status">
                <i class="fas fa-chart-line"></i>
            </div>
            <div class="nav-icon" title="AI Assistant">
                <i class="fas fa-robot"></i>
            </div>
            <img src="data:image/png;base64,{}" class="user-profile-img" alt="Profile">
        </div>
        """.format(get_image_base64("default.png") if get_image_base64("default.png") else ""), unsafe_allow_html=True)

def get_image_base64(image_path):
    """Convert image to base64 for embedding"""
    try:
        img = Image.open(image_path)
        import io
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except:
        return None

# AI Chat Button (Floating)
def render_ai_button():
    st.markdown("""
    <div class="ai-button-container">
        <div class="ai-chat-button" onclick="document.getElementById('chat-trigger').click();">
            <i class="fas fa-comments"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Groq API Setup
def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY", "your-groq-api-key-here")
    return Groq(api_key=api_key)

# Vet Database
VET_DATABASE = """
Available Veterinary Hospitals:

1. **PawCare Emergency Vet Clinic**
   - Location: Connaught Place, New Delhi
   - Specialties: 24/7 Emergency, Surgery, ICU, Trauma Care
   - Best for: Critical injuries, accidents, severe trauma
   - Cost Range: ₹1000-3000
   - Contact: +91-11-4567-8901
   - Ambulance: Available

2. **AnimalAid Veterinary Hospital**
   - Location: Hauz Khas, South Delhi
   - Specialties: Emergency Care, X-Ray, Stray Animal Treatment
   - Best for: General injuries, broken bones, wound care
   - Cost Range: ₹800-2500
   - Contact: +91-11-4567-8902
   - Ambulance: Available

3. **Street Paws Rescue Center**
   - Location: Indirapuram, Ghaziabad
   - Specialties: Stray Animal Specialist, Budget-Friendly, Rehabilitation
   - Best for: Stray animals, abuse cases, long-term care
   - Cost Range: ₹500-1500
   - Contact: +91-120-456-7890
   - Ambulance: Available

4. **VetPlus Clinic**
   - Location: Rohini, North Delhi
   - Specialties: General Care, Vaccination, Minor Surgeries
   - Best for: Minor injuries, skin conditions, infections
   - Cost Range: ₹600-2000
   - Contact: +91-11-4567-8904
   - Ambulance: Not Available

5. **Emergency Pet Care Center**
   - Location: Noida Sector 18
   - Specialties: 24/7 Critical Care, Advanced Surgery, Blood Bank
   - Best for: Life-threatening conditions, major surgeries
   - Cost Range: ₹1500-4000
   - Contact: +91-120-456-7891
   - Ambulance: Available

6. **Happy Tails Veterinary**
   - Location: Dwarka, West Delhi
   - Specialties: Affordable Care, Basic Treatment, Vaccination
   - Best for: Minor wounds, general checkups, preventive care
   - Cost Range: ₹400-1200
   - Contact: +91-11-4567-8906
   - Ambulance: Not Available

7. **Metro Animal Hospital**
   - Location: Vaishali, Ghaziabad
   - Specialties: Surgery, Rehabilitation, Post-Operative Care
   - Best for: Surgeries, fractures, recovery care
   - Cost Range: ₹1000-2800
   - Contact: +91-120-456-7892
   - Ambulance: Available
"""

# Groq AI Response Function
def get_vet_suggestions(location, issue_desc, severity, report_type):
    client = get_groq_client()
    
    prompt = f"""You are a compassionate veterinary assistant AI helping rescue injured and abused stray animals.

{VET_DATABASE}

Based on this report, suggest the 3 MOST SUITABLE veterinary hospitals:

Report Details:
- Location: {location}
- Issue Description: {issue_desc}
- Severity/Type: {severity}
- Report Type: {"Abuse Case" if report_type == "Abuse" else "Injury Case"}

IMPORTANT: Pick 3 vets that are:
1. Closest to the location mentioned
2. Have appropriate facilities for this type of case
3. Within reasonable cost range

Format your response EXACTLY like this for each vet:

**[Vet Name]**
📍 Location: [Area, City]
📏 Distance: [Estimate like "2.5 km" or "15 minutes"]
💰 Estimated Cost: ₹[range]
🏥 Key Facilities: [List 3-4 key facilities]
✨ Why Recommended: [1-2 sentences explaining why this vet is suitable for THIS specific case]
🚑 Ambulance: [Available/Not Available]
📞 Contact: [Phone number]

---

Provide EXACTLY 3 suggestions. Be specific and caring in your recommendations."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a compassionate veterinary assistant helping rescue animals. Always be empathetic and provide clear, actionable recommendations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting vet suggestions: {str(e)}\n\nPlease try again or contact emergency services directly."

# Generate Case ID
def generate_case_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"PA{timestamp}"

# Home Page
def render_home():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # Try to load and display main.png
    main_img = load_image("main.png")
    if main_img:
        st.markdown('<div class="hero-image-container">', unsafe_allow_html=True)
        st.image(main_img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hero-image-container" style="background: rgba(255,255,255,0.1); padding: 100px; text-align: center; color: white;">
            <i class="fas fa-paw" style="font-size: 5rem; margin-bottom: 1rem;"></i>
            <h2 style="font-size: 2rem; font-weight: 500;">Welcome to PawAlert</h2>
            <p style="font-size: 1.2rem; opacity: 0.9;">Saving Lives, One Paw at a Time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat Interface
def render_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header"><i class="fas fa-robot"></i> AI Assistant - Report Animal Emergency</div>', unsafe_allow_html=True)
    
    # Chat Messages
    for msg in st.session_state.chat_messages:
        role_class = "user" if msg["role"] == "user" else "assistant"
        st.markdown(f'<div class="chat-message {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Initial greeting
    if len(st.session_state.chat_messages) == 0:
        st.markdown('''
        <div class="chat-message assistant">
            <i class="fas fa-paw"></i> Hello! I'm here to help you report an animal emergency.<br><br>
            Please tell me:<br>
            1. <strong>Location</strong> where the animal is<br>
            2. <strong>What happened</strong> (injury or abuse)<br>
            3. <strong>Animal type</strong> (dog, cat, etc.)<br>
            4. <strong>Condition</strong> of the animal<br><br>
            You can also upload photos/videos to help me understand better.
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Report Form
    if not st.session_state.report_submitted:
        st.markdown("---")
        st.markdown('<div class="form-section-title"><i class="fas fa-clipboard-list"></i> Fill Report Details</div>', unsafe_allow_html=True)
        
        with st.form("report_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                report_type = st.selectbox(
                    "Report Type",
                    ["Injury", "Abuse"],
                    help="Select whether this is an injury or abuse case"
                )
                
                location = st.text_input(
                    "📍 Location",
                    placeholder="e.g., Near Connaught Place Metro, Delhi",
                    help="Where is the animal located?"
                )
                
                animal_type = st.selectbox(
                    "🐕 Animal Type",
                    ["Dog", "Cat", "Cow", "Other"]
                )
            
            with col2:
                severity = st.selectbox(
                    "⚠️ Severity",
                    ["Minor Injury", "Moderate Injury", "Severe/Critical", "Abuse Case"]
                )
                
                issue_desc = st.text_area(
                    "📋 Description",
                    placeholder="Describe what happened and the animal's condition...",
                    help="Please provide as much detail as possible"
                )
                
                uploaded_file = st.file_uploader(
                    "📸 Upload Photo/Video (Optional)",
                    type=['jpg', 'jpeg', 'png', 'mp4'],
                    help="Visual evidence helps us provide better care"
                )
            
            submit_btn = st.form_submit_button("🚨 Submit Report", use_container_width=True)
            
            if submit_btn:
                if not location or not issue_desc:
                    st.error("⚠️ Please fill in location and description!")
                else:
                    with st.spinner("🔍 Analyzing situation and finding best veterinary care..."):
                        vet_suggestions = get_vet_suggestions(location, issue_desc, severity, report_type)
                        case_id = generate_case_id()
                        
                        case = {
                            "case_id": case_id,
                            "type": report_type,
                            "location": location,
                            "animal_type": animal_type,
                            "severity": severity,
                            "description": issue_desc,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "Case Registered - Help On The Way",
                            "vet_suggestions": vet_suggestions
                        }
                        st.session_state.cases.append(case)
                        st.session_state.report_submitted = True
                        st.rerun()
    
    # Show results after submission
    if st.session_state.report_submitted and len(st.session_state.cases) > 0:
        latest_case = st.session_state.cases[-1]
        
        st.markdown(f"""
        <div class="success-message">
            <h2><i class="fas fa-check-circle"></i> Report Submitted Successfully!</h2>
            <h3>Case ID: {latest_case['case_id']}</h3>
            <p><i class="fas fa-paw"></i> Your report is helping an animal in need</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="vet-suggestions">', unsafe_allow_html=True)
        st.markdown('<h3><i class="fas fa-hospital"></i> Recommended Veterinary Care</h3>', unsafe_allow_html=True)
        st.markdown(latest_case['vet_suggestions'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🚑 DISPATCH AMBULANCE NOW", key="ambulance", use_container_width=True):
                with st.spinner("🚨 Dispatching ambulance..."):
                    time.sleep(2)
                    st.success("✅ Ambulance #1247 dispatched! ETA: 15 minutes")
                    st.balloons()
        
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.show_chat = False
            st.session_state.report_submitted = False
            st.session_state.current_page = 'home'
            st.rerun()

# Status Page
def render_status():
    st.markdown('<div class="form-section-title"><i class="fas fa-chart-line"></i> Case Status Tracker</div>', unsafe_allow_html=True)
    
    if len(st.session_state.cases) == 0:
        st.markdown('''
        <div class="no-cases-container">
            <i class="fas fa-folder-open" style="font-size: 5rem; opacity: 0.7;"></i>
            <p class="no-cases-text">No cases created yet.<br>Click the AI button to report an emergency.</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for case in reversed(st.session_state.cases):
            st.markdown(f"""
            <div class="case-card">
                <div class="case-id"><i class="fas fa-paw"></i> {case['case_id']}</div>
                <div style="margin-top: 0.5rem; line-height: 1.8;">
                    <strong><i class="fas fa-tag"></i> Type:</strong> {case['type']}<br>
                    <strong><i class="fas fa-dog"></i> Animal:</strong> {case['animal_type']}<br>
                    <strong><i class="fas fa-map-marker-alt"></i> Location:</strong> {case['location']}<br>
                    <strong><i class="fas fa-exclamation-triangle"></i> Severity:</strong> {case['severity']}<br>
                    <strong><i class="fas fa-clock"></i> Time:</strong> {case['timestamp']}<br>
                    <strong><i class="fas fa-file-alt"></i> Description:</strong> {case['description']}
                </div>
                <div class="case-status"><i class="fas fa-check-circle"></i> {case['status']}</div>
            </div>
            """, unsafe_allow_html=True)

# Main App Logic
def main():
    # Navigation Bar with functional buttons
    col_left, col_space, col_status, col_ai, col_profile = st.columns([3, 5, 1, 1, 1])
    
    with col_left:
        logo_col, name_col = st.columns([1, 3])
        with logo_col:
            logo_img = load_image("logo.png")
            if logo_img:
                st.image(logo_img, width=50)
            else:
                st.markdown('<i class="fas fa-paw" style="font-size: 2.5rem; color: white;"></i>', unsafe_allow_html=True)
        with name_col:
            st.markdown('<div class="app-name">PawAlert</div>', unsafe_allow_html=True)
    
    with col_status:
        if st.button("", key="status_nav", help="View Status", use_container_width=True):
            st.session_state.current_page = 'status'
            st.session_state.show_chat = False
            st.rerun()
        st.markdown('<div style="text-align: center; margin-top: -45px;"><i class="fas fa-chart-line" style="font-size: 1.4rem; color: white;"></i></div>', unsafe_allow_html=True)
    
    with col_ai:
        if st.button("", key="ai_nav", help="AI Assistant", use_container_width=True):
            st.session_state.show_chat = True
            st.session_state.current_page = 'chat'
            st.rerun()
        st.markdown('<div style="text-align: center; margin-top: -45px;"><i class="fas fa-robot" style="font-size: 1.4rem; color: white;"></i></div>', unsafe_allow_html=True)
    
    with col_profile:
        profile_img = load_image("default.png")
        if profile_img:
            st.image(profile_img, width=45)
        else:
            st.markdown('<div style="text-align: center;"><i class="fas fa-user-circle" style="font-size: 2.5rem; color: white;"></i></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hidden button for floating AI chat trigger
    if st.button("Open Chat", key="chat-trigger", type="primary", help="Open AI Chat"):
        st.session_state.show_chat = True
        st.session_state.current_page = 'chat'
        st.rerun()
    
    # Show appropriate page
    if st.session_state.show_chat or st.session_state.current_page == 'chat':
        render_chat()
    elif st.session_state.current_page == 'status':
        render_status()
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.session_state.show_chat = False
            st.rerun()
    else:
        render_home()
    
    # Floating AI Button
    render_ai_button()

if __name__ == "__main__":
    main()
