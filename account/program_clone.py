from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import ProgramClone
import tzlocal

from account.models import Inactiveuser, CloneProgramInfo, Program
from wagtail.core.models import Page
import datetime
#from datetime import datetime
# from datetime import datetime, timedelta





@login_required
def cloneprogram(request):
    if request.method == "POST":
        form = ProgramClone(request.POST)
        if form.is_valid():
            user = request.user
            new_start_date = str(form.cleaned_data['new_start_date'])
            program_to_clone = form.cleaned_data['program_to_clone']
            new_program = form.clean()['new_program']

            date_fields = new_start_date.split('-')
            new_start_datetime = datetime.datetime(int(date_fields[0]), int(date_fields[1]), int(date_fields[2]),
                                                   tzinfo=tzlocal.get_localzone())
            new_program_slug = '-'.join(new_program.lower().split(' '))

            if Page.objects.filter(slug=new_program_slug).count() > 0 \
                    or Page.objects.filter(title=new_program).count() > 0:
                message = "Error: A program with this name already exists"
            elif CloneProgramInfo.objects.filter(new_program=new_program, active=True).count() > 0:
                message = "Error: This program is already scheduled for setup"
            else:
                new_program_info = CloneProgramInfo()
                new_program_info.program_to_clone = program_to_clone
                new_program_info.new_program = new_program
                new_program_info.new_start_date = new_start_datetime
                new_program_info.active = True
                new_program_info.user = user
                new_program_info.save()
                message = 'Your program is being created.  This will take several minutes. You will receive an email when the process is complete.'
                return render(request, 'account/cloneprogram.html', {'form': form, 'message': message})
        else:
            message = 'Error: Invalid data'
            return render(request, 'account/cloneprogram.html', {'form': form, 'message': message})
    else:
        form = ProgramClone()
        return render(request, 'account/cloneprogram.html', {'form': form})

