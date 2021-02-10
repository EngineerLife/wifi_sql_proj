import db_utils
from time import sleep
import iwlist
import datetime

def parse_reading(reading):
    chan = reading.get('channel')
    enc = reading.get('encryption')
    essid = reading['essid']
    sig_lvl_dbm = reading['signal_level_dBm']
    sig_qual = reading['signal_quality']
    sig_total = reading['signal_total']
    mode = reading['mode']
    mac = reading['mac']
    return (chan,enc,essid,sig_lvl_dbm,sig_qual,sig_total,mode,mac)

seconds_to_collect = 60

if __name__ == '__main__':
    db_con = db_utils.db_setup()
    last_commit = datetime.datetime.now()
    for i in range(0,int(seconds_to_collect/5)):
        time_start = datetime.datetime.now()
        content = iwlist.scan(interface='wlp4s0')
        cells = iwlist.parse(content)
        # add to db
        for k in range(0,len(cells)):
            reading = cells[k]
            (chan,enc,essid,sig_lvl_dbm,sig_qual,sig_total,mode,mac) = parse_reading(reading)
            db_utils.insert_reading(db_con,chan,enc,essid,sig_lvl_dbm,sig_qual,sig_total,mode,mac)
            #{'cellnumber': '01', 'mac': 'F0:72:EA:32:9B:E5', 'signal_quality': '68', 'signal_total': '70', 'signal_level_dBm': '-42', 'encryption': 'wpa2', 'essid': 'Echo', 'mode': 'Master'}
            #chan = 
            #print(reading)
        time_end = datetime.datetime.now()
        time_diff = (time_end - time_start)
        exec_time = time_diff.total_seconds()
        print(exec_time)
        sleep(5-exec_time)
    db_con.commit()
        