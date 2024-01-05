from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Note
from .serializers import NoteSerializer

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user is None:
        return Response({'error': 'Invalid username/password.'}, status=status.HTTP_404_NOT_FOUND)
    if not user.check_password(password):
        return Response({'error': 'Invalid username/password.'}, status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def note_list(request):
    if request.method == 'GET':
        queryset = Note.objects.filter(owner=request.user)
        
        query = request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(content__icontains=query)
        
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def note_detail(request, pk):
    try:
        note = Note.objects.get(pk=pk, owner=request.user)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request, pk):
    try:
        note = Note.objects.get(pk=pk, owner=request.user)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)

    user_to_share_with_username = request.data.get('username')
    if not user_to_share_with_username:
        return Response({'error': 'Username is required to share a note.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_to_share_with = User.objects.get(username=user_to_share_with_username)
    except User.DoesNotExist:
        return Response({'error': 'User to share with not found.'}, status=status.HTTP_404_NOT_FOUND)

    if user_to_share_with == request.user:
        return Response({'error': "You can't share a note with yourself."}, status=status.HTTP_400_BAD_REQUEST)

    note.shared_with.add(user_to_share_with)
    note.save()

    return Response({'message': 'Note shared successfully.'}, status=status.HTTP_200_OK)