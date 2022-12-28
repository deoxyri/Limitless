from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import os

# from google.colab import auth
# auth.authenticate_user()

credential_path = "X:\Limitless\A - Skeletal Tracking\Tracking Programs\service_key_gcloud.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# Python Connector database creator function
def getconn():
    with Connector() as connector:
        conn = connector.connect(
            "applied-craft-372501:australia-southeast2:imikami-demo-v1", # Cloud SQL Instance Connection Name
            "pg8000",
            user="root",
            password="Limitless@96",
            db="postgres",
            ip_type=IPTypes.PUBLIC # IPTypes.PRIVATE for private IP
        )
    return conn

# create SQLAlchemy connection pool
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

getconn()

# interact with Cloud SQL database using connection pool
# with pool.connect() as db_conn:
#     # query database
#     result = db_conn.execute("SELECT * from my_table").fetchall()
#
#     # Do something with the results
#     for row in result:
#         print(row)