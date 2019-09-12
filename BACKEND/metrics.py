from sklearn.metrics import f1_score
from fastai.text import *

def f1(preds,targs):
    targs=targs.cpu().numpy()
    preds=np.argmax(F.softmax(V(preds)).data.cpu().numpy(),axis=1)
    return f1_score(targs,preds)
