from django.shortcuts import render, HttpResponse
from .chains.chat import chat
from .chains.search import search
from .chains.upload import upload
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get('query')
            model_name = data.get('model_name')
            history = data.get('history')
            with_memory = data.get('with_memory')

            if not query:
                return HttpResponseBadRequest('Query must not be empty.')

            response = chat(query, model_name, with_memory, history)

            return JsonResponse(response, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def upload_view(request):
    if request.method == "POST":
        print("yesy")
        print(request.FILES.get('file'))
        try:
            # The frond-end better to use formData to post file
            upload_file = request.FILES.get('file')
            print(type(upload_file))
            collection_name = request.POST.get('collection_name')

            if not upload_file or not collection_name:
                return HttpResponseBadRequest('Both file and collection name are required.')

            result = upload(upload_file, collection_name)
            if result['result'] == 'success':
                return JsonResponse(result, safe=False, status=200)
            else:
                return JsonResponse({'error': result['message']}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def query_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get('query')
            model_name = data.get('model_name')
            history = data.get('history')
            with_memory = data.get('with_memory')
            with_database = data.get('with_database')
            collection_name = data.get('collection_name')

            if not query:
                return HttpResponseBadRequest('Query must not be empty.')

            if with_database:
                response = search(query, model_name, with_memory,
                                  history, collection_name)
            else:
                response = chat(query, model_name, with_memory, history)

            return JsonResponse(response, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
