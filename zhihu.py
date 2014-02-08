# encoding: utf-8

#!/usr/bin/env python

HOME_URL              = 'http://www.zhihu.com'

LOGIN_URL             = HOME_URL + '/login'
GLOBAL_QUESTIONS_URL  = HOME_URL + '/log/questions'

SLUG_URL              = HOME_URL + '/people/%s'

MY_ANSWERS_URL        = HOME_URL + '/people/%s' + '/answers'
MY_ASKS_URL           = HOME_URL + '/people/%s' + '/asks'
MY_POSTS_URL          = HOME_URL + '/people/%s' + '/posts'
MY_COLLECTIONS_URL    = HOME_URL + '/people/%s' + '/collections'

POSTS_URL             = 'http://zhuanlan.zhihu.com'
POSTS_API_URL         = POSTS_URL + '/api/columns/%s/posts'

REMOVE_ANSWER_URL     = HOME_URL + '/answer/remove'

ZHIHU_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class ZhihuError(Exception):
	"""  """

	__error_dict = {
		0x1000: "Page has updated, please update this code",
		0x2001: "Parameter checking failed",
		0xFFFF: "Unknown exception, the error code has not defined yet",
	}

	def __init__(self, code):
		self.err_code = code

	def __str__(self):
		if not __error_dict.has_key(self.err_code):
			return __error_dict[0xFFFF]

		return __error_dict[self.err_code]

class ZhihuUserBase(object):

	def __init__(self,
			name         ='匿名用户',
			relative_url =None,
			link_name    =None,
			url          =None,
			agree        =0,
			thanks       =0,
			followers    =0,
			followees    =0,
			asks         =0,
			answers      =0,
			posts        =0,
			collections  =0,
			logs         =0,
			sex          =None,
			desc         =None,
			locations    =None,
			bussiness    =None,
			employment   =None,
			position     =None,
			education    =None
		):
		pass

class ZhihuUser(ZhihuUserBase):

	def __init__(self):
		super(ZhihuUser, self).__init__()

class ZhihuQuestion(object):

	def __init__(self,
			title    =None,
			url      =None,
			asker    =None,
			log_id   =None,
			datetime =None):
		self.title    = title
		self.url      = url
		self.asker    = asker
		self.log_id   = log_id
		self.datetime = datetime

class ZhihuAnswer(object):

	def __init__(self,
			question =None,
			answerer =None,
			text     =None,
			datetime =None,
			aid      =None):
		self.question = question
		self.answerer = answerer
		self.text     = text
		self.datetime = datetime
		self.aid      = aid

class ZhihuPost(object):

	def __init__(self,
			author             =None,
			rating             =None,
			source_url         =None,
			links              =None,
			column             =None,
			topics             =None,
			title              =None,
			summary            =None,
			content            =None,
			state              =None,
			title_image        =None,
			meta               =None,
			href               =None,
			comment_permission =None,
			snapshot_url       =None,
			can_comment        =True,
			slug               =None,
			comments_count     =0,
			likes_count        =0,
			datetime           =None):
		self.author             = author
		self.rating             = rating
		self.source_url         = source_url
		self.links              = links
		self.column             = column
		self.topics             = topics
		self.title              = title
		self.summary            = summary
		self.content            = content
		self.state              = state
		self.title_image        = title_image
		self.meta               = meta
		self.href               = href
		self.comment_permission = comment_permission
		self.snapshot_url       = snapshot_url
		self.can_comment        = can_comment
		self.slug               = slug
		self.comments_count     = comments_count
		self.likes_count        = likes_count
		self.datetime           = datetime