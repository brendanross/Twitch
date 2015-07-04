#!/usr/bin/python

import urllib, urllib2, datetime, time, os, json#, mysql.connector
from lxml import html

#'''
#config = {
#  'user': 'pay2stream',
#  'password': '1q0ow2i9qwopA@!#',
#  'host': '127.0.0.1',
#  'database': 'pay2stream',
#}
#'''

#config = {
#  'user': 'root',
#  'password': 'th10z',
#  'host': '127.0.0.1',
#  'database': 'pay2stream',
#}

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
            curtimestamp = datetime.datetime.fromtimestamp(time.time())
            
            #cnx = mysql.connector.connect(**config)
            #cursor = cnx.cursor()
            image_filename = curtimestamp.strftime('%Y-%m-%d %H_%M_%S') + ".jpg"
            #qry = ("INSERT INTO stream_stats (account_name, viewers_current, viewers_total, created_at, screenshot) VALUES (%s, %s, %s, %s, %s)")

            #cursor.execute(qry, (twitch_account, data["stream"]["viewers"], data["stream"]["channel"]["views"], curtimestamp, image_filename))
            #cnx.commit()
            #cursor.close()
            #cnx.close()
            print "Current viewers: {}\nTotal views: {}".format(data["stream"]["viewers"], data["stream"]["channel"]["views"], curtimestamp, image_filename)
            
            image_url_local = d + image_filename
            urllib.urlretrieve(image_url, image_url_local)
        else:
	    print "no stream"    
    except IOError, e:
            print "Channel " + twitch_account + " not on twitch!"
    return 1

def scrapeClusterChannels( cluster_name ):
    "This function will request a list of accounts from the database to start scraping"
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("SELECT name FROM accounts WHERE p2s_cluster = '" + cluster_name + "'")

    cursor.execute(query)

    for itm in cursor:
        print "scraping channel : "+ itm[0]+"\n"
        scrapeTwitchChannel( itm[0] )
    cursor.close()
    cnx.close()
    return 1
scrapeTwitchChannel('brendanross')
#scrapeClusterChannels( "p2s1" )

