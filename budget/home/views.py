from django.shortcuts import render


def home_view(request):
    template = 'home/home.html'
    greeting = '🥥    КЛАСИВЫЙ ДИЗИГН ОТ ДИЗИГНЕРА КОКОСА   🥥'
    context = {
        'greeting': greeting
    }

    return render(request, template, context)
