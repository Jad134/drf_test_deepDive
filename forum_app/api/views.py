from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAdminUser
from forum_app.models import Like, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionThrottle, QuestionGetThrottle, QuestionPostThrottle

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_throttles(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [QuestionGetThrottle()]
        
        if self.action == 'create':
            return [QuestionPostThrottle()]

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAdminUser]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
