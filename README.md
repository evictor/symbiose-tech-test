# Zeke's Solution for _Symbiose Software Engineering Take Home_

## Setup/installation

1. [Install Docker](https://docs.docker.com/get-docker/)
   - ensure you also got docker-compose with `docker-compose --version` or 
     [go get it](https://docs.docker.com/compose/install/)
2. Run `run-dev-server.sh`
   - uses `docker-compose` to fire up our dev service that uses Google Cloud Functions debug mode
   - supports code reloading on file change
3. Send requests to http://localhost:8080/
