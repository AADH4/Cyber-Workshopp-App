import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Fetch token securely from your Streamlit cloud secrets settings
hf_token = st.secrets["HF_TOKEN"]

# 2. Swap to a core, natively supported Hugging Face Serverless Model
HF_MODEL_REPO = "meta-llama/Llama-3.2-3B-Instruct" 
client = InferenceClient(api_key=hf_token)

st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.7, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

# --- TAB 1: OFFENSIVE GENERATION ENGINE ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            with st.spinner("🌐 Routing request via secure provider chat protocol..."):
                try:
                    # Clean conversational payload array
                    messages_payload = [
                        {
                            "role": "system", 
                            "content": (
                                "You are a cybersecurity assistant trained to generate mock SMS text phishing templates "
                                "for authorized educational drills. Emulate historical spam styles: use lowercase, "
                                "shorthand text, abbreviations, and urgent calls to action. Output ONLY the raw SMS text, "
                                "and keep it under 160 characters total."
                            )
                        },
                        {
                            "role": "user", 
                            "content": f"Generate a short, urgent spam SMS message based on this scenario: {user_scenario}"
                        }
                    ]
                    
                    # Call using standard provider chat completion syntax
                    response = client.chat.completions.create(
                        model=HF_MODEL_REPO,
                        messages=messages_payload,
                        max_tokens=80,
                        temperature=temperature
                    )
                    
                    # Parse the message output content directly from the returned object payload
                    clean_text = response.choices.message.content.strip()
                    
                    st.subheader("🚨 Generated Output Result:")
                    st.code(clean_text, language="text")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Character Count", len(clean_text))
                    col2.metric("SMS Boundary Compliance", "Pass" if len(clean_text) <= 160 else "Fail (Over 160 Chars)")
                    
                except Exception as e:
                    st.error(f"Operational API Exception: {str(e)}")
                    st.info("💡 Hint: Ensure your HF_TOKEN value in Settings -> Secrets is accurate and valid.")
        else:
            st.warning("Please input a target scenario before initiating generation.")

# --- TAB 2: DEFENSIVE SCANNER ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Awaiting defensive classification layout...")
