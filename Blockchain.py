import datetime
import hashlib
import json
from re import template
from flask import Flask,jsonify, render_template
#### Building a Blockchain ########
class Blockchain:
    def __init__(self):
        self.chain=[]           #list that will contain all our block
        self.create_block(proof = 1,prev_hash='0')      #to create our first block or (Genesis block)
    
    def create_block(self,proof,prev_hash):
        block={'index':len(self.chain)+ 1, 
        'timestamp':str(datetime.datetime.now()),
        'proof':proof,
        'prev_hash':prev_hash}
        self.chain.append(block)      # create and append the block to our chain
        return block
    def get_prev_block(self):
        return self.chain[-1]       # get the last block of the chain
    def proof_of_work(self,prev_proof):
        new_proof= 1
        check_proof=False
        while check_proof is False:
            hash_operation= hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] =='0000':
                check_proof=True        #when four 0 are meet then we break the loop as we have mined our coin
            else:
                new_proof+=1
        return new_proof

    def hash(self,block):
        encoed_block =json.dumps(block, sort_keys=True).encode() #get the hash of each block json dumps is used to conert our dictonary as string
        return hashlib.sha256(encoed_block).hexdigest()  #return hexvalue

    def verify(self,chain):
        previousBlock=self.chain[0]
        blockIndex=1
        while blockIndex<len(chain):
            block=chain[blockIndex]
            if block['prev_hash'] != self.hash(previousBlock):
                return False                        #return false when the hash of the previous block doesn't match the current block
            prev_proof=previousBlock['proof']
            proof=block['proof']
            hash_operation= hashlib.sha256(str(proof*3 - prev_proof*3).encode()).hexdigest()      #get the hash generated inorder to check if it follows our four 0 rule
            if hash_operation [:4]!='0000':
                return False                    #return false it the genrated hash doesn't follow our rule
            previousBlock=block     #increment the previous block to our current block
            blockIndex+=1   #increment to the next block
        return True


##### WEB APP ######
blockchain=Blockchain()
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/mine',methods=['GET'])
def mine():
    prev_block=blockchain.get_prev_block()      #get the previous block
    prev_proof=prev_block['proof']      #get the proof from the previous block
    proof=blockchain.proof_of_work(prev_proof)      #get the proof of the mined block
    prev_hash=blockchain.hash(prev_block)   #get the hash of revious block
    block=blockchain.create_block(proof,prev_hash)      #creating our new block just by inserting the value
    response= {'message':"Block Minned",
    'index':block['index'],
    'timestamp':block['timestamp'],
    'proof':block['proof'],
    'prev_hash':block['prev_hash']}
    return jsonify(response),200


#### Create a Blockchain ######


#### Get Full Blockchain ####
@app.route('/get_block',methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
    'length':len(blockchain.chain)}
    return jsonify(response),200

@app.route('/verify',methods=['GET'])
def verify():
    result=blockchain.verify(blockchain.chain)
    if result:
        msg="Verified"
    else:
        msg="Eroor Not Verified"
    response={'Verification':msg}
    return jsonify(response)


app.run(host='0.0.0.0',port= 5000,debug=True)
#The end