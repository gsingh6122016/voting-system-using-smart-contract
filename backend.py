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

contract_addr = "0x8F4fFf02f84F3332dD03FFFf1Aba14dB505842a0"

app = Flask(__name__)
app.secret_key = 'i love white chocolate too'

accounts = [ 
    '0xE4a79650293bb08873deeDF2e9AC9F15e1e4F3f1',
    '0x40bbbD9B26aC7B31004440506c9eC9c2Ccf8e7c0',
    '0xb74887C102Ff10012ecFd03FF245E7D9Fb6c0409'
]

privatekeys = [
    'aed93b732590eb6962293b31c3fad47e342447a02b28ce80c456bf31a1e6f5b3',
    'fa551b1457c37523094d987be6e5839e5188d476072826bae922508346ceb0df',
    '02472f4a764a2ef81ec6827f51552fadda9dc6597a438e72b412aa8a6e4e1319',
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
    if(ended):
            res = []
            election = web3.eth.contract(address=contract_addr, abi=abi)
            for i in range(election.caller().candidatesCount()):    
                res.append(election.caller().candidates(i+1))
            return json.dumps(res),200
    else:
        return "Election still on going",400

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