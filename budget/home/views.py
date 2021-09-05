from django.shortcuts import render
from django_plotly_dash.templatetags import plotly_dash

from .analytics import Analitic

analitic = Analitic()


def home_view(request):
    template = "home/home.html"

    return render(request, template)


def team_view(request):
    template = "home/team.html"

    return render(request, template)


def content_view(request):
    template = "home/content.html"

    return render(request, template)


def research_view(request):
    template = "home/research.html"

    return render(request, template)


def forecast_view(request):
    if request.method == "GET" and "calc" in request.GET and request.GET["calc"] == "ok":
        analitic.on_click()

    plot_div = analitic.plot
    template = "home/forecast.html"
    return render(
        request,
        template,
        {
            "dinamic": plot_div.budget,
            "nalognapr": plot_div.vat,
            "prognoz": plot_div.forecast,
            "ndfl": plot_div.pit,
        },
    )
