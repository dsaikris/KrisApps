import streamlit as st
from collections import Counter
from spellchecker import SpellChecker
import matplotlib.pyplot as plt
import re

st.set_page_config(
    page_title="WordAnalyzer",
    page_icon="👋",
)

css = '''
<style>
    .stTextArea textarea {
        height: 500px;
    }
</style>
'''

st.markdown("# WordAnalyzer")

st.markdown("## Past some text here")

text_input = st.text_area("","""
- I have no special talents. I am only passionately curious.
- The important thing is not to stop questioning. Curiosity has its own reason for existing.
- The true sign of intelligence is not knowledge but imagination.
- Logic will get you from A to B. Imagination will take you everywhere.
- Imagination is everything. It is the preview of life's coming attractions.
- The only source of knowledge is experience.
- All knowledge of reality starts from experience and ends in it.
- You need experience to gain wisdom.
- Anyone who has never made a mistake has never tried anything new.
- Life is like riding a bicycle. To keep your balance you must keep moving.
- Everything should be made as simple as possible, but not simpler.
- We cannot solve our problems with the same thinking we used to create them.
""")
st.write(css, unsafe_allow_html=True)

def plot_top_items(items, title, xlabel_rotation=45):
        st.write(f"{title}")
        fig, ax = plt.subplots()
        ax.bar([item for item, count in items], [count for item, count in items])
        plt.xticks(rotation=xlabel_rotation)
        ax.yaxis.set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        for i, (item, count) in enumerate(items):
            ax.text(i, count, str(count), ha='center', va='bottom')
        st.pyplot(fig)

if text_input:
    spell = SpellChecker()
    words = re.compile("([\w]+'?\w?)").findall(text_input.lower())
    misspelled = spell.unknown(words)
    
    st.markdown("## Misspelled words")
    if misspelled:
        for word in misspelled:
            st.markdown(f"> {word} -> {spell.candidates(word)}")
    else:
        st.markdown("> None!")

    st.markdown("## Top words")
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)
    plot_top_items(top_words, "Top 10 words")

    two_word_combinations = Counter(zip(words, words[1:]))
    top_two_word_combinations = two_word_combinations.most_common(10)
    plot_top_items([(f"{w1} {w2}", count) for (w1, w2), count in top_two_word_combinations], "Top 10 two-word combinations")

    three_word_combinations = Counter(zip(words, words[1:], words[2:]))
    top_three_word_combinations = three_word_combinations.most_common(10)
    plot_top_items([(f"{w1} {w2} {w3}", count) for (w1, w2, w3), count in top_three_word_combinations], "Top 10 three-word combinations")
st.markdown("## Here is the code for you to try.")
st.code("""
def plot_top_items(items, title, xlabel_rotation=45):
        st.write(f"{title}")
        fig, ax = plt.subplots()
        ax.bar([item for item, count in items], [count for item, count in items])
        plt.xticks(rotation=xlabel_rotation)
        ax.yaxis.set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        for i, (item, count) in enumerate(items):
            ax.text(i, count, str(count), ha='center', va='bottom')
        st.pyplot(fig)

if text_input:
    spell = SpellChecker()
    words = re.compile("([\w]+'?\w?)").findall(text_input.lower())
    misspelled = spell.unknown(words)
    
    st.markdown("## Misspelled words")
    if misspelled:
        for word in misspelled:
            st.markdown(f"> {word} -> {spell.candidates(word)}")
    else:
        st.markdown("> None!")

    st.markdown("## Top words")
    word_counts = Counter(words)
    top_words = word_counts.most_common(10)
    plot_top_items(top_words, "Top 10 words")

    two_word_combinations = Counter(zip(words, words[1:]))
    top_two_word_combinations = two_word_combinations.most_common(10)
    plot_top_items([(f"{w1} {w2}", count) for (w1, w2), count in top_two_word_combinations], "Top 10 two-word combinations")

    three_word_combinations = Counter(zip(words, words[1:], words[2:]))
    top_three_word_combinations = three_word_combinations.most_common(10)
    plot_top_items([(f"{w1} {w2} {w3}", count) for (w1, w2, w3), count in top_three_word_combinations], "Top 10 three-word combinations")        
""")