# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import io
import re
from collections import Counter

st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")
sns.set(style="whitegrid")

@st.cache_data
def load_data(path="data/cleaned_sample.csv"):
    df = pd.read_csv(path, parse_dates=['publish_time'], low_memory=False)
    # Ensure columns exist
    for c in ['title','abstract','publish_time','year','journal','source']:
        if c not in df.columns:
            df[c] = pd.NA
    df['year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
    return df

def most_common_title_words(series, n=30, extra_stop=None):
    stops = set()
    if extra_stop:
        stops |= set(extra_stop)
    text = " ".join(series.dropna().astype(str).str.lower().tolist())
    words = re.findall(r'\w+', text)
    words = [w for w in words if len(w) > 2 and w not in stops and not w.isnumeric()]
    return Counter(words).most_common(n)

def plot_publications_by_year(df):
    counts = df['year'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8,4))
    counts.plot(kind='bar', ax=ax)
    ax.set_title("Publications by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    plt.tight_layout()
    return fig

def plot_top_journals(df, top_n=10):
    top = df['journal'].fillna('Unknown').value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(8, max(3, top_n*0.4)))
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title(f"Top {top_n} Journals")
    ax.set_xlabel("Count")
    ax.set_ylabel("Journal")
    plt.tight_layout()
    return fig

def generate_wordcloud(text, stopwords=None):
    wc = WordCloud(width=800, height=400, stopwords=stopwords or set(),
                   collocations=False).generate(text)
    return wc.to_image()

# --- UI ---
st.title("CORD-19 Data Explorer")
st.write("A lightweight explorer for the CORD-19 `metadata.csv` (sample).")

# Load data
DATA_PATH = st.sidebar.text_input("Path to cleaned CSV", "data/cleaned_sample.csv")
df = load_data(DATA_PATH)

# sidebar filters
min_year = int(df['year'].dropna().min()) if df['year'].dropna().size else 2019
max_year = int(df['year'].dropna().max()) if df['year'].dropna().size else 2022
year_range = st.sidebar.slider("Year range", min_year, max_year, (min_year, max_year))

top_n = st.sidebar.slider("Top journals (n)", 5, 50, 15)
journal_choices = ['All'] + list(df['journal'].fillna('Unknown').value_counts().head(100).index)
journal_sel = st.sidebar.selectbox("Filter by journal (top 100)", journal_choices)

# apply filters
mask = (df['year'] >= year_range[0]) & (df['year'] <= year_range[1])
if journal_sel != 'All':
    mask &= (df['journal'].fillna('Unknown') == journal_sel)
filtered = df.loc[mask].copy()

st.markdown(f"**Showing** {len(filtered)} papers (years {year_range[0]}–{year_range[1]})")

# layout: two columns for charts
col1, col2 = st.columns([2,1])

with col1:
    st.header("Publications over time")
    fig = plot_publications_by_year(filtered)
    st.pyplot(fig)

    st.header("Top journals")
    fig2 = plot_top_journals(filtered, top_n=top_n)
    st.pyplot(fig2)

with col2:
    st.header("Title word cloud")
    all_titles = " ".join(filtered['title'].dropna().astype(str).tolist()).lower()
    if all_titles.strip():
        wc_img = generate_wordcloud(all_titles, stopwords=None)
        st.image(wc_img, use_column_width=True)
    else:
        st.write("No titles available in current filter.")

st.header("Most frequent words in titles")
top_words = most_common_title_words(filtered['title'], n=30)
st.table(pd.DataFrame(top_words, columns=['word','count']).head(20))

st.header("Sample of data")
st.dataframe(filtered[['publish_time','title','authors','journal','source']].head(200))

# allow CSV download of filtered
csv_bytes = filtered.to_csv(index=False).encode('utf-8')
st.download_button("Download filtered CSV", csv_bytes, file_name="cord19_filtered.csv", mime="text/csv")
