import streamlit as st
from groq import Groq
import json
from datetime import datetime
import time
import base64

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

# Custom CSS
st.markdown("""
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Main background */
    .stApp {
        background-color: #FAF9F6;
    }
    
    /* Navigation Bar */
    .navbar {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        padding: 1.2rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(226, 169, 241, 0.3);
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: white;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .nav-logo img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: white;
        padding: 5px;
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .nav-item {
        color: white;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s;
        background: rgba(255, 255, 255, 0.2);
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    .user-profile {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        border: 3px solid white;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #F5EEFA 0%, white 100%);
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(226, 169, 241, 0.2);
    }
    
    .hero-title {
        color: #4A4459;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        color: #4A4459;
        font-size: 1.3rem;
        opacity: 0.8;
        margin-bottom: 2rem;
    }
    
    .hero-image {
        max-width: 600px;
        width: 100%;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }
    
    /* AI Chat Button */
    .ai-button-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    
    .ai-chat-button {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 6px 25px rgba(226, 169, 241, 0.5);
        transition: all 0.3s;
        animation: pulse 2s infinite;
    }
    
    .ai-chat-button:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 35px rgba(226, 169, 241, 0.7);
    }
    
    .ai-chat-button img {
        width: 45px;
        height: 45px;
        border-radius: 50%;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 6px 25px rgba(226, 169, 241, 0.5);
        }
        50% {
            box-shadow: 0 6px 40px rgba(226, 169, 241, 0.8);
        }
    }
    
    /* Chat Interface */
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: 2rem auto;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .chat-message.user {
        background: #F5EEFA;
        margin-left: 20%;
    }
    
    .chat-message.assistant {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        color: white;
        margin-right: 20%;
    }
    
    /* Report Form */
    .report-form {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .form-section {
        margin: 1.5rem 0;
    }
    
    .form-label {
        color: #4A4459;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* Ambulance Button */
    .ambulance-button {
        background: linear-gradient(135deg, #FFB4A2 0%, #FF9B87 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(255, 180, 162, 0.4);
        transition: all 0.3s;
        animation: glow 2s infinite;
    }
    
    .ambulance-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 30px rgba(255, 180, 162, 0.6);
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 4px 20px rgba(255, 180, 162, 0.4);
        }
        50% {
            box-shadow: 0 6px 35px rgba(255, 180, 162, 0.7);
        }
    }
    
    /* Case Cards */
    .case-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #e2a9f1;
    }
    
    .case-id {
        color: #e2a9f1;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .case-status {
        background: #A8C9A5;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    /* Vet Cards */
    .vet-card {
        background: linear-gradient(135deg, #F5EEFA 0%, white 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(226, 169, 241, 0.2);
        border: 2px solid #e2a9f1;
    }
    
    .vet-name {
        color: #4A4459;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .vet-detail {
        color: #4A4459;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .vet-tag {
        background: #A8C9A5;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
    }
    
    /* Success Messages */
    .success-message {
        background: linear-gradient(135deg, #A8C9A5 0%, #95B892 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(168, 201, 165, 0.3);
    }
    
    /* No Cases Image */
    .no-cases-container {
        text-align: center;
        padding: 3rem;
    }
    
    .no-cases-image {
        max-width: 400px;
        width: 100%;
        opacity: 0.7;
        margin-bottom: 1rem;
    }
    
    .no-cases-text {
        color: #4A4459;
        font-size: 1.3rem;
        opacity: 0.8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(226, 169, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(226, 169, 241, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Helper function to display images
def get_image_placeholder(image_name, alt_text):
    """Returns HTML for image placeholder"""
    return f'<div style="background: #e2a9f1; color: white; padding: 20px; border-radius: 10px; text-align: center; font-weight: bold;">{alt_text}<br><small>({image_name})</small></div>'

# Navigation Bar
def render_navbar():
    st.markdown(f"""
    <div class="navbar">
        <div class="nav-logo">
            {get_image_placeholder('logo.png', '🐾')}
            <span>PawAlert</span>
        </div>
        <div class="nav-right">
            <div class="nav-item" onclick="window.location.reload();">
                <i class="fas fa-home"></i> Home
            </div>
            {get_image_placeholder('default.png', '👤')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# AI Chat Button (Floating)
def render_ai_button():
    st.markdown(f"""
    <div class="ai-button-container">
        <div class="ai-chat-button" onclick="document.getElementById('chat-trigger').click();">
            {get_image_placeholder('ai.png', '🤖')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Groq API Setup
def get_groq_client():
    # Replace with your actual API key
    api_key = st.secrets.get("GROQ_API_KEY", "your-groq-api-key-here")
    return Groq(api_key=api_key)

# Vet Database (7 vets for Delhi/Ghaziabad region)
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
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🐾 Every Life Matters</h1>
        <p class="hero-subtitle">Report animal injuries and abuse. Get instant AI-powered vet recommendations and emergency response.</p>
    """, unsafe_allow_html=True)
    
    # Placeholder for main.png
    st.markdown(get_image_placeholder('main.png', '🌟 Beautiful Hero Image - Happy rescued animals'), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # How it Works Section
    st.markdown("### 🚀 How PawAlert Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #F5EEFA; border-radius: 15px; margin: 1rem 0;">
            <div style="font-size: 3rem;">📸</div>
            <h3 style="color: #4A4459;">Report</h3>
            <p style="color: #4A4459; opacity: 0.8;">Click the AI button, describe the situation, and upload photos/videos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #F5EEFA; border-radius: 15px; margin: 1rem 0;">
            <div style="font-size: 3rem;">🤖</div>
            <h3 style="color: #4A4459;">AI Analysis</h3>
            <p style="color: #4A4459; opacity: 0.8;">Our AI suggests the best veterinary care nearby</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #F5EEFA; border-radius: 15px; margin: 1rem 0;">
            <div style="font-size: 3rem;">🚑</div>
            <h3 style="color: #4A4459;">Rescue</h3>
            <p style="color: #4A4459; opacity: 0.8;">Dispatch ambulance and track your case status</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Impact Stats
    st.markdown("### 💜 Our Impact")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%); border-radius: 15px; color: white;">
            <h2>1,247</h2>
            <p>Animals Rescued</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #A8C9A5 0%, #95B892 100%); border-radius: 15px; color: white;">
            <h2>324</h2>
            <p>Active Cases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #FFB4A2 0%, #FF9B87 100%); border-radius: 15px; color: white;">
            <h2>847</h2>
            <p>Community Heroes</p>
        </div>
        """, unsafe_allow_html=True)

# Chat Interface
def render_chat():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI Assistant - Report Animal Emergency")
    
    # Chat Messages
    for msg in st.session_state.chat_messages:
        role_class = "user" if msg["role"] == "user" else "assistant"
        st.markdown(f'<div class="chat-message {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Initial greeting
    if len(st.session_state.chat_messages) == 0:
        st.markdown('''
        <div class="chat-message assistant">
            🐾 Hello! I'm here to help you report an animal emergency.<br><br>
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
        st.markdown("### 📝 Fill Report Details")
        
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
                        # Get AI suggestions
                        vet_suggestions = get_vet_suggestions(location, issue_desc, severity, report_type)
                        
                        # Generate Case ID
                        case_id = generate_case_id()
                        
                        # Save case
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
            <h2>✅ Report Submitted Successfully!</h2>
            <h3>Case ID: {latest_case['case_id']}</h3>
            <p>🐾 Your report is helping an animal in need</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🏥 Recommended Veterinary Care")
        st.markdown(latest_case['vet_suggestions'])
        
        st.markdown("---")
        
        # Ambulance Dispatch Button
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
    st.markdown("### 📊 Case Status Tracker")
    
    if len(st.session_state.cases) == 0:
        st.markdown('<div class="no-cases-container">', unsafe_allow_html=True)
        st.markdown(get_image_placeholder('image1.png', '📭 No Cases Yet'), unsafe_allow_html=True)
        st.markdown('<p class="no-cases-text">No cases are created yet.<br>Click the AI button to report an emergency.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        for case in reversed(st.session_state.cases):
            st.markdown(f"""
            <div class="case-card">
                <div class="case-id">🐾 {case['case_id']}</div>
                <div style="margin-top: 0.5rem;">
                    <strong>Type:</strong> {case['type']}<br>
                    <strong>Animal:</strong> {case['animal_type']}<br>
                    <strong>Location:</strong> {case['location']}<br>
                    <strong>Severity:</strong> {case['severity']}<br>
                    <strong>Time:</strong> {case['timestamp']}<br>
                    <strong>Description:</strong> {case['description']}
                </div>
                <div class="case-status">✅ {case['status']}</div>
            </div>
            """, unsafe_allow_html=True)

# Main App Logic
def main():
    render_navbar()
    
    # Page Navigation
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("📊 Status", key="status_nav"):
            st.session_state.current_page = 'status'
            st.rerun()
    
    # Hidden button for chat trigger
    if st.button("Open Chat", key="chat-trigger", type="primary"):
        st.session_state.show_chat = True
        st.rerun()
    
    # Show appropriate page
    if st.session_state.show_chat:
        render_chat()
    elif st.session_state.current_page == 'status':
        render_status()
        if st.button("🏠 Back to Home"):
            st.session_state.current_page = 'home'
            st.rerun()
    else:
        render_home()
    
    # Floating AI Button
    render_ai_button()

if __name__ == "__main__":
    main()
