from datetime import datetime
import hashlib
import json


class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount


class Block:
    def __init__(self, tstamp, transaction_list, prevhash=''):
        self.nonce = 0
        self.tstamp = tstamp
        self.transaction_list = transaction_list
        self.prevhash = prevhash
        self.hash = self.calc_hash()

    def calc_hash(self):
        block_string = json.dumps(
            {"nonce": self.nonce,
             "tstamp": str(self.tstamp),
             "transaction_list": self.transaction_list[0].amount,   # temporary
             "prevhash": self.prevhash},
            sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != str('').zfill(difficulty):
            self.nonce += 1
            self.hash = self.calc_hash()
        print('Block mined', self.hash)

    def __str__(self):
        string = "nonce: " + str(self.nonce) + '\n'
        string += "tstamp: " + str(self.tstamp) + '\n'
        string += "transaction_list: " + str(self.transaction_list) + '\n'
        string += "prevhash: " + str(self.prevhash) + '\n'
        string += "hash: " + str(self.hash)
        return string


class BlockChain:
    def __init__(self):
        self.chain = [self.generate_genesis_block(), ]
        self.pending_transactions = []
        self.mining_reward = 100
        self.difficulty = 3

    def generate_genesis_block(self):
        return Block('25/08/2019', [Transaction(None, None, 0), ])

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transaction(self, mining_reward_address):
        block = Block(datetime.now(), self.pending_transactions)
        block.mine_block(self.difficulty)
        print('Block is mined to got reward', self.mining_reward)
        self.chain.append(block)
        self.pending_transactions = [Transaction(None, mining_reward_address, self.mining_reward)]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance(self, address):
        balance = 0
        for b in self.chain:
            for t in b.transaction_list:
                if t.to_address == address:
                    balance += t.amount
                if t.from_address == address:
                    balance += t.amount
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prevb = self.chain[i - 1]
            currb = self.chain[i]
            if currb.hash != currb.calc_hash():
                print('invalid block')
                return False
            if currb.prevhash != prevb.hash:
                print('invalid chain')
                return False
        return True


pycoin = BlockChain()

pycoin.create_transaction(Transaction('address1', 'address2', 100))
pycoin.create_transaction(Transaction('address2', 'address1', 40))
print("Starting mining")
pycoin.mine_pending_transaction('MyAddress')
print("Pycoin miner balance is ", pycoin.get_balance("MyAddress"))

pycoin.create_transaction(Transaction('address1', 'address2', 100))
pycoin.create_transaction(Transaction('address2', 'address1', 50))
print("Starting mining 2nd")
pycoin.mine_pending_transaction('MyAddress')
print("Pycoin miner balance is ", pycoin.get_balance("MyAddress"))
# print(pycoin.is_chain_valid())
