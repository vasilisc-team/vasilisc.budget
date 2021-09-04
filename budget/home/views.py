from django.shortcuts import render
from django_plotly_dash.templatetags import plotly_dash


def home_view(request):
    template = 'home/index.html'
    greeting = '🥥    КЛАСИВЫЙ ДИЗИГН ОТ ДИЗИГНЕРА КОКОСА   🥥'
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


