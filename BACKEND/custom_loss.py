from fastai.text import *
info = np.load('config.npy',allow_pickle=True)
min_val=int(info[0])
range_val=int(info[1])
def reg_loss(pred,ref):
    ref=ref.float()
    #print (min_val,range_val)
    pred=pred.view(-1)
    #print (pred,ref)
    return  nn.functional.mse_loss(range_val*F.sigmoid(pred)+min_val,ref)
    
