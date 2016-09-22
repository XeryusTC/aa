# -*- coding: utf-8 -*-
import yaml
from ics import Calendar, Event

if __name__ == '__main__':
    with open('locations.yaml', 'r') as f:
        loc_doc = yaml.load(f)
    print(loc_doc)
    resources = []
    for room in loc_doc['rooms']:
        for time in loc_doc['times']:
            resources.append({
                'room': room['room'],
                'size': room['size'],
                'start': time['start'],
                'end': time['end']
            })

    cal = Calendar()
    for r in resources:
        e = Event()
        e.name = 'room {} ({})'.format(r['room'], r['size'])
        e.begin = '2016-09-20T{}+00:00'.format(r['start'])
        e.end = '2016-09-20T{}+00:00'.format(r['end'])
        cal.events.append(e)
    print(cal)

    with open('helloworld.ics', 'w') as f:
        f.writelines(cal)
