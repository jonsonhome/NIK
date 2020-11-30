

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import AnketaForm
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Связь с нами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О Нас',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def links (request):
        assert isinstance(request, HttpRequest)
        return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Полезные ссылки',
            'year':datetime.now().year,
        }
    )
def anketa(request):
        assert isinstance(request, HttpRequest)
        data = None
        gender = {'1': 'Мужчина', '2' : 'Женщина'}
        internet = {'1': 'Каждый день', '2': 'Несколько раз в день',
                   '3': 'Несколько раз в неделю', '4': 'Несколько раз в месяц' }
        if request.method == 'POST':
            form = AnketaForm(request.POST)
            if form.is_valid():
               data = dict()
               data['name'] = form.cleaned_data['name']
               data['city'] = form.cleaned_data['city']
               data['job'] = form.cleaned_data['job']
               data['gender'] = gender[ form.cleaned_data['gender'] ]
               data['gender'] = gender[ form.cleaned_data['gender'] ]
               data['internet'] = internet[ form.cleaned_data['internet'] ]
               if (form.cleaned_data['notice'] == True):
                   data['notice'] = 'Да'
               else:
                   data['notice'] = 'Нет'
               data['email'] = form.cleaned_data['email']
               data['massage'] = form.cleaned_data['massage']
               form = None
        else:
           form = AnketaForm()
        return render(
               request,
               'app/anketa.html',
               {
                   'form':form,
                   'data':data
                }             
        ) 
def registration(request):
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            regform.save()
            return redirect('home')
    else:
        regform = UserCreationForm()

    assert isinstance(request, HttpRequest)    
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year':datetime.now().year,
        }
    )
def blog(request):
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
        )
def blogpost(request, parametr):


    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():

            comment_f = form.save(commit=False)

            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя

            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату

            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий

            comment_f.save() # сохраняем изменения после добавления полей

            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

            comments = Comment.objects.filter(post=parametr)

    else:
 

        form = CommentForm() # создание формы для ввода комментария
    assert isinstance(request, HttpRequest)
    return render(


        request,

        'app/blogpost.html',

        {

         'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
         'comments': comments,
         'form': form,
         'year':datetime.now().year,

        }

    )
def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')

    else:
            blogform = BlogForm();

    return render(
        request,
        'app/newpost.html',
            {
                'blogform': blogform,
                'title':'Добавить статью',
    
                'year':datetime.now().year,
            }
        )

def videopost(request):

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
    'title':'О нас',
    'message':'Сведения о нас.',
    'year':datetime.now().year,
        }
)

