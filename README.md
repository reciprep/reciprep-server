# reciprep-server

This is the repository for all back-end services for ReciPrep.

If you want to run the development environment, follow these steps.

If you're on Windows, start the Vagrant machine:
```
bin/vagrant.bat
```

When inside the VM:
```
cd /vagrant
```

For Linux / OSX:

Create the databases:
```
docker-compose up postgres &
bash bin/psql-init
bash bin/psql-test-init
docker-compose down
```

Start the services:
```
docker-compose up
```

To run API tests:
```
docker-compose -f docker-test.yml up
```
