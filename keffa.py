#  -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
from collections import Counter
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob.tokenizers import WordTokenizer 
import glob
import json
import os
import re
import argparse
import sys

# Récupération des arguments
parser=argparse.ArgumentParser(description="Keffa is a program for extract keywords from French articles in txt format. It uses Python TextBlob library.")
parser.add_argument("-i","--input", help="Entry folder of text files to be analysed",required=True)
parser.add_argument("-o","--output", help="Output folder where extracted keywords will be stored",required=True)
args=parser.parse_args()

if args.input == 'None':
    print"Error : Enter input folder"
    sys.exit(1)
if not os.path.isdir(args.input):
     print "Error : Input entered is not a directory"
     sys.exit(1)
# if not os.path.isdir(args.output):
if not os.path.exists(args.output):
    os.makedirs(args.output)  

#mon chemin pour les corpus
#ouverture de mon stop liste
with open(os.getcwd()+"/stopwords_fr.json") as json_file:
    stopWord = json.load(json_file)
#ouverture de mon corpus d'entree'
corpusIn=glob.glob(args.input+"/*.txt")

#definition d'une fonction qui fait l'extraction des mots cles avec textblob 
def extraction_keywords():   
    liste_mots_without_stopWord=[]
    for word in liste_token :       
        if word not in stopWord.keys():
            liste_mots_without_stopWord.append(word)   
    
    document= [TextBlob(' '.join(liste_mots_without_stopWord), pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())]
    #print document
    count_ngrams={1:0,2:0,3:0,4:0,'all':0}

    for text in document:
        freq_word_nounPhrase= 0
        selected_nounPhrase = []
        for word in list(set(liste_mots_without_stopWord)):
            freq_word_nounPhrase+= text.words.count(word)
        for nounPhrase in text.noun_phrases: 
            if len(nounPhrase.split()) < 3: 
                selected_nounPhrase.append(nounPhrase)
        for nounPhrase in selected_nounPhrase:
            freq_word_nounPhrase+= text.noun_phrases.count(nounPhrase)
        dic_word_feq={word: (text.words.count(word)) for word in text.words}
        dic_nounPhrase_freq = {noun_phrases: (text.noun_phrases.count(noun_phrases)) for noun_phrases in selected_nounPhrase}
        dic_word_nounPhrase=dic_word_feq.copy() #dic_word_nounPhrase est un dictionniare qui contient les multitermes et leurs frequences et les mots simples et leurs frequences
        dic_word_nounPhrase.update(dic_nounPhrase_freq)
   
        liste_noun_phrase=[]
        for noun_phrase,freq_noun_phrase in dic_nounPhrase_freq.items(): # dic_nounPhrase_freq est une liste de tuples, les cles sont les multitermes et les valeurs sont les frequences
            liste_noun_phrase+=noun_phrase.split() #on casse les multitermes en terme simple et on mets tous dans une liste
        #print Counter(liste_noun_phrase).items()
        for word, freq in Counter(liste_noun_phrase).items():
            if dic_word_nounPhrase[word]==0:
                del dic_word_nounPhrase[word] #les traitements pour comptage d'une seul fois d'un mot qui apparait comme mots simple et aussi comme un multiterme
            dic_word_nounPhrase[word]=dic_word_nounPhrase[word]-freq
            freq_word_nounPhrase=freq_word_nounPhrase-freq
            # si la freq a la fin c'est zero apres les traitement on supprime ce mot de notre liste'
                
        for mot,freq in dic_word_nounPhrase.items(): #comptage les ngrams
            count_ngrams[len(mot.split())]+=freq
            count_ngrams['all']+=freq 
         #algorithme pour le calcul de score des mots       
        scores = {word:(dic_word_nounPhrase[word] / count_ngrams['all'])*1/count_ngrams[len(word.split())] for word in dic_word_nounPhrase }
        #trier les mots par leur score
        sorted_words_nounPhrase = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        liste_specifites=[]
        final_extracted_words=[] #la liste des mots sortis finals
            
        for e in sorted_words_nounPhrase:
            liste_specifites.append(e[1])
        moyenne=sum(liste_specifites)/len(liste_specifites) #pour prendre seulement les mots qui sont en dessus de la moyenne des socres
        for e in sorted_words_nounPhrase:
            if e[1]>moyenne:
                final_extracted_words.append(e)
                final_extracted_words.sort(key=lambda tup: tup[1],reverse=True)#trier par frequence          
        return final_extracted_words

#fonction qui ecrit des resultats des extractions dans les fichiers
def write_out(fileout,liste_of_final_extracted_words):        
    #sort les listes
    liste_of_final_extracted_words.sort(key=lambda tup: tup[1],reverse=True)
    #ecriture
    liste_specificity=[]
    for word, specificity in liste_of_final_extracted_words[:26]: 
        #word=word.decode('utf8')
        liste_specificity.append(specificity)
        max_specificity=  max(liste_specificity)  #calcul de maximum des specificites pour faire    
        fileout.write("Word: {}, specificity: {}".format(word.decode("utf8"), round(specificity/max_specificity, 6))+"\n")

# Boucle

for f in corpusIn:
    #ouvrir le fichier pour lire et le mettre en utf8
    fichier= open(f,"r")
    read_data = fichier.read()
    read_data=read_data.decode('utf8')
    #tokeniser le fichier
    tokenizer = WordTokenizer()
    blob = TextBlob(read_data, tokenizer=tokenizer)
    #sanitization
    liste_token=[]
    for token in blob.tokens:
        new_token=re.sub(r"^\d+",'', token).lower()
        if len(new_token)>3:                                    
            liste_token.append(new_token)

    extracted_keywords=extraction_keywords()
    #ouverture des fichiers pour ecrire
    outFile= open(args.output+"/"+os.path.basename(f),"w")
       
    write_out(outFile,extracted_keywords)


    








       
   

    
    
    
    
    
    
    
    
    
    
    
    
    



    


 
