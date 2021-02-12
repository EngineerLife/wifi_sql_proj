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

def create_mac_vendor_table(con):
    cur = con.cursor()
    table_command = """
    CREATE TABLE mac_vendor_str (
        id integer PRIMARY KEY AUTOINCREMENT,
        mac_full text,
        oui_lookup_entry_id integer,
        FOREIGN KEY (oui_lookup_entry_id) REFERENCES oui_lookup(entry_id)
    )"""
    cur.execute(table_command)

def get_unique_macs(con):
    cur = con.cursor()
    cur.execute("""SELECT DISTINCT mac FROM iwscan_readings""")
    res = cur.fetchall()
    return res

def find_oui_lookup_foreign_keys(db_con,vendor_bytes):
    cur = db_con.cursor()
    cur.execute("""SELECT entry_id FROM oui_lookup WHERE mac=?""",(vendor_bytes,))
    res = cur.fetchall()
    return res

def add_vendor_str_table_entry(db_con,unique_mac,matching_entry_id):
    db_cur = db_con.cursor()
    sql_cmd = """INSERT into mac_vendor_str(mac_full,oui_lookup_entry_id)
    VALUES(?,?) 
    """
    #print((unique_mac,vendor_bytes,matching_entry_id))
    db_cur.execute(sql_cmd,(unique_mac,matching_entry_id))

def insert_reading(db_con,chan,enc,essid,sig_lvl_dbm,sig_qual,sig_total,mode,mac):
    db_cur = db_con.cursor()
    sql_cmd = """INSERT into iwscan_readings(channel,encryption,essid,signal_level_dbm,signal_quality,signal_total,mode,mac)
    VALUES(?,?,?,?,?,?,?,?) 
    """
    db_cur.execute(sql_cmd,(chan,enc,essid,sig_lvl_dbm,sig_qual,sig_total,mode,mac))
    #db_con.commit()

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



