
import features
import transition
import conll
from joblib import load
import csv
def parse_ml(stack, queue, graph, trans):
  try:
    
    if stack and trans[:2] == 'ra':
      queue[0]['deprel'] = trans[3:]
      queue[0]['head'] = stack[0]['id']
      stack, queue, graph = transition.right_arc(stack, queue, graph, trans[3:])

      return stack, queue, graph, 'ra'
    if stack and trans[:2] == 'la':
      stack[0]['deprel'] = trans[3:]
      stack[0]['head'] = queue[0]['id']
      stack,queue,graph = transition.left_arc(stack,queue,graph,trans[3:])
      return stack, queue, graph, 'la'
    if stack and trans[:2] == 're':
      stack[0]['head'] = queue[0]['id']
      stack, queue, graph = transition.reduce(stack, queue,graph)
      return stack, queue, graph, 're'
  except Exception:
   
    stack, queue, graph = transition.shift(stack, queue, graph)
    return stack, queue, graph, 'sh'

  stack, queue, graph = transition.shift(stack, queue, graph)
  return stack, queue, graph, 'sh'

if __name__ == "__main__":

  train_file = '../../corpus/conllx/sv/swedish_talbanken05_test_blind.conll'
  test_file = '../../corpus/conllx/sv/swedish_talbanken05_test_blind.conll'
  column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
  column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

  sentences = conll.read_sentences(train_file)
  formatted_corpus = conll.split_rows(sentences, column_names_2006)
  #X,Y = features.extract_features(formatted_corpus,3)
  clf = load('./clfs/logres_mode=1_feats.joblib')
  vec = load('./vectorizers/mode=1_feats_vectorizer.joblib')
  sent_cnt = 0
  with open('out.conll','w',encoding='utf-8') as f:
    for idx,sentence in enumerate(formatted_corpus):
        sent_cnt += 1
        if sent_cnt % 1000 == 0:
            print(sent_cnt, 'sentences on', len(formatted_corpus), flush=True)
        stack = []
        queue = list(sentence)
        graph = {}
        graph['heads'] = {}
        graph['heads']['0'] = '0'
        graph['deprels'] = {}
        graph['deprels']['0'] = 'ROOT'
        transitions = []
        while(queue):
          feats = vec.transform(features.generate_feature_vector1(stack,queue,graph))
          trans = clf.predict(feats)
          stack,queue,graph,trans = parse_ml(stack,queue,graph,trans[0])
          transitions.append(trans)
        stack, graph = transition.empty_stack(stack, graph)
        #print(graph)
        for word in sentence[1:]:
          index = str(word['id'])
          word['head'] = graph['heads'][index]
          word['deprel'] = graph['deprels'][index]
          f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(word['id'],word['form'],word['lemma'],word['cpostag'],word['postag'],word['feats'],word['head'],word['deprel'],'_','_'))
        f.write('\n')
          

          





