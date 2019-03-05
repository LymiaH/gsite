# GSite
Website focused on making things easier for Grandpa.

## Running
- `pip install -r requirements.txt`
- `cp gsite/local_settings_example.py gsite/local_settings.py`
- `export DJANGO_SETTINGS_MODULE=gsite.settings`
- `python manage.py migrate`
- `python manage.py runserver`

## References
- [django](https://www.djangoproject.com/) the web framework and its examples
- [gitignore.io](https://www.gitignore.io/)
- [decentmark](https://github.com/DecentMark/decentmark) for the learning experience using django
