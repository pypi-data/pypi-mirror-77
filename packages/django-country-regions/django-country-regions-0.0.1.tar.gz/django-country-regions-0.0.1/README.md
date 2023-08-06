# django-country-regions
A simple app providing two models app providing countries and regions extracted from [django-cities-light](https://github.com/jazzband/django-cities-light)

# Requirements:
- Python >= 3.6
- Django >= 1.11
- MySQL or PostgreSQL or SQLite.


# Installation and configuration
## Install django-country-regions:
    pip install django-country-regions

## Add django-country-regions to your project's settings.INSTALLED_APPS
```python
#settings.py

INSTALLED_APPS = [
    #...some packages
    'country_regions',
    #...some packages
]
```


## Then run the full import
This command will create the corresponding tables and load the data into the database
```bash
example/manage.py migrate
```

## Author(s)
- [@afranck64](https://github.com/afranck64)