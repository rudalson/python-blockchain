from datetime import datetime
import hashlib
import json
from flask import Flask
from flask import jsonify
from time import time


class Block:
    def __init__(self, nonce, tstamp, transaction_list, prevhash='', hash=''):
        self.nonce = nonce
        self.tstamp = tstamp
        self.transaction_list = transaction_list
        self.prevhash = prevhash
        if hash == '':
            self.hash = self.calc_hash()
        else:
            self.hash = hash

    def calc_hash(self):
        block_string = json.dumps(
            {"nonce": self.nonce,
             "tstamp": str(self.tstamp),
             "transaction_list": self.transaction_list,  # temporary
             "prevhash": self.prevhash},
            sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != str('').zfill(difficulty):
            self.nonce += 1
            self.hash = self.calc_hash()
        print('Block mined', self.hash)

    def to_dict(self):
        return {"nonce": self.nonce, "tstamp": str(self.tstamp), "transaction_list": self.transaction_list,
                "prevhash": self.prevhash, "hash": self.hash}


class BlockChain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.mining_reward = 100
        self.difficulty = 3
        self.generate_genesis_block()

    def generate_genesis_block(self):
        dect = {"nonce": 0, "tstamp": "28/09/2019",
                "transaction_list": [{'from_address': None, 'to_address': None, 'amount': 0}, ], 'hash': ''}
        b = Block(**dect)
        self.chain.append(b.to_dict())

    def get_last_block(self):
        return Block(**self.chain[-1])

    def mine_pending_transaction(self, mining_reward_address):
        block = Block(0, str(datetime.now()), self.pending_transactions)
        block.prevhash = self.get_last_block().hash
        block.mine_block(self.difficulty)
        print('Block is mined to got reward', self.mining_reward)
        self.chain.append(block.to_dict())
        self.pending_transactions = [
            {'from_address': None, 'to_address': mining_reward_address, 'amount': self.mining_reward}, ]

    def create_transaction(self, from_address, to_address, amount):
        self.pending_transactions.append({'from_address': from_address, 'to_address': to_address, 'amount': amount})

    def get_balance(self, address):
        balance = 0
        for index in range(len(self.chain)):
            dict_list = self.chain[index]["transaction_list"]
            for dic in dict_list:
                if dic["to_address"] == address:
                    balance += dic['amount']
                if dic['from_address'] == address:
                    balance += dic['amount']
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prevb = Block(**self.chain[i - 1])
            currb = Block(**self.chain[i])
            if currb.hash != currb.calc_hash():
                print('invalid block')
                return False
            if currb.prevhash != prevb.hash:
                print('invalid chain')
                return False
        return True


pycoin = BlockChain()

pycoin.create_transaction('address1', 'address2', 100)
pycoin.create_transaction('address2', 'address1', 40)
print("Starting mining")
pycoin.mine_pending_transaction('MyAddress')
print("Pycoin miner balance is ", pycoin.get_balance("MyAddress"))
print(pycoin.is_chain_valid())

app = Flask(__name__)


@app.route('/mine', methods=['GET'])
def mine():
    return "we are going to mine the block with new transactions here"


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return None


@app.route('/chain', methods=['GET'])
def display_full_chain():
    response = {
        'chain': pycoin.chain,
        'length': len(pycoin.chain)
    }
    return jsonify(response), 200


@app.route('/')
def hello():
    return "Hello you are in the main page of this node"


if __name__ == "__main__":
    app.run()
