from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from core.models import Poll, Answer
from core.serializers import PollSerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    permission_classes = [IsAdminUser,]
    permission_classes_by_action = {'retrieve': [AllowAny],
                                    'list': [AllowAny]}

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Poll.objects.all()
        return Poll.objects.filter(is_active=True, end_date__gte=datetime.now())


    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        poll = get_object_or_404(self.get_queryset(), pk=pk)
        result = PollSerializer(poll).data
        result['questions'] = []
        for question in poll.questions.all():
            questions = QuestionSerializer(question).data
            if question.type == 'MANY' or question.type == 'ONE':
                questions['choices'] = ChoiceSerializer(question.choices.all(), many=True).data
            result['questions'].append(questions)
        return Response(result)

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


@api_view(['GET',])
def get_user_answers(request, pk, user_id):
    poll = Poll.objects.get(id=pk)
    result = PollSerializer(poll).data
    result['questions'] = []
    get_questions_and_answers(poll, result, user_id)
    return Response(result)


def get_questions_and_answers(poll, result, user_id):
    for _question in poll.questions.all():
        question = QuestionSerializer(_question).data
        answers = Answer.objects.filter(user=user_id, question=_question.id, poll=poll)
        for answer in answers:
            answer_serialized = AnswerSerializer(answer).data
            if _question.type == 'TEXT':
                question['answer'] = answer_serialized['value']
            elif _question.type == 'ONE':
                question['answer'] = answer_serialized['one']
            elif _question.type == 'MANY':
                question['answer'] = answer_serialized['many']
        result['questions'].append(question)


@api_view(['GET',])
def finished_polls(request, user_id):
    polls = Poll.objects.all()
    finished = []
    for poll in polls:
        answers = Answer.objects.filter(user=user_id, poll=poll)
        if len(poll.questions.all()) == len(answers) and len(answers) > 0:
            result = PollSerializer(poll).data
            result['questions'] = []
            get_questions_and_answers(poll, result, user_id)
            finished.append(result)
    return Response(finished)

#
@swagger_auto_schema(method='POST',operation_description="Answers",
                     request_body=AnswerSerializer(many=True))
@api_view(['POST',])
def take_a_survey(request):
    answers = []

    for _answer in request.data:
        serializer = AnswerSerializer(data=_answer)
        if serializer.is_valid():
            serializer.save()
            answers.append(serializer.data)
        else:
            answers.append({'error': f'question{_answer["question"]}'})

    return Response(answers)

