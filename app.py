import streamlit as st
from datetime import datetime
import base64
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="PawAlert - Animal Welfare & Rescue",
    page_icon="🐾",
    layout="wide"
)

# Initialize Groq client
try:
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    else:
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY not found!")
        st.stop()
    
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.stop()

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    * { font-family: 'Poppins', sans-serif; }
    .main { background: linear-gradient(135deg, #fef5ff 0%, #f9e7ff 100%); }
    .stButton>button {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        color: #4a0e4e; font-weight: 600; border: none; border-radius: 12px;
        padding: 12px 28px; font-size: 16px; transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(226, 169, 241, 0.3);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(226, 169, 241, 0.5); }
    h1, h2, h3 { color: #6b1e6f; }
    .header-container {
        text-align: center; padding: 20px;
        background: linear-gradient(135deg, #e2a9f1 0%, #f5d4ff 100%);
        border-radius: 20px; margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(226, 169, 241, 0.4);
    }
    .icon-button {
        background: white; padding: 20px; border-radius: 15px;
        text-align: center; cursor: pointer; transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 3px solid #e2a9f1;
    }
    .icon-button:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(226, 169, 241, 0.4); }
    .case-card {
        background: white; padding: 25px; border-radius: 15px;
        border-left: 5px solid #e2a9f1; margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #d4f5e9 0%, #a8e6cf 100%);
        padding: 20px; border-radius: 12px; border-left: 5px solid #4caf50; margin: 20px 0;
    }
    .hospital-card {
        background: white; padding: 20px; border-radius: 12px;
        margin: 10px 0; border: 2px solid #e2a9f1; transition: all 0.3s;
    }
    .hospital-card:hover { transform: translateX(5px); box-shadow: 0 6px 20px rgba(226, 169, 241, 0.3); }
    .status-badge {
        display: inline-block; padding: 8px 16px; border-radius: 20px;
        font-weight: 600; font-size: 14px; background: #e2a9f1; color: #4a0e4e;
    }
    .chat-container {
        background: white; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 20px 0;
        max-height: 500px; overflow-y: auto;
    }
    .chat-message { padding: 12px 18px; border-radius: 12px; margin: 10px 0; }
    .user-message { background: #f3e5f5; color: #4a0e4e; margin-left: 20%; }
    .bot-message { background: #e2a9f1; color: #4a0e4e; margin-right: 20%; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        border: 2px solid #e2a9f1; border-radius: 10px; color: #4a0e4e;
    }
    label { color: #6b1e6f !important; font-weight: 600 !important; }
    .stFileUploader { border: 2px dashed #e2a9f1; border-radius: 10px; padding: 10px; }
    .dispatch-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 25px; border-radius: 15px; border-left: 5px solid #ff9800;
        margin: 20px 0; box-shadow: 0 6px 20px rgba(255, 152, 0, 0.3);
    }
    .police-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 25px; border-radius: 15px; border-left: 5px solid #2196f3;
        margin: 20px 0; box-shadow: 0 6px 20px rgba(33, 150, 243, 0.3);
    }
    .detail-row {
        display: flex; justify-content: space-between; padding: 12px 0;
        border-bottom: 1px solid #e2a9f1;
    }
    .detail-label { font-weight: 600; color: #6b1e6f; }
    .detail-value { color: #4a0e4e; }
    .image-container {
        text-align: center; margin: 20px 0;
        border: 3px solid #e2a9f1; border-radius: 15px;
        padding: 10px; background: white;
    }

    .stExpander {
        background: white; border: 2px solid #e2a9f1; border-radius: 12px;
        margin: 15px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stExpander summary {
        color: #4a0e4e !important; font-weight: 600 !important;
        font-size: 16px !important; padding: 15px !important;
        background: linear-gradient(135deg, #f9e7ff 0%, #fef5ff 100%) !important;
        border-radius: 10px !important;
    }
    .stExpander summary:hover {
        background: linear-gradient(135deg, #e2a9f1 0%, #f5d4ff 100%) !important;
        color: #6b1e6f !important;
    }
    .stExpander[open] summary {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%) !important;
        color: #4a0e4e !important;
        border-bottom: 2px solid #d89fe8;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_case_id' not in st.session_state:
    st.session_state.current_case_id = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_with_groq(prompt, image_data=None):
    try:
        if image_data:
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                    ]
                }],
                max_tokens=1000
            )
        else:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis error: {str(e)}"

def show_header():
    try:
        with open("logo.png", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div class="header-container">
            <img src="data:image/png;base64,{logo_data}" width="120" style="margin-bottom: 15px; border-radius: 50%;">
            <h1 style="margin: 10px 0; color: #4a0e4e;"><i class="fas fa-paw"></i> PawAlert</h1>
            <p style="color: #6b1e6f; font-size: 18px;">Animal Welfare & Rescue Platform</p>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="header-container">
            <h1 style="margin: 10px 0; color: #4a0e4e;"><i class="fas fa-paw"></i> PawAlert</h1>
            <p style="color: #6b1e6f; font-size: 18px;">Animal Welfare & Rescue Platform</p>
        </div>
        """, unsafe_allow_html=True)

def navigate_to(page):
    st.session_state.current_page = page
    st.session_state.processing_complete = False
    st.rerun()

def home_page():
    show_header()
    
    try:
        with open("main.png", "rb") as f:
            main_img = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="text-align: center; margin: 30px 0;">
            <img src="data:image/png;base64,{main_img}" style="max-width: 600px; width: 100%; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: white; border-radius: 20px; margin: 30px 0; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
            <i class="fas fa-heart" style="font-size: 80px; color: #e2a9f1;"></i>
            <h2 style="color: #6b1e6f; margin-top: 20px;">Love & Care for Animals</h2>
            <p style="color: #8e44ad; font-size: 18px;">Together we can make a difference</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #6b1e6f; margin: 30px 0;'>How Can We Help?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="icon-button">
            <i class="fas fa-ambulance" style="font-size: 48px; color: #e2a9f1; margin-bottom: 15px;"></i>
            <h3 style="color: #6b1e6f; margin: 10px 0;">Animal Injury</h3>
            <p style="color: #8e44ad;">Report injured animals</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Report Injury", key="injury_btn", use_container_width=True):
            navigate_to('injury')
    
    with col2:
        st.markdown("""
        <div class="icon-button">
            <i class="fas fa-shield-alt" style="font-size: 48px; color: #e2a9f1; margin-bottom: 15px;"></i>
            <h3 style="color: #6b1e6f; margin: 10px 0;">Animal Abuse</h3>
            <p style="color: #8e44ad;">Report abuse cases</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Report Abuse", key="abuse_btn", use_container_width=True):
            navigate_to('abuse')
    
    with col3:
        st.markdown(f"""
        <div class="icon-button">
            <i class="fas fa-clipboard-list" style="font-size: 48px; color: #e2a9f1; margin-bottom: 15px;"></i>
            <h3 style="color: #6b1e6f; margin: 10px 0;">Case Status</h3>
            <p style="color: #8e44ad;">{len(st.session_state.cases)} cases reported</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Check Status", key="status_btn", use_container_width=True):
            navigate_to('status')
    
    with col4:
        st.markdown("""
        <div class="icon-button">
            <i class="fas fa-robot" style="font-size: 48px; color: #e2a9f1; margin-bottom: 15px;"></i>
            <h3 style="color: #6b1e6f; margin: 10px 0;">AI Sathi</h3>
            <p style="color: #8e44ad;">Chat with AI assistant</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Chat Now", key="chat_btn", use_container_width=True):
            navigate_to('chat')

def injury_page():
    show_header()
    
    if st.button("Back to Home"):
        navigate_to('home')
    
    st.markdown("<h2 style='color: #6b1e6f;'><i class='fas fa-ambulance'></i> Report Animal Injury</h2>", unsafe_allow_html=True)
    
    if st.session_state.processing_complete and len(st.session_state.cases) > 0:
        current_case = st.session_state.cases[-1]
        
        st.markdown(f"""
        <div class="success-box">
            <h3 style="color: #2e7d32; margin-top: 0;"><i class="fas fa-check-circle"></i> Case Registered!</h3>
            <p style="color: #1b5e20; font-size: 18px;"><strong>Case ID: {current_case['id']}</strong></p>
            <p style="color: #2e7d32;">Timestamp: {current_case['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
                  <div class='case-card'>
    <h3 style='color: #6b1e6f;'><i class='fas fa-notes-medical'></i> AI Analysis</h3>
    <div style='color: #4a0e4e; line-height: 1.8; white-space: pre-wrap;'>{current_case['analysis']}</div>
</div>
""", unsafe_allow_html=True)
        
        
        if current_case.get('selected_hospital'):
            hospital = current_case['selected_hospital']
            
            if 'dispatch_message' in current_case:
                st.markdown(f"""
                <div class="dispatch-box">
                    <h2 style="color: #e65100; margin-top: 0;"><i class="fas fa-ambulance"></i> Ambulance Dispatched!</h2>
                    <div class="detail-row">
                        <span class="detail-label">Hospital:</span>
                        <span class="detail-value">{hospital['name']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Speciality:</span>
                        <span class="detail-value">{hospital['speciality']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Hospital Contact:</span>
                        <span class="detail-value">{hospital['contact']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Expected Fees:</span>
                        <span class="detail-value">{hospital['fees']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Location:</span>
                        <span class="detail-value">{hospital['location']}</span>
                    </div>
                    <hr style="border: 1px solid #ff9800; margin: 15px 0;">
                    <div class="detail-row">
                        <span class="detail-label">Driver:</span>
                        <span class="detail-value">{current_case['driver_name']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Driver Contact:</span>
                        <span class="detail-value">{current_case['driver_contact']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
<div class='case-card' style='background: #fff8e1;'>
    <h3 style='color: #f57c00;'><i class='fas fa-hand-holding-heart'></i> What To Do Now</h3>
    <div style='color: #4a0e4e; line-height: 1.8; white-space: pre-wrap;'>{current_case['dispatch_message']}</div>
</div>
""", unsafe_allow_html=True)
               
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Check Detailed Status", use_container_width=True):
                        navigate_to('status')
                with col2:
                    if st.button("Ask AI Anything", use_container_width=True):
                        navigate_to('chat')
            else:
                dispatch_prompt = f"""You are a compassionate emergency dispatcher for animal rescue. An ambulance has been dispatched for an injured {current_case['animal_type']}.

Hospital: {hospital['name']}
Location: {current_case['location']}
Driver: {current_case['driver_name']}
Contact: {current_case['driver_contact']}
Injury: {current_case['description']}

Provide actionable guidance:
1. Help is arriving in 5-15 minutes
2. What to do RIGHT NOW to reduce pain
3. What NOT to do
4. Reassurance

Use bullet points."""
                
                with st.spinner("Getting ambulance details..."):
                    dispatch_message = analyze_with_groq(dispatch_prompt)
                    current_case['dispatch_message'] = dispatch_message
                    st.rerun()
        else:
            st.markdown("<h3 style='color: #6b1e6f;'><i class='fas fa-hospital'></i> Recommended Hospitals</h3>", unsafe_allow_html=True)
            
            for i, hospital in enumerate(current_case['hospitals']):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="hospital-card">
                        <h4 style="color: #6b1e6f; margin-top: 0;">{hospital['name']}</h4>
                        <p style="color: #8e44ad; margin: 5px 0;"><strong>Speciality:</strong> {hospital['speciality']}</p>
                        <p style="color: #8e44ad; margin: 5px 0;"><strong>Contact:</strong> {hospital['contact']}</p>
                        <p style="color: #8e44ad; margin: 5px 0;"><strong>Fees:</strong> {hospital['fees']}</p>
                        <span class="status-badge">{hospital['availability']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Call Ambulance", key=f"amb_{i}"):
                        current_case['selected_hospital'] = hospital
                        current_case['status'] = 'Ambulance Dispatched'
                        st.rerun()
    else:
        with st.form("injury_form"):
            animal_type = st.selectbox("Animal Type", ["Dog", "Cat", "Cow", "Horse", "Bird", "Buffalo", "Goat", "Other"])
            location = st.selectbox("Location", ["Connaught Place, Delhi", "MG Road, Bangalore", "Marine Drive, Mumbai"])
            description = st.text_area("Description of Injury", placeholder="Please describe the injury in detail...")
            uploaded_file = st.file_uploader("Upload Image/Video of Injured Animal", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
            
            submit = st.form_submit_button("Submit Report", use_container_width=True)
            
            if submit:
                if not description:
                    st.error("Please provide a description!")
                elif not uploaded_file:
                    st.error("Please upload an image!")
                else:
                    with st.spinner("Analyzing with AI..."):
                        image_data = encode_image(uploaded_file)
                        prompt = f"""Analyze this animal injury. Animal: {animal_type}, Location: {location}, Description: {description}

Provide:
1. Severity Level (Minor/Moderate/Severe/Critical)
2. Visible Injuries
3. Immediate Care Required
4. Recovery Time

Be concise and professional."""
                        
                        analysis = analyze_with_groq(prompt, image_data)
                        
                        hospitals = [
                            {"name": "PetCare Emergency Hospital", "location": location, "availability": "Available Now", 
                             "contact": "+91 98765-43210", "fees": "₹2,000 - ₹5,000", "speciality": "Emergency & Critical Care"},
                            {"name": "Animal Rescue Veterinary Clinic", "location": location, "availability": "Available in 15 mins", 
                             "contact": "+91 98765-43211", "fees": "₹1,500 - ₹4,000", "speciality": "General Treatment"},
                            {"name": "24/7 Animal Care Center", "location": location, "availability": "Available Now", 
                             "contact": "+91 98765-43212", "fees": "₹2,500 - ₹6,000", "speciality": "Surgery & ICU"}
                        ]
                        
                        case_id = f"INJ{len(st.session_state.cases) + 1001}"
                        case = {
                            "id": case_id, "type": "Injury", "animal_type": animal_type,
                            "location": location, "description": description,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "analysis": analysis, "hospitals": hospitals,
                            "driver_name": "Rajesh Kumar", "driver_contact": "+91 98765-11111",
                            "selected_hospital": None, "status": "Case Registered",
                            "image_data": image_data
                        }
                        
                        st.session_state.cases.append(case)
                        st.session_state.current_case_id = case_id
                        st.session_state.processing_complete = True
                        st.rerun()





def abuse_page():
    show_header()
    
    if st.button("Back to Home"):
        navigate_to('home')
    
    st.markdown("<h2 style='color: #6b1e6f;'><i class='fas fa-shield-alt'></i> Report Animal Abuse</h2>", unsafe_allow_html=True)
    
    if st.session_state.processing_complete and len(st.session_state.cases) > 0:
        current_case = st.session_state.cases[-1]
        
        st.markdown(f"""
        <div class="success-box">
            <h3 style="color: #2e7d32; margin-top: 0;"><i class="fas fa-check-circle"></i> Abuse Case Registered!</h3>
            <p style="color: #1b5e20; font-size: 18px;"><strong>Case ID: {current_case['id']}</strong></p>
            <p style="color: #2e7d32;">Timestamp: {current_case['timestamp']}</p>
            <p style="color: #2e7d32;">Culprit Photo: {current_case['culprit_photo']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
<div class='case-card'>
    <h3 style='color: #6b1e6f;'><i class='fas fa-gavel'></i> AI Analysis</h3>
    <div style='color: #4a0e4e; line-height: 1.8; white-space: pre-wrap;'>{current_case['analysis']}</div>
</div>
""", unsafe_allow_html=True)
      
        
        if current_case.get('police_notified'):
            if 'police_message' in current_case:
                st.markdown(f"""
                <div class="police-box">
                    <h2 style="color: #1565c0; margin-top: 0;"><i class="fas fa-shield-alt"></i> Police Notified - FIR Filed</h2>
                    <div class="detail-row">
                        <span class="detail-label">Case ID:</span>
                        <span class="detail-value">{current_case['id']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">FIR Number:</span>
                        <span class="detail-value">{current_case['fir_number']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Location:</span>
                        <span class="detail-value">{current_case['location']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Abuse Type:</span>
                        <span class="detail-value">{current_case['abuse_type']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Filed At:</span>
                        <span class="detail-value">{current_case['timestamp']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
<div class='case-card' style='background: #e8f5e9;'>
    <h3 style='color: #2e7d32;'><i class='fas fa-info-circle'></i> Police Action Details</h3>
    <div style='color: #4a0e4e; line-height: 1.8; white-space: pre-wrap;'>{current_case['police_message']}</div>
</div>
""", unsafe_allow_html=True)
               
                
                st.balloons()
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Check Detailed Status", use_container_width=True):
                        navigate_to('status')
                with col2:
                    if st.button("Ask AI Anything", use_container_width=True):
                        navigate_to('chat')
            else:
                police_prompt = f"""You are a police dispatcher handling animal abuse. Case registered.

Case ID: {current_case['id']}
FIR: {current_case['fir_number']}
Animal: {current_case['animal_type']}
Abuse: {current_case['abuse_type']}
Location: {current_case['location']}
Description: {current_case['description']}

Provide:
1. Police notified, FIR filed confirmation
2. Team arrival time (10-20 minutes)
3. Immediate actions being taken
4. What reporter should do (preserve evidence, ensure safety)
5. Legal process next steps
6. Reassurance

Use bullet points."""
                
                with st.spinner("Getting police dispatch details..."):
                    police_message = analyze_with_groq(police_prompt)
                    current_case['police_message'] = police_message
                    st.rerun()
        else:
            if st.button("Notify Police & File FIR", use_container_width=True):
                current_case['police_notified'] = True
                current_case['status'] = 'Police Notified - FIR Filed'
                st.rerun()
    else:
        with st.form("abuse_form"):
            animal_type = st.selectbox("Animal Type", ["Dog", "Cat", "Cow", "Horse", "Bird", "Buffalo", "Goat", "Other"])
            abuse_type = st.selectbox("Type of Abuse", ["Physical Abuse", "Neglect", "Abandonment", "Cruelty", "Illegal Trade", "Torture", "Illegal Slaughter", "Other"])
            location = st.selectbox("Location", ["Connaught Place, Delhi", "MG Road, Bangalore", "Marine Drive, Mumbai"])
            description = st.text_area("Description of Incident", placeholder="Please provide detailed information...")
            incident_file = st.file_uploader("Upload Image/Video of Incident", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
            culprit_file = st.file_uploader("Upload Photo of Culprit (Optional)", type=['jpg', 'jpeg', 'png'])
            
            submit = st.form_submit_button("Submit Abuse Report", use_container_width=True)
            
            if submit:
                if not description:
                    st.error("Please provide a description!")
                elif not incident_file:
                    st.error("Please upload an image!")
                else:
                    with st.spinner("Processing with AI..."):
                        image_data = encode_image(incident_file)
                        culprit_data = encode_image(culprit_file) if culprit_file else None
                        
                        prompt = f"""Analyze this animal abuse case. Animal: {animal_type}, Abuse: {abuse_type}, Location: {location}, Description: {description}

Provide:
1. Severity Assessment
2. Immediate Action Needed
3. Legal Recommendations
4. Animal Care Suggestions

Be concise and actionable."""
                        
                        analysis = analyze_with_groq(prompt, image_data)
                        
                        case_id = f"ABU{len(st.session_state.cases) + 2001}"
                        fir_number = f"FIR/{datetime.now().year}/ANM/{len(st.session_state.cases) + 5001}"
                        
                        case = {
                            "id": case_id, "type": "Abuse", "animal_type": animal_type,
                            "abuse_type": abuse_type, "location": location, "description": description,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "analysis": analysis, "culprit_photo": "Provided" if culprit_file else "Not Provided",
                            "fir_number": fir_number, "police_notified": False, "status": "Case Registered",
                            "image_data": image_data, "culprit_data": culprit_data
                        }
                        
                        st.session_state.cases.append(case)
                        st.session_state.current_case_id = case_id
                        st.session_state.processing_complete = True
                        st.rerun()

def status_page():
    show_header()
    
    if st.button("Back to Home"):
        navigate_to('home')
    
    st.markdown(f"""
    <h2 style='color: #6b1e6f;'><i class='fas fa-clipboard-list'></i> Case Status Dashboard
    <span class="status-badge"><i class='fas fa-folder-open'></i> {len(st.session_state.cases)} Cases</span></h2>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.cases) == 0:
        st.markdown("""
        <div class="case-card" style="text-align: center; padding: 60px 20px;">
            <i class="fas fa-folder-open" style="font-size: 80px; color: #e2a9f1; margin-bottom: 20px;"></i>
            <h3 style="color: #6b1e6f;">No Cases Created Yet</h3>
            <p style="color: #8e44ad; font-size: 16px;">Report an animal injury or abuse case to get started.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        injury_cases = sum(1 for c in st.session_state.cases if c['type'] == 'Injury')
        abuse_cases = sum(1 for c in st.session_state.cases if c['type'] == 'Abuse')
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="case-card" style="text-align: center; background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left: 5px solid #4caf50;">
                <h2 style="color: #2e7d32; margin: 0;">{len(st.session_state.cases)}</h2>
                <p style="color: #1b5e20; margin: 5px 0;">Total Cases</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="case-card" style="text-align: center; background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); border-left: 5px solid #ff9800;">
                <h2 style="color: #e65100; margin: 0;">{injury_cases}</h2>
                <p style="color: #bf360c; margin: 5px 0;">Injury Cases</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="case-card" style="text-align: center; background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); border-left: 5px solid #f44336;">
                <h2 style="color: #c62828; margin: 0;">{abuse_cases}</h2>
                <p style="color: #b71c1c; margin: 5px 0;">Abuse Cases</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #e2a9f1;'>", unsafe_allow_html=True)
        
        for idx, case in enumerate(reversed(st.session_state.cases)):
            with st.expander(f"{case['id']} - {case['type']} | {case['animal_type']} | {case['timestamp']}", expanded=False):
                
                if case['type'] == 'Abuse' and case.get('culprit_data'):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class="image-container">
                            <h4 style="color: #6b1e6f; margin-top: 0;">Animal/Incident</h4>
                            <img src="data:image/jpeg;base64,{case['image_data']}" style="max-width: 100%; max-height: 400px; border-radius: 10px;">
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="image-container">
                            <h4 style="color: #6b1e6f; margin-top: 0;">Culprit</h4>
                            <img src="data:image/jpeg;base64,{case['culprit_data']}" style="max-width: 100%; max-height: 400px; border-radius: 10px;">
                        </div>
                        """, unsafe_allow_html=True)
                elif 'image_data' in case:
                    st.markdown(f"""
                    <div class="image-container">
                        <h4 style="color: #6b1e6f; margin-top: 0;">Animal Image</h4>
                        <img src="data:image/jpeg;base64,{case['image_data']}" style="max-width: 100%; max-height: 400px; border-radius: 10px;">
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="case-card">
                    <h3 style="color: #6b1e6f;"><i class="fas fa-info-circle"></i> Case Information</h3>
                    <div class="detail-row">
                        <span class="detail-label">Case ID:</span>
                        <span class="detail-value">{case['id']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Type:</span>
                        <span class="detail-value">{case['type']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Animal:</span>
                        <span class="detail-value">{case['animal_type']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Location:</span>
                        <span class="detail-value">{case['location']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Timestamp:</span>
                        <span class="detail-value">{case['timestamp']}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Status:</span>
                        <span class="detail-value"><span class="status-badge">{case['status']}</span></span>
                    </div>
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e2a9f1;">
                        <span class="detail-label">Description:</span>
                        <p style="color: #4a0e4e; margin-top: 8px; line-height: 1.6;">{case['description']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if case['type'] == 'Injury' and case.get('selected_hospital'):
                    hospital = case['selected_hospital']
                    st.markdown(f"""
                    <div class="dispatch-box">
                        <h3 style="color: #e65100; margin-top: 0;"><i class="fas fa-ambulance"></i> Ambulance & Hospital</h3>
                        <div class="detail-row">
                            <span class="detail-label">Hospital:</span>
                            <span class="detail-value">{hospital['name']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Speciality:</span>
                            <span class="detail-value">{hospital['speciality']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Contact:</span>
                            <span class="detail-value">{hospital['contact']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Fees:</span>
                            <span class="detail-value">{hospital['fees']}</span>
                        </div>
                        <hr style="border: 1px solid #ff9800; margin: 15px 0;">
                        <div class="detail-row">
                            <span class="detail-label">Driver:</span>
                            <span class="detail-value">{case['driver_name']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Contact:</span>
                            <span class="detail-value">{case['driver_contact']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if case['type'] == 'Abuse':
                    st.markdown(f"""
                    <div class="case-card" style="background: #fff8e1;">
                        <h3 style="color: #f57c00;"><i class="fas fa-exclamation-triangle"></i> Abuse Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Abuse Type:</span>
                            <span class="detail-value">{case['abuse_type']}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Culprit Photo:</span>
                            <span class="detail-value">{case['culprit_photo']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if case.get('police_notified'):
                        st.markdown(f"""
                        <div class="police-box">
                            <h3 style="color: #1565c0; margin-top: 0;"><i class="fas fa-shield-alt"></i> Police Status</h3>
                            <div class="detail-row">
                                <span class="detail-label">FIR:</span>
                                <span class="detail-value">{case['fir_number']}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Status:</span>
                                <span class="detail-value">Notified & FIR Filed</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown(f"""
<div class='case-card' style='background: #f3e5f5;'>
    <h3 style='color: #6b1e6f;'><i class='fas fa-brain'></i> AI Analysis</h3>
    <div style='color: #4a0e4e; line-height: 1.8; white-space: pre-wrap;'>{case['analysis']}</div>
</div>
""", unsafe_allow_html=True)
                
                
                if st.button(f"Ask AI About This Case", key=f"ask_{case['id']}_{idx}", use_container_width=True):
                    st.session_state.current_case_id = case['id']
                    navigate_to('chat')

def chat_page():
    show_header()
    
    if st.button("Back to Home"):
        navigate_to('home')
    
    st.markdown("<h2 style='color: #6b1e6f;'><i class='fas fa-robot'></i> AI Sathi - Your Animal Welfare Assistant</h2>", unsafe_allow_html=True)
    
    if len(st.session_state.chat_history) == 0:
        if st.session_state.current_case_id:
            current_case = next((c for c in st.session_state.cases if c['id'] == st.session_state.current_case_id), None)
            if current_case:
                case_context = f"""Hello! I am your AI Sathi. I see you have an active case:

Case ID: {current_case['id']}
Type: {current_case['type']}
Animal: {current_case['animal_type']}
Location: {current_case['location']}
Status: {current_case['status']}

"""
                if current_case['type'] == 'Injury' and current_case.get('selected_hospital'):
                    hospital = current_case['selected_hospital']
                    case_context += f"""Hospital: {hospital['name']}
Contact: {hospital['contact']}
Driver: {current_case['driver_name']} ({current_case['driver_contact']})

"""
                
                if current_case['type'] == 'Abuse' and current_case.get('police_notified'):
                    case_context += f"""FIR: {current_case['fir_number']}
Police: Notified & FIR Filed

"""
                
                case_context += """I know all details about your case. Ask me anything!"""
                st.session_state.chat_history.append({"role": "assistant", "content": case_context})
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": """Hello! I am your AI Sathi. I can help with:

- Animal injuries/abuse reporting
- Animal welfare laws
- First aid tips
- Finding veterinary services
- Animal care advice

How can I help you today?"""})
    
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong><i class="fas fa-robot"></i> AI Sathi:</strong><br/>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong><i class="fas fa-user"></i> You:</strong><br/>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    user_input = st.text_area("Type your message...", height=100, placeholder="Ask me anything...", key="chat_input")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("Send", use_container_width=True):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                with st.spinner("Thinking..."):
                    context = ""
                    if st.session_state.current_case_id:
                        current_case = next((c for c in st.session_state.cases if c['id'] == st.session_state.current_case_id), None)
                        if current_case:
                            context = f"""Current Case:
- ID: {current_case['id']}
- Type: {current_case['type']}
- Animal: {current_case['animal_type']}
- Location: {current_case['location']}
- Status: {current_case['status']}
- Analysis: {current_case['analysis']}
"""
                            if current_case['type'] == 'Injury' and current_case.get('selected_hospital'):
                                hospital = current_case['selected_hospital']
                                context += f"- Hospital: {hospital['name']}, {hospital['contact']}\n"
                    
                    prompt = f"""You are AI Sathi, a compassionate animal welfare assistant.

{context}

Recent chat:
{chr(10).join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history[-5:]])}

Question: {user_input}

Respond in a caring, professional manner. Be concise but comprehensive."""
                    
                    response = analyze_with_groq(prompt)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
    
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("<h3 style='color: #6b1e6f;'>Quick Actions</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Report Injury", key="chat_injury"):
            navigate_to('injury')
    with col2:
        if st.button("Report Abuse", key="chat_abuse"):
            navigate_to('abuse')
    with col3:
        if st.button("Check Status", key="chat_status"):
            navigate_to('status')

# Main routing
if st.session_state.current_page == 'home':
    home_page()
elif st.session_state.current_page == 'injury':
    injury_page()
elif st.session_state.current_page == 'abuse':
    abuse_page()
elif st.session_state.current_page == 'status':
    status_page()
elif st.session_state.current_page == 'chat':
    chat_page()
