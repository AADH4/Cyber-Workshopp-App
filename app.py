import streamlit as st
from huggingface_hub import InferenceClient
import random

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Fetch token securely from your Streamlit cloud secrets settings
hf_token = st.secrets.get("HF_TOKEN", "")

# 2. Use a globally supported 7B model routed automatically by HF's partner cluster
HF_MODEL_REPO = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(api_key=hf_token)

st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.7, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

# Helper function to generate high-quality fallback text if the API is offline
def generate_local_fallback(scenario):
    templates = [
        f"URGENT: Your action is required regarding your recent request for: '{scenario}'. Click to resolve immediately: http://secure-verify-auth.com",
        f"ALERT: Security notification regarding '{scenario}'. Unauthorized login detected nearby. Access your dashboard immediately to secure access: http://service-alert-login.net",
        f"Notification: Update pending on your profile for '{scenario}'. Avoid service suspension by updating details within 24 hours: http://update-portal-check.org"
    ]
    return random.choice(templates)

# --- TAB 1: OFFENSIVE GENERATION ENGINE ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            clean_text = ""
            generation_method = "AI Cloud Generation"
            
            with st.spinner("🌐 Connecting to Hugging Face serverless compute architecture..."):
                try:
                    messages_payload = [
                        {
                            "role": "system", 
                            "content": (
                                "You are a cybersecurity assistant trained to generate mock SMS text phishing templates "
                                "for authorized educational drills. Emulate historical spam styles: use lowercase, "
                                "shorthand text, abbreviations, and urgent calls to action. Output ONLY the raw SMS text, "
                                "and keep it under 160 characters total. Do not include introductory notes or pleasantries."
                            )
                        },
                        {
                            "role": "user", 
                            "content": f"Generate a short, urgent spam SMS message based on this scenario: {user_scenario}"
                        }
                    ]
                    
                    # Execute modern cloud chat completion syntax
                    response = client.chat.completions.create(
                        model=HF_MODEL_REPO,
                        messages=messages_payload,
                        max_tokens=80,
                        temperature=temperature
                    )
                    clean_text = response.choices[0].message.content.strip()
                    
                except Exception as api_error:
                    # If the API hits a routing error or is overloaded, activate the safety net
                    clean_text = generate_local_fallback(user_scenario)
                    generation_method = "Local Fail-Safe Engine (API Offline)"
                    st.sidebar.warning(f"Note: Switched to Local Engine due to cloud routing limitations.")
            
            # --- RENDER RESULTS PANEL ---
            st.subheader("🚨 Generated Output Result:")
            st.code(clean_text, language="text")
            
            st.caption(f"Engine Route Utilized: {generation_method}")
            
            col1, col2 = st.columns(2)
            col1.metric("Character Count", len(clean_text))
            col2.metric("SMS Boundary Compliance", "Pass" if len(clean_text) <= 160 else "Fail (Over 160 Chars)")
            
        else:
            st.warning("Please input a target scenario before initiating generation.")

# --- TAB 2: DEFENSIVE SCANNER ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Ready to build out your defensive verification matrix code block here next...")
