from lstm_model import AttentionModel
from fastai.text import *
from create_toks import get_texts
from qwk import quadratic_weighted_kappa
torch.cuda.set_device(9)
bs=32
output_size=1
hidden_size=128
itos=pickle.load(open('./data/essay1/tmp/itos.pkl','rb'))
vocab_size=len(itos)
embedding_length=300
stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})

m=AttentionModel(output_size=output_size,hidden_size=hidden_size,vocab_size=vocab_size,
    embedding_length=embedding_length)
m.cuda()
m.load_state_dict(torch.load('models/best.pth'))

def predict(m,ds_test):
    tok_test, test_labels = get_texts(ds_test, 1)
    test_cls = np.array([[stoi[o] for o in p] for p in tok_test])
    test_labels=np.squeeze(test_labels)
    test_ds = TextDataset(test_cls, test_labels)
    test_dl=DataLoader(test_ds, bs, transpose=True, num_workers=1, pad_idx=1)
    m.eval()
    result=[]
    itrator=iter(test_dl)
    while True:
        try:
            x,y=next(itrator)
            #print (x)
            
            m.eval()
            out=m(V(x))
            result.append(F.sigmoid(out).cpu().data.numpy())
            #print (result)
        except:
            break
    #print (result)
    predictions=[]
    for ix in result:
        for iy in ix:
            predictions.append(10*iy+2)
    predictions=np.rint(np.stack(predictions))
    return np.reshape(predictions,(-1))



df_test=pd.read_csv(f'data/essay1/test.csv',header=None)
ds_test=pd.DataFrame({0:0,1:df_test[1]})
ans=predict(m,ds_test)
print(quadratic_weighted_kappa(df_test[0].values,ans))


#df_test[4]=ans
#df_test.to_csv('data/task1_results.csv',header=None,index=False)




