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
    raw_image = service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image'].split('@', 2)[0]
    parts_image = raw_image.split(':', 2)
    new_image = client.images.pull(parts_image[0], parts_image[1])
    print('name: ' + new_image.id, flush=True)
    service.update(image=raw_image)
    return "Service successfully updated."
  except docker.errors.NotFound:
    abort(404)
