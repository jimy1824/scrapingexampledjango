from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
import json
from .serializers import TweetListSerializer

# Create your views here.
import requests
from bs4 import BeautifulSoup

class TweetsListView(APIView):
    serializers_class = TweetListSerializer
    # def get_tweets(self):
    #     list_of_repo=[]
    #     response = requests.get('https://github.com/trending')
    #     print(response.status_code)
    #     if response.status_code:
    #         # Create a BeautifulSoup object
    #         raw_html = BeautifulSoup(response.text, 'html.parser')
    #         repo_list = raw_html.find_all(class_='Box-row')
    #         for repo in repo_list:
    #             repo_name = repo.find(class_='col-9 text-gray my-1 pr-4')
    #             repo_link=repo.find('a')
    #             # print(repo_link)
    #             if repo_name:
    #               repo_obj={'first_name': repo_name.get_text().strip(), 'last_name': 'developerer', }
    #               list_of_repo.append(repo_obj)
    #               # print(repo_link.get_text())
    #     return  list_of_repo

    def get_twitter_tweets(self):
        list_of_tweets = []
        handle = input('Input your account name on Twitter: ')
        ctr = int(input('Input number of tweets to scrape: '))
        print('https://twitter.com/' + handle)
        res = requests.get('https://twitter.com/' + handle)
        bs = BeautifulSoup(res.content, 'lxml')
        all_tweets = bs.find_all('div', {'class': 'tweet'})
        if all_tweets:
            for tweet in all_tweets[:ctr]:
                context = tweet.find('div', {'class': 'context'}).text.replace("\n", " ").strip()
                content = tweet.find('div', {'class': 'content'})
                header = content.find('div', {'class': 'stream-item-header'})
                user = header.find('a', {
                    'class': 'account-group js-account-group js-action-profile js-user-profile-link js-nav'}).text.replace(
                    "\n", " ").strip()
                time = header.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}).find(
                    'span').text.replace("\n", " ").strip()
                message = content.find('div', {'class': 'js-tweet-text-container'}).text.replace("\n", " ").strip()
                footer = content.find('div', {'class': 'stream-item-footer'})
                stat = footer.find('div', {'class': 'ProfileTweet-actionCountList u-hiddenVisually'}).text.replace("\n",
                                                                                                                   " ").strip()
                if context:

                    print(context)
                print(user, time)
                print(message)
                print(stat)
                tweets = {'full_name': user.strip(), 'message': message, }
                list_of_tweets.append(tweets)
        else:
            print("List is empty/account name not found.")
        return list_of_tweets

    def get_tweet_list(self):
        # self.get_twitter_tweets()
        data=self.get_twitter_tweets()
        # data={'first_name': 'jimy', 'last_name': 'developerer', }
        return self.serializers_class(data,many=True).data

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        return Response(self.get_tweet_list(), status=HTTP_200_OK)
