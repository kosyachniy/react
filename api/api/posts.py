import time
# import shutil

from func.mongodb import db
from api._error import ErrorInvalid, ErrorAccess, ErrorWrong, ErrorUpload
from api._func import reimg, get_user, check_params, get_preview, next_id, load_image


# Add / edit

def edit(this, **x):
	# Checking parameters

	# Edit
	if 'id' in x:
		check_params(x, (
			('id', True, int),
			('name', False, str),
			('cont', False, str),
			('cover', False, str),
			('file', False, str),
			('category', False, int),
			('tags', False, list, str),
		))

	# Add
	else:
		check_params(x, (
			('name', True, str),
			('cont', True, str),
			('cover', False, str),
			('file', False, str),
			('category', False, int),
			('tags', False, list, str),
		))

	# Post formation

	if 'id' in x:
		post = db['posts'].find_one({'id': x['id']})

		# Wrong ID
		if not post:
			raise ErrorWrong('id')

	else:
		post = {
			'id': next_id('posts'),
			'time': this.timestamp,
			'reactions': {
				'likes': [],
				'reposts': [],
				'comments': [],
				'views': [],
			},
		}

	# Change fields

	for field in ('name', 'category', 'tags'):
		if field in x:
			post[field] = x[field]

	## Content
	if 'cont' in x:
		post['cont'] = reimg(x['cont'])

	## Cover
	if 'cover' in x:
		try:
			file_type = x['file'].split('.')[-1]

		# Invalid file extension
		except:
			raise ErrorInvalid('file')

		try:
			load_image('posts', x['cover'], post['id'], file_type)

		# Error loading cover
		except:
			raise ErrorUpload('cover')

	### Cover from the first image
	# try:
	# 	img = re.search('<img src="[^"]*">', post['cont'])[0].split('"')[1].split('/')[2]
	# 	shutil.copyfile('app/static/{}'.format(img), 'app/static/posts/{}.{}'.format(post['id'], img.split('.')[-1]))
	# except:
	# 	pass

	# Save post
	db['posts'].save(post)

	# Response

	res = {
		'id': post['id'],
	}

	return res

# Получение

def get(this, **x):
	# Checking parameters

	check_params(x, (
		('id', False, (int, list), int),
		('count', False, int),
		('category', False, int),
		# ('language', False, (int, str)),
	))

	# Condition formation

	process_single = False

	db_condition = {}

	if 'id' in x:
		if type(x['id']) == int:
			db_condition['id'] = x['id']

			process_single = True

		else:
			db_condition['id'] = {'$in': x['id']}

	# # Language

	# if 'language' in x:
	# 	x['language'] = get_language(x['language'])
	# else:
	# 	x['language'] = this.language

	# Get posts

	count = x['count'] if 'count' in x else None

	db_filter = {
		'_id': False,
		'id': True,
		'name': True,
		# 'cont': True,
		# 'reactions': True,
		# 'time': True,
	}

	if process_single:
		db_filter['cont'] = True

	posts = list(db['posts'].find(db_condition, db_filter).sort('time', -1)[:count])

	# Processing

	for i in range(len(posts)):
		## Cover
		posts[i]['cover'] = get_preview(posts[i]['id'], 'posts')

		## Content
		# if not process_single:
		# 	posts[i]['cont'] = re.sub('<[^>]*>', '', posts[i]['cont'])

	# Response

	res = {
		'posts': posts,
	}

	return res