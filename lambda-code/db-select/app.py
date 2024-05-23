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

    select_users_query = '''
    SELECT
        u.name AS "Name",
        u.email AS "Email",
        s.state_name AS "State",
        r.region_name AS "Region",
        c.city_name AS "City",
        (SELECT u1.name FROM Users u1 WHERE u1.user_id = s.admin_id) AS "Admin of State",
        (SELECT u2.name FROM Users u2 WHERE u2.user_id = r.admin_id) AS "Admin of Region",
        (SELECT u3.name FROM Users u3 WHERE u3.user_id = c.admin_id) AS "Admin of City",
        CASE WHEN u.is_superadmin THEN 'Yes' ELSE 'No' END AS "Superadmin",
        u.phone_number AS "Phone Number"
    FROM
        Users u
    LEFT JOIN
        States s ON u.state_id = s.state_id
    LEFT JOIN
        Regions r ON u.region_id = r.region_id
    LEFT JOIN
        Cities c ON u.city_id = c.city_id;
    '''

    cur.execute(select_users_query)
    results1 = cur.fetchall()

    print("Query 1 Results:")
    for row in results1:
        print(row)
    
    # Zapytanie 2: Wyświetlanie informacji o grupach skautów i ich liderach
    query2 = """
    SELECT
        u.name AS "Name",
        (SELECT u1.name FROM Users u1 WHERE u1.user_id = sg.group_leader_id) AS "Scout Group Leader",
        sg.group_name AS "Own Scout Group"
    FROM
        Users u
    LEFT JOIN
        Users_ScoutGroups usg ON u.user_id = usg.user_id
    LEFT JOIN
        ScoutGroups sg ON usg.scout_group_id = sg.scout_group_id;
    """

    # Wykonanie zapytania 2
    cur.execute(query2)
    results2 = cur.fetchall()

    # Wyświetlenie wyników zapytania 2
    print("\nQuery 2 Results:")
    for row in results2:
        print(row)

    # Zamknięcie kursora i połączenia
    cur.close()
    conn.close()
