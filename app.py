import streamlit as st
from groq import Groq
import json
from datetime import datetime
import time
import os

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

# Custom CSS with Your Beautiful Color Palette
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
    
    /* Main background - Cream */
    .stApp {
        background-color: #FAF9F6;
        min-height: 100vh;
    }
    
    /* Navigation Bar - Primary Lavender */
    .navbar-container {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        padding: 1.5rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(226, 169, 241, 0.4);
    }
    
    .nav-logo-section {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .logo-container {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 4px solid rgba(255, 255, 255, 0.8);
    }
    
    .logo-icon {
        font-size: 3rem;
        color: #e2a9f1;
    }
    
    .app-name {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        letter-spacing: 1px;
    }
    
    .nav-icon-btn {
        width: 55px;
        height: 55px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid rgba(255, 255, 255, 0.4);
    }
    
    .nav-icon-btn:hover {
        background: rgba(255, 255, 255, 0.4);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    }
    
    .nav-icon-btn i {
        font-size: 1.6rem;
        color: white;
    }
    
    .profile-container {
        width: 55px;
        height: 55px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 3px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .profile-container:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    .profile-icon {
        font-size: 2rem;
        color: #4A4459;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(226, 169, 241, 0.15);
    }
    
    /* AI Chat Button - Warm Peach */
    .ai-button-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    
    .ai-chat-button {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FFB4A2 0%, #FF9B87 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 8px 30px rgba(255, 180, 162, 0.5);
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        border: 3px solid rgba(255, 255, 255, 0.8);
    }
    
    .ai-chat-button:hover {
        transform: scale(1.15);
        box-shadow: 0 10px 40px rgba(255, 180, 162, 0.7);
    }
    
    .ai-chat-button i {
        font-size: 2.5rem;
        color: white;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 8px 30px rgba(255, 180, 162, 0.5);
        }
        50% {
            box-shadow: 0 10px 45px rgba(255, 180, 162, 0.8);
        }
    }
    
    /* Chat Interface - Lavender */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        max-width: 900px;
        margin: 2rem auto;
        border: 2px solid #e2a9f1;
    }
    
    .chat-header {
        color: #4A4459;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e2a9f1;
    }
    
    .chat-message {
        padding: 1.2rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #4A4459;
    }
    
    .chat-message.user {
        background: #FAF9F6;
        margin-left: 20%;
        border: 2px solid #e2a9f1;
    }
    
    .chat-message.assistant {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        color: white;
        margin-right: 20%;
    }
    
    /* Form Section */
    .form-section-title {
        color: #4A4459;
        font-size: 1.6rem;
        font-weight: 600;
        margin: 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    /* Success Message - Sage Green */
    .success-message {
        background: linear-gradient(135deg, #A8C9A5 0%, #95B892 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 6px 25px rgba(168, 201, 165, 0.4);
    }
    
    .success-message h2 {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .success-message h3 {
        font-size: 1.5rem;
        font-weight: 400;
        margin: 0.5rem 0;
    }
    
    /* Ambulance Button - Warm Peach */
    .ambulance-btn {
        background: linear-gradient(135deg, #FFB4A2 0%, #FF9B87 100%) !important;
        color: white !important;
        padding: 1.2rem 2.5rem !important;
        border-radius: 30px !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 6px 25px rgba(255, 180, 162, 0.5) !important;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 6px 25px rgba(255, 180, 162, 0.5);
        }
        50% {
            box-shadow: 0 8px 35px rgba(255, 180, 162, 0.8);
        }
    }
    
    /* Case Cards */
    .case-card {
        background: white;
        padding: 1.8rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border-left: 6px solid #e2a9f1;
        color: #4A4459;
    }
    
    .case-id {
        color: #e2a9f1;
        font-weight: 700;
        font-size: 1.4rem;
        margin-bottom: 1rem;
    }
    
    .case-status {
        background: linear-gradient(135deg, #A8C9A5 0%, #95B892 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        display: inline-block;
        margin-top: 1rem;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Vet Suggestions - Deep Plum Text */
    .vet-suggestions {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        color: #4A4459;
        line-height: 1.9;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 2px solid #e2a9f1;
    }
    
    .vet-suggestions h3 {
        color: #e2a9f1;
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    .vet-suggestions strong {
        color: #4A4459;
        font-weight: 600;
    }
    
    /* No Cases Container */
    .no-cases-container {
        text-align: center;
        padding: 4rem 2rem;
        color: #4A4459;
    }
    
    .no-cases-icon {
        font-size: 6rem;
        color: #e2a9f1;
        opacity: 0.6;
        margin-bottom: 1.5rem;
    }
    
    .no-cases-text {
        font-size: 1.4rem;
        font-weight: 400;
        opacity: 0.8;
    }
    
    /* Buttons - Primary Lavender */
    .stButton > button {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2rem !important;
        border-radius: 25px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(226, 169, 241, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(226, 169, 241, 0.6) !important;
    }
    
    /* Input Fields - Deep Plum borders */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background: white !important;
        border: 2px solid #4A4459 !important;
        color: #4A4459 !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
        padding: 0.8rem !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #e2a9f1 !important;
        box-shadow: 0 0 0 2px rgba(226, 169, 241, 0.2) !important;
    }
    
    /* Labels - Deep Plum */
    label {
        color: #4A4459 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: white;
        border: 2px dashed #4A4459;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2a9f1, transparent);
        margin: 2rem 0;
    }
</style>
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

# AI Chat Button (Floating)
def render_ai_button():
    st.markdown("""
    <div class="ai-button-container">
        <div class="ai-chat-button" onclick="document.getElementById('chat-trigger').click();">
            <i class="fas fa-robot"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Home Page
def render_home():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # Check if main.png exists
    if os.path.exists("main.png"):
        try:
            st.image("main.png", use_container_width=True)
        except Exception as e:
            st.markdown("""
            <div style="text-align: center; padding: 100px; background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%); border-radius: 20px;">
                <i class="fas fa-paw" style="font-size: 6rem; color: white; margin-bottom: 1rem;"></i>
                <h2 style="color: white; font-size: 2.5rem; font-weight: 600;">Welcome to PawAlert</h2>
                <p style="color: white; font-size: 1.3rem; opacity: 0.95; margin-top: 1rem;">Saving Lives, One Paw at a Time</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 100px; background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%); border-radius: 20px;">
            <i class="fas fa-paw" style="font-size: 6rem; color: white; margin-bottom: 1rem;"></i>
            <h2 style="color: white; font-size: 2.5rem; font-weight: 600;">Welcome to PawAlert</h2>
            <p style="color: white; font-size: 1.3rem; opacity: 0.95; margin-top: 1rem;">Saving Lives, One Paw at a Time</p>
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
            <i class="fas fa-paw"></i> <strong>Hello! I'm here to help you report an animal emergency.</strong><br><br>
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
                    help="Please provide as much detail as possible",
                    height=150
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
            st.markdown('<style>.ambulance-btn-wrapper button { background: linear-gradient(135deg, #FFB4A2 0%, #FF9B87 100%) !important; }</style>', unsafe_allow_html=True)
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
            <div class="no-cases-icon">
                <i class="fas fa-folder-open"></i>
            </div>
            <p class="no-cases-text">No cases created yet.<br>Click the AI button to report an emergency.</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for case in reversed(st.session_state.cases):
            st.markdown(f"""
            <div class="case-card">
                <div class="case-id"><i class="fas fa-paw"></i> {case['case_id']}</div>
                <div style="margin-top: 0.5rem; line-height: 2;">
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
    # Navigation Bar
    st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
    
    nav_col1, nav_col2 = st.columns([2, 1])
    
    with nav_col1:
        logo_col, name_col = st.columns([1, 4])
        with logo_col:
            # Check if logo.png exists
            if os.path.exists("logo.png"):
                try:
                    st.image("logo.png", width=80)
                except:
                    st.markdown('<div class="logo-container"><i class="fas fa-paw logo-icon"></i></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="logo-container"><i class="fas fa-paw logo-icon"></i></div>', unsafe_allow_html=True)
        
        with name_col:
            st.markdown('<div class="app-name">PawAlert</div>', unsafe_allow_html=True)
    
    with nav_col2:
        icon_col1, icon_col2, icon_col3 = st.columns(3)
        
        with icon_col1:
            if st.button("", key="status_nav_btn", help="View Status"):
                st.session_state.current_page = 'status'
                st.session_state.show_chat = False
                st.rerun()
            st.markdown('<div style="margin-top: -50px; text-align: center;"><div class="nav-icon-btn"><i class="fas fa-chart-line"></i></div></div>', unsafe_allow_html=True)
        
        with icon_col2:
            if st.button("", key="ai_nav_btn", help="AI Assistant"):
                st.session_state.show_chat = True
                st.session_state.current_page = 'chat'
                st.rerun()
            st.markdown('<div style="margin-top: -50px; text-align: center;"><div class="nav-icon-btn"><i class="fas fa-robot"></i></div></div>', unsafe_allow_html=True)
        
        with icon_col3:
            # Check if default.png exists
            if os.path.exists("default.png"):
                try:
                    st.image("default.png", width=55)
                except:
                    st.markdown('<div class="profile-container"><i class="fas fa-user-circle profile-icon"></i></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="profile-container"><i class="fas fa-user-circle profile-icon"></i></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hidden button for floating AI chat trigger
    if st.button("Open Chat", key="chat-trigger", help="Open AI Chat"):
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
