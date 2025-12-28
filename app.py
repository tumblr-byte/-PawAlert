import streamlit as st
from datetime import datetime
import base64
from groq import Groq
import os

st.set_page_config(page_title="PawAlert", page_icon="🐾", layout="wide")

try:
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not found!")
        st.stop()
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"⚠️ Error: {str(e)}")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
* { font-family: 'Poppins', sans-serif; }
.main { background: linear-gradient(135deg, #fef5ff 0%, #f9e7ff 100%); }
.stButton>button { background: linear-gradient(135deg, #e2a9f1 0%, #d89fe8 100%); color: #4a0e4e; font-weight: 600; border: none; border-radius: 12px; padding: 12px 28px; }
h1, h2, h3, h4 { color: #6b1e6f !important; }
.header-container { text-align: center; padding: 20px; background: linear-gradient(135deg, #e2a9f1 0%, #f5d4ff 100%); border-radius: 20px; margin-bottom: 30px; }
.case-card { background: white; padding: 25px; border-radius: 15px; border-left: 5px solid #e2a9f1; margin: 15px 0; }
.case-card p, .case-card strong, .hospital-card p, .hospital-card strong { color: #2d1b2e !important; }
.success-box { background: linear-gradient(135deg, #d4f5e9 0%, #a8e6cf 100%); padding: 20px; border-radius: 12px; }
.hospital-card { background: white; padding: 20px; border-radius: 12px; margin: 10px 0; border: 2px solid #e2a9f1; }
.status-badge { display: inline-block; padding: 8px 16px; border-radius: 20px; background: #e2a9f1; color: #4a0e4e !important; }
.detail-box { background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #e2a9f1; }
.detail-box p { color: #2d1b2e !important; }
</style>
""", unsafe_allow_html=True)

if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
if 'popup_data' not in st.session_state:
    st.session_state.popup_data = None

def encode_image(f):
    f.seek(0)
    return base64.b64encode(f.getvalue()).decode('utf-8')

def analyze_with_groq(prompt, image_data=None):
    try:
        if image_data:
            response = client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]}],
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
    st.markdown("""
    <div class="header-container">
        <h1 style="margin: 10px 0; color: #4a0e4e;"><i class="fas fa-paw"></i> PawAlert</h1>
        <p style="color: #6b1e6f; font-size: 18px;">Animal Welfare & Rescue Platform</p>
    </div>
    """, unsafe_allow_html=True)

def nav(page):
    st.session_state.current_page = page
    st.rerun()

def home_page():
    show_header()
    st.markdown("<h2 style='text-align: center; color: #6b1e6f;'>How Can We Help?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div style='text-align:center'><i class='fas fa-ambulance' style='font-size:48px;color:#e2a9f1'></i><h3>Injury</h3></div>", unsafe_allow_html=True)
        if st.button("Report Injury", use_container_width=True): nav('injury')
    with col2:
        st.markdown("<div style='text-align:center'><i class='fas fa-shield-alt' style='font-size:48px;color:#e2a9f1'></i><h3>Abuse</h3></div>", unsafe_allow_html=True)
        if st.button("Report Abuse", use_container_width=True): nav('abuse')
    with col3:
        st.markdown(f"<div style='text-align:center'><i class='fas fa-clipboard-list' style='font-size:48px;color:#e2a9f1'></i><h3>Status</h3><p>{len(st.session_state.cases)} cases</p></div>", unsafe_allow_html=True)
        if st.button("Check Status", use_container_width=True): nav('status')
    with col4:
        st.markdown("<div style='text-align:center'><i class='fas fa-robot' style='font-size:48px;color:#e2a9f1'></i><h3>AI Sathi</h3></div>", unsafe_allow_html=True)
        if st.button("Chat Now", use_container_width=True): nav('chat')

def injury_page():
    show_header()
    if st.button("⬅️ Back"): nav('home')
    
    st.markdown("<h2><i class='fas fa-ambulance'></i> Report Animal Injury</h2>", unsafe_allow_html=True)
    animal_type = st.selectbox("Animal Type", ["Dog", "Cat", "Cow", "Horse", "Bird", "Buffalo", "Goat", "Other"])
    location = st.selectbox("Location", ["Connaught Place, Delhi", "MG Road, Bangalore", "Marine Drive, Mumbai"])
    description = st.text_area("Description", placeholder="Describe injury...")
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
    
    if st.button("🚨 Submit", use_container_width=True):
        if not description or not uploaded_file:
            st.error("⚠️ Please fill all fields!")
        else:
            with st.spinner("Analyzing..."):
                img_data = encode_image(uploaded_file)
                analysis = analyze_with_groq(f"Analyze injury: {animal_type}, {location}, {description}. Give: Severity, Injuries, What Happened, Care Needed, Recovery Time", img_data)
                
                hospitals = [
                    {"name": "PetCare Emergency", "location": location, "contact": "+91 98765-43210", "fees": "₹2,000-₹5,000", "speciality": "Emergency", "distance": "2.5km"},
                    {"name": "Animal Rescue Clinic", "location": location, "contact": "+91 98765-43211", "fees": "₹1,500-₹4,000", "speciality": "General", "distance": "4.2km"}
                ]
                
                case_id = f"INJ{len(st.session_state.cases)+1001}"
                st.session_state.cases.append({
                    "id": case_id, "type": "Injury", "animal_type": animal_type, "location": location,
                    "description": description, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "analysis": analysis, "hospitals": hospitals, "image_data": img_data,
                    "selected_hospital": None, "status": "Registered"
                })
                
                st.markdown(f"""
                <div class="success-box">
                    <h3 style="color:#2e7d32">✅ Case Registered! ID: {case_id}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.image(f"data:image/jpeg;base64,{img_data}", caption="Uploaded Image")
                st.markdown(f"""
                <div class="case-card">
                    <h3>AI Analysis</h3>
                    <p style="color:#2d1b2e!important">{analysis}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h3>Available Hospitals</h3>", unsafe_allow_html=True)
                for i, h in enumerate(hospitals):
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.markdown(f"""
                        <div class="hospital-card">
                            <h4 style="color:#6b1e6f">🏥 {h['name']}</h4>
                            <p style="color:#2d1b2e!important"><strong>Speciality:</strong> {h['speciality']}</p>
                            <p style="color:#2d1b2e!important"><strong>Contact:</strong> {h['contact']}</p>
                            <p style="color:#2d1b2e!important"><strong>Fees:</strong> {h['fees']}</p>
                            <p style="color:#2d1b2e!important"><strong>Distance:</strong> {h['distance']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.button("🚑 Call", key=f"amb_{i}"):
                            st.session_state.cases[-1]['selected_hospital'] = h
                            st.session_state.cases[-1]['status'] = 'Ambulance Dispatched'
                            st.session_state.show_popup = True
                            st.session_state.popup_data = {'hospital': h, 'case_id': case_id}
                            st.rerun()
    
    if st.session_state.show_popup and st.session_state.popup_data:
        d = st.session_state.popup_data
        st.success("🎉 Ambulance Dispatched!")
        st.balloons()
        st.markdown(f"""
        <div class="detail-box" style="background:#e8f5e9">
            <h4 style="color:#2e7d32">🏥 Hospital: {d['hospital']['name']}</h4>
            <p><strong>Contact:</strong> {d['hospital']['contact']}</p>
            <p><strong>Fees:</strong> {d['hospital']['fees']}</p>
        </div>
        <div class="detail-box" style="background:#fff3e0">
            <h4 style="color:#e65100">🚑 Driver: Rajesh Kumar</h4>
            <p><strong>Contact:</strong> +91 98765-11111</p>
            <p><strong>Vehicle:</strong> DL 1A 2345</p>
            <p><strong>ETA:</strong> 15-20 mins</p>
        </div>
        <div class="detail-box" style="background:#e3f2fd">
            <h4 style="color:#1565c0">📍 Case ID: {d['case_id']}</h4>
            <p>Track in Case Status section</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ Got It!", use_container_width=True):
            st.session_state.show_popup = False
            st.session_state.popup_data = None
            st.rerun()
        if st.button("📊 Case Status", use_container_width=True):
            st.session_state.show_popup = False
            nav('status')

def abuse_page():
    show_header()
    if st.button("⬅️ Back"): nav('home')
    
    st.markdown("<h2><i class='fas fa-shield-alt'></i> Report Animal Abuse</h2>", unsafe_allow_html=True)
    animal_type = st.selectbox("Animal", ["Dog", "Cat", "Cow", "Horse", "Bird", "Buffalo", "Goat", "Other"])
    abuse_type = st.selectbox("Abuse Type", ["Physical Abuse", "Neglect", "Abandonment", "Cruelty", "Illegal Trade", "Other"])
    location = st.selectbox("Location", ["Connaught Place, Delhi", "MG Road, Bangalore", "Marine Drive, Mumbai"])
    description = st.text_area("Description", placeholder="Describe incident...")
    incident_file = st.file_uploader("Incident Image *", type=['jpg', 'jpeg', 'png'])
    culprit_file = st.file_uploader("Culprit Photo (Optional)", type=['jpg', 'jpeg', 'png'])
    
    if st.button("📢 Submit", use_container_width=True):
        if not description or not incident_file:
            st.error("⚠️ Please fill all required fields!")
        else:
            with st.spinner("Processing..."):
                inc_img = encode_image(incident_file)
                culp_img = encode_image(culprit_file) if culprit_file else None
                analysis = analyze_with_groq(f"Analyze abuse: {animal_type}, {abuse_type}, {location}, {description}. Give: Severity, What Happened, Action, Legal, Care", inc_img)
                
                case_id = f"ABU{len(st.session_state.cases)+2001}"
                fir_num = f"FIR/{datetime.now().year}/ANM/{len(st.session_state.cases)+5001}"
                
                st.session_state.cases.append({
                    "id": case_id, "type": "Abuse", "animal_type": animal_type, "abuse_type": abuse_type,
                    "location": location, "description": description, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "analysis": analysis, "incident_image": inc_img, "culprit_image": culp_img,
                    "fir_number": fir_num, "police_notified": False, "status": "Registered"
                })
                
                st.markdown(f"""
                <div class="success-box">
                    <h3 style="color:#2e7d32">✅ Abuse Case Registered! ID: {case_id}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(2) if culp_img else [st]
                if len(cols) == 2:
                    with cols[0]:
                        st.markdown("<h4>Incident Photo</h4>", unsafe_allow_html=True)
                        st.image(f"data:image/jpeg;base64,{inc_img}")
                    with cols[1]:
                        st.markdown("<h4>Culprit Photo</h4>", unsafe_allow_html=True)
                        st.image(f"data:image/jpeg;base64,{culp_img}")
                else:
                    st.image(f"data:image/jpeg;base64,{inc_img}", caption="Incident Photo")
                
                st.markdown(f"""
                <div class="case-card">
                    <h3>AI Analysis</h3>
                    <p style="color:#2d1b2e!important">{analysis}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📞 Notify Police & File FIR"):
                        st.session_state.cases[-1]['police_notified'] = True
                        st.session_state.cases[-1]['status'] = 'Police Notified'
                        st.success(f"✅ Police Notified!\n🚔 FIR: {fir_num}")
                        st.balloons()
                with col2:
                    if st.button("📊 Case Status"):
                        nav('status')

def status_page():
    show_header()
    if st.button("⬅️ Back"): nav('home')
    
    st.markdown(f"<h2>📋 Case Status ({len(st.session_state.cases)} Cases)</h2>", unsafe_allow_html=True)
    
    if not st.session_state.cases:
        st.info("No cases yet. Report an injury or abuse case to get started.")
    else:
        for case in reversed(st.session_state.cases):
            with st.expander(f"📋 {case['id']} - {case['type']} | {case['animal_type']} | {case['timestamp']}"):
                st.markdown(f"""
                <div class="case-card">
                    <h3>Case Information</h3>
                    <p><strong>ID:</strong> {case['id']}</p>
                    <p><strong>Type:</strong> {case['type']}</p>
                    <p><strong>Animal:</strong> {case['animal_type']}</p>
                    <p><strong>Location:</strong> {case['location']}</p>
                    <p><strong>Status:</strong> <span class="status-badge">{case['status']}</span></p>
                    <p><strong>Description:</strong> {case['description']}</p>
                    <p><strong>Time:</strong> {case['timestamp']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if case['type'] == 'Injury':
                    st.image(f"data:image/jpeg;base64,{case['image_data']}", caption="Injury Photo")
                    if case.get('selected_hospital'):
                        h = case['selected_hospital']
                        st.markdown(f"""
                        <div class="detail-box" style="background:#e8f5e9">
                            <h4 style="color:#2e7d32">🚑 Ambulance Dispatched</h4>
                            <p><strong>Hospital:</strong> {h['name']}</p>
                            <p><strong>Driver:</strong> Rajesh Kumar (+91 98765-11111)</p>
                            <p><strong>Vehicle:</strong> DL 1A 2345</p>
                            <p><strong>Fees:</strong> {h['fees']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.image(f"data:image/jpeg;base64,{case['incident_image']}", caption="Incident Photo")
                    if case.get('culprit_image'):
                        st.image(f"data:image/jpeg;base64,{case['culprit_image']}", caption="Culprit Photo")
                    if case.get('police_notified'):
                        st.markdown(f"""
                        <div class="detail-box" style="background:#e3f2fd">
                            <h4 style="color:#1565c0">🚔 Police Notified</h4>
                            <p><strong>FIR:</strong> {case['fir_number']}</p>
                            <p><strong>Status:</strong> ✅ Filed</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="case-card">
                    <h4>AI Analysis</h4>
                    <p style="color:#2d1b2e!important">{case['analysis']}</p>
                </div>
                """, unsafe_allow_html=True)

def chat_page():
    show_header()
    if st.button("⬅️ Back"): nav('home')
    
    st.markdown("<h2><i class='fas fa-robot'></i> AI Sathi</h2>", unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({"role": "assistant", "content": "Namaste! I'm AI Sathi. How can I help with animal welfare?"})
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            st.markdown(f"""<div style='background:#e2a9f1;padding:10px;border-radius:10px;margin:10px 0;color:#4a0e4e'><strong>🤖 AI:</strong> {msg['content']}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style='background:#f3e5f5;padding:10px;border-radius:10px;margin:10px 0;color:#4a0e4e'><strong>You:</strong> {msg['content']}</div>""", unsafe_allow_html=True)
    
    user_input = st.text_area("Message", height=100)
    
    col1, col2 = st.columns([4,1])
    with col1:
        if st.button("📤 Send", use_container_width=True):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                response = analyze_with_groq(f"You're AI Sathi. Previous: {st.session_state.chat_history[-2:]}. User: {user_input}. Reply helpfully.")
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# Router
page = st.session_state.current_page
if page == 'home': home_page()
elif page == 'injury': injury_page()
elif page == 'abuse': abuse_page()
elif page == 'status': status_page()
elif page == 'chat': chat_page()
