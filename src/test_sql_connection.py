
import pyodbc

SERVER = r".\SQLEXPRESS"
DATABASE = "ShopFlowDB"

available_drivers = pyodbc.drivers()

if "ODBC Driver 18 for SQL Server" in available_drivers:
    driver = "ODBC Driver 18 for SQL Server"
elif "ODBC Driver 17 for SQL Server" in available_drivers:
    driver = "ODBC Driver 17 for SQL Server"
else:
    raise RuntimeError(
        "Aucun pilote ODBC SQL Server 17 ou 18 detecte."
    )

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

try:
    with pyodbc.connect(
        connection_string,
        timeout=10
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DB_NAME(), @@SERVERNAME"
        )
        database_name, server_name = cursor.fetchone()

        print("Connexion SQL Server reussie !")
        print(f"Pilote : {driver}")
        print(f"Base : {database_name}")
        print(f"Serveur : {server_name}")

except pyodbc.Error as error:
    print("Erreur de connexion SQL Server.")
    print(error)
    raise
