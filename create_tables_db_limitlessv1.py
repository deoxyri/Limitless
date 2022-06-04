# DATABASE
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection("limitless_v1", "postgres", "Limitless@96", "127.0.0.1", "5432")


# FUNCTION TO EXECUTE QUERIES
def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


joints_description = ['head', 'neck', 'torso', 'waist', 'left_collar', 'left_shoulder', 'left_elbow',
                      'left_wrist', 'left_hand', 'right_collar', 'right_shoulder',
                      'right_elbow', 'right_wrist', 'right_hand', 'left_hip', 'left_knee', 'left_ankle',
                      'right_hip', 'right_knee', 'right_ankle']

# -----------------------------------------------------------------------------------
# LOOP ALL TABLES TO BE CREATED IN DATABASE
i = 0
while i < len(joints_description):
    create_table = """
     CREATE TABLE IF NOT EXISTS {}_data (
     id SERIAL PRIMARY KEY,
     x_location REAL,
     y_location REAL,
     depth REAL
    )
    """.format(joints_description[i])
    execute_query(connection, create_table)
    i += 1
