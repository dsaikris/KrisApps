import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="ToyTaxService",
    page_icon="👋",
)

st.write("""# ToyTaxService design
Let's try to analyse this Streamlit ToyTaxCalc PyApp
- We want to make this app work for millions of calculation requests (QPS)
- We want to support real tax rules for every city in USA
""");

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
            "021124-ASDF": [f"${price}",f"${tax}",f"${price + tax}"]
        }
    )
    st.write(df);
st.code("""
import streamlit as st
import pandas as pd
import numpy as np
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
            "021124-ASDF": [f"${price}",f"${tax}",f"${price + tax}"]
        }
    )
    st.write(df);
""");

st.markdown("""### Observations
- This app loads the rules for each calc run which is extremely slow.
- One machine cannot take so much load so we may need a cluster of machines taking the load evenly.
- Also there is no ledger and due process to handle transactions and taxes.
- We also have the rendering, tax calculation and rule access all mixed up, it needs to be separated. We need
    - UI to place orders
    - Service to manage orders
    - Helper service to calculate taxes
    - Helper services to invoice, process payments, etc.
- From the code you can see we are doing O(n) search in **rules.loc**.
    - With lot of rules this would be extremely slow.
    - We also have **rules.loc(...).values[0]** which is hacky, we should avoid it.
- May be we should organize city level live Seattle.csv and Spokane.csv.
- We can do with category but, I believe typically business will expand region wise than on product wise.
- Pick the column(s) based on access pattern and fan out benefits.
""")

st.markdown("## Now we will have to build these things to make this app as a service.");
st.markdown("""### A place order web page
- Responsible for allowing users to place an order for a product
- Calls order service
- Shows the bill or invoice
""");
st.code("""
    price = selectedProduct.price()
    order = orderService.place(user, product, price, ...);
    st.write(order.invoice);
""")

st.markdown("""### A /place post api in OrderService
- Accepts user, product, price, ... and returns invoice
- responsibility of orders table
- access to call payment gateway, invoice service and others
- logic to generate invoice
- Typical order states are Pending, Charged, Canceled.
""")
st.code("""
    order = create(user, product, price, ...);
    ordersRepo.save(order)
    rate,tax,total = taxService.calc(order);
    ordersRepo.saveTaxes(order,rate,tax,total)
    if(paymentGateway.charge(order)):
        ordersRepo.markCharged(order)
        ordersRepo.setinvoice(invoiceService.generate(order))
""")

st.markdown("""### A /calc get api in TaxService
- Accepts cat, city and returns rate,tax,total
- Responsible for just calculating taxes
- Pre loads all the rules into memory LRU cache with TTL of few hours
- LRU cache is for quickly serving high velocity orders in main cities
- Also, this way the cache becomes localized and it becomes easy to add new cities as we expand.
""")
st.code("""
    rules = preLoadedDataFrames.get(city+".csv"))
    rate = first(rules.loc[(rules['Category'] == cat)), 'TaxRate%'].values)
    tax = price * rate/100
    total = price + tax
""")

st.markdown("> These are my personal pages. Please contact me for any questions or suggestions. Thank you.")