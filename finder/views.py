from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Subject
import json


def index(request):
    if request.method == "POST":
        value = request.POST.get("subject_title")
        subject_list = Subject.objects.filter(title__contains=value)
        return render(request, "index.html", {"subjects": subject_list})
    subject_list = Subject.objects.all()
    return render(request, "index.html", {"subjects": subject_list})


def subject_view(request, subject_name):
    names = subject_name.split('-')
    title = Subject.objects.get(title__istartswith=names[0])
    with open(f"data/{title}.json", "r") as file:
        data = json.load(file)

    return render(request, "table.html", {"subject": title, "data": data})


def autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        subjects = Subject.objects.filter(title__contains=q)
        results = []
        for subject in subjects:
            subject_json = {}
            subject_json = subject.title
            results.append(subject_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
