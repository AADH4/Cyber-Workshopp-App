import streamlit as st
from huggingface_hub import InferenceClient
import random
import re
import time

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Fetch token securely from secrets
hf_token = st.secrets.get("HF_TOKEN", "")
HF_MODEL_REPO = "Qwen/Qwen2.5-7B-Instruct"
client = InferenceClient(api_key=hf_token)

st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.8, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

def generate_dynamic_fallback(scenario):
    """Creates a hyper-targeted phishing lure matching the exact description."""
    clean_scen = scenario.lower().strip().replace(".", "")
    
    # Financial contexts
    if any(x in clean_scen for x in ["bank", "invoice", "payment", "card", "tax", "fee"]):
        templates = [
            f"ALERT: Transaction alert for your account regarding '{scenario}'. Security hold placed. Authorize immediately to avoid suspension: http://secure-vault-auth.net",
            f"Notice: Urgent payment correction required for '{scenario}'. Overdue status will incur a penalty within 24h. Remit instantly: http://billing-portal-pay.org"
        ]
    # Delivery/Shipping contexts
    elif any(x in clean_scen for x in ["usps", "package", "delivery", "post", "shipment", "mail"]):
        templates = [
            f"USPS Notice: Your parcel relating to '{scenario}' has been suspended due to an incorrect address string. Fix details now to clear shipping: http://track-package-usps.com",
            f"ALERT: Delivery failure notice for '{scenario}'. Package held at regional sorting center. Schedule redelivery fee ($1.50): http://redeliver-post-hub.info"
        ]
    # General corporate / Account login contexts
    else:
        templates = [
            f"Security Portal: Critical login update requested for '{scenario}'. Access will expire in 12 hours. Re-authenticate here: http://secure-login-portal.org",
            f"Notification: Action required on your application for '{scenario}'. Review the updated status files immediately: http://review-application-check.net"
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
                                "for authorized educational drills. You must create a hyper-specific, realistic lure "
                                "tailored EXACTLY to the user's description. Avoid generic boilerplate templates.\n"
                                "RULES:\n"
                                "1. Incorporate precise details from the scenario naturally.\n"
                                "2. Emulate historical spam: use lowercase, shorthand text, and intense urgency.\n"
                                "3. Output MUST be exclusively in English. No Chinese characters or symbols.\n"
                                "4. Output ONLY the raw SMS text, keeping it under 160 characters total."
                            )
                        },
                        {
                            "role": "user", 
                            "content": f"Generate a highly specific, realistic spam SMS text based ONLY on this setup: {user_scenario}"
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
                    # Activate our new context-aware safety net
                    clean_text = generate_dynamic_fallback(user_scenario)
                    generation_method = "Local Context-Aware Fail-Safe Engine (API Offline)"
            
            # Simulated telemetry tracking display
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.005)
                progress_bar.progress(i + 1)
                
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
            
            # 🛡️ THE SECURITY SHIELD (Cyber for AI)
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
            
            # 🤖 THE AI CLASSIFICATION ROUTINE (AI for Cyber)
            else:
                with st.spinner("🧠 Scanning text and extracting safety telemetry..."):
                    try:
                        defense_payload = [
                            {
                                "role": "system", 
                                "content": (
                                    "You are an expert AI threat analyst running an SMS security gateway. "
                                    "Analyze the incoming text for phishing indicators. Respond strictly in this format:\n"
                                    "RISK: [Score 0 to 100]\n"
                                    "EXPLANATION: [A 1-sentence analytical reason detailing the psychological hooks used]"
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
                            temperature=0.1
                        )
                        
                        analysis_output = response.choices.message.content.strip()
                        
                        risk_match = re.search(r"RISK:\s*(\d+)", analysis_output)
                        explanation_match = re.search(r"EXPLANATION:\s*(.*)", analysis_output)
                        
                        extracted_risk = int(risk_match.group(1)) if risk_match else 50
                        extracted_explanation = explanation_match.group(1) if explanation_match else "Suspicious payload structure identified."
                        
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
                        if "http" in suspicious_text.lower() or "urgent" in suspicious_text.lower():
                            st.error("❌ SUSPECTED SPAM SIGNATURE FLAGGED (Deterministic Engine Fallback)")
                        else:
                            st.success("✅ CLEAN (Deterministic Engine Fallback)")
        else:
