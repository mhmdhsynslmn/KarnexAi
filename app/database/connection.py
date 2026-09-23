import urllib.parse
import os
import threading

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# SQL Server bilgileri
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_NAME")
# Windows Authentication
DRIVER = "ODBC Driver 17 for SQL Server"


# ============================================================
# ENGINE SINGLETON
# ============================================================
# FIX: Eskiden get_engine() her cagrildiginda create_engine() ile
# sifirdan yeni bir engine/connection pool olusturuluyordu. Tek bir
# chat() istegi icinde birden fazla tool calisirsa (ör. financial_summary
# + top_expense_categories), her biri get_engine() cagirdigi icin
# SQL Server'a defalarca "sicak" pool olmadan yeni fiziksel baglanti
# aciliyordu. Bu, gozle gorulur bir yavasligin ana kaynagiydi.
#
# Cozum: engine'i process basina bir kere olustur, sonraki cagrilarda
# ayni nesneyi don. Boylece connection pool gercekten "isinir" ve
# ardisik sorgular mevcut baglantilari yeniden kullanir.
#
# Thread-safety icin lock kullaniyoruz (ör. bir web sunucusunda ayni
# anda birden fazla istek get_engine()'i ilk kez cagirabilir).

_engine = None
_engine_lock = threading.Lock()


def get_engine():
    global _engine

    if _engine is not None:
        return _engine

    with _engine_lock:
        # Lock alindiktan sonra tekrar kontrol et (double-checked
        # locking): baska bir thread lock'u bizden once alip engine'i
        # olusturmus olabilir.
        if _engine is not None:
            return _engine

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

        _engine = create_engine(
            connection_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            # Uzun sure bos kalan baglantilari geri dondurmeden once
            # SQL Server tarafinda kapatilmis olabilir; pool_recycle
            # bunlari periyodik olarak tazeler.
            pool_recycle=1800
        )

    return _engine


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