create_table = """create table if not exists companies (c_id integer PRIMARY KEY, c_name text not null, c_legent text, c_employed integer, c_shacap integer)"""

select_stm = """select * from {}"""

update_row = """update {} set {} = {} where c_id = {}"""

insert_company = """insert into companies values ({})"""
