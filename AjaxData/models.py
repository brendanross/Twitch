#AjaxData Models

from django.dispatch import receiver
from django.db import models
from allauth.account.signals import user_signed_up

#test
import urllib, urllib2, datetime, time, os, json
from lxml import html

def scrapeTwitchChannel( twitch_account ):
    "This function will save a timestamped image along with the total views at that moment"
    channel_url = "https://api.twitch.tv/kraken/streams/" + twitch_account + "?client_id=1rnx514hmnogu2sc4rc9vrb7rsoy5qu"
    image_url = "http://static-cdn.jtvnw.net/previews-ttv/live_user_" + twitch_account + "-1920x1080.jpg"
	
    try:
        response = urllib2.urlopen(channel_url)
        data = json.load(response)
	
        if data["stream"] != None:
            d= "/home/ubuntu/Twitch/script/TwitchTV/" + twitch_account + "/"
            if not os.path.isdir(d):
                    os.makedirs(d)
            curtimestamp = strftime("%Y-%m-%d %H:%M:%S")
            
            image_filename = curtimestamp + ".jpg"
            #needs json
            timestamp = []
            curViewers = []
            totViewers = []
            followers = []
            
            timestamp.append(curtimestamp)
            curViewers.append(data["stream"]["viewers"])
            totViewers.append(data["stream"]["channel"]["views"])
            followers.append(data["stream"]["channel"]["followers"])
            
            if userStats.objects.filter(username=twitch_account).exists():
              #handle existing users
              user = userStats.objects.get(username=twitch_account)
              
              #handle viewers
              currViewersJson = json.loads(user.currentViewers)
              currViewersJson.append(data["stream"]["viewers"])

              #handle views
              totalViewsJson = json.loads(user.totalViews)
              totalViewsJson.append(data["stream"]["channel"]["views"])

              #handle timestamp
              curtimestampJson = json.loads(user.timestamp)
              curtimestampJson.append(curtimestamp)
              
              #handle followers
              followersJson = json.loads(user.followers)
              followersJson.append(data["stream"]["channel"]["followers"])
              
              #save to DB
              user.currentViewers = json.dumps(currViewersJson)
              user.totalViews = json.dumps(totalViewsJson)
              user.timestamp = json.dumps(curtimestampJson)
              user.followers = json.dumps(followersJson)
              user.save()
            else:
              print "1"
              userStats.objects.create(username=twitch_account,
                                      currentViewers=json.dumps(curViewers),
                                      totalViews=json.dumps(totViewers),
                                      followers=json.dumps(followers),
                                      timestamp = json.dumps(curtimestamp))
            #cursor.execute(qry, (twitch_account, data["stream"]["viewers"], data["stream"]["channel"]["views"], curtimestamp, image_filename))
            
            #print "Current viewers: {}\nTotal views: {}".format(data["stream"]["viewers"], data["stream"]["channel"]["views"], curtimestamp, image_filename)
            
            image_url_local = d + image_filename
            urllib.urlretrieve(image_url, image_url_local)
        else:
	         userStats.objects.create(username=twitch_account,
	                                currentViewers="[]",
	                                totalViews="[]",
	                                followers="[]",
	                                timestamp="[]")
	         
    except IOError, e:
            print "Channel " + twitch_account + " not on twitch!"
    return 1

# def scrapeTwitchChannel( twitch_account ):
#     "This function will save a timestamped image along with the total views at that moment"
#     channel_url = "https://api.twitch.tv/kraken/streams/" + twitch_account + "?client_id=1rnx514hmnogu2sc4rc9vrb7rsoy5qu"
#     image_url = "http://static-cdn.jtvnw.net/previews-ttv/live_user_" + twitch_account + "-1920x1080.jpg"
	
#     try:
#         response = urllib2.urlopen(channel_url)
#         data = json.load(response)
	
#         if data["stream"] != None:
#             d= "/home/ubuntu/Twitch/script/TwitchTV/" + twitch_account + "/"
#             if not os.path.isdir(d):
#                     os.makedirs(d)
#             curtimestamp = datetime.datetime.fromtimestamp(time.time())
            
#             image_filename = curtimestamp.strftime('%Y-%m-%d %H_%M_%S') + ".jpg"
#             #needs json
#             curViewers = {}
#             totViewers = {}
#             curViewers[curtimestamp.strftime('%Y-%m-%d %H_%M_%S')] = data["stream"]["viewers"]
#             totViewers[curtimestamp.strftime('%Y-%m-%d %H_%M_%S')] = data["stream"]["channel"]["views"]
#             print curViewers[curtimestamp.strftime('%Y-%m-%d %H_%M_%S')]
#             print totViewers[curtimestamp.strftime('%Y-%m-%d %H_%M_%S')]
#             userStats.objects.create(username=twitch_account, currentViewers=json.dumps(curViewers), totalViews=json.dumps(totViewers))
#             #cursor.execute(qry, (twitch_account, data["stream"]["viewers"], data["stream"]["channel"]["views"], curtimestamp, image_filename))
            
#             print "Current viewers: {}\nTotal views: {}".format(data["stream"]["viewers"], data["stream"]["channel"]["views"], curtimestamp, image_filename)
            
#             image_url_local = d + image_filename
#             urllib.urlretrieve(image_url, image_url_local)
#         else:
# 	    print "no stream"
#     except IOError, e:
#             print "Channel " + twitch_account + " not on twitch!"
#     return 1

@receiver(user_signed_up)
def ensure_profile_exists(sender, **kwargs):
	user_registered = kwargs.get('user')
	scrapeTwitchChannel(user_registered.username)
	print "success"

# Create your models here.
class userStats(models.Model):

    username = models.TextField(
    )
    
    timestamp = models.TextField(
    )
    
    currentViewers = models.TextField(
    )

    totalViews = models.TextField(
    )
    
    followers = models.TextField(
    )
    
    
    def __str__(self):              # __unicode__ on Python 2
        return self.username
