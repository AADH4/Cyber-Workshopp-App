import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Fetch token securely from your Streamlit cloud secrets settings
hf_token = st.secrets["HF_TOKEN"]

# 2. Use a universally accessible, non-gated model on core Hugging Face infrastructure
HF_MODEL_REPO = "HuggingFaceH4/zephyr-7b-beta" 
client = InferenceClient(model=HF_MODEL_REPO, token=hf_token)

st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.7, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

# --- TAB 1: OFFENSIVE GENERATION ENGINE ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            with st.spinner("🌐 Connecting directly to free public model tier..."):
                try:
                    # Format standard open instruction layout
                    prompt_input = (
                        f"<|system|>\n"
                        f"You are a cybersecurity training assistant. Generate a realistic mock SMS phishing template "
                        f"for authorized corporate awareness drills. Emulate historical spam: use lowercase, "
                        f"shorthand text, typos, and urgent calls to action. Output ONLY the raw SMS text, and keep it under 160 characters.</s>\n"
                        f"<|user|>\nGenerate an SMS based on this scenario: {user_scenario}</s>\n"
                        f"<|assistant|>\n"
                    )
                    
                    # Call using the standard text_generation method (guarantees zero provider routing errors)
                    response = client.text_generation(
                        prompt_input,
                        max_new_tokens=80,
                        temperature=temperature,
                        do_sample=True
                    )
                    
                    # Isolate text string output and clean trailing structural metadata
                    clean_text = str(response).strip()
                    if "<|assistant|>" in clean_text:
                        clean_text = clean_text.split("<|assistant|>")[-1].strip()
                    if "</s>" in clean_text:
                        clean_text = clean_text.split("</s>")[0].strip()
                    
                    st.subheader("🚨 Generated Output Result:")
                    st.code(clean_text, language="text")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Character Count", len(clean_text))
                    col2.metric("SMS Boundary Compliance", "Pass" if len(clean_text) <= 160 else "Fail")
                    
                except Exception as e:
                    st.error(f"Operational API Exception: {str(e)}")
                    st.info("💡 Troubleshooting: Double-check your Streamlit Secrets string formatting.")
        else:
            st.warning("Please input a target scenario before initiating generation.")

# --- TAB 2: DEFENSIVE SCANNER ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Awaiting defensive dataset classification layout...")
