import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests
from django.conf import settings


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=self.hash('127.0.0.1'))

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1

        trusted_hosts = settings.TRUSTED_HOSTS
        hash_trusted_hosts = []
        for trusted_host in trusted_hosts:
            hash_trusted_hosts.append(self.hash(trusted_host))
        print(hash_trusted_hosts)

        while current_index < len(chain):
            block = chain[current_index]
            # print(f'{last_block}')
            # print(f'{block}')
            # print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                print("block['previous_hash'] != last_block_hash")
                return False

            # Check that the Proof of Authority is correct
            # if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
            #     return False
            # trusted_hosts = settings.TRUSTED_HOSTS
            # check = False
            # for trusted_host in trusted_hosts:
            #     print(str(trusted_host))
            #     if self.hash(trusted_host) == last_block['proof']:
            #         check = True
            #         print('Check is True:' + str(trusted_host))
            #         break
            # if check == False:
            #     return False
            if last_block['proof'] not in hash_trusted_hosts:
                print("last_block['proof']" + str(last_block['proof']))
                print("last_block['proof'] not in hash_trusted_hosts")
                return False
            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            print('node in neighbours')
            print(node)
            response = requests.get(f'http://{node}/api/full-chain')
            print(response.status_code)

            if response.status_code == 200:
                length = response.json()['length']
                print('Length: ' + str(length))
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            print('New Chain')
            print(self.chain)
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, tx_hash, device, version, file_hash):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'tx_hash': tx_hash,
            'device': device,
            'version': version,
            'file_hash': file_hash
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_authentication(self, node_address):
        if self.valid_proof(node_address):
            return self.hash(node_address)
        return None

    # def proof_of_work(self, last_block):
    #     """
    #     Simple Proof of Work Algorithm:
    #      - Find a number p' such that hash(pp') contains leading 4 zeroes
    #      - Where p is the previous proof, and p' is the new proof

    #     :param last_block: <dict> last Block
    #     :return: <int>
    #     """
    #     print(last_block)
    #     last_proof = last_block['proof']
    #     last_hash = self.hash(last_block)

    #     proof = 0
    #     while self.valid_proof(last_proof, proof, last_hash) is False:
    #         proof += 1

    #     return proof

    @staticmethod
    def valid_proof(node_address):
        trusted_hosts = settings.TRUSTED_HOSTS
        print(trusted_hosts)
        for trusted_host in trusted_hosts:
            if str(node_address) == trusted_host:
                return True
        return False
        # guess = f'{last_proof}{proof}{last_hash}'.encode()
        # guess_hash = hashlib.sha256(guess).hexdigest()
        # return guess_hash[:4] == "0000"
