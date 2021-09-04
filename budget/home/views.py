from django.shortcuts import render
from django_plotly_dash.templatetags import plotly_dash
import json


def home_view(request):
    template = 'home/index.html'
    greeting = '🥥    КЛАСИВЫЙ ДИЗИГН ОТ ДИЗИГНЕРА КОКОСА   🥥'

    with open("fig.json", "r") as read_file:
        data = json.load(read_file)

    context = {
        'greeting': greeting
    }

    return render(request, template, context)


def team_view(request):
    template = 'home/team.html'
    greeting = '🥥    КЛАСИВЫЙ ДИЗИГН ОТ ДИЗИГНЕРА КОКОСА   🥥'
    context = {
        'greeting': greeting
    }

    return render(request, template, context)


def content_view(request):
    template = 'home/content.html'
    greeting = '🥥    КЛАСИВЫЙ ДИЗИГН ОТ ДИЗИГНЕРА КОКОСА   🥥'
    context = {
        'greeting': greeting
    }
    return render(request, template, context)


def research_view(request):
    template = 'home/research.html'
    greeting = '🥥    КЛАСИВЫЙ ДИЗИГН ОТ ДИЗИГНЕРА КОКОСА   🥥'
    context = {
        'greeting': greeting
    }

    return render(request, template, context)


