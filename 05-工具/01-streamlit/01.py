import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

code = '''def hello():
    print("Hello, Streamlit!")'''


st.code(code, language="python")

st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')


df = pd.DataFrame(
    rng(0).standard_normal((10, 20)), columns=("col %d" % i for i in range(20))
)

st.dataframe(df.style.highlight_max(axis=0))

st.title("Hello World")
st.write("This is a test")
st.write("This is a test")
st.markdown(":blue-badge[Home]")

