import hashlib
import json
import os
import datetime
import random

# Set the path of the file to delete
filename = 'blockchain.json'

# Check if the file exists before deleting it
if os.path.isfile(filename):
    os.remove(filename)
    print(f'{filename} has been deleted.')
else:
    print(f'{filename} does not exist.')


class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
        
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.current_transactions = []
        self.file_path = 'blockchain.json'
        self.load_from_file()
        
    def create_genesis_block(self):
        return Block(0,'2022-01-01 00:00:00',[], '0')
    
    def add_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'label':"",
        })
        
    def mine_block(self):
        last_block = self.chain[-1]
        index = last_block.index + 1
        transactions = self.current_transactions
        timestamp = str(datetime.datetime.now())
        previous_hash = last_block.hash
        block = Block(index, timestamp, transactions, previous_hash)
        self.chain.append(block)
        self.current_transactions = []
        self.save_to_file()
        
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def save_to_file(self):
        with open(self.file_path, 'w') as f:
            data = {
                'chain': [block.__dict__ for block in self.chain],
                'current_transactions': self.current_transactions,
            }
            json.dump(data, f)
            
    def load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.chain = [Block(**block_data) for block_data in data['chain']]
                self.current_transactions = data['current_transactions']
                
# Example usage
blockchain = Blockchain()
users = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve']
num_users = len(users)

for i in range(100):
    sender = users[random.randint(0, num_users - 1)]
    recipient = users[random.randint(0, num_users - 1)]
    while recipient == sender:
        recipient = users[random.randint(0, num_users - 1)]
    amount = random.randint(1, 200)
    blockchain.add_transaction(sender, recipient, amount)
    if i%10==0:
      blockchain.mine_block()
print(blockchain.chain)

def analyze_transactions(input_file, output_file):
    # Load the blockchain from the input file
    with open(input_file, 'r') as f:
        blockchain = json.load(f)

    # Analyze each transaction and add a label
    for block in blockchain['chain']:
      for tx in block['transactions']:
        if int(tx['amount']) > 100:
          tx['label'] = 'abnormal'
        else:
          tx['label'] = 'normal'

    # Write the updated blockchain to the output file
    with open(output_file, 'w') as f:
        json.dump(blockchain, f, indent=4)

analyze_transactions("blockchain.json","labelled.json")
