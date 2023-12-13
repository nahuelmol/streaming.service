from waitress import serve
from stream_site.wsgi import application


waitress_options = {
	'host':'127.0.0.1',
	'port':'8000',
	'threads':4,
}


if __name__ == '__main__':
	serve(application, **waitress_options)