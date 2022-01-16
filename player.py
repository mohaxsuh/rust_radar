#!/usr/bin/python3
# -*- coiding: utf-8 -*-

class Player(object):
    
    def __init__(self, nic, steamid, addr, con_time, x, y):
        self.__Nic = nic
        self.__Steamid = steamid
        self.__Addr = addr
        self.__Con_time = con_time
        self.__X = x
        self.__Y = y
    
    nic = property(lambda self: self.__Nic)
    steamid = property(lambda self: self.__Steamid)
    addr = property(lambda self: self.__Addr)
    con_time = property(lambda self: self__Con_time)
    x = property(lambda self: int(self.__X))
    y = property(lambda self: int(self.__Y))
    
    @x.setter
    def x (self, value):
        self.__X = value
    
    @y.setter
    def y(self, value):
        self.__Y = value
    
    @nic.setter
    def nic(self, value):
        self.__Nic = value
    
    @addr.setter
    def addr(self, value):
        self.__Addr = value
    
    @con_time.setter
    def con_time(self, value):
        self.__Con_time = value
