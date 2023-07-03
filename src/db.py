import math
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def convert_to_dict(datas: list, keys: str):
    list_dict = []
    if datas and keys:
        for row in datas:
            convert = {}
            for index, value in enumerate(row):
                convert.update({keys[index]: value})
            list_dict.append(convert)
    return list_dict


class Database():
    def __init__ (self):
        self.conn = None
        self.HOST = os.getenv('HOST')
        self.USER = os.getenv('USERDB')
        self.PASSWORD = os.getenv('PASSWORD')
        self.DBNAME = os.getenv('DBNAME')
        self.SSLMODE = os.getenv('SSLMODE')

    def connect(self) -> None:
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.HOST,
                    user=self.USER,
                    password=self.PASSWORD,
                    dbname=self.DBNAME,
                )
            except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
                print('\t ERROR! -> ' + str(error))
                return False
            return True


    def select(self, query: str) -> list:
        if self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(query)
                    response = cur.fetchall()
                    cur.close()
                except:
                    print('\t ! -> Erro ao selecionar dados')
                return response

    def insert(self, query: str) -> None:
        with self.conn.cursor() as cur:
            try:
                cur.execute(query)
                print('\tINSERT INTO successfully')
                self.conn.commit()
            except:
                print('\t ! -> Values incorrect to insert db. Please, review the validations')
            cur.close()

    def delete(self, query: str) -> None:
        with self.conn.cursor() as cur:
            try:
                cur.execute(query)
                print('\tDELETE successfully')
                self.conn.commit()
            except:
                print('\t ! -> Values incorrect to delete db. Please, review the validations')
            cur.close()


    def update(self, query: str) -> None:
        pass

    def disconnect(self) -> None:
        connection = self.conn
        connection.close()
