#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml

class Room:
    def __init__(self, name, size, beamer, start_time, end_time):
        self.name = name
        self.size = size
        self.beamer = beamer
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return '{} (seats {}|beamers {}) {:0>2}:00:00-{:0>2}:00:00'.format(
                self.name, self.size, self.beamer, self.start_time, self.end_time)

    def get_size(self):
        return self.size
    
    def get_beamer(self):
        return self.beamer
                   
def load_rooms(filename):
    with open(filename, 'r') as f:
        room_doc = yaml.load(f)

    available_rooms = []
    for room in room_doc['rooms']:
        for time in room_doc['times']:
            r = Room((room['room']), room['size'], room['beamer'], time['start'], time['end'])
            available_rooms.append(r)
    return available_rooms

if __name__ == '__main__':
    print('Testing room loading')
    rooms = load_rooms('locations.yaml')
    for room in rooms:
        print(room)
