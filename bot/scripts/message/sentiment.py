from textblob import TextBlob
from operator import itemgetter
from pprint import pprint as pp


"""
Add this to heroku buildpacks
https://github.com/heroku/heroku-buildpack-python.git
"""


argument = [
    "please do. I would much prefer to know how you are misinterpreting of misattributing my words than suffer public humiliation.",
    "please leave me alone.",
]



def example():
    
    text = '''
    The titular threat of The Blob has always struck me as the ultimate movie
    monster: an insatiably hungry, amoeba-like mass able to penetrate

    '''

    blob = TextBlob(text)
    blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                        #  ('threat', 'NN'), ('of', 'IN'), ...]

    blob.noun_phrases   # WordList(['titular threat', 'blob',
                        #            'ultimate movie monster',
                        #            'amoeba-like mass', ...])

    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)
    # 0.060
    # -0.341

    # print(blob.translate(to="ja") ) # 'La amenaza titular de The Blob...'

    # print(blob.detect_language())


def is_positive(line):
    line = TextBlob(line)
    # print(line.sentiment)
    return line.sentiment

def get_polarity(line):
    line = TextBlob(line)
    # print(line.sentiment)
    return line.sentiment.polarity
# data = []
# for line in argument:
#     blob = TextBlob(line)
#     data.append([blob.sentiment.polarity,blob.sentiment.subjectivity, blob.raw])

# print(type(data[0][0]))
# data.sort()
# # pp)data.sort()
# # print(is_positive(line))

# pp(data)

