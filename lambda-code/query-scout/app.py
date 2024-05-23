from logging import getLogger
from psycopg2 import connect
from os import environ
from boto3 import client
from botocore.exceptions import ClientError
from json import loads

logger = getLogger()
logger.setLevel("INFO")


region = environ.get('AWS_REGION')
secret = environ.get('SECRET')

secretManager = client(service_name='secretsmanager',region_name=region)

try:
    secretValue = secretManager.get_secret_value(SecretId=secret)
except ClientError as e:
    raise e
logger.info('recieved secret value')
dbname = environ.get('DBNAME')
logger.info(f'DBNAME={dbname}')
user = loads(secretValue['SecretString'])['username']
password = loads(secretValue['SecretString'])['password']
logger.info('recieved user and pass')
host = environ.get('HOST')
logger.info(f'HOST={host}')
port = environ.get('PORT')
logger.info(f'PORT={port}')

logger.info("Try to connect")
try:
    conn = connect(dbname=dbname, user=user, password=password, host=host, port=port)
    logger.info("Connected to database")
except:
    logger.error("Unable to connect to database")

def handler(event, context):
    cur = conn.cursor()

    create_table_users_query = '''
    CREATE TABLE IF NOT EXISTS Users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20),
        state_id INT,
        region_id INT,
        city_id INT,
        is_admin_state BOOLEAN DEFAULT FALSE,
        is_admin_region BOOLEAN DEFAULT FALSE,
        is_admin_city BOOLEAN DEFAULT FALSE,
        is_superadmin BOOLEAN DEFAULT FALSE,
        CONSTRAINT fk_state
            FOREIGN KEY(state_id)
                REFERENCES States(state_id),
        CONSTRAINT fk_region
            FOREIGN KEY(region_id)
                REFERENCES Regions(region_id),
        CONSTRAINT fk_city
            FOREIGN KEY(city_id)
                REFERENCES Cities(city_id)
    );
    '''

    create_table_states_query = '''
    CREATE TABLE IF NOT EXISTS States (
        state_id SERIAL PRIMARY KEY,
        state_name VARCHAR(255) NOT NULL,
        admin_id INT,
        CONSTRAINT fk_admin_state
            FOREIGN KEY(admin_id)
                REFERENCES Users(user_id)
    );
    '''

    create_table_regions_query = '''
    CREATE TABLE IF NOT EXISTS Regions (
        region_id SERIAL PRIMARY KEY,
        region_name VARCHAR(255) NOT NULL,
        state_id INT,
        admin_id INT,
        CONSTRAINT fk_state_region
            FOREIGN KEY(state_id)
                REFERENCES States(state_id),
        CONSTRAINT fk_admin_region
            FOREIGN KEY(admin_id)
                REFERENCES Users(user_id)
    );
    '''

    create_table_cities_query = '''
    CREATE TABLE IF NOT EXISTS Cities (
        city_id SERIAL PRIMARY KEY,
        city_name VARCHAR(255) NOT NULL,
        region_id INT,
        admin_id INT,
        CONSTRAINT fk_region_city
            FOREIGN KEY(region_id)
                REFERENCES Regions(region_id),
        CONSTRAINT fk_admin_city
            FOREIGN KEY(admin_id)
                REFERENCES Users(user_id)
    );
    '''

    create_table_scoutgroups_query = '''
    CREATE TABLE IF NOT EXISTS ScoutGroups (
        scout_group_id SERIAL PRIMARY KEY,
        group_name VARCHAR(255) NOT NULL,
        group_leader_id INT,
        CONSTRAINT fk_group_leader
            FOREIGN KEY(group_leader_id)
                REFERENCES Users(user_id)
    );
    '''

    create_table_users_scoutgroups_query = '''
    CREATE TABLE IF NOT EXISTS Users_ScoutGroups (
        scout_group_id SERIAL PRIMARY KEY,
        group_name VARCHAR(255) NOT NULL,
        group_leader_id INT,
        CONSTRAINT fk_group_leader
            FOREIGN KEY(group_leader_id)
                REFERENCES Users(user_id)
    );
    '''

    create_tables = '''
    CREATE TABLE States (
        state_id SERIAL PRIMARY KEY,
        state_name VARCHAR(255) NOT NULL,
        admin_id INT
    );

    CREATE TABLE Regions (
        region_id SERIAL PRIMARY KEY,
        region_name VARCHAR(255) NOT NULL,
        state_id INT,
        admin_id INT
    );

    CREATE TABLE Cities (
        city_id SERIAL PRIMARY KEY,
        city_name VARCHAR(255) NOT NULL,
        region_id INT,
        admin_id INT
    );

    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20),
        state_id INT,
        region_id INT,
        city_id INT,
        is_admin_state BOOLEAN DEFAULT FALSE,
        is_admin_region BOOLEAN DEFAULT FALSE,
        is_admin_city BOOLEAN DEFAULT FALSE,
        is_superadmin BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE ScoutGroups (
        scout_group_id SERIAL PRIMARY KEY,
        group_name VARCHAR(255) NOT NULL,
        group_leader_id INT
    );

    CREATE TABLE Users_ScoutGroups (
        user_id INT,
        scout_group_id INT,
        PRIMARY KEY (user_id, scout_group_id)
    );'''

    create_FK = '''
    ALTER TABLE Regions
    ADD CONSTRAINT fk_state_region
    FOREIGN KEY(state_id)
    REFERENCES States(state_id);

    ALTER TABLE Cities
    ADD CONSTRAINT fk_region_city
    FOREIGN KEY(region_id)
    REFERENCES Regions(region_id);

    ALTER TABLE Users
    ADD CONSTRAINT fk_state
    FOREIGN KEY(state_id)
    REFERENCES States(state_id);

    ALTER TABLE Users
    ADD CONSTRAINT fk_region
    FOREIGN KEY(region_id)
    REFERENCES Regions(region_id);

    ALTER TABLE Users
    ADD CONSTRAINT fk_city
    FOREIGN KEY(city_id)
    REFERENCES Cities(city_id);

    ALTER TABLE States
    ADD CONSTRAINT fk_admin_state
    FOREIGN KEY(admin_id)
    REFERENCES Users(user_id);

    ALTER TABLE Regions
    ADD CONSTRAINT fk_admin_region
    FOREIGN KEY(admin_id)
    REFERENCES Users(user_id);

    ALTER TABLE Cities
    ADD CONSTRAINT fk_admin_city
    FOREIGN KEY(admin_id)
    REFERENCES Users(user_id);

    ALTER TABLE ScoutGroups
    ADD CONSTRAINT fk_group_leader
    FOREIGN KEY(group_leader_id)
    REFERENCES Users(user_id);

    ALTER TABLE Users_ScoutGroups
    ADD CONSTRAINT fk_user
    FOREIGN KEY(user_id)
    REFERENCES Users(user_id);

    ALTER TABLE Users_ScoutGroups
    ADD CONSTRAINT fk_scout_group
    FOREIGN KEY(scout_group_id)
    REFERENCES ScoutGroups(scout_group_id);
    '''
    # Wykonanie zapytań tworzących tabele
    cur.execute(create_tables)
    cur.execute(create_FK)

    # Zatwierdzenie zmian
    conn.commit()

    # Zamknięcie kursora i połączenia
    cur.close()
    conn.close()
