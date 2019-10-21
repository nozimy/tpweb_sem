from django.shortcuts import render, get_object_or_404, redirect, reverse
# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from faker import Faker
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from asker.models import *

from django.contrib.auth.decorators import login_required
from asker.forms import *
from django.contrib.auth import authenticate, logout as d_logout, login as d_login
from urllib import parse
from django.db.models import Count


fake = Faker()


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 5)
    page = request.GET.get('page')
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    return objects_page


def index(request, tag=None):
    tab = request.GET.get('tab') # TODO: study .get() and eliminate 1 level if if else
    if tag is not None:
        qs = Question.objects.by_tag(tag, tab)
    else:
        if tab is not None:
            if tab == 'new':
                qs = Question.objects.new()
            elif tab == 'hot':
                qs = Question.objects.hot()
            else:
                qs = Question.objects.new()
        else:
            qs = Question.objects.new()

    qs = qs.annotate(answer_count1=Count('answer'))
    page = paginate(qs, request)
    return render(request, 'question_list.html', {'questions': qs, 'page': page })


def response_ajax(status, message):
    return JsonResponse({'status': status, 'message': message})


def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            try:
                user = User.objects.get(email__iexact=cdata['email'])
            except User.DoesNotExist:
                return response_ajax(False, {'email': 'User by this email not found!!'})
            else:
                user = authenticate(username=user.username, password=cdata['password'])
                if user is not None:
                    d_login(request, user)
                    next = request.POST.get('next', '/')
                    return response_ajax(True, next)
                else:
                    return response_ajax(False, {'login': 'Login or password is wrong!!'})
        else:
            return response_ajax(False, form.errors)

    next = parse.urlparse(request.META.get('HTTP_REFERER')).path
    return render(request, 'login.html', {'next': next})


@login_required
def logout(request):
    d_logout(request)
    return redirect(reverse('index'))


@login_required(login_url='/login/')
def ask(request):
    if request.POST:
        form = QuestionsForm(request.user.profile, request.POST)
        if form.is_valid():
            question = form.save(request.POST.get('tags'))
            return response_ajax(True, '/question/' + str(question.pk))
        else:
            return response_ajax(False, form.errors)

    return render(request, 'ask.html')


def signup(request):
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            d_login(request, user)
            return response_ajax(True, '/')
        else:
            return response_ajax(False, form.errors)

    return render(request, 'signup.html')


def question(request, qid):
    one_question = get_object_or_404(Question, pk=qid)
    answers = Answer.objects.filter(question_id=qid)
    has_correct_answer = answers.filter(is_correct=True).count() >= 1
    page = paginate(answers, request)

    user_id = 0
    if request.user:
        user_id = request.user.pk

    return render(request, 'question.html', {
        'question': one_question,
        'has_correct_answer': has_correct_answer,
        'answers': answers,
        'page': page,
        'user_id': user_id,
    })


@login_required(login_url='/login/')
def profile(request):
    profile = Profile.objects.get(user_id__exact=request.user.pk)

    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html', {'user': profile.user})
        else:
            print(form.errors)
            return render(request, 'profile.html', {
                        'user': profile.user,
                        'errors': form.errors
                        })
    return render(request, 'profile.html')


@login_required(login_url='/login/')
def answer(request, question_id):
    if request.POST:
        form = AnswerForm(request.user.profile, request.POST)
        if form.is_valid():
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return redirect(reverse('index'))
            else:
                form.save(question)
                return response_ajax(True, 'Answer has been added and published')
        else:
            return response_ajax(False, form.errors)


@login_required(login_url='/login/')
def vote(request):        #todo: накрутка голосов не должно быть (юзер не может больше одного раза залайкать)
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    try:
        qid = int(request.POST.get('qid'))
    except Exception:
        return JsonResponse(dict(error='bad question id'))
    vote = request.POST.get('vote')
    question = Question.objects.get(pk=qid)
    if vote == 'inc':
        question.rating += 1
        question.save()
    elif vote == 'dec':
        question.rating -= 1
        question.save()
    return JsonResponse(dict(ok=1, rating=question.rating))