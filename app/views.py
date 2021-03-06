from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app import models
from django.contrib import auth
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, Vote, AnswerVote
from app.forms import LoginForm, RegisterForm, SettingsForm, AskForm, AnswerForm

from django.http import JsonResponse
from django.db.models import F
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.db.models import Count


def paginate(object_list, requset, per_page=3):
    paginator = Paginator(object_list, per_page)
    page = requset.GET.get('page')
    try:
        return paginator.get_page(page)
    except PageNotAnInteger:
        return paginator.get_page(1)


def index(request):
    questions = Question.objects.new().annotate(num_answers=Count('answer'))
    pagination_questions = paginate(questions, request, 5)
    return render(request, 'index.html', {'questions': pagination_questions})


@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user.profile
            question.save()
            tags_name = form.cleaned_data.get('tags')
            tag_name_array = [x.strip() for x in tags_name.split(',')]
            for tag_name in tag_name_array:
                tag_names = Tag.objects.filter(name=tag_name)
                if not tag_names:
                    tags = Tag.objects.create(name=tag_name)
                    tags.save()
                tag = Tag.objects.get(name=tag_name)
                question.tags.add(tag.id)
            return redirect(reverse('one_question', kwargs={'pk': question.pk}))

    return render(request, 'ask.html', {'form': form})


def one_question(request, pk):
    question = Question.objects.find_by_pk(pk)
    answers = Answer.objects.find_by_question(question)
    pagination_answers = paginate(answers, request, 5)
    question.num_answers = len(answers)

    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                answer = form.save(commit=False)
                answer.user = request.user.profile
                answer.question_id = pk
                answer.save()
                return redirect(reverse('one_question', kwargs={'pk': pk}))
            else:
                return redirect(reverse('login'))
    return render(request, 'question.html', {"question": question, "answers": pagination_answers, 'form': form})


def tag_questions(request, pk):
    tag_questions_array = Question.objects.find_by_tag(pk).annotate(num_answers=Count('answer'))
    pagination_questions = paginate(tag_questions_array, request, 5)
    return render(request, 'tag-questions.html', {"questions": pagination_questions, "tag": pk})


@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial={'login': request.user.username, 'email': request.user.email})
    else:
        form = SettingsForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            if form.cleaned_data.get('login'):
                request.user.username = form.cleaned_data.get('login')
            if form.cleaned_data.get('email'):
                request.user.email = form.cleaned_data.get('email')
            avatar = form.cleaned_data.get('avatar')
            if avatar:
                request.user.profile.avatar = avatar
            request.user.save()
            request.user.profile.save()
            return redirect(reverse('settings'))

    return render(request, 'settings.html', {'form': form})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        next_page = request.GET.get('next', '')
        request.session['next_page'] = next_page
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                next_page = request.session.pop('next_page')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(reverse('index'))
            else:
                form.add_error(None, 'Authentication error')

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")


def registration(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile = Profile.objects.create(user=user, nickname=user.username)
            profile.save()
            return redirect(reverse('index'))

    return render(request, 'signup.html', {'form': form})


def hot_questions(request):
    questions = Question.objects.hot()
    questions = questions.annotate(num_answers=Count('answer'))
    pagination_questions = paginate(questions, request, 5)

    return render(request, 'hot-questions.html', {'questions': pagination_questions})


# ----------------------------------------

@login_required
@require_POST
def vote(request):
    data = request.POST
    qid = data['qid']
    action = data['action']
    type_ = data['type']

    inc = models.Vote.ACTIONS[action]
    user = Profile.objects.get(pk=request.user.profile.id)

    if type_ == 'question':
        q = models.Question.objects.get(pk=qid)
        temp = Vote.objects.filter(user=user, question=q)
        temp_flag = 0
        if temp:
            if temp.get().value == inc:
                print('such vote already exist')
                return JsonResponse({"error code": 1, "new rating": q.rating, "type": type_})
            temp.get().delete()
            temp_flag = 1

        q.rating = F('rating') + inc
        q.save()
        q.refresh_from_db()

        if temp_flag:
            print('old vote was removed')
            return JsonResponse({"error code": 0, "new rating": q.rating, "type": type_})

        Vote.objects.create(user=user, question=q, value=inc)

    else:
        q = models.Answer.objects.get(pk=qid)
        temp = AnswerVote.objects.filter(user=user, answer=q)
        temp_flag = 0
        if temp:
            if temp.get().value == inc:
                print('such vote already exist')
                return JsonResponse({"error code": 1, "new rating": q.rating, "type": type_})
            temp.get().delete()
            temp_flag = 1

        q.rating = F('rating') + inc
        q.save()
        q.refresh_from_db()

        if temp_flag:
            print('old vote was removed')
            return JsonResponse({"error code": 0, "new rating": q.rating, "type": type_})

        AnswerVote.objects.create(user=user, answer=q, value=inc)

    return JsonResponse({"error code": 0, "new rating": q.rating, "type": type_})


# ----------------------------------

@login_required
@require_POST
def check(request):
    data = request.POST
    action = data['action']
    qid = data['qid']
    aid = data['aid']

    user = Profile.objects.get(pk=request.user.profile.id)

    question = models.Question.objects.get(pk=qid)
    answer = models.Answer.objects.get(pk=aid)

    if question.user != user:
        print('not allowed - u r not author of question')
        return JsonResponse(data)

    if action == 'checked':
        answer.is_correct = True
        print('answer is correct')
    else:
        answer.is_correct = False
        print('answer is not correct')
    answer.save()
    answer.refresh_from_db()

    print(data)

    return JsonResponse(data)
