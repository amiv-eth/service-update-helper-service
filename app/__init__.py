from flask import Flask, request, abort
from functools import wraps
import docker


app = Flask(__name__)
app.config.from_pyfile("config.py")
client = docker.from_env()


def verify_authorization(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    token = request.headers.get('Authorization', '').strip()
    if (' ' in token):  # Remove keywords, e.g. "Token (...)" or "Bearer (...)"
      token = token.split(' ')[1]

    if token in app.config['TOKEN']:
      return func(*args, **kwargs)
    return abort(401)
  return wrapper


@app.errorhandler(401)
def error_not_authenticated(e):
  return 'Authorization header missing or invalid!'


@app.errorhandler(404)
def error_not_found(e):
  return 'Service not found!'


@app.errorhandler(500)
def error_internal(e):
  return 'Could not update the requested service!'


@verify_authorization
@app.route('/service/<name>/update')
def service_update(name):
  try:
    service = client.services.get(name)
    if service.force_update():
      return "Service successfully updated."
    print('Updating service failed', flush=True)
    abort(500)
  except docker.errors.NotFound:
    abort(404)
  except e:
    print('Updating service failed', flush=True)
    print(e, flush=True)
    abort(500)
