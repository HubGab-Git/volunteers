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

    insert_example_data_query = '''
    -- Wypełnienie tabeli States
    INSERT INTO States (state_name, admin_id) VALUES
    ('California', NULL),
    ('Texas', NULL),
    ('New York', NULL);

    -- Wypełnienie tabeli Regions
    INSERT INTO Regions (region_name, state_id, admin_id) VALUES
    ('Northern California', 1, NULL),
    ('Southern California', 1, NULL),
    ('Central Texas', 2, NULL),
    ('Eastern Texas', 2, NULL),
    ('New York City', 3, NULL),
    ('Upstate New York', 3, NULL);

    -- Wypełnienie tabeli Cities
    INSERT INTO Cities (city_name, region_id, admin_id) VALUES
    ('San Francisco', 1, NULL),
    ('Los Angeles', 2, NULL),
    ('Austin', 3, NULL),
    ('Houston', 4, NULL),
    ('Manhattan', 5, NULL),
    ('Albany', 6, NULL);

    -- Wypełnienie tabeli Users
    INSERT INTO Users (name, email, phone_number, state_id, region_id, city_id, is_admin_state, is_admin_region, is_admin_city, is_superadmin) VALUES
    ('Alice Johnson', 'alice@example.com', '555-1234', 1, 1, 1, TRUE, FALSE, FALSE, FALSE),
    ('Bob Smith', 'bob@example.com', '555-5678', 1, 2, 2, FALSE, TRUE, FALSE, FALSE),
    ('Charlie Brown', 'charlie@example.com', '555-8765', 2, 3, 3, FALSE, FALSE, TRUE, FALSE),
    ('Diana Prince', 'diana@example.com', '555-4321', 3, 5, 5, FALSE, FALSE, FALSE, TRUE);

    -- Aktualizacja tabeli States z adminami
    UPDATE States SET admin_id = (SELECT user_id FROM Users WHERE name = 'Alice Johnson') WHERE state_name = 'California';
    UPDATE States SET admin_id = (SELECT user_id FROM Users WHERE name = 'Charlie Brown') WHERE state_name = 'Texas';
    UPDATE States SET admin_id = (SELECT user_id FROM Users WHERE name = 'Diana Prince') WHERE state_name = 'New York';

    -- Aktualizacja tabeli Regions z adminami
    UPDATE Regions SET admin_id = (SELECT user_id FROM Users WHERE name = 'Bob Smith') WHERE region_name = 'Southern California';

    -- Aktualizacja tabeli Cities z adminami
    UPDATE Cities SET admin_id = (SELECT user_id FROM Users WHERE name = 'Charlie Brown') WHERE city_name = 'Austin';

    -- Wypełnienie tabeli ScoutGroups
    INSERT INTO ScoutGroups (group_name, group_leader_id) VALUES
    ('Scout Group 1', (SELECT user_id FROM Users WHERE name = 'Alice Johnson')),
    ('Scout Group 2', (SELECT user_id FROM Users WHERE name = 'Bob Smith'));

    -- Wypełnienie tabeli Users_ScoutGroups
    INSERT INTO Users_ScoutGroups (user_id, scout_group_id) VALUES
    ((SELECT user_id FROM Users WHERE name = 'Charlie Brown'), 1),
    ((SELECT user_id FROM Users WHERE name = 'Diana Prince'), 2);
    '''
    # Wykonanie zapytań tworzących tabele
    cur.execute(insert_example_data_query)
    logger.info("Insert executed")
    # Zatwierdzenie zmian
    conn.commit()
    logger.info("Commited")
    # Zamknięcie kursora i połączenia
    cur.close()
    conn.close()
    logger.info("Connection to database closed")
