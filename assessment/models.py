from django.db import models
from django.conf import settings

class Pre_assessment_Question(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ques1 = models.CharField(max_length=100, default =None)
    ques2 = models.CharField(max_length=100, default =None)
    ques3 = models.CharField(max_length=100, default =None)
    ques4 = models.CharField(max_length=100, default =None)
    ques5 = models.CharField(max_length=100, default =None)
    ques6 = models.CharField(max_length=100, default =None)
    ques7 = models.CharField(max_length=100, default =None)
    ques8 = models.CharField(max_length=100, default =None)
    ques9 = models.CharField(max_length=100, default =None)
    ques10 = models.CharField(max_length=100, default =None)
    ques11 = models.CharField(max_length=100, default =None)
    ques12 = models.CharField(max_length=100, default =None)
    ques13 = models.CharField(max_length=100, default =None)
    ques14 = models.CharField(max_length=100, default =None)
    ques15 = models.CharField(max_length=100, default =None)
    ques16 = models.CharField(max_length=100, default =None)
    ques17 = models.CharField(max_length=100, default =None)


class Pre_assessment_Choice(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=None)
    # models.ForeignKey(Pre_assessment_Question,on_delete = models.CASCADE)
    ans1 = models.CharField(max_length=20, default =None)
    ans2 = models.CharField(max_length=20, default =None)
    ans3 = models.CharField(max_length=20, default =None)
    ans4 = models.CharField(max_length=20, default =None)
    ans5 = models.CharField(max_length=20, default =None)
    ans6 = models.CharField(max_length=20, default =None)
    ans7 = models.CharField(max_length=20, default =None)
    ans8 = models.CharField(max_length=20, default =None)
    ans9 = models.CharField(max_length=20, default =None)
    ans10 = models.CharField(max_length=20, default =None)
    ans11 = models.CharField(max_length=20, default =None)
    ans12 = models.CharField(max_length=20, default =None)
    ans13 = models.CharField(max_length=20, default =None)
    ans14 = models.CharField(max_length=20, default =None)
    ans15 = models.CharField(max_length=20, default =None)
    ans16 = models.CharField(max_length=20, default =None)
    ans17 = models.CharField(max_length=20, default =None)

    def __str__(self):
        return str (self.user)

# Create your models here.
