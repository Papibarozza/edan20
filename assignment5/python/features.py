import transition
import dparser
import conll

def generate_feature_vector2(stack,queue,graph):
  feature_names = ['stack0_POS','stack1_POS','stack0_word','stack1_word',
  'queue0_POS','queue1_POS','queue0_word','queue1_word','can-re','can-la']
  try:
    stack0_POS = stack[0]['postag']
  except IndexError:
    stack0_POS = 'nil'
  try:
    stack1_POS = stack[1]['postag']
  except IndexError:
    stack1_POS = 'nil'
  try:
    stack0_word = stack[0]['form']
  except IndexError:
    stack0_word = 'nil'
  try:
    stack1_word = stack[1]['form']
  except IndexError:
    stack1_word = 'nil'
  #Guaranteed to exist because of while loop
  queue0_POS = queue[0]['postag'] 
  queue0_word= queue[0]['form']
  try:
    queue1_POS = queue[1]['postag']
  except IndexError:
      queue1_POS = 'nil'
  try:
    queue1_word= queue[1]['form']
  except IndexError:
      queue1_word = 'nil'
  can_left_arc = transition.can_leftarc(stack,graph)
  can_reduce = transition.can_reduce(stack,graph)
  return dict(zip(feature_names, [stack0_POS,stack1_POS,stack0_word,stack1_word,queue0_POS,queue1_POS,queue0_word,queue1_word,can_reduce,can_left_arc]))

def generate_feature_vector1(stack,queue,graph):
  feature_names = ['stack0_POS','stack0_word',
  'queue0_POS','queue1_POS','can-re','can-la']
  try:
    stack0_POS = stack[0]['postag']
  except IndexError:
    stack0_POS = 'nil'
  try:
    stack0_word = stack[0]['form']
  except IndexError:
    stack0_word = 'nil'

  #Guaranteed to exist because of while loop
  queue0_POS = queue[0]['postag'] 
  queue0_word= queue[0]['form']

  can_left_arc = transition.can_leftarc(stack,graph)
  can_reduce = transition.can_reduce(stack,graph)
  return dict(zip(feature_names, [stack0_POS,stack0_word,queue0_POS,queue0_word,can_reduce,can_left_arc]))

def generate_feature_vector3(stack,queue,graph,sentence):
  feature_names = ['stack0_POS','stack1_POS','stack0_word','stack1_word',
  'queue0_POS','queue1_POS','queue0_word','queue1_word','can-re','can-la','following_word','following_word_POS','queue3_POS','stack0_previous_word_POS']
  try:
    stack0_POS = stack[0]['postag']
  except IndexError:
    stack0_POS = 'nil'
  try:
    stack1_POS = stack[1]['postag']
  except IndexError:
    stack1_POS = 'nil'
  try:
    stack0_word = stack[0]['form']
  except IndexError:
    stack0_word = 'nil'
  try:
    stack1_word = stack[1]['form']
  except IndexError:
    stack1_word = 'nil'
  #Guaranteed to exist because of while loop
  queue0_POS = queue[0]['postag'] 
  queue0_word= queue[0]['form']
  try:
    queue1_POS = queue[1]['postag']
  except IndexError:
      queue1_POS = 'nil'
  try:
    queue1_word= queue[1]['form']
  except IndexError:
    queue1_word = 'nil'

  #POS QUEUE 3
  try:
    queue3_POS = queue[3]['postag']
  except IndexError:
    queue3_POS = 'nil'

  #POS STACK 0 pw
  try:
    idx = stack[0]['id']
    stack0_previous_word_POS= sentence[int(idx)-1]['postag']
  except IndexError:
    stack0_previous_word_POS= 'nil'
  #POS STACK 0 fw
  try:
    idx = stack[0]['id']
    following_word_POS = sentence[int(idx)+1]['postag']
  except IndexError:
    following_word_POS = 'nil'
  #LEX STACK 0 fw
  try:
    idx = stack[0]['id']
    following_word = sentence[int(idx)+1]['form']
  except IndexError:
    following_word = 'nil'

  
  can_left_arc = transition.can_leftarc(stack,graph)
  can_reduce = transition.can_reduce(stack,graph)



  return dict(zip(feature_names, [stack0_POS,stack1_POS,stack0_word,stack1_word,queue0_POS,queue1_POS,
  queue0_word,queue1_word,can_reduce,can_left_arc,following_word,following_word_POS,queue3_POS,stack0_previous_word_POS]))

def extract_features(formatted_corpus,mode):
    X = []
    Y = []
    for sentence in formatted_corpus:
      stack = []
      queue = list(sentence)
      graph = {}
      graph['heads'] = {}
      graph['heads']['0'] = '0'
      graph['deprels'] = {}
      graph['deprels']['0'] = 'ROOT'
      while queue:
        if(mode == 3):
          features = generate_feature_vector3(stack,queue,graph,sentence)
        elif(mode == 2):
          features = generate_feature_vector2(stack,queue,graph)
        else:
          #mode==1
          features = generate_feature_vector1(stack,queue,graph)

        stack, queue, graph, trans = dparser.reference(stack, queue, graph)
        X.append(features)
        Y.append(trans)
    return X,Y
if __name__ == "__main__":
    #train_file = '../../corpus/conllx/sv/swedish_talbanken05_train.conll'
    train_file = './test.conll'
    test_file = '../../corpus/conllx/sv/swedish_talbanken05_test_blind.conll'
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_2006_test = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats']

    sentences = conll.read_sentences(train_file)
    formatted_corpus = conll.split_rows(sentences, column_names_2006)
    X,Y = extract_features(formatted_corpus,3)
    i = 3
    #print(len(X[4],Y[4])