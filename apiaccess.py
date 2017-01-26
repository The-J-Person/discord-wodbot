#!/usr/bin/python3
from rauth import OAuth1Service

class ObsidianAPI():
    def __init__(self, ObsidianKey, ObsidianSecret):
        self.Obsidian = OAuth1Service(
            #name = 'some name here', #Seems obsidian doesn't require this
            consumer_key=ObsidianKey,
            consumer_secret=ObsidianSecret,
            request_token_url='https://www.obsidianportal.com/oauth/request_token',
            access_token_url='https://www.obsidianportal.com/oauth/access_token',
            authorize_url='https://www.obsidianportal.com/oauth/authorize',
            base_url='http://api.obsidianportal.com/v1/')
    def get_auth_url(self):
        self.request_token, self.request_token_secret = self.Obsidian.get_request_token()
        return self.Obsidian.get_authorize_url(self.request_token)
    def verify(self,verifier):
        self.session = self.Obsidian.get_auth_session(self.request_token, 
                                    self.request_token_secret, 
                                    method='POST', 
                                    data={'oauth_verifier': verifier})
    def get_user_data(self):
        return self.session.get('users/me.json', params={'format': 'json'}).json()    
    
    def get_user_data_xml(self):
        return self.session.get('users/me.xml', params={'format': 'xml'})
    
    def get_character_index(self,campaign_id):
        return self.session.get('campaigns/' + campaign_id + '/characters.json', params={'format': 'json'}).json()
    
    def get_wikipage_index(self,campaign_id):
        return self.session.get('campaigns/' + campaign_id + '/wikis.json', params={'format': 'json'}).json()
    
    def get_character(self,campaign_id,character_id):
        return self.session.get('campaigns/' + campaign_id + '/characters/' + character_id + '.json',params={'format': 'json'}).json()
    
    def change_char(self, campaign_id, character_id, data):
        #return self.session.put('campaigns/' + campaign_id + '/characters/' + character_id + '.json', data).json()
        return self.session.request('PUT','campaigns/' + campaign_id + '/characters/' + character_id + '.json', json=data).json()
    def create_char(self,campaign_id,data):
        return self.session.post('campaigns/' + campaign_id + '/characters.json',data=data).json()
    def create_wikipage(self,campaign_id,data):
        return self.session.post('campaigns/' + campaign_id + '/wikis.json',data=data).json()
        