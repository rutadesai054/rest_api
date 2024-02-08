from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book

@api_view(['GET','POST'])
def taskListAPI(request):
    if request.method == 'GET':
        querySet = Book.objects.all()
        serializer = BookSerializer(querySet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def taskDetailAPI(request, task_id):

    try:
        querySet = Book.objects.get(id=task_id)
    except Book.DoesNotExist:
        return Response({'message':"Task Doesn't Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(querySet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = BookSerializer(querySet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    if request.method == 'PATCH':
        serializer = BookSerializer(querySet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                'data':serializer.data,
                'message':f"{querySet.title} - Updated successfully."
            }
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    if request.method == 'DELETE':
        querySet.delete()
        return Response({'message':f"'{querySet.title}' - deleted successfully"}, status=status.HTTP_204_NO_CONTENT)