
from django.db import models


class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-created_on')

    def hot(self):
        return self.all().order_by('-rating')

    def by_tag(self, tag, tab):
        filter = '-rating'
        if tab == 'new':
            filter = '-created_on'
        elif tab == 'hot':
            filter = '-rating'
        return self.filter(tags__text__iexact=tag).order_by(filter)

    def without_answer(self):
        return self.filter(answer_count=0)
