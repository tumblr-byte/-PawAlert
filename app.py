import streamlit as st

# Page config
st.set_page_config(
    page_title="PawAlert",
    page_icon="🐾",
    layout="wide"
)

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
        padding: 15px 40px;
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
        gap: 15px;
    }
    
    .logo-img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid white;
    }
    
    .brand-name {
        color: white;
        font-size: 28px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 25px;
    }
    
    .nav-icon {
        color: white;
        font-size: 24px;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    
    .nav-icon:hover {
        transform: scale(1.2);
    }
    
    .profile-img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid white;
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
    }
    
    .main-image {
        max-width: 800px;
        width: 100%;
        height: auto;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(226, 169, 241, 0.3);
        margin: 30px auto;
        display: block;
        transition: transform 0.3s ease;
    }
    
    .main-image:hover {
        transform: scale(1.02);
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

# Navigation Bar with images
st.markdown("""
    <div class="nav-container">
        <div class="nav-left">
            <div class="brand-name">PawAlert</div>
        </div>
        <div class="nav-right">
            <i class="fas fa-chart-line nav-icon" title="Status"></i>
            <i class="fas fa-robot nav-icon" title="AI Assistant"></i>
        </div>
    </div>
""", unsafe_allow_html=True)

# Add logo and profile with absolute positioning
col1, col2, col3 = st.columns([1, 8, 1])
with col1:
    st.markdown('<div style="margin-top: -80px;">', unsafe_allow_html=True)
    try:
        st.image("logo.png", width=60)
    except:
        pass
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div style="margin-top: -80px;">', unsafe_allow_html=True)
    try:
        st.image("default.png", width=50)
    except:
        pass
    st.markdown('</div>', unsafe_allow_html=True)

# Body Section
st.markdown('<div class="body-container">', unsafe_allow_html=True)

# Hero Text
st.markdown('<h1 class="hero-text">Rescue & Protect Animals in Need</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Report animal injuries and abuse to save lives</p>', unsafe_allow_html=True)

# Main Image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("main.png", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
