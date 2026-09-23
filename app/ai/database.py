import os
import pyodbc
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Veritabanı bilgileri
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")


def get_connection():
    """
    Kârnex MSSQL veritabanına Windows Authentication
    kullanarak bağlantı oluşturur.
    """

    if not DB_SERVER:
        raise ValueError("DB_SERVER .env dosyasında bulunamadı.")

    if not DB_NAME:
        raise ValueError("DB_NAME .env dosyasında bulunamadı.")

    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    try:
        connection = pyodbc.connect(connection_string)
        return connection

    except pyodbc.Error as e:
        print("MSSQL bağlantı hatası:")
        print(e)
        raise


def test_connection():
    """
    Veritabanı bağlantısını test eder.
    """

    try:
        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT DB_NAME()")

        database_name = cursor.fetchone()[0]

        print("MSSQL bağlantısı başarılı!")
        print(f"Bağlanılan veritabanı: {database_name}")

        cursor.close()
        connection.close()

        return True

    except Exception as e:
        print("Veritabanı bağlantısı başarısız!")
        print(e)

        return False


if __name__ == "__main__":
    test_connection()