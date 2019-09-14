import regex as re
from math import log
def normalize_file(file='Selma.txt'):
  with open(file, 'r',encoding="utf-8") as file:
    text = file.read()
    #for m in re.finditer(r'([\p{Lu}][^\.\n]+\.)', text):

    txt2 = (re.sub(r'[^\P{P}.]+','',text)) #Removes every punctuation character that is not a dot
    txt3 = re.sub(r'([\p{Lu}\p{L}]+[^\.]+\.)',r' <s> \1 </s> ',txt2) #Find all sentences which begins with uppercase letter and ends with dot.
    txt4 = re.sub(r'\.','',txt3).lower() #Removes the dot and makes the text lowercase.
  return txt4


def tokenize(text):
    words = re.findall(r"[\p{L}'<s>''</s>']+", text)
    return words


def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

def likelihood_ratio(words, freq_unigrams, freq_bigrams):
    lr = {}
    for bigram in freq_bigrams:
        p = freq_unigrams[bigram[1]] / len(words)
        p1 = freq_bigrams[bigram] / freq_unigrams[bigram[0]]
        p2 = ((freq_unigrams[bigram[1]] - freq_bigrams[bigram])
              / (len(words) - freq_unigrams[bigram[0]]))
        if p1 != 1.0 and p2 != 0.0:
            lr[bigram] = 2.0 * (
                log_f(freq_bigrams[bigram],
                      freq_unigrams[bigram[0]], p1) +
                log_f(freq_unigrams[bigram[1]] -
                      freq_bigrams[bigram],
                      len(words) - freq_unigrams[bigram[0]], p2) -
                log_f(freq_bigrams[bigram],
                      freq_unigrams[bigram[0]], p) -
                log_f(freq_unigrams[bigram[1]] -
                      freq_bigrams[bigram],
                      len(words) - freq_unigrams[bigram[0]], p))
    return lr


def log_f(k, N, p):
    return k * log(p) + (N - k) * log(1 - p)

def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2]) for inx in range(len(words) - 1)]

    frequency_bigrams = {}
    for bigram in bigrams:
        if bigram in frequency_bigrams:
            frequency_bigrams[bigram] += 1
        else:
            frequency_bigrams[bigram] = 1
    return frequency_bigrams

if __name__ == "__main__":
    words = tokenize(normalize_file('Selma.txt'))
    unigrams = count_unigrams(words)
    bigrams = count_bigrams(words)
    lr = likelihood_ratio(words,unigrams,bigrams)
    sentence = '</s> det var en gång en katt som hette nils </s>'
    sentence_words = tokenize(sentence)
    bigram_sentence = count_bigrams(tokenize(sentence))
    for word in sentence_words:
      print(word,unigrams[word],len(words),unigrams[word]/len(words))

    #for bigram in bigram_sentence:
   
    print(('stilla','på'), lr[('stilla','på')])
      
"""     i = 0
    for word in sorted(unigrams.keys(), key=unigrams.get, reverse=True):
      if(i==4):
        break
      print(word, '\t', unigrams[word])
      i+=1 """
      
      