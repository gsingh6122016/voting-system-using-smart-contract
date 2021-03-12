from flask import Flask, jsonify, abort, make_response, request, url_for,session
from flask import render_template, redirect
import json
import requests 
import hashlib
import os
from web3 import Web3

rpc = "HTTP://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(rpc))

abi = '[{"constant":false,"inputs":[{"name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"name","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"end","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"}]'

contract_addr = "0x3Bf7E6310939aE8505643ef22c14dcD763FCe3Cf"

app = Flask(__name__)
app.secret_key = 'i love white chocolate too'

accounts = [ 
    '0x9321dC58E8F26Fe3d13772F8f10c432b3e220417',
    '0x26cAF5BD0cFB4Eb982db6505C484fe3675dC3502',
    '0x95df7861df5109d3F542D496280F42F0DF9A303b',
    '0xBf797cC587333e6f8D49fb4715a05B726b3B056E'
]

privatekeys = [
    'c08d63ff826b19c81f15c22bd5c70c79748641f71e7e769251934f49a7a6f9d2',
    '4a9c13c506e4a863f34bd6162e32e68aab95633f533f53ad3277c64bbe104efa',
    'ac6f482afe906bc55b51041b05a8e183b790e98f4511dbd7c53a7e74873ac1fd',
    '40bd2323fc5bbc9fd71b81e18b41ecfbc7855d682364e2e516b0409c43f3de54'

]

vote_tx = []
voted = []
ended = 0

@app.route("/" , methods=['POST'])
def home():
    if(not ended):
        try:
            data = eval(request.data) # {"aadhaarID":int(),"candidateID":int()}
            print('data', data)
            
            aid = int(data["aadhaarID"])-1
            print('aid', aid)
            if(aid in voted):
                return "Already voted",400

            
            cid = int(data["candidateID"])
            print('cid', cid)
            acc = accounts[aid]
            pvt = privatekeys[aid]
            print('acc', acc)
            print('pvt', pvt)
            
            contract = web3.eth.contract(address=contract_addr, abi=abi)
            print('contract', contract)
            transaction = contract.functions.vote(cid).buildTransaction()
            print('transaction', transaction)
            transaction['nonce'] = web3.eth.getTransactionCount(acc)
            print('transaction nonce', transaction['nonce'])

            signed_tx = web3.eth.account.signTransaction(transaction, pvt)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            vote_tx.append(tx_hash)
            voted.append(aid)
            return "Vote successfully casted",200
        except:
            return "Error processing",500
    else:
        return "Election period ended",400

@app.route("/results" , methods=['GET'])
def count():
    res = []
    election = web3.eth.contract(address=contract_addr, abi=abi)
    for i in range(election.caller().candidatesCount()):    
        res.append(election.caller().candidates(i+1))
    return json.dumps(res),200


@app.route("/end" , methods=['POST'])
def end_election():
    global ended
    
    acc = accounts[3]
    pvt = privatekeys[3]
    contract = web3.eth.contract(address=contract_addr, abi=abi)
    print('acc', acc)
    print('pvt', pvt)
    transaction  = contract.functions.end().buildTransaction()

    transaction['nonce'] = web3.eth.getTransactionCount(acc)

    signed_tx = web3.eth.account.signTransaction(transaction, pvt)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    ended += 1
    return "Election successfully ended\nTx Hash : %s"%(str(tx_hash)),200

@app.route("/number_of_users" , methods=['GET'])
def number_of_users(): 
    try:
        return str(len(accounts)),200
    except:
        return "Error processing",500

@app.route("/is_ended" , methods=['GET'])
def is_ended(): 
    return str(ended>0),200

@app.route("/candidates_list" , methods=['GET'])
def candidates_list():
    try:
        res = []

        election = web3.eth.contract(address=contract_addr, abi=abi)
        print('election', election)
     
        for i in range(election.caller().candidatesCount()):    
            res.append(election.caller().candidates(i+1)[1])
            print('candy', election.caller().candidates(i+1)) 
        
        return json.dumps(res),200
    except:
        print('res', res)
        return "Error processing",500


        

if __name__ == '__main__':
	app.run(host="0.0.0.0" ,port=80, debug = True)