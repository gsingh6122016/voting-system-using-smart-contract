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

contract_addr = web3.toChecksumAddress("0xd620514E9AfE39A6B68F23783Ef605F375daDfFd")

app = Flask(__name__)
CORS(app)
app.secret_key = 'i love white chocolate too'


accounts = [ 
    '0x36c67aa74daC10a8f31d2a025287670f7c26Ae7c',
    '0x371d3798aDEA0c839B2396c0a79DC584292ED8Dc',
    '0x3f42E4Ed29F5a24d91D19c686Fe767EB1583907c'


]

privatekeys = [
    '570220e67f74b9d7daf28b85bcea528eb4bd8e4032daeaba7e9f67ba945b42f2',
    'cde8314e9f12fc7b78101958bebee83c0085295b8d056d80a3f0b475aa97337b',
    'c1df54397c92011e17b505fa4a073d58b51f87dd7ea4cb3eaf5687cc25a34bc8'

]

vote_tx = []
voted = []
ended = 0
logged = []
voter_id = 0
admin_user='gourav'
admin_pass='12345'


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

            if(ano in logged):
                return "Already voted",401

            global voter_id
            voter_id+=1
            logged.append(ano)
            print('voter id', voter_id)
            return json.dumps(voter_id),200
        except:
            return "Error processing",500
    else:
        return "Election period ended",400


@app.route("/admin-login" , methods=['POST'])
def adminLogin():
    data = eval(request.data) 
    username = data["username"]
    password = data["password"]
    print('username and password', username, password)
    print('req username and password', admin_user, admin_pass)
    if username==admin_user and password==admin_pass:
        return "Sucessfully Logged In",200
    else:
        return "wrong username or password",401



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
    ended += 1
    return "Election successfully ended",200

@app.route("/number_of_users" , methods=['GET'])
def number_of_users(): 
    try:
        return str(len(accounts)),200
    except:
        return "Error processing",500

@app.route("/is_ended" , methods=['GET'])
def is_ended(): 
    return str(ended>0),200

# @app.route("/candidates_list" , methods=['GET'])
# def candidates_list():
#     try:
#         res = []

#         election = web3.eth.contract(address=contract_addr, abi=abi)
#         print('election', election)
     
#         for i in range(election.caller().candidatesCount()):    
#             res.append(election.caller().candidates(i+1)[1])
#             print('candy', election.caller().candidates(i+1)) 
        
#         return json.dumps(res),200
#     except:
#         print('res', res)
#         return "Error processing",500


        

if __name__ == '__main__':
	app.run(host="0.0.0.0" ,port=80, debug = True)