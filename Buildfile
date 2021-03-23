01_install_requirements: pip3 install -r ./requirements.txt
02_migrate: python3 manage.py migrate
03_collectstatic: python3 manage.py collectstatic
