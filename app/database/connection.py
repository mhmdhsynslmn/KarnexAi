import urllib.parse
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()
# SQL Server bilgileri
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_NAME")
# Windows Authentication
DRIVER = "ODBC Driver 17 for SQL Server"


def get_engine():
    connection_string = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    connection_url = (
        "mssql+pyodbc:///?odbc_connect="
        + urllib.parse.quote_plus(connection_string)
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True
    )


def test_connection():
    engine = get_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

            print("MSSQL bağlantısı başarılı.")
            print("Test sonucu:", value)

            return True

    except Exception as e:
        print("MSSQL bağlantı hatası:")
        print(e)

        return False