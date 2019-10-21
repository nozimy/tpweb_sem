from django import forms
from asker.models import *
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(max_length=20)
    avatar = forms.ImageField()
    username = forms.CharField(max_length=20)
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

    def __init__(self, *args, **kwargs):
        self.username = args[0]['username']
        self.email = args[0]['email']
        super().__init__(*args, **kwargs)

    def save(self, *args, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            obj.user.username = self.username
            obj.user.email = self.email
            obj.user.save()


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        qs = User.objects.filter(email=self.cleaned_data['email'])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.count():
            raise forms.ValidationError('User with this email address is already exist')
        else:
            return self.cleaned_data['email']

    def save(self, *args, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            _profile = Profile(user=obj, nickname=obj.username)
            _profile.save()




class QuestionsForm(forms.ModelForm):
    title = forms.CharField(required=True, min_length=8)
    text = forms.CharField(required=True, min_length=8)
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, *args, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author

        if commit:
            obj.save()

        tags_for_question = str(args[0]).split(',')
        tags = []

        for tag in tags_for_question:
            tag = tag.strip()
            try:
                _tag = Tag.objects.get(text__iexact=tag)
            except Tag.DoesNotExist:
                _tag = Tag(text=tag)
                _tag.save()
            finally:
                tags.append(_tag.pk)

        obj.tags.add(*tags)
        return obj


class AnswerForm(forms.ModelForm):
    text = forms.CharField(required=True, min_length=8)

    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, *args, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author
        obj.question = args[0]
        if commit:
            obj.save()

        return obj
