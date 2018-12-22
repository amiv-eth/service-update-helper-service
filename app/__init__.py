from flask import Flask, request, abort
import docker


app = Flask(__name__)
app.config.from_pyfile("config.py")
client = docker.from_env()


@app.errorhandler(401)
def error_not_authenticated(e):
  return 'Authorization header missing or invalid!'


@app.errorhandler(404)
def error_not_found(e):
  return 'Service not found!'


@app.errorhandler(500)
def error_internal(e):
  return 'Could not update the requested service!'


@app.route('/service/<name>/update')
def service_update(name):
  # Check authorization header first
  token = request.headers.get('Authorization', '').strip()
  if (' ' in token):  # Remove keywords, e.g. "Token (...)" or "Bearer (...)"
    token = token.split(' ')[1]

  if token not in app.config['TOKENS']:
    return abort(401)

  # Try to update the requested service
  try:
    service = client.services.get(name)
    print(service.attrs, flush=True)
    # client.images.pull(service.attrs[''], service.attrs[''])
    if service.force_update():
      return "Service successfully updated."
    abort(500)
  except docker.errors.NotFound:
    abort(404)
