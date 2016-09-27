#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml

class Course:
    def __init__(self, name, size):
        self._name = name
        self._size = size

    def get_size(self):
        return self._size
                   
def load_courses(filename):
    with open(filename, 'r') as f:
        room_doc = yaml.load(f)

    courses = []
    for course in room_doc['rooms']:
        for time in room_doc['times']:
            r = Room(room['room'], room['size'], time['start'], time['end'])
            available_rooms.append(r)
    return available_rooms

if __name__ == '__main__':
    print('Testing room loading')
    rooms = load_rooms('locations.yaml')
    for room in rooms:
        print(room)
