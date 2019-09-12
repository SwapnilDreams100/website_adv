from lstm_model import AttentionModel
from fastai.text import *
from create_toks import get_texts,fixup
from custom_tokenizer import tokenize_it
torch.cuda.set_device(9)
output_size=1
hidden_size=128
itos=pickle.load(open('./data/essay1/tmp/itos.pkl','rb'))
stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})
vocab_size=len(itos)
embedding_length=300
stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})

m=AttentionModel(output_size=output_size,hidden_size=hidden_size,vocab_size=vocab_size,
    embedding_length=embedding_length)
m.cuda()
m.load_state_dict(torch.load('models/best_e1_7.pth'))
#m.cpu()
#torch.save(m.state_dict(),'models/best_e1_cpu.pth')

def get_results(text):
    tokenizer=Tokenizer()
    tokens=tokenize_it(fixup(text))
    tok=[stoi[o] for o in tokens]
    tok=V(np.array(tok))
    tok=tok.view((-1,1))
    out,attn=(m(tok,return_attn=True))
    score=(np.rint((F.sigmoid(out.view(-1))*10+2).data.cpu().numpy())[0])
    attn=attn.view(-1).data.cpu().numpy()
    return (score,attn,tokens)

if __name__=='__main__':
    print(get_results("hi this is me"))
