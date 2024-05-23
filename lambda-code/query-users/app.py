from logging import getLogger
from psycopg2 import connect
from os import environ
from json import loads,dumps
from boto3 import client
from botocore.exceptions import ClientError

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
    results = cur.fetchall()

    # Convert the results to a list of dictionaries
    data = [
        {
            "Name": row[0],
            "Email": row[1],
            "State": row[2],
            "Region": row[3],
            "City": row[4],
            "Admin of State": row[5],
            "Admin of Region": row[6],
            "Admin of City": row[7],
            "Superadmin": row[8],
            "Phone Number": row[9]
        }
        for row in results
    ]

    # Return the data as a JSON response
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        },
        "body": dumps(data)
    }