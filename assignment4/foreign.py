import conll
import sys
from collections import Counter




def match_triple(collector_pair,collector_objects):
  triples = []
  for tup in collector_objects:
    _object = tup[0]
    head_reference = tup[1]
    for pair,head in collector_pair.items():
      if(head_reference == head):
        triples.append((pair[0],pair[1],_object))
        break
  return triples

if __name__ == "__main__":
  column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']
  fname = sys.argv[1]
  print(fname)
  sentences = conll.read_sentences(fname)
  formatted_corpus = conll.split_rows(sentences, column_names_u)
  frequencies = {}
  for sentence in formatted_corpus:
    for token in sentence:
      if(token['deprel'] == 'nsubj'):
        subject = token['form']
        head = token['head']
        verb = sentence[int(head)]['form']
        pair = (subject.lower(),verb.lower())
        if pair in frequencies:
          frequencies[pair]+=1 
        else:
          frequencies[pair] = 1

  cnt = Counter(frequencies)
  print(cnt.most_common(5))
  print(sum(cnt.values()))
  i=0
  frequencies2 = {}
  for sentence in formatted_corpus:
    collector_pair = {}
    collector_objects = []
    for token in sentence:
      if(token['deprel'] == 'nsubj'):
        subject = token['form']
        head = token['head'] #The index of the related verb
        verb = sentence[int(head)]['form']
        pair = (subject.lower(),verb.lower())
        collector_pair[pair] = head #Maps the (subject,verb) to the index of the verb, to later see if object is belonging to this pair.
      if(token['deprel'] == 'obj'):
        _object = token['form']
        head_reference = token['head'] #The index of the related verb
        collector_objects.append((_object,head_reference))#Save all objects and the head they map to

    triples = match_triple(collector_pair,collector_objects) #Find the triples by looking at objects and finding their heads among the subject-verbs
    for triple in triples:
      if(triple in frequencies2):
        frequencies2[triple]+=1
      else:
        frequencies2[triple] = 1
    
  cnt2 = Counter(frequencies2)
  print(cnt2.most_common(5))
  print(sum(cnt2.values()))