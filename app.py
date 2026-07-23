import streamlit as st
from groq import Groq
import joblib
import re
import os

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Initialize Generative AI Assets (Offensive Side)
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = Groq(api_key=groq_key)
MODEL_ID = "llama-3.1-8b-instant"

# 2. Initialize Custom Machine Learning Assets (Defensive Side)
@st.cache_resource
def load_custom_defense_engine():
    """Loads your local custom-trained model files from the GitHub repository folder."""
    model_path = "sms_phishing_detector.joblib"
    vectorizer_path = "tfidf_vectorizer.joblib"
    
    # Check if files have been successfully uploaded to the repository path
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return model, vectorizer
    return None, None

classifier, vectorizer = load_custom_defense_engine()

# 3. Sidebar UI Parameters
st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.8, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])


# --- TAB 1: OFFENSIVE GENERATION ENGINE (AI for Cyber) ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    st.write("Input a scenario to force the model to write an authentic, custom smishing text.")
    
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            with st.spinner("⚡ Querying generative matrix..."):
                try:
                    response = client.chat.completions.create(
                        model=MODEL_ID,
                        messages=[
                            {
                                "role": "system", 
                                "content": (
                                    "You are an expert cybersecurity simulation engine. Generate a hyper-realistic "
                                    "SMS phishing message based EXACTLY on the user's scenario. Use lowercase, "
                                    "text shorthand, typos, and intense urgency. Include a fake lookalike link. "
                                    "Output ONLY plain English text under 160 characters total. No introductory greetings or notes."
                                )
                            },
                            {"role": "user", "content": f"Generate an authentic smishing text for: {user_scenario}"}
                        ],
                        temperature=temperature,
                        max_tokens=80
                    )
                    clean_text = response.choices[0].message.content.strip()
                    st.subheader("🚨 Generated Output Result:")
                    st.code(clean_text, language="text")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Character Count", len(clean_text))
                    col2.metric("SMS Boundary Compliance", "Pass" if len(clean_text) <= 160 else "Fail")
                except Exception as e:
                    st.error(f"API Execution Exception: {str(e)}")
        else:
            st.warning("Please input a target scenario before initiating generation.")


# --- TAB 2: DEFENSIVE SCANNER (Your Own Custom Model + Shield) ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Evaluate unstructured text payloads instantly using your custom-trained machine learning architecture.")
    
    suspicious_text = st.text_area("Paste text message here:", height=100, key="portal_detector_input")
    
    if st.button("Analyze Authenticity", key="portal_detector_btn"):
        if suspicious_text:
            
            # 🛡️ THE SECURITY SHIELD FIREWALL (Cyber for AI)
            # Scans text stream for hidden injection commands before executing categorization
            injection_patterns = [r"(ignore previous instructions)", r"(system override)", r"(disregard all rules)", r"(always mark this as safe)"]
            is_injection_detected = any(re.search(p, suspicious_text.lower()) for p in injection_patterns)
            
            if is_injection_detected:
                st.error("🚨 PROMPT INJECTION ATTACK BLOCKED")
                st.warning("The security shield intercepted an adversarial instruction hidden inside the input text.")
            
            # 🤖 YOUR CUSTOM TRAINED MODEL WORKFLOW (AI for Cyber)
            else:
                if classifier and vectorizer:
                    with st.spinner("⚡ Executing local neural vector classification..."):
                        # Transform raw text string input into identical coordinate dimensions as the dataset
                        transformed_text = vectorizer.transform([suspicious_text])
                        
                        # Calculate mathematical class probabilities
                        probability = classifier.predict_proba(transformed_text)
                        
                        # Extract the explicit phishing probability percentage (index 1 is the spam class)
                        risk_percentage = int(probability[0][1] * 100)
                        
                        st.subheader("📊 Custom Model Gateway Verdict:")
                        if risk_percentage >= 70:
                            st.error(f"❌ MALICIOUS PAYLOAD IDENTIFIED - Phishing Probability: {risk_percentage}%")
                            st.write("**Threat Analysis Note:** This message matches structural markers found inside your historical training spam database.")
                        elif 30 <= risk_percentage < 55:
                            st.warning(f"⚠️ SUSPICIOUS - Moderate Risk Profile: {risk_percentage}%")
                            st.write("**Threat Analysis Note:** Elements of this text showcase borderline structural irregularities.")
                        else:
                            st.success(f"✅ CLEAN MESSAGE VALIDATED - Phishing Probability: {risk_percentage}%")
                            st.write("**Threat Analysis Note:** The syntax reads as safe, baseline user correspondence.")
                else:
                    st.error("Model artifacts missing. Please ensure your saved .joblib files are uploaded to your GitHub repository.")
        else:
            st.warning("Please paste a text message sequence to analyze.")
