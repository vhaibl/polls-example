from rest_framework import serializers

from .models import Poll, Answer, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields =['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields =['id', 'poll', 'text', 'type', 'choices']
        extra_kwargs = {'poll': {'required': False}, }


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'created_at', 'end_date', 'is_active', 'questions']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        poll = Poll()
        poll.name = validated_data['name']
        poll.description = validated_data['description']
        poll.end_date = validated_data['end_date']
        poll.save()
        for q in validated_data.get('questions'):
            q = QuestionSerializer(q).data
            question = Question.objects.create(poll=poll)
            question.text = q['text']
            question.type = q['type']
            question.save()
            if q['type'] == 'ONE' or q['type'] == 'MANY':
                if 'choices' in q:
                    for c in q['choices']:
                        c = ChoiceSerializer(c).data
                        Choice.objects.create(question=question, text=c['text'])
        return poll

    def update(self, instance, validated_data):
        _questions = validated_data.pop('questions', instance.questions.all())
        if _questions:
            Question.objects.filter(poll=instance).delete()
            for question in _questions:
                instance.questions.add(Question.objects.create(**question))
        return super(PollSerializer, self).update(instance, validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields ='__all__'
    def create(self, validated_data):
        answer, created = Answer.objects.get_or_create(user=validated_data['user'], poll=validated_data['poll'],
                                                       question=validated_data['question'])
        answer.save()
        if answer.question.type == 'TEXT':
            if 'value' in validated_data:
                answer.value = validated_data['value']
        elif answer.question.type == 'ONE':
            if 'one' in validated_data:
                answer.one = validated_data['one']
        elif answer.question.type == 'MANY':
            if 'many' in validated_data:
                if not created:
                    answer.many.clear()
                for choice in validated_data['many']:
                    answer.many.add(choice)

        answer.save()
        return answer






