from datetime import datetime

from django.conf import settings
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Publication


def index(request):
    return render(request, 'index.html')


def contacts(request):
    return render(request, 'contacts.html')


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
        return render(request, 'publication.html', pub)
    else:
        return redirect('/')


def status(request):
    return HttpResponse('<h2>OK</h2>')
