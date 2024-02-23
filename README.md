## How to run pyflink in AWS Manageg Flink service

I'm publishing this code with my notes on how to deploy pyflink with AWS Kinesis  
because it was not trivial to do so. I encountered lots of bumps in the road   
but eventually successful. 

- only supported with flink version 1.15.2 in AWS 
- only one JAR is supported
    
    - add / remove dependencies in [fat-jar-generator/pom.xml](fat-jar-generator/pom.xml):
        ```xml
        <dependencies>
            <!-- Apache Flink dependencies -->
            <!-- These dependencies are provided, because they should not be packaged into the JAR file. -->
            <dependency>
                <groupId>org.apache.flink</groupId>
                <artifactId>flink-sql-connector-kafka</artifactId>
                <version>${flink.version}</version>
            </dependency>

            <dependency>
                <groupId>org.apache.flink</groupId>
                <artifactId>flink-connector-jdbc</artifactId>
                <version>${flink.version}</version>
            </dependency>

            <dependency>
                <groupId>org.postgresql</groupId>
                <artifactId>postgresql</artifactId>
                <version>${postgres.version}</version>
            </dependency>

            <dependency>
                <groupId>com.mysql</groupId>
                <artifactId>mysql-connector-j</artifactId>
                <version>${mysql.version}</version>
            </dependency>


            <dependency>
                <groupId>org.apache.kafka</groupId>
                <artifactId>kafka-clients</artifactId>
                <version>${kafka.clients.version}</version>
            </dependency>
        </dependencies>
        ```
    - run: 
        ```bash
        cd fat-jar-generator
        mvn package
        cp target FlinkFatJar-0.1.jar ../code/
        ```
- zip code with `zip -r code.zip code` and upload to S3
- in the Stream applcation variables choose:
    - `kinesis.analytics.flink.run.options` - key: `jarfile`, value: `code/FlinkFatJar-0.1.jar`
    - `kinesis.analytics.flink.run.options` - key: `python`, value: `code/flink_run.py`

- the python code here is not operational, just a boilerplate


sources: 
- https://github.com/confluentinc/realtime-sentiment-analysis
