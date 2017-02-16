# BUILD
    sudo docker build -t <name of image> <location of docker file>

#### Example
    sudo docker build -t reciprep_hello_world .

# RUN
    sudo docker run -d -p <ports> --name <process name> <image name>

#### Example
    sudo docker run -d -p 5000:5000 --name reciprep_process reciprep_hello_world


#### See Results

go to localhost:5000


# REBUILD
    sudo docker stop <process name>
    sudo docker rm <process name>
    sudo docker build -t <name of image> <location of docker file>
    sudo docker run -d -p <ports> --name <process name> <image name>
