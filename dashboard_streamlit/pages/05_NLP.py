import streamlit as st
import pandas as pd
import os
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("📝 NLP Insights on Supply Chain Data")

# --- Load deliveries dataset ---
DATA_PATH = os.path.join("data", "deliveries_curated.csv")
df = pd.read_csv(DATA_PATH)

# --- Create a text column for demo ---
# If you have actual description text, replace this column
if 'description' not in df.columns:
    df['description'] = (
        df['product_id'].astype(str) + " " +
        df['supplier_id'].astype(str) + " delivery"
    )

# --- Combine all text ---
all_text = " ".join(df['description'].astype(str).tolist())

# --- Word Frequency ---
words = all_text.lower().split()
word_freq = Counter(words)

st.header("🔹 Top 20 Words")
top_words = pd.DataFrame(word_freq.most_common(20), columns=['Word', 'Frequency'])
st.dataframe(top_words)

# --- Word Cloud ---
st.header("☁️ Word Cloud")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# --- Sample Data ---
st.header("📄 Sample Delivery Text Data")
st.dataframe(df[['product_id', 'supplier_id', 'description']].head(50))
