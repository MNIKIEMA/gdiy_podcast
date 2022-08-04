import streamlit as st
import pandas as pd
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
from bertopic import BERTopic
from wordcloud import WordCloud
from nltk.corpus import stopwords
import pickle
import plotly.express as px

nlp = spacy.load("fr_core_news_sm")
stopword = stopwords.words('french')
import warnings
warnings.filterwarnings('ignore')
from nltk import FreqDist

df = pd.read_csv("gdiy_data.csv", sep=',',
                 parse_dates=['release_date'])  # use `release_date` as date in  pandas


def clean_data(df):
    df = df.drop('Unnamed: 0', axis=1)
    df['description'] = df['description'].str.lower()
    df = df.set_index('release_date')
    df = df.loc[[not (df['name'][i].startswith(('[EXTRAIT]', '[REDIFF]'))) for i in range(len(df))]]
    df.loc[:, 'duration_min'] = df['duration_ms'].apply(
        lambda row: row / (60 * 1000))  # convertir la durée de ms en minutes
    df['year'] = df.index.year
    df['month'] = df.index.month
    return df


df_clean = clean_data(df)


def clean_up1(row: str, stopword, pos=None):
    """ Prend une un text:
    - Supprime les caractères `\xa0` et `\u200a`
    - Supprime les mots avec moins de lettres """

    texts = row.replace(f'\xa0', '')
    texts = texts.replace(f'\u200a', '')
    text_ = " ".join([token for token in texts.split() if token.isalpha() and len(token) > 2])
    texts = nlp(text_)
    if pos is not None:
        list_tokens = [token.lemma_ for token in texts if token.lemma_ not in stopword \
                       and token.pos_ not in pos]

    else:
        list_tokens = [token.lemma_ for token in texts if token.lemma_ not in stopword]

    return list_tokens


pos = ['ADV', 'PRON', 'CCONJ', 'PUNCT', 'DET', 'ADP', 'SPACE', 'ADJ', 'VERB']

context = ['épisode', 'faire', 'morgan','prudhomme', 'lire', 'génération','podcast', 'gdiy',
           'recommande','deux','quand','the','livre', 'être','yourself', 'orso', 'doi', 'an',
           'merci', 'avoir','timeline','face','million','monde', 'vie','and','fait']
stopword = stopword + context # add some frequent words in the documents

clean_text = df_clean['description'].apply(lambda x: clean_up1(x, stopword, pos))
docs = clean_text.apply(lambda x: " ".join(x)).tolist()

topic_model = BERTopic(language="multilingual",
                       nr_topics=6,
                       top_n_words=30,
                       low_memory=True,
                       n_gram_range=(1, 2))

topics, _ = topic_model.fit_transform(docs)

topic_fig = topic_model.visualize_barchart(n_words=10)

timestamps = df_clean.index
topics_over_time = topic_model.topics_over_time(docs, topics, timestamps,
                                                global_tuning=True,
                                                evolution_tuning=True,
                                                nr_bins=20)

time_fig = topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=10)

topics_over_time = topics_over_time[topics_over_time['Topic'] != -1]
topics_over_time.set_index('Timestamp', inplace=True)
topics_over_time['year'] = topics_over_time.index.year
topic_per_year = topics_over_time.groupby(['year'])['Words'].apply(lambda x: x.str.cat(sep=' '))

fig1, ax = plt.subplots()
sns.countplot(ax=ax, x='year', data=df_clean, palette='viridis');


# plt.ylabel('Nombre de podcasts');

def wordscloud(text: str):
    WordCloud()
    word_cloud = WordCloud(background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot(fig)


data = df_clean.resample('Y')['duration_min'].mean()
fig = px.line(x=data.index.year, y=data, text=data.astype('int'), markers=True)
fig.update_traces(textposition="bottom right")

st.write('''
# Nous sommes la moyenne des personnes que nous fréquentons.
Hello''')

st.header('Nombre de podcasts par année')

st.write(fig1)

st.header('Durée moyenne des podcasts par année')
st.plotly_chart(fig, use_container_width=False,
                sharing="streamlit")

st.header('Les mots fréquemment utilisés dans le podcast')
text_cloud = clean_text.apply(lambda x: " ".join(x)).str.cat(sep=' ')
wordcloud = WordCloud(background_color='white').generate(text_cloud)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
st.pyplot(fig)

st.header('Sujets évoqués dans le podcast')
st.plotly_chart(topic_fig, use_container_width=False,
                sharing="streamlit")

st.header('Sujets évoqués au cours du temps dans le podcast')
st.plotly_chart(time_fig, use_container_width=False,
                sharing="streamlit")

st.header('Sujets en 2O17')
text = topic_per_year[2017].replace(',', "")
wordscloud(text)

st.header('Sujets en 2O18')
text = topic_per_year[2018].replace(',', "")
wordscloud(text)

st.header('Sujets en 2O19')
text = topic_per_year[2019].replace(',', "")
wordscloud(text)

st.header('Sujets en 2O20')
text = topic_per_year[2020].replace(',', "")
wordscloud(text)

st.header('Sujets en 2O21')
text = topic_per_year[2021].replace(',', "")
wordscloud(text)

st.header('Sujets en 2O22')
text = topic_per_year[2022].replace(',', "")
wordscloud(text)
