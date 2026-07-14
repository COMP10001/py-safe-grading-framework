# build the docker image containing the tests and run them
docker run --rm -it --memory=512m -v $(pwd)/build/docker:/output $(docker build --quiet .)