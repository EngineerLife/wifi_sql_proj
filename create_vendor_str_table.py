import db_utils
import re

def parse_vendor_bytes(mac):
    # converts 'AB:CD:EF:XX:XX:XX' to 'ABCDEF'
    reg_exp = '(..):(..):(..):(..):(..):(..)'
    x = re.search(reg_exp, mac)
    res = f'{x.group(1)}{x.group(2)}{x.group(3)}'
    return res


if __name__ == '__main__':
    db_con = db_utils.db_setup()
    
    # check if it already exists or create it
    if not db_utils.table_exists(db_con,'mac_vendor_str'):
        db_utils.create_mac_vendor_table(db_con)
    
    #print(db_utils.get_unique_macs(db_con))
    for unique_mac in db_utils.get_unique_macs(db_con):
        vendor_bytes = parse_vendor_bytes(unique_mac[0])
        matching_entry_ids = db_utils.find_oui_lookup_foreign_keys(db_con,vendor_bytes)
        #print(matching_entry_ids)
        for match_id in matching_entry_ids:
            #print(match_id)
            db_utils.add_vendor_str_table_entry(db_con,unique_mac[0],match_id[0])
        
        #break
        # for each unique_mac, vendor string insert row
    db_con.commit()
        