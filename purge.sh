docker container ls -a | awk '{print $1}' | xargs sudo docker rm -f
docker image ls -a | awk '{print $3}' | xargs sudo docker rmi $(sudo docker images -aq) --force
