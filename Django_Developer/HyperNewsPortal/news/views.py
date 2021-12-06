import json
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Optional

from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from hypernews.settings import BASE_DIR, NEWS_JSON_PATH

JSON_FILE_PATH = Path(BASE_DIR, "hypernews", NEWS_JSON_PATH)


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")


def load_news(query: Optional[str] = None):
    json_file_path = Path(BASE_DIR, "hypernews", NEWS_JSON_PATH)
    news_by_date = {}
    with open(json_file_path) as news_file:
        loaded_news = json.load(news_file)
    for news in loaded_news:
        if query and query not in news["title"]:
            continue
        day = datetime.strptime(news["created"].split()[0], '%Y-%m-%d')
        if day not in news_by_date:
            news_by_date[day] = []

        news_by_date[day].append(
            {
                "created": datetime.strptime(news["created"], '%Y-%m-%d %H:%M:%S'),
                "link": news["link"],
                "title": news["title"],
                "text": news["text"],
            })
    return OrderedDict(sorted(news_by_date.items(), reverse=True))


def load_news_to_dict():
    with open(JSON_FILE_PATH, mode="r", encoding="utf-8") as news_file:
        return json.load(news_file)


class NewsMainView(TemplateView):
    template_name = "news_main.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', None)
        news = load_news(query=query)
        context["sorted_news"] = news
        return context


class NewsView(TemplateView):
    template_name = "news.html"

    def get_context_data(self, news_id, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_news = load_news_to_dict()
        for news in loaded_news:
            # print(news_id, news, news["link"])
            if news_id == str(news["link"]):
                context["title"] = news["title"]
                context["created"] = news["created"]
                context["text"] = news["text"]
                break

        return context


class CreateNewsView(TemplateView):
    template_name = "create_news.html"

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        # print(title, text)
        loaded_news = load_news_to_dict()
        loaded_news.append({
            "link": randint(1, 10 ** 10),
            "created": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "title": title,
            "text": text})

        with open(JSON_FILE_PATH, mode="w", encoding="utf-8") as news_file:
            news_file.write(json.dumps(loaded_news))

        return redirect("/news/")
