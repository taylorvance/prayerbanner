# prayerbanner

To set up using the Django dev server on your local system:
```
git clone https://github.com/taylorvance/prayerbanner.git
cd prayerbanner
cp prayerbanner/.env.example prayerbanner/.env
source venv/bin/activate
pip install -r requirements.py
python manage.py migrate
python manage.py runserver
```

To set up using docker on your local system:
```
git clone https://github.com/taylorvance/prayerbanner.git
cd prayerbanner
cp prayerbanner/.env.example prayerbanner/.env
docker-compose build
docker-compose up -d
docker-compose down -v
```
