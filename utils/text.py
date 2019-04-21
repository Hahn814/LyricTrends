import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from base.environment import env

logger = env.get_logger(context=__name__)


class Corpus(object):

    def __init__(self, corpus=None):
        self.logger = env.get_logger(context=self.__class__.__name__)
        self.__corpus = corpus if corpus else ""
        self.__sia = SentimentIntensityAnalyzer()

    def __str__(self):
        return "{classname} - Lyric Count: {lyriccount}".format(classname=self.__class__.__name__, lyriccount=len(self.__corpus.split()))

    def __len__(self):
        return len(self.__corpus.split())

    @property
    def corpus(self):
        return self.__corpus

    @corpus.setter
    def corpus(self, corpus):
        if isinstance(corpus, str):
            self.__corpus = corpus
        else:
            raise TypeError("Corpus text must be string, not {}".format(type(corpus)))

    def get_average_sentiment_score(self):
        sent_score = 0.0
        c = 0.0

        for score in self.get_sentiment_scores():
            sent_score += score.get('compound')
            c += 1

        return float(sent_score) / float(c)

    def get_sentiment_scores(self):
        sent_text = nltk.sent_tokenize(self.corpus)
        for sentence in sent_text:
            score = self.__sia.polarity_scores(sentence)
            yield score
