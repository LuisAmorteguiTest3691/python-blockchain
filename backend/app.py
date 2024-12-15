import sys
import os

# Añade la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from blockchain.blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    """
    Ruta inicial que da la bienvenida a la API.
    """
    return "Welcome to the Supply Chain Blockchain API!"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    Ruta para crear una nueva transacción.
    """
    values = request.get_json()
    required = ['sender', 'recipient', 'product', 'quantity']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['product'],
        values['quantity'],
    )
    return jsonify({'message': f'Transaction will be added to Block {index}'}), 201

@app.route('/mine', methods=['GET'])
def mine():
    """
    Ruta para minar un nuevo bloque.
    """
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])
    block = blockchain.new_block(proof)
    return jsonify({'message': 'New block mined!', 'block': block}), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    """
    Ruta para devolver la cadena completa de bloques.
    """
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
