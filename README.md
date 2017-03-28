# stockworks
This is a repository that attempts to orchestrate the use of our microservices
into a coherent retrieval process.  This is simply a testing harness to prove out
the data flow is correct.


## Configuration
The included docker-compose.yml is meant to be used to bring up the microservice
scaffolding. You will need to include an env.list file in the directory of the following
format

    BLUEMIXTONEURL=https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19
    BLUEMIXUSER=<bluemixuserid>
    BLUEMIXPASS=<bluemixpassword>

Optional - you can additionally setup the tone service to use the optional Redis Sidecar cache
as defined in the docker-compose file by setting the SIDECAR environment variable

    SIDECAR=sidecar


## Usage

    docker-compose up
    python app.py <STOCK TICKER>

Example for SNAP chat

    python app.py SNAP

