from django.core.management.base import BaseCommand, CommandError
from pprint import pprint
from asker.models import *
from faker import Faker
from random import choice
import random

fake = Faker()

USERS_COUNT = 10
TAGS_COUNT = 10
QUESTIONS_COUNT = 100
ANSWERS_COUNT = 10000
VOTES_COUNT = 20000


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--questions', type=int)
        parser.add_argument('--users', type=int)

    def handle(self, *args, **options):
        # self.generate_users()
        users = User.objects.all()

        # self.generate_profiles(users=users)
        profiles = Profile.objects.all()

        # self.generate_tags()
        tags = Tag.objects.all()

        # self.generate_questions(profiles=profiles)
        questions = Question.objects.all()

        # self.add_tag_question_relations(questions=questions, tags=tags)

        # self.generate_answers(profiles=profiles, questions=questions)

        # self.answer_count(questions=questions)

        self.generate_votes(profiles=profiles)

        # users_count = options.get('users')
        # questions_count = options.get('questions')
        # if users_count is not None:
        #     self.generate_users(users_count)
        #
        # if questions_count is not None:
        #     self.generate_questions(questions_count)

    def generate_users(self):
        print(f"GENERATE USERS {USERS_COUNT}")
        users = []
        for i in range(USERS_COUNT):
            user = User(username=fake.user_name() + str(i), password='userPassword{}'.format(i), email=fake.email())
            users.append(user)
        User.objects.bulk_create(users, batch_size=10000)

    def generate_profiles(self, users):
        profiles = []
        for user in users:
            _profile = Profile.objects.filter(user__username__exact=user.username) # TODO:
            if not _profile:
                profile = Profile(user=user, nickname=user.username[:-2])
                profiles.append(profile)

        Profile.objects.bulk_create(profiles, batch_size=10000)

    def generate_tags(self):
        tags = []
        for i in range(TAGS_COUNT):
            tag = Tag(text=fake.word() + str(i))
            tags.append(tag)

        Tag.objects.bulk_create(tags, batch_size=10000)

    def generate_questions(self, profiles):
        # uids = list(Profile.objects.values_list('id', flat=True))
        questions = []
        for i in range(QUESTIONS_COUNT):
            question = Question(author=random.choice(profiles),
                                title=fake.sentence()[:random.randint(20, 100)],
                                text=fake.text())
            questions.append(question)

        Question.objects.bulk_create(questions, batch_size=10000)

    def add_tag_question_relations(self, questions, tags):
        for question in questions:
            tags_for_questions = []
            for _ in range(random.randint(1, 5)):
                tag = random.choice(tags)
                if tag.pk not in tags_for_questions:
                    tags_for_questions.append(tag.pk)
            question.tags.add(*tags_for_questions)

    def generate_answers(self, profiles, questions):
        answers = []
        for _ in range(ANSWERS_COUNT):
            answer = Answer(author=random.choice(profiles), question=random.choice(questions), text=fake.text(),
                            is_correct=False)
            answers.append(answer)

        Answer.objects.bulk_create(answers, batch_size=10000)

    def answer_count(self, questions):
        for question in questions:
            question.answer_count = question.answer_set.count()
            question.save()

    def generate_votes(self, profiles):
        Vote.objects.all().delete()

        questions = Question.objects.filter(pk__lte=10000)
        answers = Answer.objects.filter(pk__lte=10000)

        while Vote.objects.all().count() < VOTES_COUNT:
            profile = random.choice(profiles)
            votes = []

            _questions = questions.exclude(author=profile)
            for question in _questions:
                value = random.choice([1, -1])
                vote = Vote(value=value, profile=profile, content_object=question)
                votes.append(vote)

            _answers = answers.exclude(author=profile)
            for answer in _answers:
                value = random.choice([1, -1])
                vote = Vote(value=value, profile=profile, content_object=answer)
                votes.append(vote)

            Vote.objects.bulk_create(votes)
            for vote in votes:
                vote.content_object.rating += vote.value
                vote.content_object.save(update_fields=['rating'])
