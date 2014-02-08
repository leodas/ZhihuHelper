# encoding: utf-8

#!/usr/bin/env python

import zhihu
import json
import re

try:
	import requests
	from bs4 import BeautifulSoup
except:
	print "Library requests/BeautifulSoup NOT FOUND, and I need them."

class ZhihuSession(requests.Session):
	""" Wrapper of requests.Session at zhihu.com. """

	def __init__(self):
		super(ZhihuSession, self).__init__()
		r = self.get(url=zhihu.HOME_URL)
		self._cookies = r.cookies
		self.me = None

	def getData(self, url, **kwargs):
		res = self.get(url=url, **kwargs)
		self._cookies = res.cookies
		return res

	def postData(self, url, data=None, **kwargs):
		data['_xsrf'] = self._cookies['_xsrf']
		return self.post(url=url, data=data, cookies = self._cookies, **kwargs)

	def login(self, user, passwd):
		""" Login zhihu.com with 'user' and 'passwd' """

		login_data = {
			'email': user,
			'password': passwd,
			'rememberme': 'y',
			}
		res = self.postData(url=zhihu.LOGIN_URL, data=login_data)

		tag_result = BeautifulSoup(res.text).find('div', {'class': 'failure'})
		if tag_result:
			print tag_result.find('li').text
			return False

		me = zhihu.ZhihuUser()
		soup = BeautifulSoup(res.text)
		tag = soup.find('div', {'role': 'navigation'}).find('a', {'class': 'zu-top-nav-userinfo '})
		me.relative_url = tag['href']
		me.link_name = me.relative_url[len('/people/'):]
		me.url = zhihu.HOME_URL + me.relative_url
		self.me = me

		return True

	# TODO: logout
	def logout(self):
		""" Logout zhihu.com """
		pass

	def getUserProfile(self, url=None):
		""" Get a user's profile, 'url' is the user's page link. """

		if url:
			user = zhihu.ZhihuUser()
			user.url = url
			user.link_name = url[len(zhihu.HOME_URL + '/people/'):]
			user.relative_url = url[len(zhihu.HOME_URL):]
		else:
			assert self.me
			user = self.me

		res = self.getData(user.url)
		soup = BeautifulSoup(res.text)

		try:
			tag_p = soup.find('div', class_='title-section ellipsis')
			user.name = tag_p.find('span', {'class': 'name'}).string
			user.desc  = tag_p.find('span', {'class': 'bio'}).string

			tag_p = soup.find('div', class_='zm-profile-header-user-describe')
			_attr_dict = {
				'location':   'location item',
				'business':   'bussiness item',
				'employment': 'employment item',
				'position':   'position item',
				'education':  'education item',
			}
			for attr_key in _attr_dict:
				try:
					attr_value = tag_p.find('span', {'class': _attr_dict[attr_key]})
					user.__setattr__(attr_key, attr_value)
				except:
					raise

			if soup.find('input', class_='female').has_attr('checked'):
				sex = 'female'
			elif soup.find('input', class_='male').has_attr('checked'):
				sex = 'male'
			user.sex = sex

			tag_agrees = soup.find('span', class_='zm-profile-header-user-agree')
			tag_thanks = soup.find('span', class_='zm-profile-header-user-thanks')

			user.agrees = int(tag_agrees.strong.string)
			user.thanks = int(tag_thanks.strong.string)

			tag_personal    = soup.find('div', class_ = 'profile-navbar clearfix')
			personal_href   = tag_personal.find('a', class_ = 'item home first active')['href']

			tag_asks        = tag_personal.find('a', href = personal_href+'/asks')
			tag_answers     = tag_personal.find('a', href = personal_href+'/answers')
			tag_posts       = tag_personal.find('a', href = personal_href+'/posts')
			tag_collections = tag_personal.find('a', href = personal_href+'/collections')
			tag_logs        = tag_personal.find('a', href = personal_href+'/logs')
			tag_follow      = soup.find('div', class_ = 'zm-profile-side-following')
			tag_followees   = tag_follow.find('a', href = personal_href+'/followees')
			tag_followers   = tag_follow.find('a', href = personal_href+'/followers')

			user.asks        = int(tag_asks.span.string)
			user.answers     = int(tag_answers.span.string)
			user.posts       = int(tag_posts.span.string)
			user.collections = int(tag_collections.span.string)
			user.logs        = int(tag_logs.span.string)
			user.followees   = int(tag_followees.strong.string)
			user.followers   = int(tag_followers.strong.string)

		except:
			raise # zhihu.ZhihuError(0x1000)

		return user

	def getAnswersOnPage(self, content):
		""" """

		answer_list = []

		soup = BeautifulSoup(content)
		tag_wrap = soup.find('div', {'class': 'zm-profile-section-list profile-answer-wrap'})
		answers_wrap = tag_wrap.find_all('div', {'class': 'zm-item'})

		for answer_wrap in answers_wrap:
			qa = answer_wrap.find('a', {'class': 'question_link'})
			question = zhihu.ZhihuQuestion()
			question.title = qa.text
			question.url = zhihu.HOME_URL + qa['href'] # TODO: This is answer link

			answerer = zhihu.ZhihuUser()
			text_wrap = answer_wrap.find('div', {'class': 'zm-item-rich-text'})
			text_area = text_wrap.find('textarea')

			tag_answer_owner = answer_wrap.find('div', {'class': 'zm-item-answer '})
			if not tag_answer_owner:
				tag_answer_owner = answer_wrap.find('div', {'class': 'zm-item-answer zm-item-answer-owner'})
			aid = tag_answer_owner['data-aid']
#			atoken = tag_answer_owner['data-atoken']
#			collapsed = tag_answer_owner['data-collapsed']
#			created = tag_answer_owner['data-created']
#			deleted = tag_answer_owner['data-deleted']
#			isowner = tag_answer_owner['data-isowner']
#			helpful = tag_answer_owner['data-helpful']

			answer = zhihu.ZhihuAnswer(
				question=question,
				text=text_area.text,
				aid=aid
				)

			answer_list.append(answer)

		return answer_list, len(answer_list)

	def getAnswers(self, url=None):
		""" """

		if url:
			user = self.getUserProfile(url)
		else:
			assert self.me
			user = self.me

		answer_list = []

		answers_url = zhihu.MY_ANSWERS_URL % user.link_name
		res = self.getData(url=answers_url)

		soup = BeautifulSoup(res.text)

		page_size = 1
		# Calculating pages
		pager_tag = soup.find('div', {'class': 'zm-invite-pager'})
		if pager_tag:
			pagers = pager_tag.find_all('span')
			last_pager = pagers[-2]
			if last_pager.a:
				page_size = int(last_pager.a.text)
			else:
				page_size = int(last_pager.text)
			#print '%d pages found' % page_size

		start_page = 1
		while start_page <= page_size:
			res = self.getData(url=(answers_url + ('?page=%d' % start_page)))
			answers_on_page, size_on_page = self.getAnswersOnPage(res.text)
			answer_list.extend(answers_on_page)
			#print 'Page %d has cached, %d answers' % (start_page, size_on_page)
			start_page += 1

		return answer_list, len(answer_list)

	def delAnswer(self, answer):

		remove_data = {
			aid: answer.aid,
		}
		self.postData(url=zhihu.REMOVE_ANSWER_URL, data=remove_data)

		# TODO: Error handling

		return True

	def getPostUrls(self, content):

		post_url_list = []

		soup = BeautifulSoup(content)
		tag = soup.find('div', {'id': 'zh-profile-posts'}).find('div', {'class': 'profile-column-posts'})
		posts_tags = tag.find_all('div', {'class': 'header'})
		for posts_tag in posts_tags:
			post_url_list.append(posts_tag.a['href'])

		return post_url_list, len(post_url_list)

	def getPosts(self, url=None):
		""" """

		if url:
			user = self.getUserProfile(url)
		else:
			assert self.me
			user = self.me

		post_list = []

		posts_link_url = zhihu.MY_POSTS_URL % user.link_name
		res = self.getData(url=posts_link_url)
		posts_urls, posts_urls_size = self.getPostUrls(res.text)
		print '%d blogs found' % posts_urls_size

		for posts_url in posts_urls:
			# Posts short name
			posts_name = posts_url[len(zhihu.POSTS_URL) + 1:] # '1' for '/'
			size = 0
			while True:
				res = self.getData(url=(zhihu.POSTS_API_URL % posts_name + '?limit=10&offset=%d' % size))
				r = json.loads(res.text)
				if len(r) == 0:
					break

				for e in r:
					post = zhihu.ZhihuPost(
						author=e['author']['name'],
						rating=e['rating'],
						source_url=e['sourceUrl'],
						links=e['links']['comments'],
						column=e['column']['name'],
						topics=e['topics'],
						title=e['title'],
						summary=e['summary'],
						content=e['content'],
						state=e['state'],
						title_image=e['titleImage'],
						meta=e['meta'],
						href=e['href'],
						comment_permission=e['commentPermission'],
						snapshot_url=e['snapshotUrl'],
						can_comment=e['canComment'],
						slug=e['slug'],
						comments_count=e['commentsCount'],
						likes_count=e['likesCount'],
						datetime=e['publishedTime']
						)
					print e['title']
					size += 1
					post_list.append(post)

		return post_list, len(post_list)

	@staticmethod
	def __buildQuestions(soup):

		questions = []

		for qs in soup.find_all('div', class_='zm-item'):
			r = qs.find_all('a', target='_blank')
			dt = qs.find('time')
			q = zhihu.ZhihuQuestion(
				title=r[0].text,
				url=zhihu.HOME_URL + r[0]['href'],
				log_id=qs['id'][len('logitem-'):],
				datetime=datetime.datetime.strptime(dt['datetime'], zhihu.ZHIHU_DATETIME_FORMAT)
				)
			if len(r) > 1: # Not an anonymous user
				q.questioner = r[1].text
				q.questioner_url = zhihu.HOME_URL + r[1]['href']
			questions.append(q)

		return questions, len(questions)

	def getGlobalQuestions(self, size=-1):
		""" Get global log question, default size depends on zhihu.com. """

		questions = []

		res = self.getData(url=zhihu.GLOBAL_QUESTIONS_URL)
		soup = BeautifulSoup(res.text)

		question_wrap = soup.find('div', id='zh-global-logs-questions-wrap')

		qs, s = self.__buildQuestions(question_wrap)
		questions.extend(qs)

		size -= s
		while size > 0:
			_data = {
				'start': questions[-1].log_id,
				'offset': size - len(questions), # Actually this field can be any value,
				                                 # it just using for the page show.
			}
			res = self.session.postData(url=zhihu.GLOBAL_QUESTIONS_URL, data=_data)
			jm = json.loads(res.text)
			qs, s = self.__buildQuestions(BeautifulSoup(jm['msg'][1]))
			questions.extend(qs)
			size -= jm['msg'][0] # or s

		return questions, len(questions)