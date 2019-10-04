
import features
def parse_ml(stack,queue,graph,trans):
  print('fo')


if __name__ == "__main__":

  train_file = './test.conll'
  test_file = '../../corpus/conllx/sv/swedish_talbanken05_test_blind.conll'
  column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
  column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

  sentences = conll.read_sentences(train_file)
  formatted_corpus = conll.split_rows(sentences, column_names_2006)
  X,Y = extract_features(formatted_corpus,3)
  
  while(queue):

