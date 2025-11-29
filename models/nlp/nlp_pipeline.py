
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

nlp = spacy.blank("de")  # German
texts = [
    "Die Lieferung kam verspätet an und Teile waren beschädigt.",
    "Guter Service, schnelle Lieferung.",
    "Qualität der gelieferten Komponenten ist schlecht."
]

tokens = [" ".join([t.lemma_ for t in nlp(text) if not t.is_stop]) for text in texts]

vec = TfidfVectorizer(max_features=100)
X = vec.fit_transform(tokens)
svd = TruncatedSVD(n_components=2)
topics = svd.fit_transform(X)

print("NLP topics matrix:")
print(topics)
