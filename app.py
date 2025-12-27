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

# Custom CSS with Beautiful Color Palette
st.markdown("""
<style>
    /* Font Awesome */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Base Theme - Beautiful Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Remove all black backgrounds */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Navigation Bar */
    .nav-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
    }
    
    .logo-text {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-left: 1rem;
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .nav-icon-btn {
        background: none;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        padding: 0.5rem;
    }
    
    .nav-icon {
        font-size: 1.8rem;
        color: #667eea;
        transition: all 0.3s ease;
    }
    
    .nav-icon:hover {
        color: #764ba2;
        transform: scale(1.15);
    }
    
    /* Hero Section - Only main.png */
    .hero-section {
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
    }
    
    /* Floating AI Button */
    .floating-ai-btn {
        position: fixed;
        bottom: 35px;
        right: 35px;
        width: 75px;
        height: 75px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 10px 25px rgba(245, 87, 108, 0.4);
        z-index: 9999;
        animation: pulse 2s infinite;
        transition: transform 0.3s ease;
    }
    
    .floating-ai-btn i {
        font-size: 2rem;
        color: white;
    }
    
    .floating-ai-btn:hover {
        transform: scale(1.1);
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 10px 25px rgba(245, 87, 108, 0.4);
        }
        50% { 
            transform: scale(1.08);
            box-shadow: 0 15px 35px rgba(245, 87, 108, 0.6);
        }
    }
    
    /* Chat Container */
    .chat-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 25px;
        padding: 2.5rem;
        max-width: 950px;
        margin: 0 auto;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    .chat-header i {
        margin-right: 0.5rem;
    }
    
    /* Messages */
    .message {
        padding: 1.2rem 1.5rem;
        margin: 1.2rem 0;
        border-radius: 18px;
        max-width: 85%;
        animation: fadeIn 0.4s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .message.assistant {
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e7ff 100%);
        color: #1a1a1a;
        border-left: 4px solid #667eea;
    }
    
    /* Form Styling */
    .stForm {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf0ff 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .form-section-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
    }
    
    .form-section-title i {
        margin-right: 0.5rem;
    }
    
    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 12px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Status Cards */
    .status-container {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .status-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .status-header h1 {
        color: #667eea;
        font-size: 2.5rem;
        margin: 0;
    }
    
    .status-header i {
        margin-right: 1rem;
    }
    
    .status-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border-left: 5px solid #667eea;
    }
    
    .status-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e0e7ff;
    }
    
    .case-id {
        font-size: 1.3rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .case-id i {
        margin-right: 0.5rem;
    }
    
    .status-badge {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .status-badge i {
        margin-right: 0.5rem;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(132, 250, 176, 0.3);
    }
    
    .success-box h2 {
        color: white;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .success-box i {
        font-size: 3rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Vet Suggestions Box */
    .vet-suggestions {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .vet-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
    }
    
    .vet-title i {
        margin-right: 0.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.9rem 2.5rem !important;
        font-size: 1.15rem !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 15px rgba(245, 87, 108, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(245, 87, 108, 0.4) !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* All text should be black except where specified */
    p, span, div, label, input, textarea, select {
        color: #1a1a1a !important;
    }
    
    /* White text only on gradients */
    .chat-header, .message.user, .success-box h2, .success-box i, 
    .status-badge, .form-section-title, .vet-title, .logo-text {
        color: white !important;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed rgba(102, 126, 234, 0.3);
    }
    
    /* No cases message */
    .no-cases {
        background: rgba(255, 255, 255, 0.95);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .no-cases i {
        font-size: 4rem;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .no-cases p {
        font-size: 1.2rem;
        color: #666;
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
    <div class="floating-ai-btn" onclick="document.querySelector('[key=chat-trigger]').click()">
        <i class="fas fa-robot"></i>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden trigger button
    if st.button("Open Chat", key="chat-trigger", help="Open AI Chat"):
        st.session_state.show_chat = True
        st.session_state.current_page = 'chat'
        st.rerun()

# Home Page
def render_home():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # Check if main.png exists
    if os.path.exists("main.png"):
        try:
            st.image("main.png", use_container_width=True)
        except Exception as e:
            st.info("Place your main.png image in the app directory to display the hero image.")
    else:
        st.info("Place your main.png image in the app directory to display the hero image.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat Interface
def render_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header"><i class="fas fa-comment-medical"></i> AI Assistant - Report Animal Emergency</div>', unsafe_allow_html=True)
    
    # Chat Messages
    for msg in st.session_state.chat_messages:
        role_class = "user" if msg["role"] == "user" else "assistant"
        st.markdown(f'<div class="message {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Initial greeting
    if len(st.session_state.chat_messages) == 0:
        st.markdown('''<div class="message assistant">
            <i class="fas fa-paw"></i> Hello! I'm here to help you report an animal emergency. Please tell me:<br><br>
            1. Location where the animal is<br>
            2. What happened (injury or abuse)<br>
            3. Animal type (dog, cat, etc.)<br>
            4. Condition of the animal<br><br>
            You can also upload photos/videos to help me understand better.
        </div>''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Report Form
    if not st.session_state.report_submitted:
        st.markdown("---")
        st.markdown('<div class="form-section-title"><i class="fas fa-file-medical"></i> Fill Report Details</div>', unsafe_allow_html=True)
        
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
                    "Animal Type",
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
        
        st.markdown(f"""<div class="success-box">
            <i class="fas fa-check-circle"></i>
            <h2>Report Submitted Successfully!</h2>
            <p style="color: white; font-size: 1.2rem;">Case ID: <strong>{latest_case['case_id']}</strong></p>
            <p style="color: white;">Your report is helping an animal in need</p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown('<div class="vet-suggestions">', unsafe_allow_html=True)
        st.markdown('<div class="vet-title"><i class="fas fa-hospital"></i> Recommended Veterinary Care</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="status-container">', unsafe_allow_html=True)
    st.markdown('<div class="status-header"><h1><i class="fas fa-clipboard-list"></i> Case Status Tracker</h1></div>', unsafe_allow_html=True)
    
    if len(st.session_state.cases) == 0:
        st.markdown('''<div class="no-cases">
            <i class="fas fa-folder-open"></i>
            <p>No cases created yet.</p>
            <p>Click the AI button to report an emergency.</p>
        </div>''', unsafe_allow_html=True)
    else:
        for case in reversed(st.session_state.cases):
            st.markdown(f"""<div class="status-card">
                <div class="status-card-header">
                    <div class="case-id"><i class="fas fa-hashtag"></i> {case['case_id']}</div>
                    <div class="status-badge"><i class="fas fa-check-circle"></i> {case['status']}</div>
                </div>
                <p><i class="fas fa-exclamation-triangle"></i> <strong>Type:</strong> {case['type']}</p>
                <p><i class="fas fa-paw"></i> <strong>Animal:</strong> {case['animal_type']}</p>
                <p><i class="fas fa-map-marker-alt"></i> <strong>Location:</strong> {case['location']}</p>
                <p><i class="fas fa-heartbeat"></i> <strong>Severity:</strong> {case['severity']}</p>
                <p><i class="fas fa-clock"></i> <strong>Time:</strong> {case['timestamp']}</p>
                <p><i class="fas fa-comment-dots"></i> <strong>Description:</strong> {case['description']}</p>
            </div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main App Logic
def main():
    # Navigation Bar
    st.markdown('''<div class="nav-container">
        <div class="nav-left">
            <div class="logo-container">''', unsafe_allow_html=True)
    
    # Logo
    if os.path.exists("logo.png"):
        try:
            st.image("logo.png", width=100)
        except:
            st.markdown('<i class="fas fa-paw" style="font-size: 3rem; color: #667eea;"></i>', unsafe_allow_html=True)
    else:
        st.markdown('<i class="fas fa-paw" style="font-size: 3rem; color: #667eea;"></i>', unsafe_allow_html=True)
    
    st.markdown('''
            </div>
            <div class="logo-text">PawAlert</div>
        </div>
        <div class="nav-right">''', unsafe_allow_html=True)
    
    # Navigation Icons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("", key="status_nav_btn", help="View Status"):
            st.session_state.current_page = 'status'
            st.session_state.show_chat = False
            st.rerun()
        st.markdown('<i class="fas fa-chart-line nav-icon"></i>', unsafe_allow_html=True)
    
    with col2:
        if st.button(" ", key="ai_nav_btn", help="AI Assistant"):
            st.session_state.show_chat = True
            st.session_state.current_page = 'chat'
            st.rerun()
        st.markdown('<i class="fas fa-robot nav-icon"></i>', unsafe_allow_html=True)
    
    with col3:
        if os.path.exists("default.png"):
            try:
                st.image("default.png", width=55)
            except:
                st.markdown('<i class="fas fa-user-circle nav-icon"></i>', unsafe_allow_html=True)
        else:
            st.markdown('<i class="fas fa-user-circle nav-icon"></i>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

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
        # Floating AI Button only on home page
        render_ai_button()

if __name__ == "__main__":
    main()
