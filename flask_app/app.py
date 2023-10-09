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
# The file to initialize and start Flask server

from flask import Flask, request, jsonify
from modules.actions.chat import ChatBase
from modules.roles.seller import Seller
from modules.roles.sommelier import Sommelier
from modules.roles.Informer import Informer
from modules.actions.search import search
from modules.actions.upload import upload
from flasgger import Swagger, swag_from
from config import get_config
from dotenv import load_dotenv
from utils.logging import LOGGER


def create_app(config_key='dev'):

    app = Flask(__name__)
    config = get_config(key=config_key)
    app.config.update(config)
    load_dotenv()
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
        if request.method == 'POST':
            try:
                data = request.get_json()
                query = data.get('query')
                model_name = data.get('model_name')
                history = data.get('history')
                with_memory = data.get('with_memory')

                if not query:
                    LOGGER.error('Query must not be empty.')
                    return jsonify({'error': 'Query must not be empty.'}), 400

                LOGGER.info(
                    'Received chat request with query: {}, model_name: {}, with_memory: {}, history length: {}.'
                    .format(query, model_name, with_memory, 0 if history is None else len(history)))
                response = ChatBase().chat(query)

                LOGGER.info('Generated chat response: {}.'.format(response))

                return jsonify(response), 200
            except ValueError as e:
                LOGGER.error('Post content error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify(({'error': str(e)})), 400
            except Exception as e:
                LOGGER.error('An error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

        if request.method == 'GET':
            try:
                history = ChatBase().get_history()
                LOGGER.info('Generated chat history: {}.'.format(history))
                return jsonify({'history': history}), 200
            except Exception as e:
                LOGGER.error('An error occurred in chat_view_GET: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

    @app.route("/wine_sales_given_history", methods=['POST', 'GET'])
    def wine_sales_given_history_view():
        if request.method == 'POST':
            try:
                data = request.get_json()
                query = data.get('query')
                model_name = data.get('model_name')
                history = data.get('history')
                username = data.get('username')
                with_memory = data.get('with_memory')

                if not query:
                    LOGGER.error('Query must not be empty.')
                    return jsonify({'error': 'Query must not be empty.'}), 400

                LOGGER.info(
                    'Received chat request with query: {}, model_name: {}, with_memory: {}, history : {}., username :{}'
                    .format(query, model_name, with_memory, history, username))
                response = Seller(query, model_name, with_memory, chat_history_dict=history,
                                  username=username).chat_reply_given_history()

                LOGGER.info('Generated chat response: {}.'.format(response))

                return jsonify(response), 200
            except ValueError as e:
                LOGGER.error('Post content error occurred in wine_sales_given_history_view function: {}.'.format(e))
                return jsonify(({'error': str(e)})), 400
            except Exception as e:
                LOGGER.error('An error occurred in wine_sales_given_history_view function: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

        if request.method == 'GET':
            try:
                history = Seller().get_history()
                LOGGER.info('Generated wine sales chat history: {}.'.format(history))
                return jsonify({'history': history}), 200
            except Exception as e:
                LOGGER.error('An error occurred in wine_sales_given_history_view: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

    @app.route("/wine_sales", methods=['POST', 'GET'])
    def wine_sales_view():
        if request.method == 'POST':
            try:
                data = request.get_json()
                query = data.get('query')
                model_name = data.get('model_name')
                history = data.get('history')
                username = data.get('username')
                with_memory = data.get('with_memory')

                if not query:
                    LOGGER.error('Query must not be empty.')
                    return jsonify({'error': 'Query must not be empty.'}), 400

                LOGGER.info(
                    'Received chat request with query: {}, model_name: {}, with_memory: {}, history length: {}.'
                    .format(query, model_name, with_memory, 0 if history is None else len(history)))
                response = Seller(query, model_name, with_memory, chat_history_dict=history, username=username).chat_reply()

                LOGGER.info('Generated chat response: {}.'.format(response))

                return jsonify(response), 200
            except ValueError as e:
                LOGGER.error('Post content error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify(({'error': str(e)})), 400
            except Exception as e:
                LOGGER.error('An error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

        if request.method == 'GET':
            try:
                history = Seller().get_history()
                LOGGER.info('Generated wine sales chat history: {}.'.format(history))
                return jsonify({'history': history}), 200
            except Exception as e:
                LOGGER.error('An error occurred in wine_sales_view_GET: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

    @app.route("/wine_somme_given_history", methods=['POST', 'GET'])
    def wine_somme_given_history_view():
        if request.method == 'POST':
            try:
                data = request.get_json()
                query = data.get('query')
                model_name = data.get('model_name')
                history = data.get('history')
                with_memory = data.get('with_memory')

                if not query:
                    LOGGER.error('Query must not be empty.')
                    return jsonify({'error': 'Query must not be empty.'}), 400

                LOGGER.info(
                    'Received chat request with query: {}, model_name: {}, with_memory: {}, history length: {}.'
                    .format(query, model_name, with_memory, 0 if history is None else len(history)))
                response = Sommelier(query, model_name, with_memory, chat_history_dict=history).chat_reply_given_history()

                LOGGER.info('Generated chat response: {}.'.format(response))

                return jsonify(response), 200
            except ValueError as e:
                LOGGER.error('Post content error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify(({'error': str(e)})), 400
            except Exception as e:
                LOGGER.error('An error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify({'error': str(e)}), 500
    @app.route("/wine_somme", methods=['POST', 'GET'])
    def wine_somme_view():
        if request.method == 'POST':
            try:
                data = request.get_json()
                query = data.get('query')
                model_name = data.get('model_name')
                history = data.get('history')
                with_memory = data.get('with_memory')

                if not query:
                    LOGGER.error('Query must not be empty.')
                    return jsonify({'error': 'Query must not be empty.'}), 400

                LOGGER.info(
                    'Received chat request with query: {}, model_name: {}, with_memory: {}, history length: {}.'
                    .format(query, model_name, with_memory, 0 if history is None else len(history)))
                response = Sommelier(query, model_name, with_memory, history).chat_reply()

                LOGGER.info('Generated chat response: {}.'.format(response))

                return jsonify(response), 200
            except ValueError as e:
                LOGGER.error('Post content error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify(({'error': str(e)})), 400
            except Exception as e:
                LOGGER.error('An error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

        if request.method == 'GET':
            try:
                history = Sommelier().get_history()
                LOGGER.info('Generated wine sales chat history: {}.'.format(history))
                return jsonify({'history': history}), 200
            except Exception as e:
                LOGGER.error('An error occurred in wine_sales_view_GET: {}.'.format(e))
                return jsonify({'error': str(e)}), 500

    @app.route("/informer_given_history", methods=['POST', 'GET'])
    def informer_given_history_view():
        if request.method == 'POST':
            try:
                data = request.get_json()
                query = data.get('query')
                model_name = data.get('model_name')
                history = data.get('history')
                with_memory = data.get('with_memory')

                if not query:
                    LOGGER.error('Query must not be empty.')
                    return jsonify({'error': 'Query must not be empty.'}), 400

                LOGGER.info(
                    'Received chat request with query: {}, model_name: {}, with_memory: {}, history length: {}.'
                    .format(query, model_name, with_memory, 0 if history is None else len(history)))
                response = Informer(query, model_name, with_memory, history).chat_reply_given_history()

                LOGGER.info('Generated chat response: {}.'.format(response))

                return jsonify(response), 200
            except ValueError as e:
                LOGGER.error('Post content error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify(({'error': str(e)})), 400
            except Exception as e:
                LOGGER.error('An error occurred in chat_view_POST function: {}.'.format(e))
                return jsonify({'error': str(e)}), 500


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
                    response = ChatBase().chat(query, model_name, with_memory, history)

                return jsonify(response), 200

            except Exception as e:
                return jsonify({'error': str(e)}), 400

    return app
