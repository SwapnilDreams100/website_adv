import numpy as np 
import fastText


def embs(itos,path):
	model=fastText.load_model(path)
	emb=[]
	for w in itos:
		emb.append(model.get_word_vector(w))
	np.save('embeddings.npy',np.stack(emb))

itos_path  =
model_path =

itos = pickle.load(open(itos_path))

embs(itos,model_path)
