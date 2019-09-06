
import re
import pickle
import os
import math
import numpy as np;
def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    @param dir
    @param suffix
    @return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

def index_file(input_file,output_path=''):
    dictionary = {}
    with open(input_file, 'r',encoding="utf-8") as file:
        text = file.read()
    for m in re.finditer(r'(\w+)', text.lower()):
        word = m.group(0)
        if( word in dictionary):
            dictionary[word].append(m.start())
        else:
            dictionary[word] = [m.start()]
        
        #print(dictionary)
    if(output_path !=''):
        pickle.dump(dictionary,open(output_path,'wb'))
    
    return dictionary

def generate_masterfile(directory):

    masterDictionary = {}
    files = get_files(directory,'txt')
    for f in files:
        currentDic = index_file(directory+f)
        for word in currentDic :
            if(word in masterDictionary):
                masterDictionary[word][f] = currentDic[word]
            else:
                masterDictionary[word]={f:currentDic[word]}

    print(masterDictionary['samlar'])
            
def generate_tf_idf_vector(word_dictionary):
    nmbr_words=0
    document_vector = {}
    for key,value in word_dictionary.items():
        nmbr_words+=len(value)
    for key in word_dictionary:
        document_vector[key] = tf_idf(len(word_dictionary[key]),nmbr_words)

    return document_vector

def tf_idf(count,N):
    return (count/N)*math.log10(N/(1+count))

def cosine_similarity(dict1,dict2):
    vector1 = generate_tf_idf_vector(word_dictionary1)
    vector2 = generate_tf_idf_vector(word_dictionary2)

    nominator = 0
    sum1 = 0
    sum2 = 0

    for key,value in vector1.items():
        if(key in vector2):
            tf_idf1 = vector1[key]
            tf_idf2 = vector2[key]

            nominator+=tf_idf1*tf_idf2
            sum1 += math.pow(tf_idf1,2)
            sum2 += math.pow(tf_idf2,2)
    
    sim=nominator/(math.sqrt(sum1)*math.sqrt(sum2))
    return sim

if __name__ == "__main__":
    word_dictionary1 = pickle.load(open('./dicts/marbacka.pickle','rb'))
    word_dictionary2 = pickle.load(open('./dicts/gosta.pickle','rb'))
    files = get_files('./dicts/','.pickle')

    similarity_matrix =  [[-1 for x in range(len(files))] for y in range(len(files))] 
    for i,filename1 in enumerate(files):
        word_dictionary1 = pickle.load(open('./dicts/'+filename1,'rb'))
        for k,filename2 in enumerate(files):
            #Avoiding calculation if it's already been set due to symmetry
            if(i==k):
                similarity_matrix[i][k]=-1
                similarity_matrix[k][i]=-1
            elif(similarity_matrix[k][i] == -1):
                word_dictionary2 = pickle.load(open('./dicts/'+filename2,'rb'))
                similarity = cosine_similarity(word_dictionary1,word_dictionary2)
                similarity_matrix[i][k] = similarity
                similarity_matrix[k][i] = similarity #It's symmetric
    #print(np.argmax(similarity_matrix))
    
    # Find index of maximum value from 2D numpy array
    result = np.where(similarity_matrix == np.amax(similarity_matrix))
    
    print('Tuple of arrays returned : ', result)
    
    print('List of coordinates of maximum value in Numpy array : ')
    # zip the 2 arrays to get the exact coordinates
    listOfCordinates = list(zip(result[0], result[1]))
    # travese over the list of cordinates
    for cord in listOfCordinates:
        print('Text {} most similar to {} with similarity score of {} '.format(files[cord[0]],files[cord[1]],3))
    #print(word_dictionary1)