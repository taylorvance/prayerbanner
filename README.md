# Prayer Banner

Prayer Banner is a site for people to reserve prayer slots and pray for a Pilgrimage/Cursillo weekend. The site is run by Presbyterian Pilgrimage & Cursillo National Council.

## Installation

### Production

For production installation, follow this [excellent guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04) (or this [archived version](https://web.archive.org/web/20201207185142/https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04)).

### Local

There are a handful of prerequisites including but not limited to python3, pip, and virtualenv. The production installation guide above may help to fill in any gaps.

1. Clone this repo.
```
git clone https://github.com/taylorvance/prayerbanner.git
```

2. Prep environment settings. Make changes to the new `prayerbanner/.env` file.
```
cd prayerbanner
cp prayerbanner/.env.example prayerbanner/.env
```

3. Activate the virtual environment and install requirements.
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.py
```

4. Do the initial Django setup and run the local server.
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

5. Open the site in your browser (by default it's at `http://127.0.0.1:8000`).
