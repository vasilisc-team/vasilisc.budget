import json

from django.shortcuts import render
from django_plotly_dash.templatetags import plotly_dash


def home_view(request):
    template = 'home/index.html'

    return render(request, template)


def team_view(request):
    template = 'home/team.html'

    return render(request, template)


def content_view(request):
    template = 'home/content.html'

    return render(request, template)


def research_view(request):
    template = 'home/research.html'

    return render(request, template)


def forecast_view(request):
    template = 'home/forecast.html'

    return render(request, template)


