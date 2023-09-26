import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import pyLDAvis.gensim_models as gensimvis
import ssl
import pyLDAvis
import webbrowser

# 禁用SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 下载并安装NLTK的"punkt"和"stopwords"数据
nltk.download('punkt')
nltk.download('stopwords')

# 下载《爱丽丝梦游仙境》文本
nltk.download('gutenberg')
nltk.corpus.gutenberg.fileids()  # 列出可用的文本文件

# 选择《爱丽丝梦游仙境》文本
alice_corpus = gutenberg.raw('carroll-alice.txt')

# 预处理文本
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return tokens

# 构建文档-词矩阵
processed_corpus = [preprocess_text(alice_corpus)]
dictionary = Dictionary(processed_corpus)
corpus = [dictionary.doc2bow(text) for text in processed_corpus]

# 执行LDA主题建模
lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

# 可视化主题
vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.display(vis_data)

# 生成主题可视化
vis_data = gensimvis.prepare(lda_model, corpus, dictionary)

# 将主题可视化保存为HTML文件
pyLDAvis.save_html(vis_data, 'lda_visualization.html')

# 在浏览器中打开保存的HTML文件
webbrowser.open('lda_visualization.html')