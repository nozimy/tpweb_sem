from django.contrib import admin

# Register your models here.

from asker.models import Profile, Question, Tag, Answer, Vote

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Vote)

