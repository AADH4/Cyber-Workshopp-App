import streamlit as st
from groq import Groq
import re

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Initialize the ultra-fast Groq Client
groq_key = st.secrets.get("GROQ_API_KEY", "")
client = Groq(api_key=groq_key)

# We use Llama 3.1 8B because it processes text instantly and handles context beautifully
MODEL_ID = "llama-3.1-8b-instant"

st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.8, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

# --- TAB 1: OFFENSIVE GENERATION ENGINE ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    st.write("Input a scenario to force the model to write an authentic, custom smishing text.")
    
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            with st.spinner("⚡ Querying high-speed LLM processing matrix..."):
                try:
                    # Explicit behavioral mapping forcing the model to mirror your dataset's styling rules
                    response = client.chat.completions.create(
                        model=MODEL_ID,
                        messages=[
                            {
                                "role": "system", 
                                "content": (
                                    "You are an expert cybersecurity simulation engine. Your task is to generate a hyper-realistic "
                                    "SMS phishing (smishing) message based EXACTLY on the user's scenario. Do not use generic templates.\n"
                                    "STYLING CONSTRAINTS (Mirroring real-world spam data):\n"
                                    "1. Use lowercase letters, shorthand, text abbreviations, and urgent hooks.\n"
                                    "2. Craft a unique, context-specific fake link matching the scenario (e.g., if scenario is apple, link should look like apple-claim-reward.com).\n"
                                    "3. Output MUST be exclusively in plain English. No conversational text, introductory greetings, or exit notes.\n"
                                    "4. Keep the entire final output under 160 characters total."
                                )
                            },
                            {
                                "role": "user", 
                                "content": f"Generate an authentic smishing text for this specific target scenario: {user_scenario}"
                            }
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

# --- TAB 2: DEFENSIVE SCANNER & SECURITY SHIELD ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Paste an incoming text message to evaluate its security risk and check for hidden prompt injections.")
    
    suspicious_text = st.text_area("Paste text message here:", height=100)
    
    if st.button("Analyze Authenticity"):
        if suspicious_text:
            
            # 🛡️ THE SECURITY SHIELD (Cyber for AI)
            injection_patterns = [r"(ignore previous instructions)", r"(system override)", r"(disregard all rules)", r"(always mark this as safe)"]
            is_injection_detected = any(re.search(p, suspicious_text.lower()) for p in injection_patterns)
            
            if is_injection_detected:
                st.error("🚨 PROMPT INJECTION ATTACK BLOCKED")
                st.warning("The security shield intercepted an adversarial instruction hidden inside the input text.")
            
            # 🤖 THE AI CLASSIFICATION ROUTINE (AI for Cyber)
            else:
                with st.spinner("🧠 Scanning text and extracting safety telemetry..."):
                    try:
                        response = client.chat.completions.create(
                            model=MODEL_ID,
                            messages=[
                                {
                                    "role": "system", 
                                    "content": (
                                        "You are an expert AI threat analyst running an SMS security gateway. "
                                        "Analyze the text for phishing indicators. Respond strictly in this format:\n"
                                        "RISK: [Score 0 to 100]\n"
                                        "EXPLANATION: [A 1-sentence analytical reason detailing the psychological hooks used]"
                                    )
                                },
                                {"role": "user", "content": f"Analyze this text message: '{suspicious_text}'"}
                            ],
                            temperature=0.1,
                            max_tokens=100
                        )
                        
                        analysis_output = response.choices[0].message.content.strip()
                        risk_match = re.search(r"RISK:\s*(\d+)", analysis_output)
                        explanation_match = re.search(r"EXPLANATION:\s*(.*)", analysis_output)
                        
                        extracted_risk = int(risk_match.group(1)) if risk_match else 50
                        extracted_explanation = explanation_match.group(1) if explanation_match else "Suspicious structure identified."
                        
                        st.subheader("📊 Security Analysis Gateway Verdict:")
                        if extracted_risk >= 70:
                            st.error(f"❌ MALICIOUS TRIGGER FLAG DETECTED - Phishing Risk: {extracted_risk}%")
                        elif 30 <= extracted_risk < 70:
                            st.warning(f"⚠️ SUSPICIOUS - Moderate Risk Level: {extracted_risk}%")
                        else:
                            st.success(f"✅ CLEAN - Low Risk Level: {extracted_risk}%")
                            
                        st.write(f"**Threat Intelligence Report:** {extracted_explanation}")
                        
                    except Exception as e:
                        st.error(f"Gateway connection error: {str(e)}")
        else:
            st.warning("Please paste a text message sequence to analyze.")
