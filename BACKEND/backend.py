# import mysql.connector

from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api, reqparse
import argparse

app = Flask(__name__)

import ast
import pickle

from lstm_model import AttentionModel
from fastai.text import *
from create_toks import get_texts,fixup
from custom_tokenizer import tokenize_it


# CNXN = mysql.connector.connect(host ="localhost",user ="root",database='hosp_db',passwd="xxx@555")
# CURSOR = CNXN.cursor()

@app.errorhandler(404)
def pageNotFound(error):
    return ("page not found")

@app.errorhandler(500)
def raiseError(error):
    return (error)

# torch.cuda.set_device(9)
output_size=1
hidden_size=128
itos=pickle.load(open('./data/essay1/tmp/itos.pkl','rb'))
stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})
vocab_size=len(itos)
embedding_length=300
stoi = collections.defaultdict(lambda:0, {v:k for k,v in enumerate(itos)})

m=AttentionModel(output_size=output_size,hidden_size=hidden_size,vocab_size=vocab_size,
    embedding_length=embedding_length)
# m.cuda()
# m.load_state_dict(torch.load('models/best.pth'))
m.load_state_dict(torch.load('models/best_e1_cpu.pth'))


@app.route('/get_essay', methods=['GET'])
def get_essay():
    
    parser = reqparse.RequestParser()

    parser.add_argument('prompt', type=str, required=True)  
    parser.add_argument('essay', type=str, required=True)
    args = parser.parse_args()
    
    essay = args['essay']
    prompt = args['prompt']

    text = essay
    
    tokenizer=Tokenizer()
    tokens=tokenize_it(fixup(text))
    tok=[stoi[o] for o in tokens]
    tok=V(np.array(tok))
    tok=tok.view((-1,1))
    out,attn=(m(tok,return_attn=True))
    score=(np.rint((F.sigmoid(out.view(-1))*10+2).data.cpu().numpy())[0])
    attn=attn.view(-1).data.cpu().numpy()
    # return (score,attn,tokens)
    # print(attn)
    # print(score)
    # print(tokens)
    # print('-----------------------------------------------------')
    # print(type(attn))
    # print(type(score))
    # print(type(tokens))

    new_data=[]
    new_data.append({ 'score':int(score),'attn':str(list(attn)),'tokens':tokens })
    return jsonify(new_data)

@app.route('/send_log', methods=['GET'])
def send_log():
    
    parser = reqparse.RequestParser()
    
    parser.add_argument('prompt', type=str, required=True)  
    parser.add_argument('essay', type=str, required=True)
    parser.add_argument('feedback_score', type=str, required=True)  
    parser.add_argument('reorder', type=str, required=True)
    
    args = parser.parse_args()
    
    essay = args['essay']
    prompt = args['prompt']

    feedback_score = args['feedback_score']
    reorder = args['reorder']

    dict_new = {}

    dict_new['feed_score'] = int(feedback_score)
    dict_new['prompt'] = int(prompt)
    dict_new['reorder'] = ast.literal_eval(reorder.split(':')[1].split('}')[0])
    dict_new['essay'] = essay
    
    import os.path
    
    if os.path.exists('./json_store.pkl'):
    
        with open('json_store.pkl','rb') as f:
            data = pickle.load(f)
        data.append(dict_new)
        with open('json_store.pkl','wb') as f:
            pickle.dump(data,f)
    else:
        data = []
        data.append(dict_new)
        with open('json_store.pkl','wb') as f:
            pickle.dump(data,f)
        
    new_data=[]
    return jsonify(new_data)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return (response)

if __name__ == '__main__':
    app.run(debug=True)