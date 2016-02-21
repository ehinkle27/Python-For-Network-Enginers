import Exscript.util.file as euf
import Exscript.util.start as eus
import Exscript.util.match as eum
import pysvn
import os
import time
import datetime

hosts = euf.get_hosts_from_file('c:\\network_configs\\hosts.txt')
accounts = euf.get_accounts_from_file('c:\\network_configs\\accounts.cfg')

def dump_config(job, host, conn):
    """Connect to device, trim config file a bit, write to file"""
    conn.execute('term len 0')
    conn.execute('show run')
    #get the actual hostname of the device
    hostname = eum.first_match(conn, r'^hostname\s(.+)$')
    cfg_file = 'c:\\network_configs\\' + hostname.strip() + '.cfg'
    config = conn.response.splitlines()
    # a little cleanup
    for i in range(3):
        config.pop(i)
    config.pop(-0)
    config.pop(-1)
    # write config to file
    with open(cfg_file, 'w') as f:
        for line in config:
            f.write(line +'\n')
eus.start(accounts, hosts, dump_config, max_threads=2)
