FROM python:3.7-alpine

WORKDIR /service
# Service will run on port 8080
EXPOSE 8080

# Install bjoern and dependencies for install
RUN apk add --no-cache --virtual .deps \
        musl-dev python-dev gcc git && \
    # Keep libev for running bjoern
    apk add --no-cache libev-dev && \
    pip install bjoern

# Copy files to /api directory, install requirements
COPY ./ /service
RUN pip install -r /service/requirements.txt

# Cleanup dependencies
RUN apk del .deps

# Start application
CMD [ "python", "server.py" ]
