from rauth.session import OAuth1Session
import json

class TradeKing:
	def __init__(self, conf):
		self.sess = OAuth1Session(
			consumer_key=conf['consumer_key'],
			consumer_secret=conf['consumer_secret'],
			access_token=conf['oauth_token'],
			access_token_secret=conf['oauth_token_secret'])

		self.quote_ep = 'https://api.tradeking.com/v1/market/ext/quotes.json'
		self.stream_ep = 'https://stream.tradeking.com/v1/market/quotes.json'

	def getQuotes(self, symbols):
		symbols_str = ','.join(symbols)
		resp = self.sess.get(self.quote_ep, params={'symbols': symbols_str})
		return  json.loads(resp.text)['response']['quotes']['quote']

	def getStream(self, symbols):
		symbols_str = ','.join(symbols)
		resp = self.sess.get(self.stream_ep, params={'symbols': symbols_str}, 
			stream=True)

		json_str = ''
		for char in resp.iter_content():
			if char:
				json_str += char
				try:
					data = json.loads(json_str)
					json_str = ''
					yield data
				except:
					pass