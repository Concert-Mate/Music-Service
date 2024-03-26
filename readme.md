# How to launch

```bash
poetry run -vvv python app.py
```

> `poetry run -vvv` runs python in poetry-environment and uses its plugin to read `.env` and load variables to environment.

> Server reads `PORT` and `HOST` from `.env`. Default values can be found in `app/settings.py`


# How to run tests?

```bash
python -m unittest discover tests
```
