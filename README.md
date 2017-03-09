# reciprep-server

This is the repository for all back-end services for ReciPrep.

If you want to run the development environment, follow these steps.

If you're on Windows, start the Vagrant machine:
```
bin/vagrant.bat
```

For Linux / OSX / Windows:

Create the database:
```
docker-compose up postgres
bash bin/psql-init
docker-compose down
```

Start the services:
```
docker-compose up
```
