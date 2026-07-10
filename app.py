import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Initialize the free Hugging Face Serverless Client
# Replace 'your-username' with your actual Hugging Face profile username
HF_MODEL_REPO = "your-username/my-custom-smish-generator" 
client = InferenceClient(model=HF_MODEL_REPO)

# 2. Control Sidebar Parameters
st.sidebar.header("⚙️ Simulation Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.2, 1.3, 0.8, 0.1)

tab1, tab2 = st.tabs(["🔥 Offensive Generation Engine", "🛡️ Defensive Scanning Gateway"])

# --- TAB 1: GENERATION ENGINE ---
with tab1:
    st.header("Generate Realistic Security Training Scenarios")
    user_scenario = st.text_input("Enter a training scenario:", placeholder="e.g., Post Office missed parcel package delivery fee scam.")
    
    if st.button("Generate Smishing Blueprint"):
        if user_scenario:
            with st.spinner("🌐 Querying your hosted cloud model API..."):
                try:
                    # Construct your instruction-following prompt
                    prompt_input = (
                        f"<|im_start|>system\nYou are a cyber security training assistant. Generate a realistic phishing SMS template.<|im_end|>\n"
                        f"<|im_start|>user\nGenerate a text message based on this scenario: {user_scenario}<|im_end|>\n"
                        f"<|im_start|>assistant\n"
                    )
                    
                    # Make a fast, free serverless request to Hugging Face
                    response = client.text_generation(
                        prompt_input,
                        max_new_tokens=80,
                        temperature=temperature,
                        do_sample=True
                    )
                    
                    # Clean up the output string
                    generated_text = response.split("<|im_start|>")[0].strip()
                    
                    st.subheader("🚨 Generated Output Result:")
                    st.code(generated_text, language="text")
                    
                except Exception as e:
                    st.error(f"API Connection Error: {str(e)}")
                    st.info("💡 Make sure you have successfully uploaded your model folder to Hugging Face and that the repo is set to Public!")

# --- TAB 2: DEFENSIVE SCANNER ---
with tab2:
    st.header("Security Scanning Gateway")
    st.write("Awaiting connection to your upcoming Defensive Scanner weights...")
