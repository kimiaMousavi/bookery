from django.shortcuts import render, redirect
import json
from elasticsearch import Elasticsearch
from django.contrib.auth.decorators import login_required
from search.models import BookMark
from datetime import datetime

@login_required
def main_page(request):
    """The export page choose what kind of export wanted and related things"""
    if request.method == 'POST':

        query = request.POST.get('search') or "null"
        title = request.POST.get('title') or "null"
        publisher = request.POST.get('publisher') or "null"
        author = request.POST.get('author') or "null"
        language = request.POST.get('choices-language') or "null"

        pages = request.POST.get("choices-page") or "null"
        rate = request.POST.get("choices-rate") or "null"

        context = ''
        if title != "null" or publisher != "null" or author != "null" or\
                language != "null" or pages != "null" or rate != "null":

            dic = {'title': title, 'authors': author, 'average_rating': rate, 'pages': pages, 'publisher': publisher,
                   'language_code': language, 'summery': title}
            print(dic)
            result_l = advanced_search(dic)
        else:
            result_l = normal_search(query)
        return render(request, 'search/result.html', {'result': result_l})

    else:
        return render(request, 'search/index.html')


def normal_search(query):
    """ """
    elastic_client = Elasticsearch(hosts=["localhost"])

    chunk_size = 1
    query_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title"]
                # "fields": ["title", "summery", "author"]

            }
        }
    }

    results = elastic_client.search(index="books", body=query_body, size=20)

    result_list = []
    for result in results['hits']['hits']:
        # print(result)
        # print('##############')
        result_list.append({
            'title': result['_source']['title'],
            'authors': result['_source']['authors'],
            'average_rating': result['_source']['average_rating'],
            'pages': result['_source']['pages'],
            'date': result['_source']['date'],
            'publisher': result['_source']['publisher'],
            'language_code': result['_source']['language_code'],
            'summary': result['_source']['summery'],
        })
    result_list = sorted(result_list, key=lambda i: i['average_rating'], reverse=True)
    return result_list


def advanced_search(dic):

    query_body = "{"'"query"'": {"'"bool"'":"  "{"'"must"'":["
    b = ''
    for f in dic:
        if dic[f] != 'null':
            n = ("{"'"match"'": {"'"' + f + '"'":"'"' + dic[f] + '"'"}}")

            b = b + n + ','

    query_body = query_body + b[:-1] + ']}}}'

    print(query_body)
    elastic_client = Elasticsearch(hosts=["localhost"])
    results = elastic_client.search(index="books", body=query_body, size=20)

    result_list = []
    for result in results['hits']['hits']:
        # print(result)
        # print('##############')
        result_list.append({
            'title': result['_source']['title'],
            'authors': result['_source']['authors'],
            'average_rating': result['_source']['average_rating'],
            'pages': result['_source']['pages'],
            'date': result['_source']['date'],
            'publisher': result['_source']['publisher'],
            'language_code': result['_source']['language_code'],
            'summary': result['_source']['summery'],
        })
    result_list = sorted(result_list, key=lambda i: i['average_rating'], reverse=True)
    print(result_list)
    return result_list


def add_bookmark(request):
    b_m = BookMark()
    b_m.user = request.user

    print(request.POST.get('want'))
    print(request.POST.get('read'))
    if request.POST.get('want') is None:
        b_m.book_id = request.POST.get('read')[5:]
        b_m.date_added = datetime.today().strftime('%Y-%m-%d')
        b_m.read()

    else:
        b_m.book_id = request.POST.get('want')[5:]
        b_m.date_added = datetime.today().strftime('%Y-%m-%d')

    b_m.save()

    user = request.user
    book_list = BookMark.objects.filter(user=user)

    bl = book_list.values_list().distinct()
    return render(request, 'search/book_mark.html', {'book_list': bl})


def bookmark_history(request):

    user = request.user
    book_list = BookMark.objects.filter(user=user)

    bl = book_list.values_list().distinct()
    return render(request, 'search/book_mark.html', {'book_list': bl})


def comingSoon(request):
    return render(request, 'search/comingSoon.html')
