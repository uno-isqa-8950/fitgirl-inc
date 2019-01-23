from django.shortcuts import render

def pre_assessment(request):
    return render(request,
                  'assessment/pre_assessment.html',
                  {'section': 'pre_assessment'})

def post_assessment(request):
    return render(request,
                  'assessment/post_assessment.html',
                  {'section': 'post_assessment'})