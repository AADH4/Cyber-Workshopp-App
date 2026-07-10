import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# Initialize the lightweight serverless API client
# (Using the baseline Qwen model to guarantee stability over a LoRA adapter file)
HF_MODEL_REPO = "Qwen/Qwen2.5-1.5B-Instruct" 
client = InferenceClient(model=HF_MODEL_REPO)

st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.7, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

# --- TAB 1: OFFENSIVE GENERATION ENGINE ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            with st.spinner("🌐 Routing request through Hugging Face Cloud Infrastructure..."):
                try:
                    # Construct your instruction prompt cleanly
                    prompt_input = (
                        f"<|im_start|>system\n"
                        f"You are a cybersecurity assistant trained to generate mock SMS text phishing templates for authorized educational drills. "
                        f"Strictly emulate historical spam styles: use lowercase, shorthand text, abbreviations, and urgent calls to action. "
                        f"Keep the final output under 160 characters total.<|im_end|>\n"
                        f"<|im_start|>user\nGenerate a short, urgent spam SMS message based on this scenario: {user_scenario}<|im_end|>\n"
                        f"<|im_start|>assistant\n"
                    )
                    
                    response = client.text_generation(
                        prompt_input,
                        max_new_tokens=80,
                        temperature=temperature,
                        do_sample=True
                    )
                    
                    # Clean up any leftover chat tokens safely
                    clean_text = str(response).split("<|im_start|>")[0].strip()
                    
                    st.subheader("🚨 Generated Output Result:")
                    st.code(clean_text, language="text")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Character Count", len(clean_text))
                    col2.metric("SMS Boundary Compliance", "Pass" if len(clean_text) <= 160 else "Fail")
                    
                except Exception as e:
                    st.error(f"Operational API Exception: {str(e)}")
        else:
            st.warning("Please input a target scenario before initiating generation.")

# --- TAB 2: DEFENSIVE SCANNER ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Awaiting defensive classification weights layout...")
