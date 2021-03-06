# GSite
Website focused on making things easier for Grandpa.

## Example

![GRadio: Podcast Aggregator](https://user-images.githubusercontent.com/13083365/110930604-45720280-8364-11eb-86cd-0d15e062e383.png)

## Running
- `pip install -r requirements.txt`
- `cp gsite/local_settings_example.py gsite/local_settings.py`
- `export DJANGO_SETTINGS_MODULE=gsite.local_settings`
- `python manage.py migrate`
- `python manage.py runserver`

## Deploying
- Activate virtualenv
- `pip install -r requirements.txt`
- `cp gsite/local_settings_example.py gsite/local_settings.py`
- `python manage.py collectstatic --settings gsite.local_settings`
- Edit local_settings.py
- `gunicorn gsite.asgi:application -k uvicorn.workers.UvicornWorker`

## References
- [django](https://www.djangoproject.com/) the web framework and its examples
- [gitignore.io](https://www.gitignore.io/)
- [decentmark](https://github.com/DecentMark/decentmark) for the learning experience using django
