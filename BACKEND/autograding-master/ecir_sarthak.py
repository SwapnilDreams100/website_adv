from metrics import f1
from fastai.text import *
from lstm_model import AttentionModel
import argparse
from early import EarlyStopping
#from custom_metrics import get_metric
#from custom_loss import reg_loss
#print (get_metric)
def train(bs,cuda_id,embedding_length=200,nh=128,output_size=1,info=None):
    dir_path=Path('./data/essay1/')
    tmp_path=dir_path/'tmp/'
    torch.cuda.set_device(cuda_id)

    np.save('config.npy',np.array(info))
    from custom_metrics import get_metric
    from custom_loss import reg_loss
    itos = pickle.load(open(tmp_path/'itos.pkl', 'rb'))
    vs = len(itos)
    stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})

    trn_sent = np.load(tmp_path/'trn_ids.npy',allow_pickle=True)
    val_sent = np.load(tmp_path/'val_ids.npy',allow_pickle=True)
    trn_labels=np.squeeze(np.load(tmp_path/'lbl_trn.npy',allow_pickle=True))
    val_labels=np.squeeze(np.load(tmp_path/'lbl_val.npy',allow_pickle=True))

    trn_ds = TextDataset(trn_sent, trn_labels)
    val_ds = TextDataset(val_sent, val_labels)
    trn_samp = SortishSampler(trn_sent, key=lambda x: len(trn_sent[x]), bs=bs)
    val_samp = SortSampler(val_sent, key=lambda x: len(val_sent[x]))
    trn_dl = DataLoader(trn_ds, bs, transpose=True, num_workers=1, pad_idx=1, sampler=trn_samp,drop_last=True)
    val_dl = DataLoader(val_ds, bs, transpose=True, num_workers=1, pad_idx=1, sampler=val_samp,drop_last=True)
    md = ModelData(dir_path, trn_dl, val_dl)
    print ('Building Model')
    emb_weights=np.load(tmp_path/'embeddings.npy',allow_pickle=True)
    m=AttentionModel(output_size=output_size,hidden_size=nh,vocab_size=vs,
                 embedding_length=embedding_length,load_emb=True,emb_weights=emb_weights)
    m=m.cuda()
    lo=LayerOptimizer(optim.Adam,m,1e-2,1e-5)
    cb=[CosAnneal(lo,len(md.trn_dl),cycle_mult=2),EarlyStopping(m,'best.pth')]
    #print (reg_loss)
    fit(m, md, 2**5-1, lo.opt,reg_loss ,metrics=[accuracy,get_metric],callbacks=cb)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('bs',type=int)
    parser.add_argument('cuda_id',type=int)
    args=parser.parse_args()
    train(args.bs,args.cuda_id,embedding_length=300,info=[2,10])
