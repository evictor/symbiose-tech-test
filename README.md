# Zeke's Solution for _Symbiose Software Engineering Take Home_

## Setup/installation

1. [Install Docker](https://docs.docker.com/get-docker/), a newer version with `docker compose` support (i.e. after
   they deprecated independent `docker-compose` installation)
2. Run `run-dev-server.sh`
   - uses `docker compose` to fire up our dev service that uses Google Cloud Functions debug mode
   - supports code reloading on file change
3. Send requests to http://localhost:8080/
