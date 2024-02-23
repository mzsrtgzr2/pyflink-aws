
from pyflink.table import EnvironmentSettings, TableEnvironment


# 1. Creates a Table Environment

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table_env.get_config().get_configuration().set_string(
    "taskmanager.network.numberOfBuffers",
    "99999"
)

table_env.get_config().get_configuration().set_string(
    "taskmanager.memory.network.min",
    "1024mb"
)

table_env.get_config().get_configuration().set_string(
    "taskmanager.memory.network.max",
    "4096mb"
)

table_env.get_config().get_configuration().set_string(
    "taskmanager.memory.network.fraction",
    "0.1"
)

stmt_set = table_env.create_statement_set()


KAFKA_URL='broker:9092'
KAFKA_USER='...user...'
KAFKA_PASS='...pass...'
KAFKA_GROUP='flink-streams'


def main():

    table_env.execute_sql(f"""
    CREATE TABLE IF NOT EXISTS source (
        `id` bigint,
        PRIMARY KEY (id) NOT ENFORCED
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'source_topic',
        'properties.bootstrap.servers' = '{KAFKA_URL}',
        'properties.security.protocol' = 'SASL_SSL',
        'properties.sasl.mechanism' = 'PLAIN',
        'properties.sasl.jaas.config' = 'org.apache.kafka.common.security.plain.PlainLoginModule required username="{KAFKA_USER}" password="{KAFKA_PASS}";',
        'format' = 'debezium-json',
        'properties.group.id' = '{KAFKA_GROUP}',
        'properties.auto.offset.reset' = 'earliest'
    )
    """)

    # findings assets flat
    stmt_set.add_insert_sql(f"""
        INSERT INTO sink (
    `id`,
    `counts`,
    `aggs`
    )
    SELECT 
        ...
    GROUP BY 
        ...
    """)

    table_result = stmt_set.execute()

    print(table_result.get_job_client().get_job_status())

if __name__ == '__main__':
    main()


