import streamlit as st
import base64

# Page config
st.set_page_config(
    page_title="PawAlert",
    page_icon="🐾",
    layout="wide"
)

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

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* White background */
    .stApp {
        background-color: white;
    }
    
    /* Custom Navigation Bar */
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
    
    /* Body Section */
    .body-container {
        text-align: center;
        padding: 50px 20px;
        background-color: white;
    }
    
    .main-img-container img {
        background-color: transparent !important;
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
    </style>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Navigation Bar with embedded images
logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo-img">' if logo_base64 else '<div style="width:60px;height:60px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:30px;">🐾</div>'
profile_html = f'<img src="data:image/png;base64,{default_base64}" alt="Profile" class="profile-img">' if default_base64 else '<div style="width:50px;height:50px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;">👤</div>'

st.markdown(f"""
    <div class="nav-container">
        <div class="nav-left">
            {logo_html}
            <div class="brand-name">PawAlert</div>
        </div>
        <div class="nav-right">
            <i class="fas fa-chart-line nav-icon" title="Status"></i>
            <i class="fas fa-robot nav-icon" title="AI Assistant"></i>
            {profile_html}
        </div>
    </div>
""", unsafe_allow_html=True)

# Body Section
st.markdown('<div class="body-container">', unsafe_allow_html=True)

# Hero Text
st.markdown('<h1 class="hero-text">Rescue & Protect Animals in Need</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Report animal injuries and abuse to save lives</p>', unsafe_allow_html=True)

# Main Image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="main-img-container">', unsafe_allow_html=True)
    try:
        st.image("main.png", use_container_width=True)
    except Exception as e:
        st.error(f"Cannot load main.png: {e}")
        st.info("Make sure main.png is in the same folder as app.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
