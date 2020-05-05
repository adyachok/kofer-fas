# FunctionAsService 

![alt text][id]

[id]: img/fas.png "Title"

### Description

FAS service provides functionality for custom code to be executed in the system.
The service is responsible for code verification. 

The code verification is done by Python [Bandit](https://github.com/PyCQA/bandit)
package. We tested different packages and frameworks, like CodeJail, AppArmour, 
PYT, and have found out Bandit as perfectly suitable.


**DISCLAIMER** the service is the integral part of ZZ project, but because the 
project is build using **service choreography architecture pattern** there are 
no strong, tight relations in it. This means that every part of ZZ can be 
modified - removed - rewritten accordingly to the needs of customer.


### Main components
- **dao** - this folder contains classes, which represent the main entities 
 in the service. We use [SQLAlchemy](https://www.sqlalchemy.org/) ORM for 
 facilitation of Python - PostgeSQL persistence process.
 - **app** - is the main entry point.
 - **config** - contains all configuration settings/logic.
 - **repositories** - contains persistence logic
 - **services** - contains processing logic for pre- and post persistence
 
### Interaction process


![alt text][schema]

[schema]: img/how%20fas%20works.png "Title"


### Installation


#### Run locally


To run locally application requires Kafka broker and MongoDB.

To install seamlessly **Kafka** broker we recommend 
[Kafka-docker](https://github.com/wurstmeister/kafka-docker) project. 
In the project you can find **docker-compose-single-broker.yml**

We suggest to create next alias

```bash alias kafka="docker-compose --file {PATH_TO}/kafka-docker/docker-compose-single-broker.yml up```

For PostgeSQL there can be found a few images, for example 
[postgres](https://hub.docker.com/_/postgres)


#### For local and dev/prod installations

  - Create PostgreSQL database:
   ```sql
    CREATE DATABASE zz_fas;
    -- Create user if needed
    CREATE USER testu WITH ENCRYPTED PASSWORD 'testp';
    -- Set permissions
    GRANT ALL PRIVILEGES ON DATABASE zz_fas TO testu;
   ```
  - Add persistent volume in OpenShif (prod env). Mount in */opt/app-root/src/uploads*
   or any you would like (You have to change **UPLOAD_FOLDER**).
   
  - Create Kafka topic:
   ```bash
   oc exec -it bus-kafka-1 -c kafka -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic runner-update --create --partitions 3 --replication-factor 3
   ```

### Debugging

We created instance of [Kafdrop](https://github.com/obsidiandynamics/kafdrop) with
the aim to facilitate debugging process. The running example instance can be found
in [BIX ZZ project](https://kafdrop-zz-test.22ad.bi-x.openshiftapps.com/)

Kafdrop has reach interface which helps a lot in tracking messages / events.

![alt text][kafdrop]

[kafdrop]: img/kafdrop.png "Title"

Yoiu can easily trace / read all messages in any topic:

![alt text][kafdrop_read]

[kafdrop_read]: img/kafdrop%202.png "Title"
    
### Used packages

 - [PYT](https://github.com/python-security/pyt)
 - [Confluent Kafka Python](https://github.com/confluentinc/confluent-kafka-python)
 - [Bandit](https://github.com/PyCQA/bandit)
 
### Interesting to know
 - Third party Python code can be executed via [CodelJail](https://github.com/edx/codejail)
 - [Apparmour in OpenShift](https://docs.openshift.com/container-platform/3.10/admin_guide/disabling_features.html)
  