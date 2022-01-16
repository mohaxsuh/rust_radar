#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import re

from config import AUTH
from helpers import dialog
# from alternative import dialog
from player import Player


def player_info(game_pool=None, idnt=1001):

    playerlist = 'playerlist'
    printpos = 'printpos {}'

    if not game_pool:
        result = []
    else:
        result = game_pool

    crop = dialog(playerlist, AUTH)
    # print(crop)
    players = json.loads(crop)
    for plyr in players:
        # print(plyr)
        player_id = plyr['SteamID']
        pos = dialog(printpos.format(plyr['SteamID']), AUTH, identifier=idnt)
        pos_x, pos_z, pos_y = eval(pos)
        # print(player)
        for p in result:
            if p.steamid == player_id:
                # nic, steamid, addr, con_time, x, y
                p.nic = plyr['DisplayName']
                p.addr = plyr['Address']
                p.con_time = plyr['ConnectedSeconds']
                p.x, p.y = pos_x, pos_y
                break
        else:
            gamer = Player(plyr['DisplayName'], plyr['SteamID'], 
                           plyr['Address'], plyr['ConnectedSeconds'], 
                           pos_x, pos_y)
            result.append(gamer)

    return result

def airdrop_info(idnt=1011):
    
    Result = []
    snoop = re.compile( 'supply_drop\s\(([\-\d.]+),\s([\-\d.]+),\s([\-\d.]+)\)' )
    getpos_airdrops = 'entity.find_entity supply_drop'
    crop = dialog(getpos_airdrops, AUTH, identifier=idnt)
    lines_crop = crop.split('\r\n')
    # print(lines_crop)
    for line in lines_crop:
        ore = snoop.search(line)
        if ore:
            # print(ore.groups())
            point = ore.groups()
            x = float(point[0])
            y = float(point[2])
            Result.append((x,y))
    return Result

def patrolhelicopter_info(idnt=1021):
    
    Result = []
    snoop = re.compile( '\spatrolhelicopter\s+\(([\-\d.]+),\s([\-\d.]+),\s([\-\d.]+)\)' )
    getpos_airdrops = 'entity.find_entity patrolhelicopter'
    crop = dialog(getpos_airdrops, AUTH, identifier=idnt)
    lines_crop = crop.split('\r\n')
    # print(lines_crop)
    for line in lines_crop:
        ore = snoop.search(line)
        if ore:
            # print(ore.groups())
            point = ore.groups()
            x = float(point[0])
            y = float(point[2])
            Result.append((x,y))
    return Result

if __name__ == '__main__':

    # situation = player_info()
    # if situation:
        # print(situation)
    airdrop_info()
