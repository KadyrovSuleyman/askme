from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger

questions = [
    {
        'id': idx,
        'title': f'Title number {idx}',
        'text': f'Some text for questions #{idx}',
        'author': f'Author name # {idx}',
        'date': f'{idx}.05.2021',
        'tags': [
            {
                'tag': f'tag{j}'
            } for j in range(3)
        ]
    } for idx in range(10)
]

tags = [
    {
        'name': f'tag{idx}',
    } for idx in range(10)
]

profiles = [
    {
        'id': idx,
        'login': f'login #{idx}',
        'email': f'email #{idx}',
        'nickname': f'nickname #{idx}',
    } for idx in range(10)
]

authors = [
    {
        'name': f'Author name #{idx}',
    } for idx in range(5)
]

def paginate(object_list, requset, per_page = 3):
    paginator = Paginator(object_list, per_page)
    page = requset.GET.get('page')
    try:
        return paginator.get_page(page)
    except PageNotAnInteger:
        return paginator.get_page(1)

def questions_listning(request):
    pagination = paginate(questions, request, 3)
    return render(request, '1-questions listning.html', {'questions': questions,
                                                         'tags': tags,
                                                         'profiles': profiles,
                                                         'authors': authors,
                                                         'pagination': pagination})




def index(request):
    pagination = paginate(questions, request, 3)
    return render(request, 'index.html', {'questions': questions,
                                          'tags': tags,
                                          'profiles': profiles,
                                          'authors': authors,
                                          'pagination': pagination})

def new_question(request):
    return render(request, '2-add new question.html', {'tags': tags,
                                                       'profiles': profiles,
                                                       'authors': authors})

def view_question(request, pk):
    question = questions[pk]
    return render(request, '3-question page.html', {'question': question,
                                                    'tags': tags,
                                                    'profiles': profiles,
                                                    'authors': authors})

def view_tag(request, tagname):
    tag = tagname
    pagination = paginate(questions, request, 3)
    return render(request, '4-tags listning.html', {'questions': questions,
                                                    'tags': tags,
                                                    'tag': tag,
                                                    'profiles': profiles,
                                                    'authors': authors,
                                                    'pagination': pagination})

def settings(request, profileid):
    profile = profiles[profileid]
    return render(request, '5-profile settings.html', {'tags': tags,
                                                       'profile': profile,
                                                       'profiles': profiles,
                                                       'authors': authors})

def login(request):
    return render(request, '6-autorization form.html', {'tags': tags,
                                                        'profiles': profiles,
                                                        'authors': authors})

def registration(request):
    return render(request, '7-registration form.html', {'tags': tags,
                                                        'profiles': profiles,
                                                        'authors': authors})

def hot_questions(request):
    pagination = paginate(questions, request, 3)
    return render(request, '0-hot questions.html', {'questions': questions,
                                                    'tags': tags,
                                                    'profiles': profiles,
                                                    'authors': authors,
                                                    'pagination': pagination})

def view_author(request, authorname):
    author = authorname
    pagination = paginate(questions, request, 3)
    return render(request, '8-author listning.html', {'questions': questions,
                                                      'tags': tags,
                                                      'author': authorname,
                                                      'profiles': profiles,
                                                      'authors': authors,
                                                      'pagination': pagination})