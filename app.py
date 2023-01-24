import streamlit as st
import pandas as pd
import regex as reg
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from io import StringIO
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer


with open('lr.joblib','rb') as f:
    lr=load(f)

with open('Tfidf.joblib','rb') as f:
    vectorizer=load(f)


# class MyVectorizer(TfidfVectorizer):
#     # plug our pre-computed IDFs
#     TfidfVectorizer.idf_ = idf
#     TfidfVectorizer.vocabulary_ = vocabulary
#     # TfidfVectorizer._tfidf._idf_diag=sp.spdiags(idf,diags=0,m=len(idf),n=len(idf))

# # instantiate vectorizer
# vectorizer = MyVectorizer()



word_net = WordNetLemmatizer()

stop_words=set(stopwords.words('english'))

stop_words=stop_words.difference({'not'})

st.title('Emotion Classifier')

st.header('Input the text and it will tell the emotion of the text')

text=st.text_area(label='Write here')
contractions = { 
"ain't": "am not / are not / is not / has not / have not",
"aren't": "are not / am not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had / he would",
"he'd've": "he would have",
"he'll": "he shall / he will",
"he'll've": "he shall have / he will have",
"he's": "he has / he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how has / how is / how does",
"I'd": "I had / I would",
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I shall have / I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had / it would",
"it'd've": "it would have",
"it'll": "it shall / it will",
"it'll've": "it shall have / it will have",
"it's": "it has / it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had / she would",
"she'd've": "she would have",
"she'll": "she shall / she will",
"she'll've": "she shall have / she will have",
"she's": "she has / she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as / so is",
"that'd": "that would / that had",
"that'd've": "that would have",
"that's": "that has / that is",
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there has / there is",
"they'd": "they had / they would",
"they'd've": "they would have",
"they'll": "they shall / they will",
"they'll've": "they shall have / they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had / we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what shall / what will",
"what'll've": "what shall have / what will have",
"what're": "what are",
"what's": "what has / what is",
"what've": "what have",
"when's": "when has / when is",
"when've": "when have",
"where'd": "where did",
"where's": "where has / where is",
"where've": "where have",
"who'll": "who shall / who will",
"who'll've": "who shall have / who will have",
"who's": "who has / who is",
"who've": "who have",
"why's": "why has / why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had / you would",
"you'd've": "you would have",
"you'll": "you shall / you will",
"you'll've": "you shall have / you will have",
"you're": "you are",
"you've": "you have"
}
def clean(text):
    # expand the contractions
    contractions_re = reg.compile('(%s)' % '|'.join(contractions.keys()))
    def replace(match):
         return contractions[match.group(0)]
    text=contractions_re.sub(replace, text)
   

    # removing URL
    url_pattern = reg.compile(r'https?://\S+|www\.\S+')
    text=url_pattern.sub(r'', text)
    #text=reg.sub('[a-z]+://[a-z]+\.[a-z]+/[a-z0-9]+','',text)
    
    # removing punctuations
    text=reg.sub('[%s]' % reg.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"""), ' ', text)
    #text=reg.sub("!|\"|#|$|%|&|\|'|(|)|\*|\+|,|-|\.|/|:|;|<|=|>|\?|@|[|\|\|]|^|_|`|{|}|~|'",'',text)
    
    # removing extra spaces
    text=text.strip()
    text=reg.sub('\s+',' ',text)
    
    # removing digits
    text=reg.sub('[0-9]','',text)
    
    # lowering the case
    text=text.lower()
    text=text.strip()
    # lemmatizing the text
    tokens=text.split(' ')
    tokens_lemmatize=[word_net.lemmatize(w) for w in tokens if w not in stop_words]
    
    # remove unneccessary words
    extra_words=set({'day','today','tomorrow','week','weekend','go','going','still','time','back','tonight','got','really','home','twitter','one','think','need','amp','last'})
    tokens_lemmatize_clnd=[w for w in tokens_lemmatize if w not in extra_words]

    # removing the word with length less than 2
    tokens_cleaned=[]
    for i in tokens_lemmatize_clnd:
        if (len(i)>2) & (len(i)<12):
            tokens_cleaned.append(i)
    if len(tokens_cleaned)>2:
        string=' '.join(tokens_cleaned)
    else:
        string=np.nan
    
    
    return ' '.join(tokens_cleaned)

data=('text\n''hello')
df=pd.read_csv(StringIO(data),index_col=False)
df.loc[0]['text']=text
df['text']=df['text'].apply(lambda x:clean(x))
X=vectorizer.transform(df['text']).toarray()


output=lr.predict(X)


if st.button('Predict'):
    st.write(output)
