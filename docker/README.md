# The docker part is no longer maintained.

## Run Docker

Example of running the server from Docker

```docker container run --interactive -p "1234:1234" --tty --rm --name stiqueue ahmad88me/stiqueue```


# Update Docker

For example, to update docker image with version `v1.0`

`sh scripts/update_docker_image.sh v1.0`


*Note: the tests will use the default port and would

start and the server automatically, so you don't

need to run it before running the tests. Also note that

after running the tests, the operating system might take

a couple of seconds to release the port.*