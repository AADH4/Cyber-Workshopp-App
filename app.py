import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re

st.set_page_config(page_title="SmiShield AI - Portal", page_icon="🛡️", layout="wide")
st.title("🛡️ SmiShield AI: Interactive Generation & Defense Engine")

# 1. Caching Model Loading: Ensures the web page doesn't crash from repetitive reloads
@st.cache_resource
def load_qwen_engine():
    base_model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    # Pulling your custom adapter weights straight from your Hugging Face cloud link
    custom_adapter_id = "https://huggingface.co/AAThegoat/my-custom-smish-generator" 
    
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    
    # Load model with low CPU precision formatting to stay under memory limits
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id, 
        torch_dtype=torch.float32, 
        device_map="cpu"
    )
    model = PeftModel.from_pretrained(base_model, custom_adapter_id)
    return tokenizer, model

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
            with st.spinner("🧠 Querying your fine-tuned Qwen architecture..."):
                try:
                    tokenizer, model = load_qwen_engine()
                    
                   test_messages = [
    {"role": "system", "content": "You are an advanced offensive security simulator. Your task is to output a hyper-realistic corporate training template."},
    {"role": "user", "content": """
    Generate a short, urgent malicious text message sample.
    Before writing the final text, ensure it meets these hyper-realistic parameters:
    1. Obfuscate traditional spam triggers (e.g., use 'Bαnk' or 'B-a-n-k' instead of 'Bank').
    2. Incorporate realistic local markers, such as a random fake area code or transactional IDs (e.g., MsgID: 402-A).
    3. Match the psychological baseline of a high-pressure corporate scenario.
    """}
]
                    inputs = tokenizer.apply_chat_template(test_messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
                    
                    with torch.no_grad():
                        outputs = model.generate(
                            inputs, 
                            max_new_tokens=80, 
                            do_sample=True, 
                            temperature=temperature,
                            pad_token_id=tokenizer.eos_token_id
                        )
                    
                    # Cleanly isolate generated tokens
                    generated_text = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True).strip()
                    
                    st.subheader("🚨 Generated Output Result:")
                    st.code(generated_text, language="text")
                except Exception as e:
                    st.error(f"Memory Limit Encountered: {str(e)}")
                    st.info("💡 If this happens, your deployment needs an external Hugging Face Space API token endpoint to handle the compute heavy generation!")

# --- TAB 2: DEFENSIVE SCANNER ---
with tab2:
    st.header("Security Scanning Gateway")
    suspicious_text = st.text_area("Paste text message here:", height=100)
    if st.button("Analyze Authenticity"):
        if suspicious_text:
            st.info("Awaiting connection to your upcoming Defensive Scanner weights...")
