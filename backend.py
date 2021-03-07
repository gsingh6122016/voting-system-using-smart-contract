from flask import Flask, jsonify, abort, make_response, request, url_for,session
from flask import render_template, redirect
import json
import requests 
import hashlib
import os
from web3 import Web3

rpc = "HTTP://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(rpc))
abi = '[{"constant": false,"inputs": [{"name": "_candidateId","type": "uint256"}],"name": "vote","outputs": [],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [],"name": "candidatesCount","outputs":[{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"	},{		"constant": true,		"inputs": [			{				"name": "",				"type": "uint256"			}		],		"name": "candidates",		"outputs": [			{				"name": "id",				"type": "uint256"			},			{				"name": "name",				"type": "string"			},			{				"name": "voteCount",				"type": "uint256"			}		],		"payable": false,		"stateMutability": "view",		"type": "function"	},	{		"constant": true,		"inputs": [			{				"name": "",				"type": "address"			}		],		"name": "voters",		"outputs": [			{				"name": "",				"type": "bool"			}		],		"payable": false,		"stateMutability": "view",		"type": "function"	},	{		"constant": false,		"inputs": [],		"name": "end",		"outputs": [],		"payable": false,		"stateMutability": "nonpayable","type": "function"	},{"inputs": [],"payable": false,"stateMutability": "nonpayable","type": "constructor"},{"anonymous": false,"inputs": [{"indexed": true,"name": "_candidateId","type": "uint256"}],"name": "votedEvent","type": "event"	}]'


contract_addr = "0xC3d005F516E7aAA2d08eE32a6e4311D27A319952"


app = Flask(__name__)
app.secret_key = 'i love white chocolate too'

accounts = [ 
    '0x35e6B58457F5c347522b64cC5D2a7B4605EC16a8',
    '0x00F60A577C8f9D577300cA35280848C30Faac0F1',
    '0xDB4B8aBb2Ba9565FD5945f848355531Cb5ed6a4F'

]

privatekeys = [
    '4a4600e80b9e95a6489b1b981a1d5f60d0e8faa953143c026c3b0d5239fd4731',
    'b722382c98098448325d298622ebfd809d66e176f64650c9ecebe49f44f5e1ac',
    '7cc068cc378d5473edbd42a8812eb0d3b31e4ad9ef7765c1444d4ec62eacef40',
]

vote_tx = []
voted = []
ended = 0

# @app.route("/" , methods=['POST'])
# def home():
#     if(not ended):
#         try:
#             data = eval(request.data) # {"aadhaarID":int(),"candidateID":int()}
#             aid = int(data["aadhaarID"])-1
#             if(aid in voted):
#                 return "Already voted",400
#             cid = int(data["candidateID"])
#             acc = accounts[aid]
#             pvt = privatekeys[aid]
#             contract = web3.eth.contract(address=contract_addr, abi=abi)
#             transaction  = contract.functions.vote(cid).buildTransaction()
#             transaction['nonce'] = web3.eth.getTransactionCount(acc)

#             signed_tx = web3.eth.account.signTransaction(transaction, pvt)
#             tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
#             vote_tx.append(tx_hash)
#             voted.append(aid)
#             return "Vote successfully casted",200
#         except:
#             return "Error processing",500
#     else:
#         return "Election period ended",400

# @app.route("/results" , methods=['GET'])
# def count():
#     if(ended):
#             res = []
#             election = web3.eth.contract(address=contract_addr, abi=abi)
#             for i in range(election.caller().candidatesCount()):    
#                 res.append(election.caller().candidates(i+1))
#             return json.dumps(res),200
#     else:
#         return "Election still on going",400

# @app.route("/end" , methods=['POST'])
# def end_election():
#     global ended
#     ended += 1
#     acc = '0x6613a49512fE3B3243be92913343BD61CceA9535'
#     pvt = '25d9479cd21fb800522f8e0c74513f0730f7afac9f3ac7a23d8ad69b7103be52'
#     contract = web3.eth.contract(address=contract_addr, abi=abi)
#     transaction  = contract.functions.end().buildTransaction()
#     transaction['nonce'] = web3.eth.getTransactionCount(acc)

#     signed_tx = web3.eth.account.signTransaction(transaction, pvt)
#     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
#     return "Election successfully ended\nTx Hash : %s"%(str(tx_hash)),200

@app.route("/number_of_users" , methods=['GET'])
def number_of_users(): 
    try:
        return str(len(accounts)),200
    except:
        return "Error processing",500

# @app.route("/isended" , methods=['GET'])
# def isended(): 
#     return str(ended>0),200

@app.route("/candidates_list" , methods=['GET'])
def candidates_list():
    try:
        res = []

        election = web3.eth.contract(address=contract_addr, abi=abi)
     
        for i in range(election.caller().candidatesCount()):    
            res.append(election.caller().candidates(i+1)[1]) 
        
        return json.dumps(res),200
    except:
        print('res', res)
        return "Error processing",500

# @app.route("/test" , methods=['GET'])
# def candidates_list():
# 	res = []
# 	contract = web3.eth.contract(address=contract_addr, abi=abi)
# 	transaction = contract.caller().candidatesCount()
# 	print('count', transaction)
        

if __name__ == '__main__':
	app.run(host="0.0.0.0" ,port=80, debug = True)