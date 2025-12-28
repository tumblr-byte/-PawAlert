# 🐾 PawAlert - Animal Welfare & Rescue Platform


## Inspiration

One day, I witnessed something that changed everything. I saw a biker intentionally hit a stray dog and drive away without looking back. The poor animal was left injured and helpless on the road. 

I've seen this happen too many times - little kids throwing stones at animals, people beating innocent creatures, and abusers getting away without consequences. These voiceless animals deserve better. They deserve justice, care, and protection.

**PawAlert was born from a simple belief:** Every animal deserves to be safe, and every abuser must be held accountable. This platform bridges the gap between witnesses and action - connecting injured animals to veterinary care and abuse cases to law enforcement.

## Features

###  **Injury Reporting & Ambulance Dispatch**
- Report injured animals with photos and location
- AI-powered injury severity analysis using Vision LLM
- Instant veterinary hospital recommendations based on location
- One-click ambulance dispatch with driver details
- Real-time care instructions until help arrives

###  **Abuse Reporting & FIR Filing**
- Report animal abuse incidents with evidence (photos/videos)
- Optional culprit photo upload for identification
- AI analysis of abuse severity and legal recommendations
- Automatic FIR filing with police notification
- Case tracking with FIR number

###  **Case Status Dashboard**
- Track all reported cases (injury & abuse)
- View complete case details including:
  - Animal photos and incident images
  - Hospital information (name, contact, fees, location, speciality)
  - Ambulance driver details
  - FIR numbers and police status
  - AI analysis reports
- Filter by case type (Injury/Abuse)

### **AI Sathi - Smart Assistant**
- 24/7 AI-powered animal welfare assistant
- Provides first aid guidance for injuries
- Explains animal welfare laws (IPC 428, 429, PCA Act 1960)
- Case-specific advice based on your reported incidents
- Answers questions about veterinary care and legal procedures

###  **Smart Features**
- Vision AI analyzes injury severity from photos
- Automatic hospital recommendations based on case urgency
- Driver contact and hospital details for complete transparency
- Evidence preservation with photo storage
- Multi-case tracking system

## Tech Stack

### **Frontend & Framework**
- **Streamlit** - Interactive web application
- **HTML/CSS** - Custom styling with gradient themes
- **Font Awesome** - Professional icons

### **AI & Machine Learning**
- **Groq API** - Fast LLM inference
- **Llama 4 Scout 17B** - Vision model for injury analysis
- **Llama 3.3 70B** - Text generation for assistance

### **Backend**
- **Python 3.10** - Core application logic
- **Base64** - Image encoding and storage
- **Session State Management** - Case tracking

##  How It Works

### **For Injury Cases:**
1. User reports injured animal with photo and description
2. AI analyzes injury severity and provides immediate assessment
3. System recommends nearby veterinary hospitals with specialities
4. User selects hospital and calls ambulance
5. Driver details and care instructions provided instantly
6. Case tracked in dashboard with full transparency

### **For Abuse Cases:**
1. User reports abuse incident with evidence photos
2. Optional culprit photo upload for identification
3. AI analyzes severity and suggests legal actions
4. User files FIR with one click
5. Police notified with case details and FIR number
6. Legal guidance provided by AI assistant

### **AI Assistant Flow:**
- User asks questions about animal care, laws, or their case
- AI provides context-aware responses using case details
- Includes hospital info, driver contacts, and legal guidance
- Maintains conversation history for continuous support

##  Installation

```bash
# Clone the repository
git clone https://github.com/tumblr-byte/-PawAlert.git
cd pawalert

# Install dependencies
pip install requirements.txt

# Set up Groq API Key
# Create .streamlit/secrets.toml
echo 'GROQ_API_KEY = "your_groq_api_key_here"' > .streamlit/secrets.toml

# Or set environment variable
export GROQ_API_KEY="your_groq_api_key_here"

# Run the application
streamlit run app.py
```


We plan to expand PawAlert with multi-language support, real-time GPS tracking for ambulances, and blockchain-based evidence verification for legal cases. Additionally, we aim to implement live veterinary consultations and a donation system to ensure no animal goes untreated due to financial constraints.

---

**Made with ❤️ for our voiceless friends**

*"Be the voice they don't have. Be the hero they deserve."*

🐾 **Together, we can make a difference!**
