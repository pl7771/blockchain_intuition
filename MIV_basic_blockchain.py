# Create blockchain
# Important libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

##### BUILDING BLOCKCHAIN #####
class Blockchain:
    
    # Constructor
    def __init__(self):
        self.chain = [] 
        self.create_block(proof = 1, previous_hash = '0')
    
    # block creating and adding to chain        
    def create_block(self, proof, previous_hash):
        block = {
                 'index': len(self.chain)+1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                }
        self.chain.append(block)
        return block
    
    #return last block of chain
    def get_previous_block(self):
        return self.chain[-1]
    
    # working on proof to get hash starting with 0000
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else: 
                new_proof += 1
        return new_proof
    
    # hash given block   
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # check or chain is fully valid
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
            
##### CREATE WEBAPP #####
app = Flask(__name__)

# get blockchain
blockchain = Blockchain()

# Mine a block on user side
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    responce = {'message': 'Congratulations you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(responce), 200

# Get full blockchain on user side
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    responce = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(responce, 200)    

# Is chain valid request on user side
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    responce = {'is_valid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(responce, 200) 

# Run application
app.run(host = '0.0.0.0', port = '5000')


































            
            
            
            
            
            
            