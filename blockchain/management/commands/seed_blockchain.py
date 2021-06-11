from django.core.management.base import BaseCommand
from blockchain.blockchain import Blockchain
import uuid

blockchain = Blockchain()

node_identifier = str(uuid.uuid4()).replace('-', '')


class Command(BaseCommand):
    def handle(self, *args, **options):
        transactions = [
            {'tx_hash': '6a4c39085fde4f5d95be69c872781a29', 'device': 'Device 1',
                'version': '0.0.1', 'hash': 'c7d720641a8cba02cc2428379fd5970c'},
            {'tx_hash': '6a4c39085fde4f5d95be69c872781a29', 'device': 'Device 1',
                'version': '0.0.2', 'hash': '44acf3c48938bfc43603ea1228643749'}
        ]
        # create fake transaction
        dummy_transactions = []
        for index in range(100):
            device = 'Device ' + str(index)
            version = '0.0.' + str(index)
            dummy_transaction = {
                'tx_hash': uuid.uuid4().hex,
                'device': device,
                'version': version,
                'hash': uuid.uuid4().hex
            }
            dummy_transactions.append(dummy_transaction)

        for dummy_transaction in dummy_transactions:
            new_dummy_transaction = blockchain.new_transaction(
                dummy_transaction['tx_hash'], dummy_transaction['device'], dummy_transaction['version'], dummy_transaction['hash']
            )
            print(new_dummy_transaction)
            node_address = '127.0.0.1'
            last_block = blockchain.last_block
            proof = blockchain.proof_of_authentication(node_address)
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)
            print(block)

            # create transaction
        for transaction in transactions:
            new_transaction = blockchain.new_transaction(
                transaction['tx_hash'], transaction['device'], transaction['version'], transaction['hash'])
            print(new_transaction)
            # create node
            node_address = '127.0.0.1'
            last_block = blockchain.last_block
            proof = blockchain.proof_of_authentication(node_address)
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)
            print(block)
