from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id BIGINT NOT NULL PRIMARY KEY,
        first_name varchar(50) NOT NULL,
        last_name varchar(50) NOT NULL,
        contact varchar(20) NOT NULL,
        birthday DATE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_hisobot(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Hisobot (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        sana DATE NOT NULL,
        zayafka NUMERIC,
        gaplashilgan NUMERIC, 
        sotilgan NUMERIC,
        tel_tushmagan NUMERIC,
        xato_nomer NUMERIC,
        berma_adash NUMERIC,
        otkaz NUMERIC,
        naqt NUMERIC,
        click NUMERIC,
        boshqacha_tolov NUMERIC,
        maxsus_narx NUMERIC,
        ehson NUMERIC,
        sotilgan2 NUMERIC,
        mijozlar NUMERIC,
        summa NUMERIC      
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, id, first_name, last_name, contact, birthday:str=None):
        sql = "INSERT INTO Users (id, first_name, last_name, contact, birthday) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, id, first_name, last_name, contact, birthday, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def add_hisobot(self,user_id,sana, zayafka,gaplashilgan,sotilgan,tel_tushmagan: int,
                          xato_nomer: int,berma_adash: int,otkaz: int, naqt: int,click: int,
                          boshqacha_tolov: int, maxsus_narx: int,ehson: int,sotilgan2: int,
                            mijozlar: int,summa: int):
        sql = """
        INSERT INTO Hisobot(user_id, sana, zayafka, gaplashilgan, sotilgan, tel_tushmagan, 
        xato_nomer, berma_adash, otkaz, naqt, click, boshqacha_tolov, maxsus_narx, ehson, sotilgan2, mijozlar, summa)
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17) returning *
        """
        return await self.execute(sql,
                                  user_id, sana, zayafka, gaplashilgan, sotilgan, tel_tushmagan, xato_nomer,
                                  berma_adash, otkaz, naqt, click, boshqacha_tolov, maxsus_narx, ehson, sotilgan2,
                                  mijozlar, summa, fetchrow=True)

    async def delete_hisobot(self, id):
        sql = "DELETE FROM Hisobot WHERE id=$1"
        await self.execute(sql,id,execute=True)

    async def count_hisobot(self):
        sql = "SELECT COUNT(*) FROM Hisobot;"
        return await self.execute(sql,fetchval=True)

    async def select_days_hisobot(self, **kwargs):
        sql = "SELECT * FROM Hisobot WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    #sanalar orasidagi hisobotlar maulotlarini olish uchun
    #hafta va oylik uchun ishlaydi
    async def select_between_hisobot(self,user_id, sana1, sana2):
        sql = """SELECT
        user_id,
        SUM(zayafka) ,
        SUM(gaplashilgan) ,
        SUM(sotilgan) ,
        SUM(tel_tushmagan) ,
        SUM(xato_nomer),
        SUM(berma_adash) ,
        SUM(otkaz) ,
        sum(naqt) ,
        sum(click),
        sum(boshqacha_tolov) ,
        sum(maxsus_narx) ,
        sum(ehson) ,
        sum(sotilgan2) ,
        sum(mijozlar) ,
        sum(summa) as summa
        FROM hisobot WHERE user_id=$1 AND sana BETWEEN $2 AND $3 GROUP BY user_id;
        """
        return await self.execute(sql,user_id, sana1, sana2, fetchrow=True)

    async def select_all_between_hisobot(self, sana1, sana2):
        sql = """SELECT
        sum(zayafka) as zayafka,
        sum(gaplashilgan) as gaplashilgan,
        sum(sotilgan) as sotilgan,
        sum(tel_tushmagan) as tel_tushmagan,
        sum(xato_nomer) as xato_nomer,
        sum(berma_adash) as berma_adash,
        sum(otkaz) as  otkaz,
        sum(naqt) as naqt,
        sum(click) as click,
        sum(boshqacha_tolov) as boshqacha_tolov,
        sum(maxsus_narx) as maxsus_narx,
        sum(ehson) as ehson,
        sum(sotilgan2) as sotilgan2,
        sum(mijozlar) as mijozlar,
        sum(summa) as summa
        FROM Hisobot WHERE sana BETWEEN $1 AND $2 
        """
        return await self.execute(sql,sana1, sana2,fetchrow=True)

    async def select_group_by_between_hisobot(self, sana1, sana2):
        sql = """SELECT
        user_id,
        sum(zayafka) as zayafka,
        sum(gaplashilgan) as gaplashilgan,
        sum(sotilgan) as sotilgan,
        sum(tel_tushmagan) as tel_tushmagan,
        sum(xato_nomer) as xato_nomer,
        sum(berma_adash) as berma_adash,
        sum(otkaz) as  otkaz,
        sum(naqt) as naqt,
        sum(click) as click,
        sum(boshqacha_tolov) as boshqacha_tolov,
        sum(maxsus_narx) as maxsus_narx,
        sum(ehson) as ehson,
        sum(sotilgan2) as sotilgan2,
        sum(mijozlar) as mijozlar,
        sum(summa) as summa
        FROM Hisobot WHERE sana BETWEEN $1 AND $2 GROUP BY user_id;
        """
        return await self.execute(sql,sana1, sana2,fetch=True)


    async def st_gaplashilgan(self):
        sql = "SELECT user_id, SUM(gaplashilgan) as gaplashilgan FROM Hisobot GROUP BY user_id ORDER BY SUM(gaplashilgan) DESC"
        return  await self.execute(sql,fetch=True)

    async def st_sotilgan(self):
        sql= "SELECT user_id, SUM(sotilgan) as sotilgan FROM Hisobot GROUP BY user_id ORDER BY SUM(sotilgan) DESC"
        return await self.execute(sql,fetch=True)