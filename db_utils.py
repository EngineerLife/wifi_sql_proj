import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.db3')

def create_readings_table(con):
    cur = con.cursor()
    table_command = """
    CREATE TABLE iwscan_readings (
        id integer PRIMARY KEY AUTOINCREMENT,
        channel integer,
        encryption text,
        essid text,
        signal_level_dbm real,
        signal_quality integer,
        signal_total integer,
        mode text,
        mac text
    )"""
    cur.execute(table_command)

def insert_reading(db_con,chan,enc,essid,sig_lvl_dbm,sig_qual,sig_total,mode,mac):
    db_cur = db_con.cursor()
    sql_cmd = """INSERT into iwscan_readings(channel,encryption,essid,signal_level_dbm,signal_quality,signal_total,mode,mac)
    VALUES(?,?,?,?,?,?,?,?) 
    """
    db_cur.execute(sql_cmd,(chan,enc,essid,sig_lvl_dbm,sig_qual,sig_total,mode,mac))
    db_con.commit()

def table_exists(con,table_name):
    cur = con.cursor()
    cur.execute("""SELECT name FROM sqlite_master
                WHERE type='table' AND name='"""+table_name+"'")
    res = cur.fetchall()
    return len(res) == 1

def db_setup():
    con = sqlite3.connect(DEFAULT_PATH);
    if not table_exists(con,str('iwscan_readings')):
        create_readings_table(con)
    return con



