# The goal of this Dockerfile is to install 'curl' for health check, to make sure other services
# Won't try to address it before it's ready. it's like a readyness probe.
# source: https://stackoverflow.com/questions/31746182/docker-compose-wait-for-container-x-before-starting-y

FROM rabbitmq:3-management
RUN apt-get update
RUN apt-get install -y curl 
EXPOSE 4369 5671 5672 25672 15671 15672