#Profile Views
from django.shortcuts import render
from AjaxData.models import userStats
# Create your views here.

def viewProfile(request):
  print request.user.username
  user = userStats.objects.get(username=request.user.username)
  print user
  return render(request, 'profile.html', {'currentViewers':user.currentViewers,
                                        'totalViews':user.totalViews,
                                        'followers':user.followers,
                                        'timestamp':user.timestamp})