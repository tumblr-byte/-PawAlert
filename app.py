import streamlit as st
import base64
import json
import random
from datetime import datetime
import requests

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

# Function to call Groq API directly
def call_groq_api(prompt):
    """Call Groq API using requests"""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error calling Groq API: {e}")
        return None

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

    result = call_groq_api(prompt)
    if result:
        try:
            result = result.strip()
            if result.startswith("```json"):
                result = result[7:]
            if result.endswith("```"):
                result = result[:-3]
            return json.loads(result.strip())
        except:
            return None
    return None

def generate_abuse_case(abuse_type, location, description):
    """Generate abuse case with Groq AI"""
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

    result = call_groq_api(prompt)
    if result:
        try:
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
        except:
            return None
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
    
    /* Hide default buttons */
    div[data-testid="column"]:nth-child(2) button,
    div[data-testid="column"]:nth-child(3) button {
        display: none;
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
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(226, 169, 241, 0.3);
        margin: 20px 0;
    }
    
    .welcome-box {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border-left: 6px solid #e2a9f1;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .form-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 20px 0;
    }
    
    .hospital-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 5px solid #e2a9f1;
        transition: transform 0.3s ease;
    }
    
    .hospital-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(226, 169, 241, 0.3);
    }
    
    .case-card {
        background: linear-gradient(135deg, #fff5f5 0%, #fff0f8 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 6px solid #e2a9f1;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .case-card:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 20px rgba(226, 169, 241, 0.3);
    }
    
    .status-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 600;
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
    
    /* Beautiful form styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2a9f1;
        padding: 12px;
        font-size: 16px;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e2a9f1;
        padding: 12px;
        font-size: 16px;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e2a9f1;
    }
    
    .stButton > button {
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(226, 169, 241, 0.4);
    }
    </style>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Navigation Bar
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo-img">' if logo_base64 else '<div style="width:60px;height:60px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;">🐾</div>'
profile_html = f'<img src="data:image/png;base64,{default_base64}" alt="Profile" class="profile-img">' if default_base64 else '<div style="width:50px;height:50px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;">👤</div>'

# Buttons for functionality
col1, col2, col3 = st.columns([6, 1, 1])

with col2:
    if st.button("status_btn", key="status_button"):
        st.session_state.show_status = not st.session_state.show_status
        st.session_state.show_chatbot = False
        st.rerun()

with col3:
    if st.button("ai_btn", key="ai_button"):
        st.session_state.show_chatbot = not st.session_state.show_chatbot
        st.session_state.show_status = False
        st.rerun()

with col1:
    st.markdown(f"""
        <div class="nav-container">
            <div class="nav-left">
                {logo_html}
                <div class="brand-name">PawAlert</div>
            </div>
            <div class="nav-right">
                <i class="fas fa-chart-line nav-icon" title="Status" onclick="document.querySelectorAll('button')[0].click()"></i>
                <i class="fas fa-robot nav-icon" title="AI Assistant" onclick="document.querySelectorAll('button')[1].click()"></i>
                {profile_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Status Panel
if st.session_state.show_status:
    st.markdown("### <i class='fas fa-chart-bar' style='color: #e2a9f1;'></i> Case Status Dashboard", unsafe_allow_html=True)
    
    if len(st.session_state.cases) == 0:
        st.info("No cases filed yet. Use AI Sathi to report incidents.")
    else:
        for idx, case in enumerate(st.session_state.cases):
            with st.expander(f"Case {idx + 1}: {case.get('case_title', 'Case Details')}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**<i class='fas fa-id-card'></i> Case ID:** {case['case_id']}", unsafe_allow_html=True)
                    st.markdown(f"**<i class='fas fa-calendar'></i> Date:** {case['date']}", unsafe_allow_html=True)
                    st.markdown(f"**<i class='fas fa-map-marker-alt'></i> Location:** {case['location']}", unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<span class="status-badge status-reported">{case["status"]}</span>', unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"**Complaint:** {case.get('formal_complaint', 'N/A')}")
                st.markdown(f"**Recommended Action:** {case.get('recommended_action', 'N/A')}")
                st.markdown(f"**<i class='fas fa-exclamation-circle'></i> Urgency:** {case.get('urgency_level', 'N/A')}", unsafe_allow_html=True)
                
                if st.button(f"Inform Police", key=f"police_{idx}", type="primary"):
                    st.success("Police have been notified! Case forwarded to authorities.")
                    st.session_state.cases[idx]['status'] = 'Under Investigation'

# AI Chatbot Panel
if st.session_state.show_chatbot:
    st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="welcome-box">
            <h2 style="color: #e2a9f1; margin: 0;"><i class="fas fa-robot"></i> Hello! Welcome</h2>
            <p style="color: #666; margin: 10px 0 0 0; font-size: 18px;">I am your <strong>AI Sathi</strong>, here to help rescue and protect animals in need. 
            Report injuries or file abuse complaints, and I'll assist you immediately!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Inquiry Type Selection
    inquiry_type = st.radio(
        "**<i class='fas fa-clipboard-list' style='color: #e2a9f1;'></i> Select Inquiry Type:**",
        ["Animal Injury", "Animal Abuse"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if inquiry_type == "Animal Injury":
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("### <i class='fas fa-hospital' style='color: #e2a9f1;'></i> Report Animal Injury", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            animal_type = st.text_input("<i class='fas fa-paw'></i> Animal Type", placeholder="e.g., Dog, Cat, Bird...", key="animal_type")
            location = st.selectbox(
                "<i class='fas fa-map-marker-alt'></i> Location",
                ["Current Location (GPS)", "Sector 12, Nearby Park", "Main Road, City Center", "Industrial Area, Zone 5"]
            )
        
        with col2:
            description = st.text_area("<i class='fas fa-file-alt'></i> Description", placeholder="Describe the injury in detail...", height=100)
            media_file = st.file_uploader("<i class='fas fa-camera'></i> Upload Image/Video (Optional)", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("<i class='fas fa-search'></i> Analyze Injury", type="primary", use_container_width=True):
            if animal_type and description:
                with st.spinner("AI Sathi is analyzing..."):
                    analysis = analyze_injury_with_groq(animal_type, description, location)
                    
                    if analysis:
                        st.success("Analysis Complete!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**<i class='fas fa-paw'></i> Animal:** {analysis.get('animal_confirmed', animal_type)}")
                            st.markdown(f"**<i class='fas fa-chart-bar'></i> Severity:** `{analysis.get('severity', 'Unknown')}`")
                        with col2:
                            st.markdown(f"**<i class='fas fa-info-circle'></i> What Happened:** {analysis.get('injury_analysis', 'Analysis in progress')}")
                        
                        st.markdown("### <i class='fas fa-lightbulb' style='color: #e2a9f1;'></i> Immediate Suggestions:")
                        suggestions = analysis.get('immediate_suggestions', [])
                        for i, sug in enumerate(suggestions, 1):
                            st.markdown(f"{i}. {sug}")
                        
                        st.markdown("---")
                        st.markdown("### <i class='fas fa-hospital-alt' style='color: #e2a9f1;'></i> Recommended Veterinary Hospitals:", unsafe_allow_html=True)
                        
                        selected_hospitals = random.sample(HOSPITALS, 3)
                        
                        for hospital in selected_hospitals:
                            st.markdown(f"""
                                <div class="hospital-card">
                                    <h4 style="color: #e2a9f1; margin: 0 0 15px 0;"><i class="fas fa-hospital"></i> {hospital['name']}</h4>
                                    <p style="margin: 8px 0;"><strong><i class="fas fa-map-marker-alt"></i> Location:</strong> {hospital['location']}</p>
                                    <p style="margin: 8px 0;"><strong><i class="fas fa-stethoscope"></i> Speciality:</strong> {hospital['speciality']}</p>
                                    <p style="margin: 8px 0;"><strong><i class="fas fa-clock"></i> Availability:</strong> {hospital['availability']}</p>
                                    <p style="margin: 8px 0;"><strong><i class="fas fa-rupee-sign"></i> Price Range:</strong> {hospital['price']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"<i class='fas fa-ambulance'></i> Call Ambulance - {hospital['name']}", key=f"ambulance_{hospital['name']}", type="secondary"):
                                st.success(f"Ambulance dispatched from {hospital['name']}! ETA: 15-20 minutes")
            else:
                st.warning("Please fill in all required fields!")
    
    else:  # Animal Abuse
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("### <i class='fas fa-exclamation-triangle' style='color: #e2a9f1;'></i> File Animal Abuse Complaint", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            abuse_type = st.selectbox(
                "<i class='fas fa-list'></i> Type of Abuse",
                ["Physical Abuse", "Neglect", "Abandonment", "Illegal Trade", "Cruelty", "Other"]
            )
            location = st.selectbox(
                "<i class='fas fa-map-marker-alt'></i> Location",
                ["Current Location (GPS)", "Sector 12, Nearby Park", "Main Road, City Center", "Industrial Area, Zone 5"]
            )
        
        with col2:
            description = st.text_area("<i class='fas fa-file-alt'></i> Detailed Description", placeholder="Describe the incident in detail...", height=100)
            abuse_media = st.file_uploader("<i class='fas fa-camera'></i> Upload Evidence (Optional)", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("<i class='fas fa-file-signature'></i> File Complaint", type="primary", use_container_width=True):
            if abuse_type and description:
                with st.spinner("AI Sathi is preparing your complaint..."):
                    case = generate_abuse_case(abuse_type, location, description)
                    
                    if case:
                        st.session_state.cases.append(case)
                        
                        st.success("Complaint Filed Successfully!")
                        
                        st.markdown(f"""
                            <div class="case-card">
                                <h3 style="color: #e2a9f1; margin: 0 0 20px 0;"><i class="fas fa-file-alt"></i> {case['case_title']}</h3>
                                <p style="margin: 10px 0;"><strong><i class="fas fa-id-card"></i> Case ID:</strong> {case['case_id']}</p>
                                <p style="margin: 10px 0;"><strong><i class="fas fa-calendar"></i> Date:</strong> {case['date']}</p>
                                <p style="margin: 10px 0;"><strong><i class="fas fa-map-marker-alt"></i> Location:</strong> {case['location']}</p>
                                <p style="margin: 10px 0;"><strong><i class="fas fa-exclamation-circle"></i> Urgency:</strong> <span style="color: #d32f2f; font-weight: 700;">{case['urgency_level']}</span></p>
                                <hr style="margin: 20px 0;">
                                <p style="margin: 10px 0;"><strong>Complaint:</strong> {case['formal_complaint']}</p>
                                <p style="margin: 10px 0;"><strong>Recommended Action:</strong> {case['recommended_action']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("<i class='fas fa-police'></i> Inform Police Now", key="inform_police_main", type="primary"):
                            st.success("Police have been notified! Authorities will investigate the case.")
                            st.balloons()
            else:
                st.warning("Please fill in all required fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Body
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
                    <h2 style="color: white; font-size: 48px;"><i class="fas fa-paw"></i></h2>
                    <p style="color: white; font-size: 18px;">Click the <i class="fas fa-robot"></i> AI Assistant to get started!</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
