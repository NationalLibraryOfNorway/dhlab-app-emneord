import streamlit as st
import re
from collections import Counter

COL_FREQ = "frekvens"

@st.cache_data(show_spinner=False)
def get_topic_counts(corpus, column='subjects'):
    import pandas as pd
    try:
        emneord =  Counter([x.strip() 
                        for y in corpus[column].values 
                        for x in set(y.split('/')) 
                        if isinstance(y, str)])
    except AttributeError:
        emneord =  Counter([y for y in corpus[column].values])

    emner = pd.DataFrame.from_dict(emneord, orient='index', columns=[COL_FREQ]).sort_values(by = COL_FREQ, ascending=False)
    return emner

def process_corpus(corpus):
    import pandas as pd
    corpusdf = corpus.corpus.fillna("")
    corpusdf.year = pd.to_datetime(corpusdf.year.map(lambda x:str(int(x))), format="mixed")
    corpusdf.timestamp = pd.to_datetime(corpusdf.timestamp.map(lambda x:str(int(x))), format="mixed")

    col1, col2 = st.columns(2)
    with col1:
        gruppering = st.selectbox(
                    'Velg grupperingskolonne', 
                    options = [x for x in corpusdf.columns 
                               if x not in "urn dhlabid isbn isbn10 sesamid oaiid".split()]
        )
        assert isinstance(gruppering, str)

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
        sum_group = df[df.index != ''][COL_FREQ].sum()
        sum_total = df[COL_FREQ].sum()
        if percent == True:
            st.write(f"Sum over alle elementer i _{gruppering}_ blir {sum_group} %, av totalt  {sum_total} inkludert blanke _{gruppering}_.")
        else:
            st.write(f"Sum over alle elementer i _{gruppering}_ blir {sum_group}, av totalt  {sum_total} inkludert blanke _{gruppering}_.")
        st.write(f"Antall _{gruppering}_ er {len(df)}.")
        st.write(f"Korpusstørrelsen er {len(corpusdf)}.")

def get_corpus(urner="", file=None):
    import pandas as pd
    corpus = None

    if file is not None:
        import dhlab as dh
        dataframe = pd.read_excel(file)
        corpus = dh.Corpus(doctype='digibok',limit=0)
        corpus.extend_from_identifiers(list(dataframe.urn))
    elif urner != "":
        import dhlab as dh
        urns = re.findall(r"URN:NBN[^\s.,]+", urner)
        if urns != []:
            corpus = dh.Corpus(doctype='digibok',limit=0)
            corpus.extend_from_identifiers(urns)
        else:
            st.write('Fant ingen URNer')

    return corpus


st.set_page_config(
    page_title="Metadata",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

st.sidebar.markdown("Velg et korpus fra [corpus-appen](https://beta.nb.no/dhlab/corpus/)" 
                    " eller hent en eller flere URNer fra nb.no eller andre steder")

urner = st.sidebar.text_area("Lim inn URNer:","", help="Lim en tekst som har URNer i seg. Teksten trenger ikke å være formatert")
uploaded_file = st.sidebar.file_uploader("Last opp et korpus", help="Dra en fil over hit, fra et nedlastningsikon, eller velg fra en mappe")

st.header('Inspiser metadata')

corpus = get_corpus(urner, uploaded_file)

if corpus is None:
    st.write(' -- venter på korpus --')
    import dhlab as _
    import pandas as _
else:
    process_corpus(corpus)
