import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import warnings
warnings.filterwarnings('ignore')
os.environ['TRANSFORMERS_VERBOSITY'] = 'error' 

model_name = "openai-community/gpt2"
@st.cache_resource
def tokenizer(model_name):
    return AutoTokenizer.from_pretrained(model_name)

@st.cache_resource
def model(model_name):
    return AutoModelForCausalLM.from_pretrained(model_name)

with st.spinner(f"""Loading ...
                As GenAI business is costly, I am doing a cold start to save some ducks and bucks.
                See source code to understand how `@streamlit.cache_resource` and `streamlit.spinner` are used.
                Downloading {model_name} from Hugging Face `transformers` can take upto 3-5 minutes, please be patient.
                """):
    model = model(model_name)
    tokenizer = tokenizer(model_name)

st.markdown(f"## Blaby - A toy chatbot backed by {model_name} model")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant",
         "content": "Ask me a good question and I will answer it. Otherwise, I will go crazy."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

userPrompt = st.chat_input()
if userPrompt:
    st.session_state.messages.append({"role": "user", "content": userPrompt})
    st.chat_message("user").write(userPrompt)
else:
    st.stop()

system_prompt = """You are Blaby, a friendly and helpful chatbot. Here are some guidelines for your responses:
- Your responses should be clear, concise, and relevant to the user's query.
- Answer to a 5 year old child, so, keep it simple and easy to understand. So, no contraversial topics or adult language.
- User goes first and you follow, so, do not start the conversation.
- If you don't know the answer, it's okay to say so. You can also ask the user for more information if needed.
- Always be polite and respectful.
- Avoid repeating the same information multiple times.
- If the user asks for a specific format (like a list or a summary), try to follow that format.
- Use emojis to make the conversation more engaging, but don't overdo it.
"""
# Separate system prompt and user prompt for better results
prompt = system_prompt + "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]) + "\nassistant:"
inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    inputs,
    max_length=inputs.shape[1] + 50,  # Limit response length for chat optimization
    num_return_sequences=1, 
    no_repeat_ngram_size=3,  # Reduce repetition for better chat responses
    temperature=0.7,  # Add randomness for more natural responses
    top_k=50,  # Limit to top-k tokens for diversity
    top_p=0.9  # Use nucleus sampling for better quality
)
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)[len(prompt):]
generated_text = generated_text.split("\n", 1)[0].strip()
st.session_state.messages.append({"role": "assistant", "content": generated_text})
st.chat_message("assistant").write(generated_text)