#!/bin/bash
read -p 'This will update the docker image on docker hub, are you sure? (y/N) ' execflag
if [[ $execflag == y* || $execflag == Y* ]]
then
    echo "Preparing to push ontoology image to docker hub"
    if [ $# -eq 0 ]
  then
        docker image build -t ahmad88me/stiqueue . --no-cache
    docker image push ahmad88me/stiqueue
  else
    docker image build -t ahmad88me/stiqueue:$1 . --no-cache
    docker image push ahmad88me/stiqueue:$1
    fi
else
    echo "The docker image will not be updated in docker hub"
fi
#echo Your answer is $execflag