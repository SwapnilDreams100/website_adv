import re
import nltk
def tokenize_it(string):
   tokens = nltk.word_tokenize(string)
   for index, token in enumerate(tokens):
       if token == '@' and (index+1) < len(tokens):
           tokens[index+1] = '@' + re.sub('[0-9]+.*', '', tokens[index+1])
           tokens.pop(index)
   return ['_start_']+tokens+['_end_']

def tokenize_it_all(rows):
	tokens=[tokenize_it(i) for i in rows]
	return tokens


if __name__=='__main__':
   tok=tokenize_it_all(['this is a sting'])
   print (tok)
