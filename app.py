from flask import Flask, request, jsonify

from modules.chains.chat import chat
from modules.chains.search import search
from modules.chains.upload import upload

app = Flask(__name__)


@app.route("/chat", methods=['POST'])
def chat_view():
    try:
        data = request.get_json()
        query = data.get('query')
        model_name = data.get('model_name')
        history = data.get('history')
        with_memory = data.get('with_memory')

        if not query:
            return jsonify({'error': 'Query must not be empty.'}), 400

        response = chat(query, model_name, with_memory, history)

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/upload", methods=['POST'])
def upload_view():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'File must not be empty.'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'File must not be empty.'}), 400

        collection_name = request.form.get('collection_name')
        if not collection_name:
            return jsonify({'error': 'Collection_name must not be empty.'}), 400

        result = upload(file, collection_name)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route("/search", methods=['POST'])
def search_view():
    if request.method == "POST":
        try:
            data = request.get_json()
            query = data.get('query')
            model_name = data.get('model_name')
            history = data.get('history')
            with_memory = data.get('with_memory')
            with_database = data.get('with_database')
            collection_name = data.get('collection_name')

            if not query:
                return jsonify({'error': 'Query must not be empty.'}), 400

            if with_database:
                if collection_name is None:
                    return jsonify({'error': 'Collection Name must not be empty.'}), 400
                response = search(query, model_name, with_memory,
                                  history, collection_name)
            else:
                response = chat(query, model_name, with_memory, history)

            return jsonify(response), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run()
