from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
import pg8000
import os
# ----------------------------------------------------------------------------------------------------------------------
# config = {
#     'user': 'root',
#     'password': 'Limitless@96',
#     'host': '34.129.78.3',
#     'client_flags': [ClientFlag.SSL],
#     'ssl_ca': 'ssl/server-ca.pem',
#     'ssl_cert': 'ssl/client-cert.pem',
#     'ssl_key': 'ssl/client-key.pem'
# }
# ----------------------------------------------------------------------------------------------------------------------
# connect_with_connector initializes a connection pool for a
# Cloud SQL instance of Postgres using the Cloud SQL Python Connector.
def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ["applied-craft-372501:australia-southeast2:imikami-demo-v1"]  # e.g. 'project:region:instance'
    db_user = os.environ["root"]  # e.g. 'my-db-user'
    db_pass = os.environ["Limitless@96"]  # e.g. 'my-db-password'
    db_name = os.environ["postgres"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool

connect_with_connector()