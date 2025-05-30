import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="ToyTaxCalc",
    page_icon="👋",
)

st.write("# Toy Tax Calculator");
st.write("""
        A sample rule set modeled in a csv file shown in below table. Inspect these rules to see tax rates in few different situations. 
        This is just a sample in real world there would be many more rules and conditions to consider.
        """);
rules = pd.read_csv("rules.csv")
st.write(rules[['Category', 'Jurisdiction', 'TaxRate%']])
st.write("## Create a sample order");
cat = st.radio("Select product category",options=rules['Category'].unique())
city = st.radio("Select city of purchase",options=rules['Jurisdiction'].unique())
price = st.slider("Select price $", min_value=0,max_value=300, value=100)
rate = rules.loc[(rules['Category'] == cat) & (rules['Jurisdiction'] == city), 'TaxRate%'].values[0]
tax = price * rate/100
st.write("## A sample invoice");
df = pd.DataFrame(
    {
        "Invoice": [cat, f"Tax - @{rate}%", "Total"],
        "": [f"${price}",f"${tax}",f"${price + tax}"]
    }
)
st.write(df);

st.markdown("> These are my personal pages. Please contact me for any questions or suggestions. Thank you.")
