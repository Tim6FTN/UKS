# UKS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Build Status](https://api.travis-ci.com/Tim6FTN/UKS.svg?branch=dev)](https://travis-ci.org/Tim6FTN/UKS) [![GitHub release](https://img.shields.io/github/v/release/Tim6FTN/UKS?include_prereleases)](https://gitHub.com/Tim6FTN/UKS/releases/) [![Website Status](https://img.shields.io/website?down_color=red&down_message=offline&up_color=green&up_message=online&url=http%3A%2F%2Fuksapp-env.eba-phrzywrq.eu-central-1.elasticbeanstalk.com%3A1234%2F)](http://uksapp-env.eba-phrzywrq.eu-central-1.elasticbeanstalk.com:1234/) [![Visitors Count](https://visitor-badge.glitch.me/badge?page_id=Tim6FTN.UKS)](https://github.com/Tim6FTN/UKS)


## Introduction

This project is a web-based system providing support for managing collaborations and issue tracking on projects that are connected to a GitHub repository.

It was created and developed during the [Software Configuration Management course](http://www.igordejanovic.net/courses/uks.html) as part of the master degree program at the Faculty of Technical Sciences, University of Novi Sad.

## Technology stack & Tooling

- Python (Django REST Framework)
- Postgres SQL
- Next.js (React)
- Docker 
- Redis
- Grafana, Influx DB
- Elasticsearch, Logstash, Kibana
- Travis CI
- AWS Elastic Beanstalk

## Data model

[![Data model](https://raw.githubusercontent.com/Tim6FTN/UKS/dev/diagrams/UKS.png)]((https://raw.githubusercontent.com/Tim6FTN/UKS/dev/diagrams/UKS.png))


## Environment setup

The following instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### For development

#### Prerequisites

- [Python >= 3.5](https://www.python.org/downloads/)
- [Postgres SQL >= 13.0](https://www.postgresql.org/download/)
- [Node.js](https://nodejs.org/en/)
- [Docker](https://www.docker.com/get-started) *(optional)*

##### Starting backend
```
$ cd backend
$ start.sh
```

##### Starting frontend
```
$ cd frontend
$ npm install
$ npm run dev
```

#### Service access

Backend - http://localhost:8000
Frontend - http://localhost:1234
Kibana - http://localhost:5601
ElasticSearch - http://localhost:9200
Logstash - http://localhost:8083
Grafana - http://localhost:3001

### For testing
1. Make sure Docker is up and running, and set the configuration to Linux containers.
2. Open `cmd` and navigate to the backend folder where `docker-compose.yml` is located
3. Start the containers using the `docker-compose up -d` command.

## Integrating with GitHub

Integrating your GitHub repository with our tool is a two-step process.

First, you need to create a project by specifying the URL of the GitHub repository you want to integrate with. The project will be created and all available branches and commits will be imported, together with metrics. The process of importing the repository can be long and directly depends of the size of your repository.

After the project has been successfully created, you then need to create a repository Webhook on GitHub. You'll first need to set up how you want your webhook to behave through GitHub i.e. what events should it listen to. Currently supported events by our system are:
- `push`
- `branch creation`
- `branch deletion`

After that, you'll need to specify the [URL to our service](http://uksapp-env.eba-phrzywrq.eu-central-1.elasticbeanstalk.com:8000/notify) where our system will automatically receive and manage the payload and crunch all the data for you. Additionally, select the content type. Note that at this moment, only the `application/json` content type is supported.

In case the delivery of the initial `ping` event is successful, you are ready to go. 😀👍

## Contributors

- [R2 7/2020 Milan Milovanović](https://github.com/m-milovanovic)
- [R2 8/2020 Marko Stanić](https://github.com/Marko131)
- [R2 9/2020 Mihailo Đokić](https://github.com/mdjokic)
- [R2 23/2020 Katarina Tukelić](https://github.com/ktukelic)
- [R2 25/2020 Filip Ivković](https://github.com/fivkovic)

## License
This is a free and open-source project licensed under the MIT License.