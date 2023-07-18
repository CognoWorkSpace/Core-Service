# -*- coding: utf-8 -*-
# File : app.py
# Author : Dijkstra Liu
# Email : l.tingjun@wustl.edu
#
# 　　　    /＞ —— フ
# 　　　　　| `_　 _ l
# 　 　　　ノ  ミ＿xノ
# 　　 　 /　　　 　|
# 　　　 /　 ヽ　　ﾉ
# 　 　 │　　|　|　\
# 　／￣|　　 |　|　|
#  | (￣ヽ＿_ヽ_)__)
# 　＼_つ
#
# Description:
# The file to start Flask server

from flask import Flask, request, jsonify
from modules.chains.chat import chat
from modules.chains.search import search
from modules.chains.upload import upload
from flasgger import Swagger, swag_from
from init import init

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Core Service',
    'uiversion': 2
}
Swagger(app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "Core Service API",
                "version": "1.0",
            },
            "servers": {
                "url": "https://cogno/v1",
            },
            "consumes": [
                "application/json",
            ],
            "produces": [
                "application/json",
            ],
        },
)


@app.route("/chat", methods=['POST', 'GET'])
@swag_from('doc/chat_post.yml', methods=['POST'])
@swag_from('doc/chat_get.yml', methods=['GET'])
def chat_view():
    # TODO: GET拿到之前的聊天记录
    # TODO: 更改错误记号，对应代码意义
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
    # TODO: Refine by Xinkai
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
    init()
    app.run()
