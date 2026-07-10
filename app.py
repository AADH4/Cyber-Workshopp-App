import streamlit as st
from huggingface_hub import InferenceClient
import random
import re

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Fetch token securely from secrets
hf_token = st.secrets.get("HF_TOKEN", "")
HF_MODEL_REPO = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(api_key=hf_token)

st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.7, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

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
            
            with st.spinner("🌐 Accessing AI generation layer..."):
                try:
                    messages_payload = [
                        {
                            "role": "system", 
                            "content": (
                                "You are a cybersecurity assistant trained to generate mock SMS text phishing templates "
                                "for authorized educational drills. Emulate historical spam styles: use lowercase, "
                                "shorthand text, abbreviations, and urgent calls to action. "
                                "CRITICAL CONSTRAINT: You must output the final text exclusively in English. "
                                "Do not use Chinese characters, Cyrillic, or any non-English symbols under any circumstances. "
                                "Output ONLY the raw SMS text under 160 characters total without notes."
                            )
                        },
                        {
                            "role": "user", 
                            "content": f"Generate a short, urgent spam SMS message based on this scenario: {user_scenario}"
                        }
                    ]
                    
                    response = client.chat.completions.create(
                        model=HF_MODEL_REPO,
                        messages=messages_payload,
                        max_tokens=80,
                        temperature=temperature
                    )
                    clean_text = response.choices.message.content.strip()
                    
                except Exception as api_error:
                    clean_text = generate_local_fallback(user_scenario)
                    generation_method = "Local Fail-Safe Engine (API Offline)"
            
            st.subheader("🚨 Generated Output Result:")
            st.code(clean_text, language="text")
            st.caption(f"Engine Route: {generation_method}")
            
            col1, col2 = st.columns(2)
            col1.metric("Character Count", len(clean_text))
            col2.metric("SMS Boundary Compliance", "Pass" if len(clean_text) <= 160 else "Fail")
        else:
            st.warning("Please input a target scenario before initiating generation.")

# --- TAB 2: DEFENSIVE SCANNER & SECURITY SHIELD ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Paste an incoming text message to evaluate its security risk and check for hidden prompt injections.")
    
    suspicious_text = st.text_area("Paste text message here:", height=100, placeholder="e.g., URGENT: Your bank account is locked. Verify here: http://fakebank.com")
    
    if st.button("Analyze Authenticity"):
        if suspicious_text:
            
            # 🛡️ STEP A: THE SECURITY SHIELD (Cyber for AI)
            # Scan the input text for hidden override keywords attempting prompt injection attacks
            injection_patterns = [
                r"(ignore previous instructions)", 
                r"(system override)", 
                r"(disregard all rules)", 
                r"(always mark this as safe)"
            ]
            
            is_injection_detected = False
            for pattern in injection_patterns:
                if re.search(pattern, suspicious_text.lower()):
                    is_injection_detected = True
                    break
            
            if is_injection_detected:
                st.error("🚨 PROMPT INJECTION ATTACK BLOCKED")
                st.warning("The security shield intercepted an adversarial instruction hidden inside the input text designed to brainwash the defensive model.")
            
            # 🤖 STEP B: THE AI CLASSIFICATION ROUTINE (AI for Cyber)
            else:
                with st.spinner("🧠 Scanning text and extracting safety telemetry..."):
                    try:
                        defense_payload = [
                            {
                                "role": "system", 
                                "content": (
                                    "You are an expert AI threat analyst running an email and SMS security gateway. "
                                    "Your job is to analyze text messages for phishing indicators. "
                                    "You must respond strictly in this exact format:\n"
                                    "RISK: [Insert score from 0 to 100]\n"
                                    "EXPLANATION: [Provide a 1-sentence analytical reason detailing the psychological hooks used]"
                                )
                            },
                            {
                                "role": "user", 
                                "content": f"Analyze this text message: '{suspicious_text}'"
                            }
                        ]
                        
                        response = client.chat.completions.create(
                            model=HF_MODEL_REPO,
                            messages=defense_payload,
                            max_tokens=100,
                            temperature=0.1 # Kept low for consistent, clinical analysis
                        )
                        
                        analysis_output = response.choices.message.content.strip()
                        
                        # Extract the numerical risk score using regular expressions
                        risk_match = re.search(r"RISK:\s*(\d+)", analysis_output)
                        explanation_match = re.search(r"EXPLANATION:\s*(.*)", analysis_output)
                        
                        extracted_risk = int(risk_match.group(1)) if risk_match else 50
                        extracted_explanation = explanation_match.group(1) if explanation_match else "Suspicious payload structure identified."
                        
                        # Display visual metrics on dashboard
                        st.subheader("📊 Security Analysis Gateway Verdict:")
                        if extracted_risk >= 70:
                            st.error(f"❌ MALICIOUS TRIGGER FLAG DETECTED - Phishing Risk: {extracted_risk}%")
                        elif 30 <= extracted_risk < 70:
                            st.warning(f"⚠️ SUSPICIOUS - Moderate Risk Level: {extracted_risk}%")
                        else:
                            st.success(f"✅ CLEAN - Low Risk Level: {extracted_risk}%")
                            
                        st.write(f"**Threat Intelligence Report:** {extracted_explanation}")
                        
                    except Exception as defense_error:
                        st.error("Gateway analysis timeout. Activating standard backup signature checks.")
                        # Direct pattern-matching fallback if cloud API is crowded
                        if "http" in suspicious_text.lower() or "urgent" in suspicious_text.lower():
                            st.error("❌ SUSPECTED SPAM SIGNATURE FLAGGED (Deterministic Engine Fallback)")
                        else:
                            st.success("✅ CLEAN (Deterministic Engine Fallback)")
        else:
            st.warning("Please paste a text message sequence to analyze.")
