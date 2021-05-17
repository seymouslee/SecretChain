import datetime as date
import hashlib as hasher
import json
import requests
import sys
import time

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
node = Flask(__name__)


################ Creation of the BlockChain ################

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # stores the name of the block - our team members names
        self.previous_hash = previous_hash
        self.hash = self.hash_block()  # stores the hash of the previous block

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode(
            'utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()


# Generate genesis block
def startblock(name):
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), name, "0")


# Generate all later blocks in the blockchain
def next_block(last_block, name):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = name
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

teamMembers = ["Sophie", "Sabrina", "Cheston", "Mabel"]

# Create the blockchain and add the first block.
blockchain = [startblock(teamMembers[0])]
previous_block = blockchain[0]

# Add the rest of the blocks to the chain
for i in range(1, len(teamMembers)):
    block_to_add = next_block(previous_block, teamMembers[i])
    blockchain.append(block_to_add)
    previous_block = block_to_add

for q in range(len(blockchain)):
    print("Block #{} has been added to the blockchain!".format(blockchain[q].data))
    print("Hash: {}\n".format(blockchain[q].hash))



################ Part 2: P2P Network ################

peer_nodes = []

# command to add a new node to the blockchain.
@node.route('/addNode')
def addnode():
    name = request.args.get('name')
    ret = []
    chain = consensus()
    if name not in chain:
        prevblock = chain[-1]
        addBlock = next_block(prevblock, name)
        blockchain.append(addBlock)
        tojson = {
            "index": str(addBlock.index),
            "timestamp": str(addBlock.timestamp),
            "data": str(addBlock.data),
            "hash": addBlock.hash,
            "prev_hash": addBlock.previous_hash,
        }
    return json.dumps(tojson), 200


# command to display the details of a particular block
@node.route('/query')
def query():
    blockIndex = request.args.get('Index')  # if key doesn't exist, returns None
    ret = []
    chain = consensus()
    block = chain[int(blockIndex)]
    tojson = {
        "index": str(block.index),
        "timestamp": str(block.timestamp),
        "data": str(block.data),
        "hash": block.hash,
        "prev_hash": block.previous_hash,
    }
    return json.dumps(tojson), 200


# command to display the time of a particular block
@node.route('/queryTime')
def queryTime():
    blockIndex = request.args.get('Index')  # if key doesn't exist, returns None
    ret = []
    chain = consensus()
    block = chain[int(blockIndex)]
    tojson = {
        "timestamp": str(block.timestamp)
    }
    return json.dumps(tojson), 200


# command to display all the details in the entire blockchain
@node.route('/blocks', methods=['GET'])
def get_blocks():
    ret = []
    updatedChain = consensus()
    for block in updatedChain:
        ret.append({
            "index": str(block.index),
            "timestamp": str(block.timestamp),
            "name": str(block.data),
            "hash": block.hash,
            "prev_hash": block.previous_hash,
        })
    return json.dumps(ret), 200


# get the last block in the chain
@node.route('/latest', methods=['GET'])
def get_latest():
    ret = []
    chain = consensus()
    block = chain[-1]
    tojson = {
        "index": str(block.index),
        "timestamp": str(block.timestamp),
        "data": str(block.data),
        "hash": block.hash,
        "prev_hash": block.previous_hash,
    }
    return json.dumps(tojson), 200


# Update the current blockchain to the longest blockchain across all other peer nodes.
# this function searches through all the peer nodes and gets the one with the largest blockchain.
# this is how every node in the network synchronise the blockchain.

def consensus():
    global blockchain
    longest_chain = blockchain
    print blockchain
    for chain in find_other_chains():
        if len(longest_chain) < len(chain):
            longest_chain = chain
    return update_blockchain(longest_chain)


# Updates current blockchain. If updated is needed, converts JSON blockchain to
# list of blocks.
def update_blockchain(src):
    if len(src) <= len(blockchain):
        return blockchain
    ret = []
    for b in src:
        ret.append(Block(b['index'], b['timestamp'], b['name'], b['hash']))
    return ret

# goes to the peer nodes and get all of their blockchains
def find_other_chains():
    ret = []
    for peer in peer_nodes:
        response = requests.get('http://%s/blocks' % peer)
        if response.status_code == 200:
            print("blocks from peer: " + response.content)
            ret.append(json.loads(response.content))
    return ret


# let itself be known to the other nodes.
# this is how nodes know which node it will need to extract the blockchain from to do synchronisation.
@node.route("/addPeer", methods=["GET"])
def get_my_ip():
    peerAddr = request.remote_addr + ':' + str(port)
    if peerAddr not in peer_nodes:
        peer_nodes.append (peerAddr)
        print peer_nodes
    return jsonify({'ip': peerAddr}), 200


def main():
    print "Starting"
    global port
    port = 5000     # set the port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    node.run(host='0.0.0.0', port=port)
    # makes sure all the nodes within the same network is able to communicate with the current node.


main()
