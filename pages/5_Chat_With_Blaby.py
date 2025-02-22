import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

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

prompt = st.chat_input()
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
else:
    st.stop()

inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(inputs, num_return_sequences=1, no_repeat_ngram_size=10)
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)[len(prompt):]

st.session_state.messages.append({"role": "assistant", "content": generated_text})
st.chat_message("assistant").write(generated_text)