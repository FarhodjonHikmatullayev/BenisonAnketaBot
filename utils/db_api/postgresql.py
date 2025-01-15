from datetime import datetime, timedelta
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from data.config import DEVELOPMENT_MODE


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        print('DEVELOPMENT_MODE', DEVELOPMENT_MODE)
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
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

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # for users
    async def create_user(self, username, telegram_id, full_name):
        sql = "INSERT INTO Users (username, telegram_id, full_name, language, joined_at, role) VALUES($1, $2, $3, $4, $5, $6) returning *"
        language = "uzb"
        joined_at = datetime.now() + timedelta(hours=5)
        role = 'user'
        return await self.execute(sql, username, telegram_id, full_name, language, joined_at, role, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_user(self, user_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE Users SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), user_id, fetchrow=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM Users WHERE id = $1 RETURNING *"
        return await self.execute(sql, user_id, fetchrow=True)

    # for branches
    # async def create_branch(self, title, region):
    #     sql = "INSERT INTO branch (title, region, created_at) VALUES($1, $2, $3) RETURNING *"
    #     created_at = datetime.now() + timedelta(hours=5)
    #     return await self.execute(sql, title, region, created_at, fetchrow=True)

    async def select_all_branches(self):
        sql = "SELECT * FROM branch"
        return await self.execute(sql, fetch=True)

    async def select_branch(self, **kwargs):
        sql = "SELECT * FROM branch WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_branch(self, branch_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE branch SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), branch_id, fetchrow=True)

    async def delete_branch(self, branch_id):
        sql = "DELETE FROM branch WHERE id = $1 RETURNING *"
        return await self.execute(sql, branch_id, fetchrow=True)

    # for vacancies
    async def create_vacancy(self, title, category_id, photo, branch_id, requirements, responsibility,
                             working_condition, schedule, description):
        sql = """
        INSERT INTO vacancy (title, category_id, photo, branch, requirements, responsibility, 
                             working_condition, schedule, description, created_at) 
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) 
        RETURNING *
        """
        created_at = datetime.now() + timedelta(hours=5)
        return await self.execute(sql, title, category_id, photo, branch_id, requirements, responsibility,
                                  working_condition, schedule, description, created_at, fetchrow=True)

    async def select_all_vacancies(self):
        sql = "SELECT * FROM vacancy"
        return await self.execute(sql, fetch=True)

    async def select_vacancy(self, **kwargs):
        sql = "SELECT * FROM vacancy WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_vacancy(self, vacancy_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE vacancy SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), vacancy_id, fetchrow=True)

    async def delete_vacancy(self, vacancy_id):
        sql = "DELETE FROM vacancy WHERE id = $1 RETURNING *"
        return await self.execute(sql, vacancy_id, fetchrow=True)

    # for resumes
    # region
    # category
    # branch
    # vacancy
    async def create_resume(self, region_id, category_id, branch_id, vacancy_id, first_name, last_name, fathers_name,
                            gender,
                            date_of_birth,
                            location, phone, email, username, marital_status, is_student,
                            education_form, education_level, uzb_language_level,
                            rus_language_level, computer_level, expected_salary,
                            photo, source_about_vacancy, agreement, user_id):
        sql = """
        INSERT INTO resume (region_id, category_id, branch_id, vacancy_id, first_name, last_name, fathers_name, gender, date_of_birth,
                            location, phone, email, username, marital_status, is_student,
                            education_form, education_level, uzb_language_level,
                            rus_language_level, computer_level, expected_salary,
                            photo, source_about_vacancy, agreement, user_id, created_at) 
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26) 
        RETURNING *
        """
        created_at = datetime.now() + timedelta(hours=5)
        return await self.execute(sql, region_id, category_id, branch_id, vacancy_id, first_name, last_name,
                                  fathers_name,
                                  gender, date_of_birth,
                                  location, phone, email, username, marital_status, is_student,
                                  education_form, education_level, uzb_language_level,
                                  rus_language_level, computer_level, expected_salary,
                                  photo, source_about_vacancy, agreement, user_id, created_at, fetchrow=True)

    async def select_all_resumes(self):
        sql = "SELECT * FROM resume"
        return await self.execute(sql, fetch=True)

    async def select_resume(self, **kwargs):
        sql = "SELECT * FROM resume WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_resume(self, resume_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE resume SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), resume_id, fetchrow=True)

    async def delete_resume(self, resume_id):
        sql = "DELETE FROM resume WHERE id = $1 RETURNING *"
        return await self.execute(sql, resume_id, fetchrow=True)

    # for regions
    async def create_region(self, name):
        sql = """
        INSERT INTO region (name, created_at) 
        VALUES($1, $2) 
        RETURNING *
        """
        created_at = datetime.now() + timedelta(hours=5)
        return await self.execute(sql, name, created_at, fetchrow=True)

    async def select_all_regions(self):
        sql = "SELECT * FROM region"
        return await self.execute(sql, fetch=True)

    async def select_region(self, **kwargs):
        sql = "SELECT * FROM region WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_region(self, region_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE region SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), region_id, fetchrow=True)

    async def delete_region(self, region_id):
        sql = "DELETE FROM region WHERE id = $1 RETURNING *"
        return await self.execute(sql, region_id, fetchrow=True)

    # for categories

    async def select_all_categories(self):
        sql = "SELECT * FROM category"
        return await self.execute(sql, fetch=True)

    async def select_category(self, **kwargs):
        sql = "SELECT * FROM category WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_category(self, category_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE category SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), category_id, fetchrow=True)

    async def delete_category(self, category_id):
        sql = "DELETE FROM category WHERE id = $1 RETURNING *"
        return await self.execute(sql, category_id, fetchrow=True)
