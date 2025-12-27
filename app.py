import streamlit as st
from datetime import datetime
import base64
from groq import Groq
import json
import os

# Page config
st.set_page_config(
    page_title="PawAlert - Animal Welfare & Rescue",
    page_icon="🐾",
    layout="wide"
)

# Initialize Groq client from secrets
GROQ_API_KEY = None
client = None

try:
    # Try to get from Streamlit secrets
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    else:
        # Fallback to environment variable
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not found in secrets or environment variables!")
        st.info("Please add GROQ_API_KEY to your Streamlit secrets.")
        st.stop()
    
    # Initialize Groq client with minimal parameters
    client = Groq(api_key=GROQ_API_KEY)
    
except Exception as e:
    st.error(f"⚠️ Error initializing Groq client: {str(e)}")
    st.info("""
    **Possible fixes:**
    1. Update groq library: `pip install --upgrade groq`
    2. Check your GROQ_API_KEY in Streamlit secrets
    3. Make sure groq version is >= 0.4.0
    """)
    st.stop()

# Custom CSS with theme color
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #fef5ff 0%, #f9e7ff 100%);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%);
        color: #4a0e4e;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-size: 16px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(226, 169, 241, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(226, 169, 241, 0.5);
    }
    
    h1, h2, h3 {
        color: #6b1e6f;
    }
    
    .header-container {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #e2a9f1 0%, #f5d4ff 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(226, 169, 241, 0.4);
    }
    
    .icon-button {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 3px solid #e2a9f1;
    }
    
    .icon-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(226, 169, 241, 0.4);
    }
    
    .case-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #e2a9f1;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4f5e9 0%, #a8e6cf 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #4caf50;
        margin: 20px 0;
    }
    
    .hospital-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border: 2px solid #e2a9f1;
        transition: all 0.3s;
    }
    
    .hospital-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(226, 169, 241, 0.3);
    }
    
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        background: #e2a9f1;
        color: #4a0e4e;
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-message {
        padding: 12px 18px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .user-message {
        background: #f3e5f5;
        color: #4a0e4e;
        margin-left: 20%;
    }
    
    .bot-message {
        background: #e2a9f1;
        color: #4a0e4e;
        margin-right: 20%;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        border: 2px solid #e2a9f1;
        border-radius: 10px;
        color: #4a0e4e;
    }
    
    label {
        color: #6b1e6f !important;
        font-weight: 600 !important;
    }
    
    .stFileUploader {
        border: 2px dashed #e2a9f1;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_hospital' not in st.session_state:
    st.session_state.selected_hospital = None

# Function to encode image
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Function to analyze with Groq
def analyze_with_groq(prompt, image_data=None):
    try:
        if image_data:
            response = client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
        else:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis error: {str(e)}"

# Header
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

# Home Page
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
            st.session_state.current_page = 'injury'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="icon-button">
            <i class="fas fa-shield-alt" style="font-size: 48px; color: #e2a9f1; margin-bottom: 15px;"></i>
            <h3 style="color: #6b1e6f; margin: 10px 0;">Animal Abuse</h3>
            <p style="color: #8e44ad;">Report abuse cases</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Report Abuse", key="abuse_btn", use_container_width=True):
            st.session_state.current_page = 'abuse'
            st.rerun()
    
    with col3:
        st.markdown(f"""
        <div class="icon-button">
            <i class="fas fa-clipboard-list" style="font-size: 48px; color: #e2a9f1; margin-bottom: 15px;"></i>
            <h3 style="color: #6b1e6f; margin: 10px 0;">Case Status</h3>
            <p style="color: #8e44ad;">{len(st.session_state.cases)} cases reported</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Check Status", key="status_btn", use_container_width=True):
            st.session_state.current_page = 'status'
            st.rerun()
    
    with col4:
        st.markdown("""
        <div class="icon-button">
            <i class="fas fa-robot" style="font-size: 48px; color: #e2a9f1; margin-bottom: 15px;"></i>
            <h3 style="color: #6b1e6f; margin: 10px 0;">AI Sathi</h3>
            <p style="color: #8e44ad;">Chat with AI assistant</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Chat Now", key="chat_btn", use_container_width=True):
            st.session_state.current_page = 'chat'
            st.rerun()

# Injury Report Page
def injury_page():
    show_header()
    
    if st.button("⬅️ Back to Home", key="back_injury"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("<h2 style='color: #6b1e6f;'><i class='fas fa-ambulance'></i> Report Animal Injury</h2>", unsafe_allow_html=True)
    
    with st.form("injury_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            animal_type = st.selectbox(
                "Animal Type",
                ["Dog", "Cat", "Cow", "Horse", "Bird", "Buffalo", "Goat", "Other"]
            )
            
            location = st.selectbox(
                "Location",
                ["Connaught Place, Delhi", "MG Road, Bangalore", "Marine Drive, Mumbai"]
            )
        
        with col2:
            description = st.text_area("Description of Injury", height=100, placeholder="Please describe the injury in detail...")
        
        uploaded_file = st.file_uploader("Upload Image/Video of Injured Animal", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
        
        submit = st.form_submit_button("🚨 Submit Report", use_container_width=True)
        
        if submit:
            if not description:
                st.error("⚠️ Please provide a description of the injury!")
            elif not uploaded_file:
                st.error("⚠️ Please upload an image or video of the injured animal!")
            else:
                with st.spinner("🔍 Analyzing injury with AI..."):
                    image_data = encode_image(uploaded_file)
                    
                    prompt = f"""Analyze this animal injury image. The animal is a {animal_type} at {location}.
Description: {description}

Provide a detailed analysis with:
1. Severity Level (Minor/Moderate/Severe/Critical)
2. Visible Injuries and Condition
3. Immediate Care Required
4. Urgency Level
5. Estimated Recovery Time

Keep response professional and structured."""
                    
                    analysis = analyze_with_groq(prompt, image_data)
                    
                    # Generate hospital recommendations
                    hospitals = [
                        {
                            "name": "PetCare Emergency Hospital",
                            "location": location,
                            "availability": "Available Now",
                            "contact": "+91 98765-43210",
                            "fees": "₹2,000 - ₹5,000",
                            "speciality": "Emergency & Critical Care"
                        },
                        {
                            "name": "Animal Rescue Veterinary Clinic",
                            "location": location,
                            "availability": "Available in 15 mins",
                            "contact": "+91 98765-43211",
                            "fees": "₹1,500 - ₹4,000",
                            "speciality": "General Treatment"
                        },
                        {
                            "name": "24/7 Animal Care Center",
                            "location": location,
                            "availability": "Available Now",
                            "contact": "+91 98765-43212",
                            "fees": "₹2,500 - ₹6,000",
                            "speciality": "Surgery & ICU"
                        }
                    ]
                    
                    case_id = f"INJ{len(st.session_state.cases) + 1001}"
                    driver_name = "Rajesh Kumar"
                    driver_contact = "+91 98765-11111"
                    
                    case = {
                        "id": case_id,
                        "type": "Injury",
                        "animal_type": animal_type,
                        "location": location,
                        "description": description,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "analysis": analysis,
                        "hospitals": hospitals,
                        "driver_name": driver_name,
                        "driver_contact": driver_contact,
                        "selected_hospital": None,
                        "status": "Case Registered"
                    }
                    
                    st.session_state.cases.append(case)
                    
                    st.markdown(f"""
                    <div class="success-box">
                        <h3 style="color: #2e7d32; margin-top: 0;"><i class="fas fa-check-circle"></i> Case Registered Successfully!</h3>
                        <p style="color: #1b5e20; font-size: 18px; margin: 10px 0;"><strong>Case ID: {case_id}</strong></p>
                        <p style="color: #2e7d32; font-size: 16px;">Timestamp: {case['timestamp']}</p>
                        <p style="color: #2e7d32;">Your report has been submitted. Please select a hospital below to dispatch ambulance!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="case-card">
                        <h3 style="color: #6b1e6f;"><i class="fas fa-notes-medical"></i> AI Analysis Report</h3>
                        <p style="color: #4a0e4e; line-height: 1.8;">{analysis}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<h3 style='color: #6b1e6f; margin-top: 30px;'><i class='fas fa-hospital'></i> Recommended Veterinary Hospitals</h3>", unsafe_allow_html=True)
                    
                    for i, hospital in enumerate(hospitals):
                        st.markdown(f"""
                        <div class="hospital-card">
                            <h4 style="color: #6b1e6f; margin-top: 0;"><i class="fas fa-hospital-alt"></i> {hospital['name']}</h4>
                            <p style="color: #8e44ad; margin: 8px 0;"><i class="fas fa-stethoscope"></i> <strong>Speciality:</strong> {hospital['speciality']}</p>
                            <p style="color: #8e44ad; margin: 8px 0;"><i class="fas fa-map-marker-alt"></i> <strong>Location:</strong> {hospital['location']}</p>
                            <p style="color: #8e44ad; margin: 8px 0;"><i class="fas fa-phone"></i> <strong>Contact:</strong> {hospital['contact']}</p>
                            <p style="color: #8e44ad; margin: 8px 0;"><i class="fas fa-rupee-sign"></i> <strong>Estimated Fees:</strong> {hospital['fees']}</p>
                            <span class="status-badge"><i class="fas fa-clock"></i> {hospital['availability']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"🚑 Dispatch Ambulance to {hospital['name']}", key=f"ambulance_{case_id}_{i}", use_container_width=True):
                            # Update case with selected hospital
                            st.session_state.cases[-1]['selected_hospital'] = hospital
                            st.session_state.cases[-1]['status'] = 'Ambulance Dispatched'
                            
                            st.success(f"""
✅ **Ambulance Dispatched Successfully!**

🏥 **Hospital:** {hospital['name']}
🚗 **Driver:** {driver_name}
📞 **Driver Contact:** {driver_contact}
📍 **Going to:** {hospital['location']}
💰 **Estimated Fees:** {hospital['fees']}

**The ambulance is on its way to pick up the animal!**

👉 Click **'Check Status'** button at the top to track your case anytime!
                            """)
                            st.balloons()

# Abuse Report Page
def abuse_page():
    show_header()
    
    if st.button("⬅️ Back to Home", key="back_abuse"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("<h2 style='color: #6b1e6f;'><i class='fas fa-shield-alt'></i> Report Animal Abuse</h2>", unsafe_allow_html=True)
    
    with st.form("abuse_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            animal_type = st.selectbox(
                "Animal Type",
                ["Dog", "Cat", "Cow", "Horse", "Bird", "Buffalo", "Goat", "Other"]
            )
            
            abuse_type = st.selectbox(
                "Type of Abuse",
                ["Physical Abuse", "Neglect", "Abandonment", "Cruelty", "Illegal Trade", "Torture", "Illegal Slaughter", "Other"]
            )
            
            location = st.selectbox(
                "Location",
                ["Connaught Place, Delhi", "MG Road, Bangalore", "Marine Drive, Mumbai"]
            )
        
        with col2:
            description = st.text_area("Description of Incident", height=150, placeholder="Please provide detailed information about the abuse incident...")
        
        incident_file = st.file_uploader("Upload Image/Video of Incident *", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
        culprit_file = st.file_uploader("Upload Photo of Culprit (Optional)", type=['jpg', 'jpeg', 'png'])
        
        submit = st.form_submit_button("📢 Submit Abuse Report", use_container_width=True)
        
        if submit:
            if not description:
                st.error("⚠️ Please provide a description of the incident!")
            elif not incident_file:
                st.error("⚠️ Please upload an image or video of the incident!")
            else:
                with st.spinner("🔍 Processing abuse report with AI..."):
                    image_data = encode_image(incident_file)
                    
                    prompt = f"""Analyze this animal abuse case seriously. 
Animal: {animal_type}
Abuse Type: {abuse_type}
Location: {location}
Description: {description}

Provide:
1. Severity Assessment (Low/Medium/High/Critical)
2. Type of Abuse Identified
3. Immediate Action Needed for Animal Safety
4. Legal Recommendations
5. Animal Care and Rehabilitation Suggestions
6. Evidence Preservation Tips

Be professional, serious, and actionable."""
                    
                    analysis = analyze_with_groq(prompt, image_data)
                    
                    case_id = f"ABU{len(st.session_state.cases) + 2001}"
                    fir_number = f"FIR/{datetime.now().year}/ANM/{len(st.session_state.cases) + 5001}"
                    
                    case = {
                        "id": case_id,
                        "type": "Abuse",
                        "animal_type": animal_type,
                        "abuse_type": abuse_type,
                        "location": location,
                        "description": description,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "analysis": analysis,
                        "culprit_photo": "Provided" if culprit_file else "Not Provided",
                        "fir_number": fir_number,
                        "police_notified": False,
                        "status": "Case Registered"
                    }
                    
                    st.session_state.cases.append(case)
                    
                    st.markdown(f"""
                    <div class="success-box">
                        <h3 style="color: #2e7d32; margin-top: 0;"><i class="fas fa-check-circle"></i> Abuse Case Registered Successfully!</h3>
                        <p style="color: #1b5e20; font-size: 18px; margin: 10px 0;"><strong>Case ID: {case_id}</strong></p>
                        <p style="color: #1b5e20; font-size: 16px;">Timestamp: {case['timestamp']}</p>
                        <p style="color: #1b5e20; font-size: 16px;">Culprit Photo: {case['culprit_photo']}</p>
                        <p style="color: #2e7d32;">Thank you for reporting. Your case has been documented!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="case-card">
                        <h3 style="color: #6b1e6f;"><i class="fas fa-gavel"></i> AI Analysis & Legal Recommendations</h3>
                        <p style="color: #4a0e4e; line-height: 1.8;">{analysis}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="case-card">
                        <h3 style="color: #6b1e6f;"><i class="fas fa-exclamation-triangle"></i> What Happens Next?</h3>
                        <ul style="color: #4a0e4e; line-height: 2;">
                            <li><strong>Animal Rescue:</strong> Animal welfare team will be dispatched to rescue the animal</li>
                            <li><strong>Medical Care:</strong> Injured animal will receive immediate veterinary care</li>
                            <li><strong>Legal Action:</strong> Evidence will be preserved for legal proceedings</li>
                            <li><strong>Police Report:</strong> Click the button below to notify police authorities</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📞 Notify Police & File FIR", use_container_width=True):
                            st.session_state.cases[-1]['police_notified'] = True
                            st.session_state.cases[-1]['status'] = 'Police Notified - FIR Filed'
                            
                            st.success(f"""
✅ **Police Notified Successfully!**

🚔 **FIR Number:** {fir_number}
📋 **Case ID:** {case_id}
👮 **Status:** Police officer has been assigned to investigate
📍 **Location:** {location}
⚖️ **Action:** Legal proceedings initiated against the culprit

**Your report has been forwarded to the authorities. They will contact you soon for further details.**

👉 Click **'Check Status'** to track your case progress!
                            """)
                            st.balloons()
                    
                    with col2:
                        if st.button("📊 Go to Case Status", use_container_width=True):
                            st.session_state.current_page = 'status'
                            st.rerun()

# Status Page
def status_page():
    show_header()
    
    if st.button("⬅️ Back to Home", key="back_status"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown(f"""
    <h2 style='color: #6b1e6f;'><i class='fas fa-clipboard-list'></i> Case Status Dashboard
    <span class="status-badge"><i class='fas fa-folder-open'></i> {len(st.session_state.cases)} Total Cases</span></h2>
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
        # Statistics
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
        
        # Display all cases
        for idx, case in enumerate(reversed(st.session_state.cases)):
            case_icon = "fa-ambulance" if case['type'] == 'Injury' else "fa-shield-alt"
            case_color = "#ff9800" if case['type'] == 'Injury' else "#f44336"
            
            with st.expander(f"📋 Case {case['id']} - {case['type']} | {case['animal_type']} | {case['timestamp']}", expanded=False):
                st.markdown(f"""
                <div class="case-card">
                    <h3 style="color: #6b1e6f;"><i class="fas fa-info-circle"></i> Case Information</h3>
                    <p><strong style="color: #6b1e6f;">Case ID:</strong> <span style="color: #4a0e4e; font-size: 16px;">{case['id']}</span></p>
                    <p><strong style="color: #6b1e6f;">Type:</strong> <span style="color: {case_color}; font-weight: 600;">{case['type']}</span></p>
                    <p><strong style="color: #6b1e6f;">Animal Type:</strong> <span style="color: #4a0e4e;">{case['animal_type']}</span></p>
                    <p><strong style="color: #6b1e6f;">Location:</strong> <span style="color: #4a0e4e;">{case['location']}</span></p>
                    <p><strong style="color: #6b1e6f;">Reported On:</strong> <span style="color: #4a0e4e;">{case['timestamp']}</span></p>
                    <p><strong style="color: #6b1e6f;">Current Status:</strong> <span class="status-badge">{case['status']}</span></p>
                    <p><strong style="color: #6b1e6f;">Description:</strong></p>
                    <p style="color: #4a0e4e; background: #f9f9f9; padding: 15px; border-radius: 8px; border-left: 3px solid #e2a9f1;">{case['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Injury case specific information
                if case['type'] == 'Injury':
                    if case.get('selected_hospital'):
                        hospital = case['selected_hospital']
                        st.markdown(f"""
                        <div class="case-card" style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border-left: 5px solid #4caf50;">
                            <h4 style="color: #2e7d32;"><i class="fas fa-ambulance"></i> Ambulance & Hospital Details</h4>
                            <p><strong style="color: #1b5e20;">Driver Name:</strong> <span style="color: #2e7d32;">{case['driver_name']}</span></p>
                            <p><strong style="color: #1b5e20;">Driver Contact:</strong> <span style="color: #2e7d32;">{case['driver_contact']}</span></p>
                            <p><strong style="color: #1b5e20;">Hospital:</strong> <span style="color: #2e7d32;">{hospital['name']}</span></p>
                            <p><strong style="color: #1b5e20;">Hospital Contact:</strong> <span style="color: #2e7d32;">{hospital['contact']}</span></p>
                            <p><strong style="color: #1b5e20;">Speciality:</strong> <span style="color: #2e7d32;">{hospital['speciality']}</span></p>
                            <p><strong style="color: #1b5e20;">Estimated Fees:</strong> <span style="color: #2e7d32;">{hospital['fees']}</span></p>
                            <p><strong style="color: #1b5e20;">What's Happening:</strong> <span style="color: #2e7d32;">Ambulance is on the way to pick up the animal and transport to {hospital['name']}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="case-card" style="background: #fff3cd; border-left: 5px solid #ffc107;">
                            <p style="color: #856404; margin: 0;"><i class="fas fa-exclamation-triangle"></i> <strong>No ambulance dispatched yet.</strong> Please select a hospital from the recommended list above.</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Abuse case specific information
                elif case['type'] == 'Abuse':
                    st.markdown(f"""
                    <div class="case-card">
                        <h4 style="color: #6b1e6f;"><i class="fas fa-gavel"></i> Abuse Case Details</h4>
                        <p><strong style="color: #6b1e6f;">Abuse Type:</strong> <span style="color: #c62828;">{case['abuse_type']}</span></p>
                        <p><strong style="color: #6b1e6f;">Culprit Photo:</strong> <span style="color: #4a0e4e;">{case['culprit_photo']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if case.get('police_notified'):
                        st.markdown(f"""
                        <div class="case-card" style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border-left: 5px solid #2196f3;">
                            <h4 style="color: #1565c0;"><i class="fas fa-police"></i> Police & Legal Status</h4>
                            <p><strong style="color: #0d47a1;">FIR Number:</strong> <span style="color: #1565c0;">{case['fir_number']}</span></p>
                            <p><strong style="color: #0d47a1;">Police Status:</strong> <span style="color: #1565c0;">✅ Police Notified & FIR Filed</span></p>
                            <p><strong style="color: #0d47a1;">Investigation:</strong> <span style="color: #1565c0;">Officer assigned - Investigation in progress</span></p>
                            <p><strong style="color: #0d47a1;">Legal Action:</strong> <span style="color: #1565c0;">Case forwarded to authorities for legal proceedings</span></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="case-card" style="background: #fff3cd; border-left: 5px solid #ffc107;">
                            <p style="color: #856404; margin: 0;"><i class="fas fa-exclamation-triangle"></i> <strong>Police not notified yet.</strong> Please click 'Notify Police & File FIR' button in the abuse report page.</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # AI Analysis for all cases
                st.markdown(f"""
                <div class="case-card">
                    <h4 style="color: #6b1e6f;"><i class="fas fa-brain"></i> AI Analysis Report</h4>
                    <div style="color: #4a0e4e; background: #f9f9f9; padding: 15px; border-radius: 8px; line-height: 1.8; border-left: 3px solid #e2a9f1;">
                        {case['analysis']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Chat Page
def chat_page():
    show_header()
    
    if st.button("⬅️ Back to Home", key="back_chat"):
        st.session_state.current_page = 'home'
        st.rerun()
    
    st.markdown("<h2 style='color: #6b1e6f;'><i class='fas fa-robot'></i> AI Sathi - Your Animal Welfare Assistant</h2>", unsafe_allow_html=True)
    
    # Initialize chat with welcome message
    if len(st.session_state.chat_history) == 0:
        initial_message = """नमस्ते Friend! 🙏

I am your **AI Sathi** - your companion in animal welfare. I'm here to help you with:

✅ **Reporting animal injuries or abuse**
✅ **Understanding animal welfare laws**
✅ **First aid tips for injured animals**
✅ **Finding nearby veterinary services**
✅ **General animal care advice**

How are you helping animals today? Please let me know what you need assistance with!"""
        st.session_state.chat_history.append({"role": "assistant", "content": initial_message})
    
    # Display chat history
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "assistant":
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong><i class="fas fa-robot"></i> AI Sathi:</strong><br/>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong><i class="fas fa-user"></i> You:</strong><br/>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Type your message here...", key="chat_input_area", height=100, placeholder="Ask me anything about animal welfare, injuries, abuse, laws, or care...")
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            send_button = st.form_submit_button("📤 Send", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner("AI Sathi is thinking..."):
            # Build conversation context
            conversation_context = "Previous conversation:\n"
            for msg in st.session_state.chat_history[-5:]:  # Last 5 messages for context
                role = "AI Sathi" if msg["role"] == "assistant" else "User"
                conversation_context += f"{role}: {msg['content']}\n"
            
            prompt = f"""You are AI Sathi, a compassionate and knowledgeable animal welfare assistant. You help people with:
- Reporting and handling animal injuries
- Understanding and reporting animal abuse cases
- Animal welfare laws in India (IPC Section 428, 429, Prevention of Cruelty to Animals Act 1960)
- First aid for injured animals
- Finding veterinary services
- General animal care and protection advice

{conversation_context}

Current user message: {user_input}

Respond in a friendly, helpful, and empathetic manner. Provide practical advice and actionable steps. If the user is reporting an emergency, guide them to use the injury or abuse report features of this app. Keep responses concise but informative."""
            
            response = analyze_with_groq(prompt)
            
            # Add AI response to history
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    # Quick action buttons
    st.markdown("<h3 style='color: #6b1e6f; margin-top: 30px;'>Quick Actions</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚨 Report Injury", key="quick_injury", use_container_width=True):
            st.session_state.current_page = 'injury'
            st.rerun()
    
    with col2:
        if st.button("🛡️ Report Abuse", key="quick_abuse", use_container_width=True):
            st.session_state.current_page = 'abuse'
            st.rerun()
    
    with col3:
        if st.button("📊 Check Status", key="quick_status", use_container_width=True):
            st.session_state.current_page = 'status'
            st.rerun()

# Main App Router
def main():
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

if __name__ == "__main__":
    main()
