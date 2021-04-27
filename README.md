# Zeke's Solution for Symbiose Tech Test

## Setup/installation

1. [Install Docker](https://docs.docker.com/get-docker/)
    - ensure you also got docker-compose with `docker-compose --version` or
      [go get it](https://docs.docker.com/compose/install/)
2. Execute `script/run-dev-server.sh`
    - uses `docker-compose` to fire up the dev service that uses Google Cloud Functions debug mode
    - supports code reloading on file change
    - server is running when you see "Running on..." text (after Docker image builds and docker-compose deploys)
3. Send requests to http://localhost:8080/
    - executable examples in [app/functions/http/send_email_samples.http](app/functions/http/send_email_samples.http)

## Example cURL request

```shell
curl -X POST --location "http://localhost:8080/email" \
    -H "Content-Type: application/json" \
    -d "{
          \"to\": \"samantha@os.one\",
          \"to_name\": \"Samantha\",
          \"from\": \"theo@handwrittenletters.com\",
          \"from_name\": \"Theodore Twombly\",
          \"subject\": \"Feelings\",
          \"body\": \"Sometimes I think I’ve felt everything I’m ever gonna feel, and from here on out, I’m not gonna feel anything new…just…lesser versions of what I’ve already felt.\"
        }"
```