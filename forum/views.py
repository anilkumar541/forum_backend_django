from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from .models import Question, Answer, Vote, Tag
from .serializers import QuestionSerializer, AnswerSerializer, UserSerializer, TagSerailzer
from rest_framework_simplejwt.tokens import RefreshToken
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from .pagination import ForumPagination


    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# signup 
@api_view(["POST"])
def signup(request):
    serializer= UserSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "User signup successful"}, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


# Login
@api_view(["POST"])
def login(request):
    username= request.data.get("username")
    password= request.data.get("password")
    user= User.objects.filter(username = username).first()
    if user and user.check_password(password):
        return Response({"token": get_tokens_for_user(user)}, status= status.HTTP_200_OK)
    return Response({"Message": "User does not exist"}, status= status.HTTP_400_BAD_REQUEST)    



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tag_list(request):
    if request.method == 'GET':
        tags = Tag.objects.order_by("-created_at")
        serializer = TagSerailzer(tags, many=True)
        return Response(serializer.data)

        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tag(request):
    if request.method == 'POST':
        serializer = TagSerailzer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors)


@api_view(['GET'])
def question_list(request):
    queryset= Question.objects.all()

    search_filter= SearchFilter()
    search_fields= ["tags"]

    queryset= search_filter.filter_queryset(request, queryset, view=None)
    serializer = QuestionSerializer(queryset, many=True)
    return Response(serializer.data)    

class QuestionListView(ListAPIView):
    queryset= Question.objects.all().order_by("-created_at")
    serializer_class= QuestionSerializer
    pagination_class= ForumPagination
    filter_backends= [SearchFilter]
    search_fields= ["tags__tag"]
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        # print(request.data)
        if serializer.is_valid():
            question= serializer.save()
            channel_layer= get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "questions_feed",
                {"type": "send_new_question", "message": serializer.data}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def question_detail(request, pk):
    try:
        question= Question.objects.get(id= pk)
    except Question.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)    

    if request.method == "GET":
        serializer= QuestionSerializer(question)
        return Response(serializer.data)    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_answer(request, question_id):
    try:
        question= Question.objects.get(id= question_id)
    except Question.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)    

    serializer= AnswerSerializer(data= request.data)
    if serializer.is_valid():
        
        serializer.save(author= request.user, question= question)
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)        



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vote_answer(request, answer_id):
    try:
        answer= Answer.objects.get(id= answer_id)
    except Answer.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)    

    is_upvote_value= request.data.get("is_upvote")
    if is_upvote_value is None:
        return Response({"error": "is_upvote field is requred"}, status= status.HTTP_400_BAD_REQUEST)

    previous_vote= None
    vote, created= Vote.objects.get_or_create(user= User.objects.get(id= request.user.id), answer= answer, defaults={'is_upvote': is_upvote_value})
    if not created:
        previous_vote= "upvote" if vote.is_upvote else "downvote"

    vote.is_upvote= is_upvote_value
    vote.save()

    upvotes= Vote.objects.filter(answer= answer, is_upvote= True).count()
    downvotes= Vote.objects.filter(answer= answer, is_upvote= False).count()

    return Response({
        "message": "success",
        "upvotes": upvotes,
        "downvotes": downvotes,
        "previous_vote": previous_vote,
    })