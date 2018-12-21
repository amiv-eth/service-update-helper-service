# Service Update Helper Service

A micro service to force update a service on a docker swarm cluster.

## Usage

The service provides just one `GET` endpoint (`/service/<service-name>/update`). This will force an update of the service with the name `<service-name>`. The request needs the header `Authorization` set to a valid token. Those are configured in the configuration fail.

## Development

### Virtualenv

The website runs using flask, and we recommend running it in a virtual
environment. To do this, you first need to initialize it:

```bash
virtualenv venv
```

In order to use a specific python version, add `--python /path/to/python<version>` to the command above.

This will initialize the virtual environment in the `venv` directory. To
activate it, source the following script:

```bash
source venv/bin/activate
```

If that was successful, your `$PS1` should start with `(venv)`.

### Dependencies

Now you need to install the dependencies listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Run

After that, you can run the service by executing `main.py`. The API is
served at `127.0.0.1:5000` by default.

## Deploy

The service is available as a docker image [amiveth/service-update-helper-service](https://hub.docker.com/r/amiveth/service-update-helper-service). 

Next, create a configuration based on `app/config.example.py` and save it (as a docker config).

Finally, create the service and mount the configuration file to `/service/app/config.py`.

*Please note that the service is available on port `8080`!*
