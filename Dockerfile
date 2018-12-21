FROM python:3.7-alpine

# Create user with home directory and no password and change workdir
RUN adduser -Dh /service service
WORKDIR /service
# Service will run on port 8080
EXPOSE 8080

# Install bjoern and dependencies for install (we need to keep libev)
RUN apk add --no-cache --virtual .deps \
        musl-dev python-dev gcc git && \
    apk add --no-cache libev-dev && \
    apk add --no-cache libffi-dev libressl-dev && \
    pip install bjoern

# Copy files to /api directory, install requirements
COPY ./ /service
RUN pip install -r /service/requirements.txt

# Cleanup dependencies
RUN apk del .deps

# Switch user
USER service

# Start application
CMD [ "python", "server.py" ]
