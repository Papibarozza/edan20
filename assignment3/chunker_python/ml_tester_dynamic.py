"""
Machine learning chunker for CoNLL 2000
"""
__author__ = "Pierre Nugues"

import sys
from joblib import dump,load
import time
import conll_reader
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV


def extract_features2(sentences, w_size, feature_names,model,vectorizer):
    """
    Builds X matrix and y vector
    X is a list of dictionaries and y is a list
    :param sentences:
    :param w_size:
    :return:
    """
    X_l = []
    y_l = []
    for sentence in sentences:
        X, y = extract_features_sent2(sentence, w_size, feature_names,model,vectorizer)
        X_l.extend(X)
        y_l.extend(y)
    return X_l, y_l


def extract_features_sent2(sentence, w_size, feature_names,model,vectorizer):
    """
    Extract the features from one sentence
    returns X and y, where X is a list of dictionaries and
    y is a list of symbols
    :param sentence: string containing the CoNLL structure of a sentence
    :param w_size:
    :return:
    """

    # We pad the sentence to extract the context window more easily
    start = "BOS BOS BOS\n"
    end = "\nEOS EOS EOS"
    start *= w_size
    end *= w_size
    sentence = start + sentence
    sentence += end

    # Each sentence is a list of rows
    sentence = sentence.splitlines()
    padded_sentence = list()
    for line in sentence:
        line = line.split()
        padded_sentence.append(line)
 
    # We extract the features and the classes
    # X contains is a list of features, where each feature vector is a dictionary
    # y is the list of classes
    X = list()
    y = list()
    tag_p = 'BOS'
    tag_pp = 'BOS'
    vec = vectorizer
    for i in range(len(padded_sentence) - 2 * w_size):
        # x is a row of X
        x = list()
        # The words in lower case
        for j in range(2 * w_size + 1):
            x.append(padded_sentence[i + j][0].lower())
        
        # The POS
        for j in range(2 * w_size + 1):
            x.append(padded_sentence[i + j][1])

        x.append(tag_pp)
        x.append(tag_p)
        temp_tag = model.predict(vec.transform(dict(zip(feature_names, x))))[0]
        tag_pp = tag_p
        tag_p = temp_tag
        
        #Useful debugging
        #if(tag_p != padded_sentence[i + w_size][2]):
            #print(tag_p,'was not',padded_sentence[i + w_size][2])
        #else:
            #print(tag_p,'was correctly classified as',padded_sentence[i + w_size][2])
        
        # We represent the feature vector as a dictionary
        X.append(dict(zip(feature_names, x)))

        
        # The classes are stored in a list
        #These are the chunk tags that we want to predict given the words and POS
        y.append(padded_sentence[i + w_size][2])

    return X, y


def predict(test_sentences, feature_names, f_out):
    model=load('./clfs/logres_dynamic.joblib')
    vec = load('./vectorizers/all_features_vectorizer.joblib')
    for test_sentence in test_sentences:
        X_test_dict, y_test = extract_features_sent2(test_sentence, w_size, feature_names,model,vec)
        # Vectorize the test sentence and one hot encoding
        X_test = vec.transform(X_test_dict)
        # Predicts the chunks and returns numbers
        y_test_predicted = classifier.predict(X_test)
        # Appends the predicted chunks as a last column and saves the rows
        rows = test_sentence.splitlines()
        rows = [rows[i] + ' ' + y_test_predicted[i] for i in range(len(rows))]
        for row in rows:
            f_out.write(row + '\n')
        f_out.write('\n')
    f_out.close()


if __name__ == '__main__':
    start_time = time.process_time()
    train_corpus = '../../../corpus/conll2000/train.txt'
    test_corpus = '../../../corpus/conll2000/test.txt'
    w_size = 2  # The size of the context window to the left and right of the word
    feature_names = ['word_n2', 'word_n1', 'word', 'word_p1', 'word_p2',
                     'pos_n2', 'pos_n1', 'pos', 'pos_p1', 'pos_p2','pos_tag1','pos_tag2']
    

    train_sentences = conll_reader.read_sentences(train_corpus)
    vectorizer = load('./vectorizers/all_features_vectorizer.joblib')
    model=load('./clfs/logres_dynamic.joblib')

    # We apply the model to the test set
    test_sentences = list(conll_reader.read_sentences(test_corpus))
    classifier = model
    # Here we carry out a chunk tag prediction and we report the per tag error
    # This is done for the whole corpus without regard for the sentence structure
    print("Predicting the chunks in the test set...")
    X_test_dict, y_test = extract_features2(test_sentences, w_size, feature_names,model,vectorizer)
    # Vectorize the test set and one-hot encoding
    X_test = vectorizer.transform(X_test_dict)  # Possible to add: .toarray()
    y_test_predicted = classifier.predict(X_test)
    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(y_test, y_test_predicted)))

    # Here we tag the test set and we save it.
    # This prediction is redundant with the piece of code above,
    # but we need to predict one sentence at a time to have the same
    # corpus structure
    print("Predicting the test set...")
    f_out = open('out', 'w',newline='\n')
    predict(test_sentences, feature_names, f_out)
    f_out.close()

