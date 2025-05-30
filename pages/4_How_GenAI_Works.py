import streamlit as st
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import warnings
warnings.filterwarnings('ignore')
os.environ['TRANSFORMERS_VERBOSITY'] = 'error' 

model_name = "openai-community/gpt2"
@st.cache_resource
def tokenizerGpt(model_name):
    return AutoTokenizer.from_pretrained(model_name)

@st.cache_resource
def modelGpt(model_name):
    return AutoModelForCausalLM.from_pretrained(model_name)

st.set_page_config(
    page_title="How GenAI Works",
    page_icon="👋",
)

with st.spinner(f"""Loading ...
                As GenAI business is costly, I am doing a cold start to save some ducks and bucks.
                See source code to understand how `@streamlit.cache_resource` and `streamlit.spinner` are used.
                Downloading {model_name} from Hugging Face `transformers` can take upto 3-5 minutes, please be patient.
                """):
    model = modelGpt(model_name)
    tokenizer = tokenizerGpt(model_name)

col1, col2  = st.columns(2)
with col1:
    st.markdown("## Past some text here")
    text_input = st.text_area("","""I have no special talents. I am only passionately curious. - by Albert Einstein
""", height=500, max_chars=300)
    if not text_input: text_input=""
    inputs = tokenizer.encode(text_input, return_tensors="pt").to(model.device)
    outputs = model.generate(inputs, max_length=inputs.shape[1] + 50, num_return_sequences=1, no_repeat_ngram_size=4)
with col2:
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    st.markdown(f"## GenAI says! 👋")
    st.text_area("", generated_text + " ..", height=500, disabled=True)

def plot_token_bars(token_ids, tokens, title, dispaly_function):
    fig, ax = plt.subplots()
    bars = ax.bar(range(len(token_ids)), token_ids, tick_label=tokens)
    plt.xticks(rotation=90)
    for bar, token in zip(bars, tokens):
        yval = bar.get_height()
        font_size = max(8, 100 // len(tokens))
        ax.text(bar.get_x() + bar.get_width()/2, yval * 0.2, dispaly_function(token, yval), ha='center', va='bottom', rotation=90, fontsize=font_size)
    ax.set_xticks(range(0, len(tokens), max(1, len(tokens) // 5)))
    ax.set_xticklabels(range(0, len(tokens), max(1, len(tokens) // 5)), rotation=90)
    ax.set_ylabel(title)
    st.pyplot(fig)

def display(token, yval):
    return f"{token} = {yval}"

def displayNone(token, yval):
    return ""

st.markdown("## How did it do?")
st.markdown("""GPT2 does in in 3 main steps.
1. Encode tokens
1. Generate output tokens
1. Decode output tokens.
### Encode tokens
GPT2 transformer will convert input words into tokens and then encode them to a number. Think of it like a dictionary of all words/tokens and the number is its index.
Actually, it will use byte pair encoding or compression algorithm to get partial words also mapped to unique id. It also uses sub word level tokenization scheme and retains the knowledge like words `book, bookings, books` all have the root word `book` so it could be modeled as one token.
I observed the tokens are similar for similar text. Below are the tokens for your text. Also, you can see few special characters like `Ġ` and `Ċ` are used to denote starting or words and new lines.
""")
tokens = tokenizer.convert_ids_to_tokens(inputs[0])
token_ids = inputs[0].numpy()
st.code(f"Tokens:\n{tokens}")
st.code(f"Tokens as numbers:\n{token_ids}")
plot_token_bars(token_ids, tokens, "Input Tokens", dispaly_function=display)

st.markdown("""### Generate output tokens
Then it will use its large neural network to get the next token number and then the next token number for 50 times. I set is to 50 here you can set a larger one for more generated output. It means the neural network is used to generate kind of word by word.
It will do many things in this step like
1. Token embedding : Since we need to capture the semantic meaning of words like `cat` and `kitten` are similar we endode each token number into 768 numbers which is called vectors or tensors. The values were optimized by the pre training done by OpenAI and are now static numbers in the model.
1. Position embedding : Also we need to know when in the sentence or paragraph a particular token has occurred like `2` in `The cat is sleeping.` and 6 in `the doorbell woke up the cat`. GPT-2 uses absolute position vectors again of 768 numbers. When they trained the neural network they used 1024 token chunks to train in batches of 512. These numbers highly depends on the hardware capability and implementation of pre training. This 1024 is called `context` length as it means the model will only care for token positions in this range. To continue the context when the batches are created typically some overlap is feed in to the pre-training it is called stride length which would be 512 about half of the context length for GPT-2.
1. Input embedding : The final input that is feed into the generator  =  token embeddings + position embeddings for each token in the context chunk or the context sequence.
1. Generation : Just generate the next token using generator neural network, that is forward pass the neural network. It is pretty interesting to know how it works and trained. I will update this sections as I learn about it.

This the the huge neural network or collection of neural networks that were pre trained by OpenAI spending a lot of compute power and feeding around 44TB of public internat data.
""")
output_tokens = tokenizer.convert_ids_to_tokens(outputs[0])
output_token_ids = outputs[0].numpy()
st.code(f"Token numbers generated by GenAi neural network:\n{output_token_ids}")
st.markdown("""### Decode output tokens
Finally, it will convert output token numbers into words/tokens.
""")
plot_token_bars(output_token_ids, output_tokens, "Output Tokens",dispaly_function=displayNone)
st.code(f"Tokens:\n{output_tokens}")
st.text_area("Generated text", generated_text + " ..", height=500, disabled=True)
st.markdown("""## Finally the code that you can take away
""")
st.code("""
import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import warnings
warnings.filterwarnings('ignore')
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

model_name = "openai-community/gpt2"
@st.cache_resource
def tokenizerGpt(model_name):
    return AutoTokenizer.from_pretrained(model_name)

@st.cache_resource
def modelGpt(model_name):
    return AutoModelForCausalLM.from_pretrained(model_name)
        
text_input ="I have no special talents. I am only passionately curious. - by Albert Einstein"
inputs = tokenizer.encode(text_input, return_tensors="pt").to(model.device)
outputs = model.generate(inputs, max_length=inputs.shape[1] + 50, num_return_sequences=1, no_repeat_ngram_size=4)
""")

st.markdown("""### Embeddings for first 3 tokens out of curiosity
""")
st.code(f"For tokens {inputs[0][0:3]}")
st.code(f"{model.transformer.wte.weight[inputs[0][0:3]]}")
st.code(f"{model.transformer.wpe.weight[inputs[0][0:3]]}")
