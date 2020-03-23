# FunctionAsService

### Installation
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
    
### Used packages

 - [PYT](https://github.com/python-security/pyt)
 - [Confluent Kafka Python](https://github.com/confluentinc/confluent-kafka-python)