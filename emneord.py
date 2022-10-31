import dhlab as dh
import streamlit as st
import pandas as pd
import re
from collections import Counter

@st.cache(suppress_st_warning=True, show_spinner=False)
def get_topic_counts(corpus = None, column='subjects'):
    try:
        emneord =  Counter([x.strip() 
                        for y in corpus[column].values 
                        for x in set(y.split('/')) 
                        if isinstance(y, str)])
    except AttributeError:
        emneord =  Counter([y for y in corpus[column].values])
    
    emner = pd.DataFrame.from_dict(emneord, orient='index', columns=["frekvens"]).sort_values(by = 'frekvens', ascending=False)
    return emner

st.set_page_config(
    page_title="Metadata", 
    page_icon=None, 
    layout="wide",
    initial_sidebar_state="auto", 
    menu_items=None
)

st.sidebar.markdown("Velg et korpus fra [corpus-appen](https://beta.nb.no/dhlab/corpus/)" 
                    " eller hent en eller flere URNer fra nb.no eller andre steder")


corpus_defined = False
urner = st.sidebar.text_area("Lim inn URNer:","", help="Lim en tekst som har URNer i seg. Teksten trenger ikke å være formatert")
if urner != "":
    urns = re.findall("URN:NBN[^\s.,]+", urner)
    if urns != []:
        corpus_defined = True
        corpus = dh.Corpus(doctype='digibok',limit=0)
        corpus.extend_from_identifiers(urns)
        #st.write(urns)
    else:
        st.write('Fant ingen URNer')

uploaded_file = st.sidebar.file_uploader("Last opp et korpus", help="Dra en fil over hit, fra et nedlastningsikon, eller velg fra en mappe")
if uploaded_file is not None:
    corpus_defined = True
    dataframe = pd.read_excel(uploaded_file)

    corpus = dh.Corpus(doctype='digibok',limit=0)
    corpus.extend_from_identifiers(list(dataframe.urn))
    corpusdf = corpus.corpus.fillna("")
    corpusdf.year = pd.to_datetime(corpusdf.year.map(lambda x:str(int(x))), infer_datetime_format=True)
    corpusdf.timestamp = pd.to_datetime(corpusdf.timestamp.map(lambda x:str(int(x))), infer_datetime_format=True)

st.header('Inspiser metadata')

if corpus_defined:
    col1, col2 = st.columns(2)
    with col1:
        gruppering = st.selectbox(
                    'Velg grupperingskolonne', 
                    options = [x for x in corpusdf.columns 
                               if x not in "urn dhlabid isbn isbn10 sesamid oaiid".split()]
        )

    with col2:
        st.write("Relativ frekvens")
        percent = st.checkbox("Vis % ", value = False)

    df = get_topic_counts(corpusdf, gruppering)
    if percent == True:
        df = (df*100/df.sum())
    
    colA, colB = st.columns(2)
    
    with colA:
        st.write(f"### Opptelling av _{gruppering}_")
        if percent == True:
            st.write(df.style.format(precision=2))
        else:
            st.write(df)
    
    with colB:
        st.write(f"### Totaler for korpuset")
        if percent == True:
            st.write(f"Sum over alle elementer i _{gruppering}_ blir {int(df[df.index != ''].sum())} %, av totalt  {int(df.sum())} inkludert blanke _{gruppering}_.")
        else:
            st.write(f"Sum over alle elementer i _{gruppering}_ blir {int(df[df.index != ''].sum())}, av totalt  {int(df.sum())} inkludert blanke _{gruppering}_.")
        st.write(f"Antall _{gruppering}_ er {len(df)}.")
        st.write(f"Korpusstørrelsen er {len(corpusdf)}.")
         
else:
    st.write(' -- venter på korpus --')
            