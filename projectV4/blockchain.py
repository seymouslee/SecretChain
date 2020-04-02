import datetime as date
import hashlib as hasher
import json
import requests
import sys

from flask import Flask
from flask import request
from flask import jsonify

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

teamMembers = ["Sabrina", "Cheston", "Mabel", "Shi Jia"]

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

peer_nodes = []
mining = True

# Transaction submit.

transactions = []


@node.route('/transaction', methods=['POST'])
def transaction():
    if request.method == 'POST':
        transaction = request.get_json()
        transactions.append(transaction)
        print "New transaction"
        print "FROM: {}".format(transaction['from'])
        print "TO: {}".format(transaction['to'])
        print "AMOUNT: {}\n".format(transaction['amount'])

        return "Transaction submission successful\n"


# @node.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
# def add_message(uuid):
#     content = request.json
#     print content['mytext']
#     return jsonify({"uuid":uuid})

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
    }
    return json.dumps(tojson)


@node.route('/queryTime')
def queryTime():
    blockIndex = request.args.get('Index')  # if key doesn't exist, returns None
    ret = []
    chain = consensus()
    block = chain[int(blockIndex)]
    tojson = {
        "timestamp": str(block.timestamp)
    }
    return json.dumps(tojson)


@node.route('/blocks', methods=['GET'])
def get_blocks():
    ret = []
    for block in consensus():
        ret.append({
            "index": str(block.index),
            "timestamp": str(block.timestamp),
            "name": str(block.data),
            "hash": block.hash,
        })
    return json.dumps(ret)


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
    }
    return json.dumps(tojson)


# Update the current blockchain to the longest blockchain across all other
# peer nodes.
def consensus():
    global blockchain
    longest_chain = blockchain
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
        ret.append(Block(b['index'], b['timestamp'], b['data'], b['hash']))
    return ret


def find_other_chains():
    ret = []
    for peer in peer_nodes:
        response = requests.get('http://%s/blocks' % peer)
        if response.status_code == 200:
            print("blocks from peer: " + response.content)
            ret.append(json.loads(response.content))
    return ret


# just manually do the thing
@node.route('/add_peer', methods=['GET'])
def add_peer():
    host = request.args['host'] if 'host' in request.args else 'localhost'
    port = request.args['port']
    peer = host + ':' + port
    peer_nodes.append(peer)
    print("Peer added: %s" % peer)
    return ""


def main():
    print "Starting"
    port = 5000
    if len(sys.argv) > 1:
        port = sys.argv[1]
    node.run(host='192.168.56.1', port=port)


main()
