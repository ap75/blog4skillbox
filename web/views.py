from datetime import datetime

from django.conf import settings
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .models import Message, Publication, Comment


def index(request):
    return render(request, 'index.html')


messages_data = []


def contacts(request):
    if request.method == 'POST':
        # Кто-то пытается добавить новое сообщение на страницу контактов
        # Секретный код проверять не будем - пусть это могут делать все
        # Проверим, все ли поля заполнены и добавим сообщение в список
        name = request.POST['name']
        text = request.POST['text']
        if not name:
            return render(request, 'contacts.html', {
                'error': 'Пустое имя, представьтесь, пожалуйста',
                'messages': Message.objects.all()
            })
        if not text:
            return render(request, 'contacts.html', {
                'error': 'Пустой текст, напишите что-нибудь',
                'messages': Message.objects.all()
            })
        Message.objects.create(
            name=name,
            text=text.replace('\n', '<br />')
        )
    # Независимо от метода (GET или PUT) мы должны отрендерить и показать
    # страницу с контактами
    return render(request, 'contacts.html', {
        'messages': Message.objects.all()
    })


def publish(request):
    if request.method == 'GET':
        return render(request, 'publish.html')
    else:
        secret = request.POST['secret']
        name = request.POST['name']
        text = request.POST['text']

        if secret != settings.SECRET_KEY:
            return render(request, 'publish.html', {
                'error': 'Неправильный Secret Key'
            })
        if len(name) == 0:
            return render(request, 'publish.html', {
                'error': 'Пустое имя'
            })
        if len(text) == 0:
            return render(request, 'publish.html', {
                'error': 'Пустой text'
            })

        Publication(
            name=name,
            text=text.replace('\n', '<br />')
        ).save()
        return redirect('/publications')


def publications(request):
    return render(request, 'publications.html', {
        'publications': Publication.objects.all()
    })


def publication(request, number):
    pubs = Publication.objects.filter(id=number)

    if len(pubs) == 1:
        pub = model_to_dict(pubs[0])
        error = ''
        if request.method == 'POST':
            # Добавляем комментарий на публикацию, проверим поля
            # Секретный код проверять не будем - пусть комментировать могут все
            name = request.POST['name']
            text = request.POST['text']
            if not name:
                error = 'Пустое имя, представьтесь, пожалуйста'
            elif not text:
                error = 'Пустой текст, напишите что-нибудь'
            if not error:
                # Все в порядке, добавляем комментарий
                Comment.objects.create(
                    publication=pubs[0],
                    name=name,
                    text=text.replace('\n', '<br />')
                )
        # Не забудем передать нужные данные (конекст) в шаблон
        context = pub
        context['comments'] = [{
            'name': comment.name,
            'date': comment.date,
            'text': comment.text,
        } for comment in pubs[0].comments.all()]
        # Если были ошибки, добавим их тоже
        context['error'] = error
        return render(request, 'publication.html', context)
    else:
        return redirect('/')


def status(request):
    return HttpResponse('<h2>OK</h2>')


def click(request):
    # Если метод не POST или нам не пришел id, то что-то не так
    if request.method != 'POST' or not 'id' in request.POST:
        return redirect('/')
    publucation, comment, operation = request.POST['id'].split('.')
    # Здесь должна быть куча проверок: publucation - число и существует,
    # comment - число и (0 или существует), operation - одно из двух
    # допустимых значений, но...
    # поступим проще: все оберенем в try ... except
    try:
        likes = 0
        publucation = int(publucation)
        comment = int(comment)
        operation = int(operation)
        if comment:
            # Лайк относится к комментарию
            if 'likes' in publications_data[publucation]['comments'][comment - 1]:
                # У этого комментария уже есть лайки
                publications_data[publucation]['comments'][comment - 1]['likes'] += operation
            else:
                # Это первый лайк для этого комментария
                publications_data[publucation]['comments'][comment - 1]['likes'] = operation
            likes = publications_data[publucation]['comments'][comment - 1]['likes']
        else:
            # Лайк относится к публикации
            if 'likes' in publications_data[publucation]:
                # У этой публикации уже есть лайки
                publications_data[publucation]['likes'] += operation
            else:
                # Это первый лайк для этой публикации
                publications_data[publucation]['likes'] = operation
            likes = publications_data[publucation]['likes']
    except:
        return redirect('/')
    return JsonResponse({'likes': likes})
