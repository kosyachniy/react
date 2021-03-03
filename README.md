# Template full stack application
## Description
Web-app on JS with JSON-RPC API

Form | Side | Stack | Language | Path
---|---|---|---|---
API | Back-end | Flask | Python | ``` api/ ```
Web app | Front-end | React | JavaScript | ``` web/ ```
Telegram bot | Back-end | AIOGram | Python | planned
iOS | Front-end | React Native | JavaScript | planned
Android | Front-end | React Native | JavaScript | planned

### Stack
<table>
	<thead>
		<tr>
			<th>Side</th>
			<th>Logo</th>
			<th>Technology</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td rowspan="3">DevOps</td>
			<td><img src="re/img/docker_logo.png" alt="Docker" height="70" /></td>
			<td><img src="re/img/docker_name.png" alt="Docker" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/nginx_logo.png" alt="NGINX" height="70" /></td>
			<td><img src="re/img/nginx_name.png" alt="NGINX" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/letsencrypt_logo.png" alt="Let's Encrypt" height="70" /></td>
			<td><img src="re/img/letsencrypt_name.png" alt="Let's Encrypt" height="70" /></td>
		</tr>
		<tr>
			<td rowspan="3">Back-end</td>
			<td><img src="re/img/flask_logo.png" alt="Flask" height="70" /></td>
			<td><img src="re/img/flask_name.png" alt="Flask" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/mongodb_logo.png" alt="MongoDB" height="70" /></td>
			<td><img src="re/img/mongodb_name.png" alt="MongoDB" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/socketio_logo.png" alt="Socket.IO" height="70" /></td>
			<td><img src="re/img/socketio_name.png" alt="Socket.IO" height="70" /></td>
		</tr>
		<tr>
			<td rowspan="4">Front-end</td>
			<td><img src="re/img/reactjs_logo.png" alt="ReactJS" height="70" /></td>
			<td><img src="re/img/reactjs_name.png" alt="ReactJS" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/redux_logo.png" alt="Redux" height="70" /></td>
			<td><img src="re/img/redux_name.png" alt="Redux" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/bootstrap_logo.png" alt="Bootstrap 4" height="70" /></td>
			<td><img src="re/img/bootstrap_name.png" alt="Bootstrap 4" height="70" /></td>
		</tr>
		<tr>
			<td><img src="re/img/ckeditor_logo.png" alt="CKEditor 5" height="70" /></td>
			<td><img src="re/img/ckeditor_name.png" alt="CKEditor 5" height="70" /></td>
		</tr>
	</tbody>
</table>

## Install & Use with Docker
### Development
1. Customize files ``` api/keys.json ``` & ``` web/src/keys.js ``` & ``` docker/.env ```

2. Run Docker Compose
```
cd docker/
docker-compose up --build
```

3. Open
Go to ``` http://localhost/ ```

### Production
1. Customize files ``` api/keys.json ``` & ``` web/src/keys.js ``` & ``` docker/.env ``` & ``` api/sets.prod.py ``` & ``` web/src/sets.prod.js ``` & ``` docker/server/nginx.prod.conf ```

2. Run Docker Compose
```
docker-compose -f docker-compose.prod.yml up --build
```

3. Install NGINX
```
sudo apt-get update
sudo apt install nginx
y
```

4. Configure NGINX (optional)
```
sudo nano /etc/nginx/nginx.conf
```

If there is no access to static:
```
	user root;
```

If there is a download of large files:
```
	types_hash_max_size 20480;
	client_max_body_size 30m;
```

5. Configure NGINX project
```
sudo cp /docker/server/nginx.prod.conf /etc/nginx/sites-available/<name of the project>

sudo ln -s /etc/nginx/sites-available/<name of the project> /etc/nginx/sites-enabled

sudo systemctl restart nginx
```

6. Install Let's Encrypt
```
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
<enter>
```

```
sudo apt-get update
sudo apt-get install certbot python-certbot-nginx
y
```

7. Set up Let's Encrypt's sertificates
```
sudo certbot --nginx
<your mail>
A
Y
1
2
```

8. Open

Go to ``` https://web.kosyachniy.com/ ``` (your link)

### Production (alone)
1. Customize files ``` api/keys.json ``` & ``` web/src/keys.js ``` & ``` docker/.env ``` & ``` api/sets.prod.py ``` & ``` web/src/sets.prod.js ``` & ``` docker/server/nginx.alone.conf ``` & ``` docker/server/nginx.cert.conf ``` & ``` docker/cert.sh ```

2. Create encryption keys
```
cd docker/
chmod 777 cert.sh
./cert.sh
```

3. Run Docker Compose
```
docker-compose -f docker-compose.alone.yml up --build
```

4. Open

Go to ``` https://web.kosyachniy.com/ ``` (your link)

## Install
### Back-end
1. Change folder
```
cd api/
```

2. Customize files ``` sets.py ``` & ``` keys.json ```

3. Virtual environment
```
python3 -m venv env
env/bin/pip install -r requirements.txt
```

### Front-end
1. Change folder
```
cd web/
```

2. Customize files ``` src/sets.js ``` & ``` src/keys.js ```

3. Virtual environment
```
npm install
```

OR

```
npm run build
```

## Usage
### Back-end
```
env/bin/gunicorn app:app -k eventlet -w 1 -b :5000 --reload
```

### Front-end
```
npm start
```

OR

```
serve -s build -p 3000
```