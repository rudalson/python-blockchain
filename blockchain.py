import hashlib
import json


class Block():
    def __init__(self, nonce, tstamp, transaction, prevhash=''):
        self.nonce = nonce
        self.tstamp = tstamp
        self.transaction = transaction
        self.prevhash = prevhash
        self.hash = self.calc_hash()

    def calc_hash(self):
        block_string = json.dumps(
            {"nonce": self.nonce,
             "tstamp": self.tstamp,
             "transaction": self.transaction,
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
        string += "transaction: " + str(self.transaction) + '\n'
        string += "prevhash: " + str(self.prevhash) + '\n'
        string += "hash: " + str(self.hash)
        return string


class BlockChain():
    def __init__(self):
        self.chain = [self.generate_genesis_block(), ]
        self.difficulty = 2

    def generate_genesis_block(self):
        return Block(0, '25/08/2019', 'Genesis Block')

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.prevhash = self.get_last_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

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
pycoin.add_block(Block(1, '26/08/2019', 100))
pycoin.add_block(Block(2, '26/08/2019', 20))
print()

for b in pycoin.chain:
    print(b)
    print()

print(pycoin.is_chain_valid())
