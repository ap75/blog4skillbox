from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


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
                'messages': messages_data
            })
        if not text:
            return render(request, 'contacts.html', {
                'error': 'Пустой текст, напишите что-нибудь',
                'messages': messages_data
            })
        messages_data.append({
            # id нам тоже не нужен, если только мы не хотим дать возможность
            # например, редактировать или удалять уже отправленные сообщения
            #'id': len(messages_data),
            'name': name,
            'text': text.replace('\n', '<br />')
        })
    # Независимо от метода (GET или PUT) мы должны отрендерить и показать
    # страницу с контактами
    return render(request, 'contacts.html', {
        'messages': messages_data
    })


publications_data = [
    {
        'id': 0,
        'name': 'Моя первая публикация',
        'date': datetime.now(),
        'text': '''Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
                   <br><br>The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.'''
    },
    {
        'id': 1,
        'name': 'Моя вторая публикация',
        'date': datetime.now(),
        'text': '''Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC
                   <br><br>"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"'''
    },
    {
        'id': 2,
        'name': 'Моя 3я публикация',
        'date': datetime.now(),
        'text': '''Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC
                   <br><br>"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"'''
    }
]


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

        publications_data.append({
            'id': len(publications_data),
            'name': name,
            'date': datetime.now(),
            'text': text.replace('\n', '<br />')
        })
        return redirect('/publications')


def publications(request):
    return render(request, 'publications.html', {
        'publications': publications_data
    })


def publication(request, number):
    if number < len(publications_data):
        return render(request, 'publication.html', publications_data[number])
    else:
        return redirect('/')


def status(request):
    return HttpResponse('<h2>OK</h2>')
