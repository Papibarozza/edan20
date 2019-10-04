
import conll
import dparser
import features
import transition
from joblib import dump,load
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
if __name__ == '__main__':

    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    train_file = '../../corpus/conllx/sv/swedish_talbanken05_train.conll'
    test_file = '../../corpus/conllx/sv/swedish_talbanken05_test.conll'
  
    train_sentences = conll.read_sentences(train_file)
    test_sentences = conll.read_sentences(test_file)
    formatted_train_corpus = conll.split_rows(train_sentences, column_names_2006)
    formatted_test_corpus = conll.split_rows(test_sentences,column_names_2006)
    for mode in [1,3]:
      print("Extracting the features...")
      X_dict, y = features.extract_features(formatted_train_corpus,mode)
      print("Encoding the features...")
      # Vectorize the feature matrix and carry out a one-hot encoding
      vec = DictVectorizer(sparse=True)
      X = vec.fit_transform(X_dict)

      print("Training the model...")
      classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear',multi_class='ovr')
      model = classifier.fit(X, y)
      dump(model,'./clfs/logres_mode='+str(mode)+'_feats.joblib')
      dump(vec,'./vectorizers/mode='+str(mode)+'_feats_vectorizer.joblib')
      print("Predicting the chunks in the test set...")
      X_test_dict, y_test = features.extract_features(formatted_test_corpus,mode)
      # Vectorize the test set and one-hot encoding
      X_test = vec.transform(X_test_dict)  # Possible to add: .toarray()
      y_test_predicted = classifier.predict(X_test)
      print("Classification report for classifier %s:\n%s\n"
            % (classifier, metrics.classification_report(y_test, y_test_predicted)))
