import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="ToyTaxCalc",
    page_icon="👋",
)

st.write("# ToyTaxCalc");
st.write("A sample rule set modeled in a csv file shown in below table. Inspect these rules to see tax rates in few different situations. This is just a sample in real world there would be many more rules and conditions to consider.");

rules = pd.read_csv("rules.csv")
col1, col2, col3  = st.columns(3)
with col1:
    st.write(rules)
with col2:
    cat = st.radio("Select product category",options=rules['Category'].unique())
    city = st.radio("Select city of purchase",options=rules['Jurisdiction'].unique())
    price = st.slider("Select price $", min_value=0,max_value=300, value=100)
with col3:
    rate = rules.loc[(rules['Category'] == cat) & (rules['Jurisdiction'] == city), 'TaxRate%'].values[0]
    tax = price * rate/100
    df = pd.DataFrame(
        {
            "Invoice": [cat, f"Tax - @{rate}%", "Total"],
            "021124-ASDF": [f"${price}",f"S{tax}",f"${price + tax}"]
        }
    )
    st.write(df);

st.markdown("> These are my personal pages. Please contact me for any questions or suggestions. Thank you.")
