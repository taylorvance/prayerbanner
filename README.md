# prayerbanner

prereqs: git, docker

to set up on local system
```
git clone https://github.com/taylorvance/prayerbanner.git
cd prayerbanner
cp prayerbanner/.env.example prayerbanner/.env
docker-compose build
docker-compose up -d
docker-compose down -v
```
