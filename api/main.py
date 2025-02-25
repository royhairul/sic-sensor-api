from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

from dotenv import load_dotenv

app = Flask(__name__)

# Load variable from dotenv
load_dotenv()

# Koneksi ke MongoDB
uri = "mongodb+srv://tstoyr:adminoyr@cluster0.u4bnb.mongodb.net/?retryWrites=true&w=majority&appName=cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['db_samsungbatch']
my_collection = db['collection1']

# Cek koneksi ke MongoDB
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(f"MongoDB connection error: {e}")

def serialize_doc(doc):
    """Konversi ObjectId ke string dalam dokumen MongoDB"""
    doc["_id"] = str(doc["_id"])  # Ubah ObjectId ke string
    return doc

# Endpoint utama
@app.route('/')
def entry_point():
    result = my_collection.find()
    serialized_result = [serialize_doc(doc) for doc in result]

    return jsonify({'data': serialized_result}), 200

# Endpoint untuk Create
@app.route('/create', methods=['POST'])
def create():
    try:
        req_data = request.get_json()

        # Simpan ke MongoDB
        result = my_collection.insert_one(req_data)

        # Ambil data yang telah disimpan
        saved_data = my_collection.find({'_id': result.inserted_id})
        serialized_result = [serialize_doc(doc) for doc in saved_data]
        
        return jsonify({
            'message': 'Data berhasil dibuat',
            'data': serialized_result,
            'inserted_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Endpoint untuk Update
@app.route('/update/<string:item_id>', methods=['PUT'])
def update(item_id):
    req_data = request.get_json()
    if not req_data:
        return jsonify({'error': 'Data tidak boleh kosong'}), 400

    result = my_collection.update_one({'id': item_id}, {'$set': req_data})
    
    if result.matched_count == 0:
        return jsonify({'error': 'Data tidak ditemukan'}), 404

    return jsonify({'message': 'Data berhasil diperbarui'}), 200

# Endpoint untuk Delete
@app.route('/delete/<string:item_id>', methods=['DELETE'])
def delete(item_id):
    result = my_collection.delete_one({'id': item_id})
    
    if result.deleted_count == 0:
        return jsonify({'error': 'Data tidak ditemukan'}), 404

    return jsonify({'message': 'Data berhasil dihapus'}), 200

if __name__ == '__main__':
    app.run(debug=True)
