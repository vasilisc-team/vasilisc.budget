import json

import plotly
import plotly.graph_objs as go
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django_plotly_dash.templatetags import plotly_dash


def home_view(request):
    template = 'home/home.html'

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
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
    plot_div = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    template = 'home/forecast.html'
    return render(request, template,  {'dinamic': plot_div, 'nalognapr': plot_div, 'prognoz': plot_div, 'ndfl': plot_div})


