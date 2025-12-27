import streamlit as st
import base64
import json
import random
from datetime import datetime
from groq import Groq

# Page config
st.set_page_config(
    page_title="PawAlert",
    page_icon="🐾",
    layout="wide"
)

# Initialize session state
if 'show_chatbot' not in st.session_state:
    st.session_state.show_chatbot = False
if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'show_status' not in st.session_state:
    st.session_state.show_status = False

# Initialize Groq client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("⚠️ Groq API key not found in secrets!")
    client = None

# Function to convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Get base64 images
logo_base64 = get_base64_image("logo.png")
default_base64 = get_base64_image("default.png")

# Sample hospitals data
HOSPITALS = [
    {"name": "City Animal Hospital", "location": "Downtown, 2.3 km", "speciality": "Emergency & Surgery", "availability": "24/7", "price": "₹500-2000"},
    {"name": "Pet Care Veterinary Clinic", "location": "North Zone, 3.1 km", "speciality": "General Care", "availability": "9 AM - 9 PM", "price": "₹300-1500"},
    {"name": "Advanced Pet Medical Center", "location": "East Side, 4.5 km", "speciality": "Critical Care", "availability": "24/7", "price": "₹800-3000"},
    {"name": "Green Valley Animal Hospital", "location": "West End, 5.2 km", "speciality": "Wildlife & Exotic", "availability": "8 AM - 8 PM", "price": "₹600-2500"},
    {"name": "Compassion Vet Clinic", "location": "South Area, 3.8 km", "speciality": "Emergency Care", "availability": "24/7", "price": "₹400-1800"},
]

def analyze_injury_with_groq(animal_type, description, location):
    """Analyze injury using Groq AI"""
    if not client:
        return None
    
    prompt = f"""You are a veterinary AI assistant. Analyze this animal injury case:
    
Animal Type: {animal_type}
Location: {location}
Description: {description}

Provide a JSON response with:
1. animal_confirmed: confirmed animal type
2. injury_analysis: what likely happened
3. severity: Low/Medium/High/Critical
4. immediate_suggestions: list of 3-4 immediate care suggestions

Format as valid JSON only."""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=500
        )
        result = response.choices[0].message.content
        # Try to parse JSON
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]
        return json.loads(result.strip())
    except Exception as e:
        st.error(f"AI Analysis Error: {e}")
        return None

def generate_abuse_case(abuse_type, location, description):
    """Generate abuse case with Groq AI"""
    if not client:
        return None
    
    case_id = f"PA-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    prompt = f"""You are a legal AI assistant. Generate an animal abuse complaint report:

Case ID: {case_id}
Abuse Type: {abuse_type}
Location: {location}
Description: {description}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Provide a JSON response with:
1. case_title: brief title for the case
2. formal_complaint: professional complaint text (2-3 sentences)
3. recommended_action: what authorities should do
4. urgency_level: Low/Medium/High/Critical

Format as valid JSON only."""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=500
        )
        result = response.choices[0].message.content
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]
        analysis = json.loads(result.strip())
        analysis['case_id'] = case_id
        analysis['date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        analysis['location'] = location
        analysis['status'] = 'Reported'
        return analysis
    except Exception as e:
        st.error(f"Case Generation Error: {e}")
        return None

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: white;
    }
    
    .nav-container {
        background: linear-gradient(135deg, #e2a9f1 0%, #d896ea 100%);
        padding: 20px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .logo-img {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid white;
    }
    
    .brand-name {
        color: white;
        font-size: 32px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 30px;
    }
    
    .nav-icon {
        color: white;
        font-size: 28px;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    
    .nav-icon:hover {
        transform: scale(1.2);
    }
    
    .profile-img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid white;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .profile-img:hover {
        transform: scale(1.1);
    }
    
    .body-container {
        text-align: center;
        padding: 50px 20px;
        background-color: white;
    }
    
    .hero-text {
        color: #e2a9f1;
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        color: #666;
        font-size: 20px;
        font-weight: 400;
        margin-bottom: 40px;
    }
    
    .chatbot-container {
        background: linear-gradient(135deg, #f5f0ff 0%, #fff0f8 100%);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .welcome-box {
        background: white;
        padding: 25px;
        border-radius: 10px;
        border-left: 5px solid #e2a9f1;
        margin-bottom: 20px;
    }
    
    .hospital-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 4px solid #e2a9f1;
    }
    
    .case-card {
        background: linear-gradient(135deg, #fff5f5 0%, #fff0f8 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 5px solid #e2a9f1;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .case-card:hover {
        transform: translateX(5px);
    }
    
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 14px;
    }
    
    .status-reported {
        background: #fff3cd;
        color: #856404;
    }
    
    .status-investigating {
        background: #cfe2ff;
        color: #084298;
    }
    
    .status-resolved {
        background: #d1e7dd;
        color: #0f5132;
    }
    </style>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Navigation Bar
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo-img">' if logo_base64 else '<div style="width:60px;height:60px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;">🐾</div>'
profile_html = f'<img src="data:image/png;base64,{default_base64}" alt="Profile" class="profile-img">' if default_base64 else '<div style="width:50px;height:50px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;">👤</div>'

# Create columns for navigation
nav_col1, nav_col2, nav_col3 = st.columns([8, 1, 1])

with nav_col1:
    st.markdown(f"""
        <div class="nav-container">
            <div class="nav-left">
                {logo_html}
                <div class="brand-name">PawAlert</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with nav_col2:
    if st.button("📊", key="status_btn", help="View Status"):
        st.session_state.show_status = not st.session_state.show_status
        st.session_state.show_chatbot = False

with nav_col3:
    if st.button("🤖", key="ai_btn", help="AI Assistant"):
        st.session_state.show_chatbot = not st.session_state.show_chatbot
        st.session_state.show_status = False

# Status Panel
if st.session_state.show_status:
    st.markdown("### 📊 Case Status Dashboard")
    
    if len(st.session_state.cases) == 0:
        st.info("🔍 No cases filed yet. Use AI Sathi to report incidents.")
    else:
        for idx, case in enumerate(st.session_state.cases):
            with st.expander(f"📋 Case {idx + 1}: {case.get('case_title', 'Case Details')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**Case ID:** {case['case_id']}")
                    st.markdown(f"**Date:** {case['date']}")
                    st.markdown(f"**Location:** {case['location']}")
                with col2:
                    st.markdown(f'<span class="status-badge status-reported">{case["status"]}</span>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"**Complaint:** {case.get('formal_complaint', 'N/A')}")
                st.markdown(f"**Recommended Action:** {case.get('recommended_action', 'N/A')}")
                st.markdown(f"**Urgency:** {case.get('urgency_level', 'N/A')}")
                
                if st.button(f"🚔 Inform Police", key=f"police_{idx}"):
                    st.success("✅ Police have been notified! Case forwarded to authorities.")
                    st.session_state.cases[idx]['status'] = 'Under Investigation'

# AI Chatbot Panel
if st.session_state.show_chatbot:
    st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="welcome-box">
            <h2 style="color: #e2a9f1; margin: 0;">👋 Hello! Welcome</h2>
            <p style="color: #666; margin: 10px 0 0 0;">I am your <strong>AI Sathi</strong> 🤖, here to help rescue and protect animals in need. 
            Report injuries or file abuse complaints, and I'll assist you immediately!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Inquiry Type Selection
    inquiry_type = st.radio(
        "📝 **Select Inquiry Type:**",
        ["🏥 Animal Injury", "⚠️ Animal Abuse"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if inquiry_type == "🏥 Animal Injury":
        st.markdown("### 🏥 Report Animal Injury")
        
        col1, col2 = st.columns(2)
        
        with col1:
            animal_type = st.text_input("🐾 Animal Type", placeholder="e.g., Dog, Cat, Bird...")
            location = st.selectbox(
                "📍 Location",
                ["Current Location (GPS)", "Sector 12, Nearby Park", "Main Road, City Center", "Industrial Area, Zone 5"]
            )
        
        with col2:
            description = st.text_area("📋 Description", placeholder="Describe the injury in detail...")
            media_file = st.file_uploader("📸 Upload Image/Video (Optional)", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
        
        if st.button("🔍 Analyze Injury", type="primary", use_container_width=True):
            if animal_type and description:
                with st.spinner("🤖 AI Sathi is analyzing..."):
                    analysis = analyze_injury_with_groq(animal_type, description, location)
                    
                    if analysis:
                        st.success("✅ Analysis Complete!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**🐾 Animal:** {analysis.get('animal_confirmed', animal_type)}")
                            st.markdown(f"**📊 Severity:** `{analysis.get('severity', 'Unknown')}`")
                        with col2:
                            st.markdown(f"**🔍 What Happened:** {analysis.get('injury_analysis', 'Analysis in progress')}")
                        
                        st.markdown("### 💡 Immediate Suggestions:")
                        suggestions = analysis.get('immediate_suggestions', [])
                        for i, sug in enumerate(suggestions, 1):
                            st.markdown(f"{i}. {sug}")
                        
                        st.markdown("---")
                        st.markdown("### 🏥 Recommended Veterinary Hospitals:")
                        
                        selected_hospitals = random.sample(HOSPITALS, 3)
                        
                        for hospital in selected_hospitals:
                            st.markdown(f"""
                                <div class="hospital-card">
                                    <h4 style="color: #e2a9f1; margin: 0 0 10px 0;">🏥 {hospital['name']}</h4>
                                    <p style="margin: 5px 0;"><strong>📍 Location:</strong> {hospital['location']}</p>
                                    <p style="margin: 5px 0;"><strong>⚕️ Speciality:</strong> {hospital['speciality']}</p>
                                    <p style="margin: 5px 0;"><strong>🕐 Availability:</strong> {hospital['availability']}</p>
                                    <p style="margin: 5px 0;"><strong>💰 Price Range:</strong> {hospital['price']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"🚑 Call Ambulance - {hospital['name']}", key=f"ambulance_{hospital['name']}"):
                                st.success(f"🚑 Ambulance dispatched from {hospital['name']}! ETA: 15-20 minutes")
            else:
                st.warning("⚠️ Please fill in all required fields!")
    
    else:  # Animal Abuse
        st.markdown("### ⚠️ File Animal Abuse Complaint")
        
        col1, col2 = st.columns(2)
        
        with col1:
            abuse_type = st.selectbox(
                "⚠️ Type of Abuse",
                ["Physical Abuse", "Neglect", "Abandonment", "Illegal Trade", "Cruelty", "Other"]
            )
            location = st.selectbox(
                "📍 Location",
                ["Current Location (GPS)", "Sector 12, Nearby Park", "Main Road, City Center", "Industrial Area, Zone 5"]
            )
        
        with col2:
            description = st.text_area("📋 Detailed Description", placeholder="Describe the incident in detail...")
            abuse_media = st.file_uploader("📸 Upload Evidence (Optional)", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
        
        if st.button("📝 File Complaint", type="primary", use_container_width=True):
            if abuse_type and description:
                with st.spinner("🤖 AI Sathi is preparing your complaint..."):
                    case = generate_abuse_case(abuse_type, location, description)
                    
                    if case:
                        st.session_state.cases.append(case)
                        
                        st.success("✅ Complaint Filed Successfully!")
                        
                        st.markdown(f"""
                            <div class="case-card">
                                <h3 style="color: #e2a9f1; margin: 0 0 15px 0;">📋 {case['case_title']}</h3>
                                <p><strong>🆔 Case ID:</strong> {case['case_id']}</p>
                                <p><strong>📅 Date:</strong> {case['date']}</p>
                                <p><strong>📍 Location:</strong> {case['location']}</p>
                                <p><strong>⚠️ Urgency:</strong> <span style="color: #d32f2f; font-weight: 600;">{case['urgency_level']}</span></p>
                                <hr>
                                <p><strong>Complaint:</strong> {case['formal_complaint']}</p>
                                <p><strong>Recommended Action:</strong> {case['recommended_action']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("🚔 Inform Police Now", key="inform_police_main"):
                            st.success("✅ Police have been notified! Authorities will investigate the case.")
                            st.balloons()
            else:
                st.warning("⚠️ Please fill in all required fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Body (only show if chatbot is not active)
if not st.session_state.show_chatbot and not st.session_state.show_status:
    st.markdown('<div class="body-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="hero-text">Rescue & Protect Animals in Need</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Report animal injuries and abuse to save lives</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("main.png", use_column_width=True)
        except:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #e2a9f1 0%, #d896ea 100%); 
                            padding: 100px; border-radius: 20px; text-align: center;">
                    <h2 style="color: white; font-size: 48px;">🐾</h2>
                    <p style="color: white;">Click the 🤖 AI Assistant to get started!</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
