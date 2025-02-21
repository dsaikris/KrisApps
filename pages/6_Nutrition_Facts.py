import streamlit as st
import pandas as pd
import numpy as np
import json

st.set_page_config(
    page_title="ExploreNutrition",
    page_icon="👋",
)

st.write("# ExploreNutrition");
foundationFoods = "foundationFoods.json"
import matplotlib.pyplot as plt

# Load the JSON file
with open(foundationFoods, 'r') as f:
    data = json.load(f)

# Convert JSON data to DataFrame
df = pd.json_normalize(data)

st.markdown("""Explore Nutrition data `foundationFoods.json`
            
Coming soon!
""")