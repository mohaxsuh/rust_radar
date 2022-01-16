#!/usr/bin/python3
# -*- coiding: utf-8 -*-

import sqlite3
import datetime

from config import SEED, SIZE

def create_db():

    CONN = sqlite3.connect('tracer_{}_{}.sqlite'.format(SEED, SIZE))
    CURS = CONN.cursor()
    CURS.execute('''
        CREATE TABLE t_journal (
            i_id integer not null primary key autoincrement,
            f_steamid	text,
            f_nic	    text,
            f_ipaddr	text,
            f_pos_x 	integer,
            f_pos_y 	integer,
            f_time_pos  text
        );
    ''' )

    CONN.commit()
    CONN.close()
    return True

def save_position(player):
    
    CONN = sqlite3.connect('tracer_{}_{}.sqlite'.format(SEED, SIZE))
    CURS = CONN.cursor()
    CURS.execute('''
        INSERT INTO t_journal(f_steamid,
                              f_nic,
                              f_ipaddr,
                              f_pos_x,
                              f_pos_y,
                              f_time_pos
                            )
        VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'));
    ''', (player.steamid, player.nic, player.addr, player.x, player.y))
    CONN.commit()
    CONN.close()
    return True
    
def load_last_point(player):

    CONN = sqlite3.connect('tracer_{}_{}.sqlite'.format(SEED, SIZE))
    CURS = CONN.cursor()
    CURS.execute('''
        SELECT  f_pos_x,
                f_pos_y
        FROM    t_journal 
        WHERE   f_steamid = ?
        ORDER BY f_time_pos DESC
        LIMIT 1;
    ''', (player.steamid, ))
    result = CURS.fetchone()
    CONN.close()
    return tuple(result) if result else tuple()

def load_full_tracks():

    result = {}
    CONN = sqlite3.connect('tracer_{}_{}.sqlite'.format(SEED, SIZE))
    CURS = CONN.cursor()
    CURS.execute('''SELECT DISTINCT f_steamid FROM t_journal;''')
    players = {}
    for steamid, in CURS:
        players[steamid] = None
    for steamid in players:
        CURS.execute('''
            SELECT f_nic 
            FROM t_journal 
            WHERE f_steamid = ? 
                AND f_time_pos = (SELECT max(f_time_pos) 
                                  FROM t_journal 
                                  WHERE f_steamid = ?
                                  );
            ''', (steamid, steamid))
        last_name,  = CURS.fetchone()
        players[steamid] = last_name
    for steamis, nic in players.items():
        CURS.execute('''
            SELECT f_pos_x, f_pos_y, f_time_pos
            FROM t_journal 
            WHERE f_steamid = ?
                ORDER BY f_time_pos ASC;
            ''', (steamis, ))
        steps = []
        for x, y, tick in CURS:
            steps.append((x, y, datetime.datetime.strptime(tick, '%Y-%m-%d %H:%M:%S')))
        result[(steamis, nic)] = steps
    CONN.close()
    return result