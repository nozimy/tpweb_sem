from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.shortcuts import reverse
from django.contrib.auth.models import User

from asker.managers import QuestionManager


class Profile(models.Model):
    user = models.OneToOneField(
        # settings.AUTH_USER_MODEL,
        User,
        on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='avatars/default-avatar.png')


class Tag(models.Model):
    text = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.pk} {self.id}"


class Vote(models.Model):
    VOTES = (
        (1, "Upvote"),
        (-1, "Downvote")
    )
    value = models.SmallIntegerField(default=VOTES[0], choices=VOTES)
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Question(models.Model):
    author = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(to='Tag', related_name='questions')
    votes = GenericRelation(Vote, related_query_name='questions')
    answer_count = models.DecimalField(default=0, max_digits=3, decimal_places=0)

    objects = QuestionManager()

    def __str__(self):
        return f"{self.pk} {self.id}"

    def get_absolute_url(self):
        return reverse("question", kwargs={"pk": self.pk})


class Answer(models.Model):
    author = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"

