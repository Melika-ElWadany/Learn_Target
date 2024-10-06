from django.shortcuts import render

def help(request):
    if request.method == "GET":
        return render(request, 'assistant/question.html')
    else:
        pass

        return render(request, 'assistant/answer.html')

