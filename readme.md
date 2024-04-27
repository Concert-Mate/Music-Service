# Creating virtual environment

```bash
poetry shell
```

```bash
poetry install
```

# Launch

```bash
uvicorn main:app
```

> You can specify arguments `--port` and `--host` (default values are 8000 and 127.0.0.1)

> You can specify environment variables `CONCERTS_EXPIRATION_TIME` and `TRACK_LISTS_EXPIRATION_TIME` (in seconds) for caching. Default values are 60 and 600 respectively 

# Documentation

You can see documentation of launched server at `/docs`. There you can also make requests.
