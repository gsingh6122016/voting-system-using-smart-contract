from flask import Flask, jsonify, abort, make_response, request, url_for,session
from flask import render_template, redirect
import json
import requests 
import hashlib
import os
from web3 import Web3
from flask_cors import CORS

rpc = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(rpc))

abi = json.loads('[{"constant":false,"inputs":[{"name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"candidatesCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"candidates","outputs":[{"name":"id","type":"uint256"},{"name":"name","type":"string"},{"name":"party","type":"string"},{"name":"voteCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"voters","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')

contract_addr = web3.toChecksumAddress("0x8996c8C51aa662029C8aa197c225069D4Db85809")

app = Flask(__name__)
CORS(app)
app.secret_key = 'i love white chocolate too'


accounts = [ 
    '0x8817bDcBCf71b015CCA177e1751209CCA6d806ba',
    '0x9F02e224FD2e5fC3F841f131d05AAC11D21C2271',
    '0xA60996bd543A50E3a38f199FD807e5941cF10666',
    '0x664E8978Bf36f479EC3E3883EA13b60ecF7e4400',
    '0x4F7579F9BBB7b7f25BDbe73d1302380dFdD74e9B',
    '0xc19a7731510D4FC92Bf5C1c56FaeC4A8Bd7e0419'

]

privatekeys = [
    '0030464ee54f4d94107e1995d1a0aa5b6e1cd361080c7cdaa703c7bfa3fe646b',
    '2c58dadba5ff418a3425fcaaa1349e540a3edc6c67487c4a68f428366d5966b1',
    '629986d72dbab950b8421a9c5d297edfdebb53e8b0ed7fcce3f6032b0546d2c5',
    '24dfa8681e6cba8805b2db7d68ab92f1ebaa163e123945aac8d848bc49c6faff',
    '456e9ac53395306cdfb0c6b32b614ba7d015b057f6e9a852533305258d12d340',
    '827c89cb6241eb852a711dac1f6acbecfee2833449a8a750fa307e385820a82d'
]

vote_tx = []
voted = []
ended = 0
logged = []
voter_id = 0



@app.route("/vote" , methods=['POST'])
def home():
    if(not ended):
        # try:

        data = eval(request.data) # {"aadhaarID":int(),"candidateID":int()}
        print('data', data)

        aid = int(data["aadhaarID"])-1
        print('aid', aid)
        # if(aid in voted):
        #     return "Already voted",400

        cid = int(data["candidateID"])
        print('cid', cid)
        print(web3.eth.accounts)
        acc = accounts[aid]
        pvt = privatekeys[aid]
        print('acc', acc)
        print('pvt', pvt)

        contract = web3.eth.contract(address=contract_addr, abi=abi)
        print('contract', contract)
        transaction = contract.functions.vote(cid).buildTransaction()
        transaction['nonce'] = web3.eth.getTransactionCount(acc)
        print('transaction', transaction)
        balance = web3.eth.getBalance(acc)
        print(balance)
        signed_tx = web3.eth.account.signTransaction(transaction, pvt)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        vote_tx.append(tx_hash)
        voted.append(aid)
        return "Vote successfully casted",200
        # except:
        #     return "Error processing",500
    else:
        return "Election period ended",400


@app.route("/login" , methods=['POST'])
def login():
    if(not ended):
        try:
            data = eval(request.data) 
            print('data', data)

            ano = int(data["aadhaarNo"])
            print('ano', ano)

            # if(ano in logged):
            #     return "Already voted",400

            global voter_id
            voter_id+=1
            logged.append(ano)
            print('voter id', voter_id)
            return json.dumps(voter_id),200
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