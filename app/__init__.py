from flask import Flask, request, abort
import docker


app = Flask(__name__)
app.config.from_pyfile("config.py")
client = docker.from_env()


@app.errorhandler(401)
def error_not_authenticated(e):
  return 'Error 401: Authorization header missing or invalid!', 401


@app.errorhandler(403)
def error_forbidden(e):
  return 'Error 403: Forbidden! You are not allowed to update the service.', 403


@app.errorhandler(404)
def error_not_found(e):
  return 'Error 404: Service not found!', 404


@app.errorhandler(500)
def error_internal(e):
  return 'Error 500: Could not update the requested service!', 500


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
    raw_image = service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image'].split('@', 2)[0]
    parts_image = raw_image.split(':', 2)
    repository_prefix = parts_image[0].split('/', 2)[0]

    if (repository_prefix not in app.config['ALLOWED_REPOSITORY_PREFIXES']):
      abort(403)

    service.update(image=raw_image)
    service.reload()

    if (service.force_update()):
      return "Success!"

    abort(500)
  except docker.errors.NotFound:
    abort(404)
