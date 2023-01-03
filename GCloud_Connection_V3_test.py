from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import os

credential_path = "X:\Limitless\A - Skeletal Tracking\Keys\service_key_gcloud.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# initialize connector
connector = Connector()

# Python Connector database creator function
def getconn():
        conn = connector.connect(
            "applied-craft-372501:australia-southeast2:imikami-demo-v1", # Cloud SQL Instance Connection Name
            "pg8000",
            user="postgres",
            password="Limitless@96",
            db="postgres",
            enable_iam_auth=True,
            ip_type=IPTypes.PUBLIC # IPTypes.PRIVATE for private IP
        )
        return conn

# create SQLAlchemy connection pool
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
    # get current datetime from database
    results = db_conn.execute("SELECT NOW()").fetchone()

    # output time
    print("Current time: ", results[0])

connector.close()
