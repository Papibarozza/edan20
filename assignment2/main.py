import regex as re
import copy
from math import log
import sys
from collections import Counter
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
def good_turing(bigrams):
    """Calculates the GT frequencies for the bigram occurences and writes it back to the bigram dictionary

        Parameters:
            argument1 {String : int }: Bigram dictionary
    """

    k = 6 #Calculate GT for occurences [0<occurences<=k]
    c_stars = [0]*(k+1)
    #Calculate GT estimates and store them
    for c in range(1,k+1):
        N_c = sum(map((c).__eq__, bigrams.values()))
        N_cplus1= sum(map((c+1).__eq__, bigrams.values()))
        c_star = (c+1)*N_cplus1/N_c
        c_stars[c]=c_star
    
    #Write the GT frequencies back to the bigram
    for c in range(1,k+1):
        for bigram in bigrams:
            if(bigrams[bigram] == c):
                bigrams[bigram]=c_stars[c]
    
    return bigrams

    
def P_katz(bigram,bigrams,bigramsGT,unigrams):
    w1 = bigram[0]
    w2 = bigram[1]
    nr_words = sum(unigrams.values())
    nr_bigrams = sum(bigrams.values())
    #print(nr_words)
    if(bigram in bigramsGT):
        #return bigrams[bigram]/unigrams[w1] #how he wants it
        return bigramsGT[bigram]/nr_bigrams #what it should be?
    else:
        #print('Using backoff..')
        if(w2 in unigrams):
            alpha = calculate_alpha2(w1,w2,nr_bigrams,nr_words,bigramsGT,unigrams)
            return alpha * unigrams[w2]/nr_words #what it should be?
        else:
            return unigrams[w1]/nr_words
        #return unigrams[w2]/nr_words #How he wants it.


def calculate_alpha2(w1,w2,nr_bigrams,nr_words,bigramsGT,unigrams):
    nominator= 1
    denominator =1
    for ngram_pair,value in bigramsGT.items():
        if(ngram_pair[0]==w1):
            #nominator-=value/unigrams[w1] #Wiggly probability
            nominator-=value/(nr_bigrams)
            denominator-=unigrams[ngram_pair[1]]/nr_words
    return nominator/denominator


def most_probable_bigram(word,bigram,bigrams_GT_estimate,unigrams):
    
    prob_old = 0
    wrd =''
    k = Counter(unigrams)
    for wrd in k.most_common(200):
        prob = P_katz((word,wrd[0]),bigrams,bigrams_GT_estimate,unigrams)
        if(prob > prob_old and wrd[0] != '<s>' and wrd[0] !='</s>' ):
            prob_old=prob
            best = wrd[0]
            print(best)
    return best
        




if __name__ == "__main__":
    words = tokenize(normalize_file('Selma.txt'))
    unigrams = count_unigrams(words)
    bigrams = count_bigrams(words)
    bigrams_GT_estimate = good_turing(copy.deepcopy(bigrams)) #Recalculate
    assert not(bigrams == bigrams_GT_estimate),'Shouldnt be equal'
    bigram=('i','till')
    print(sum(bigrams.values()),sum(unigrams.values()))
    print(len(words))
    print(P_katz(bigram,bigrams,bigrams_GT_estimate,unigrams))
    """ while True:
        word = input("-: ")
        print(most_probable_bigram(word,bigrams,bigrams_GT_estimate,unigrams)) """

    #print(bigram,P_katz(bigram,bigrams,bigrams_GT_estimate,unigrams))
    """ sentence = '<s> det var en gång en katt som hette nils </s>'
    sentence_words = tokenize(sentence)
    bigram_sentence = count_bigrams(tokenize(sentence))
    for bigram in bigram_sentence:
        print(bigram,P_katz(bigram,bigrams,bigrams_GT_estimate,unigrams)) """

    #print(bigrams[bigram])

"""     
    lr = likelihood_ratio(words,unigrams,bigrams)
    sentence = '</s> det var en gång en katt som hette nils </s>'
    sentence_words = tokenize(sentence)
    bigram_sentence = count_bigrams(tokenize(sentence))
    for word in sentence_words:
      print(word,unigrams[word],len(words),unigrams[word]/len(words)) """

    #for bigram in bigram_sentence:
   
   # print(('stilla','på'), lr[('stilla','på')])
      
"""     i = 0
    for word in sorted(unigrams.keys(), key=unigrams.get, reverse=True):
      if(i==4):
        break
      print(word, '\t', unigrams[word])
      i+=1 """
      
      