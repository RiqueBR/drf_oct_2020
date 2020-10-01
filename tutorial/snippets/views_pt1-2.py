from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt # we will handle cross-site request forgery attempts
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# import thngs from drf
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# decorate the views as REST Framework API views

# @csrf_exempt # useful only during development
@api_view(['GET', 'POST']) # which methods does this view support
def snippet_list(request, format=None): # this is the http request object being passed in
    '''
    list all code snippets or create a new one
    '''
    if request.method == 'GET':
        # list the snippets
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data) # use the drf Response object

    elif request.method == 'POST':
        # create a new snippet
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status= 201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None): # pk is the key we are interested in
    '''
    retrieve, update or delete a code snippet
    '''
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        # return HttpResponse(status=404)
        return Response(status=status.HTTP_404_NOT_FOUND)

    # determine what action to carry out
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status= 201)
            return Response(serializer.data)
        # return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        # return HttpResponse(status=204)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

