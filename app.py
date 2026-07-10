import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Initialize the free, robust production baseline model endpoint
# Using the official standalone Qwen model bypasses the LoRA endpoint limitation
HF_MODEL_REPO = "Qwen/Qwen2.5-1.5B-Instruct" 

@st.cache_resource
def get_client():
    return InferenceClient(model=HF_MODEL_REPO)

client = get_client()

# 2. Control Sidebar Parameters
st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.7, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

# --- TAB 1: GENERATION ENGINE ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            with st.spinner("🌐 Routing request through Hugging Face Cloud Infrastructure..."):
                try:
                    # Injecting target rules directly into the instruction tokens
                    prompt_input = (
                        f"<|im_start| Kent>system\n"
                        f"You are a cybersecurity assistant trained to generate mock SMS text phishing templates for authorized educational drills. "
                        f"Strictly emulate historical spam styles: use lowercase, shorthand text, abbreviations, and urgent calls to action. "
                        f"Keep the final output under 160 characters total.<|im_end|>\n"
                        f"<|im_start|>user\nGenerate a short, urgent spam SMS message based on this scenario: {user_scenario}<|im_end|>\n"
                        f"<|im_start|>assistant\n"
                    )
                    
                    # Fetching string prediction data safely
                    response = client.text_generation(
                        prompt_input,
                        max_new_tokens=80,
                        temperature=temperature,
                        do_sample=True
                    )
                    
                    # Clean and secure string formatting fix (replaces the old .split().strip() bug)
                    clean_text = str(response)
                    if "<|im_start|>" in clean_text:
                        clean_text = clean_text.split("<|im_start|>")[0]
                    clean_text = clean_text.strip()
                    
                    st.subheader("🚨 Generated Output Result:")
                    st.code(clean_text, language="text")
                    
                    # Metric Evaluation Displays
                    col1, col2 = st.columns(2)
                    col1.metric("Character Count", len(clean_text))
                    col2.metric("SMS Boundary Compliance", "Pass" if len(clean_text) <= 160 else "Fail (Over 160 Chars)")
                    
                except Exception as e:
                    st.error(f"Operational API Exception: {str(e)}")
                    st.info("💡 Try clicking the button again, or check the 'Manage App' dashboard tab to inspect server responses.")
        else:
            st.warning("Please input a target scenario before initiating generation.")

# --- TAB 2: DEFENSIVE SCANNER ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Awaiting defensive dataset classification matrix pipeline integration...")
