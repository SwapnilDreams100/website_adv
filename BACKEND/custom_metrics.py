from fastai.text import *
from qwk import quadratic_weighted_kappa
#from config import sc_min,sc_range
info = np.load('config.npy',allow_pickle=True)
def get_metric(preds,targs):
    targs=targs.cpu().numpy()
    preds=np.reshape(np.rint(F.sigmoid(V(preds)).data.cpu().numpy()*info[1] + info[0]),-1)
    return quadratic_weighted_kappa(targs,preds)

