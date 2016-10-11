# -*- coding: utf-8 -*-
from string import Template
from rooms import Days

class Schedule:
    def __init__(self):
        self.days = {
            Days.MONDAY: {},
            Days.TUESDAY: {},
            Days.WEDNESDAY: {},
            Days.THURSDAY: {},
            Days.FRIDAY: {},
        }

    def add(self, room, course):
        if room.start_time not in self.days[room.day].keys():
            self.days[room.day][room.start_time] = []

        self.days[room.day][room.start_time].append({
            'room': room.name,
            'course': course,
        })

    def as_plain(self):
        out = ""
        for day in Days:
            out = out + '\n' + str(day);
            for time in sorted(self.days[day]):
                out = "{}\n    {}:00:00".format(out, time)
                for course in self.days[day][time]:
                    out = "{}\n        {}".format(out, course['course'].name)
        return out

    def as_tex(self):
        # Find the number of columns per day and in total
        width = {}
        for day in Days:
            if day not in width.keys():
                width[day] = 1
            for time in self.days[day]:
                if len(self.days[day][time]) > width[day]:
                    width[day] = len(self.days[day][time])
        total_width = sum(width[day] for day in Days)

        # Find the timeslots
        times = set()
        for day in Days:
            for time in self.days[day]:
                times.add(time)
        times = sorted(list(times))

        # Start the table
        out = start.substitute(cols='|l' * total_width)
        # Add day header
        out += " " * 8
        for day in Days:
            out += r' & '
            first = False
            out += day_header.substitute(width=width[day],
                cols='|'.join('l'*width[day]),
                name=day)
        out += r'\\ \hline'
        out += '\n'
        # Complete the rows
        for time in times:
            out += '\n{pad}{time}:00'.format(time=time, pad=" "*8)
            for day in Days:
                if time not in self.days[day].keys():
                    out += ' & '
                    continue
                for course in self.days[day][time]:
                    out += ' & ' + course['course'].name
            out += r'\\'
        # Close the table environments
        out += end.substitute()

        return out

    def as_tex_simple(self):
        # Find the timeslots
        times = set()
        for day in Days:
            for time in self.days[day]:
                times.add(time)
        times = sorted(list(times))

        out = start.substitute(cols='|l' * len(Days))
        # Add day header
        out += " " * 8
        for day in Days:
            out += r' & ' + str(day)
        out += r'\\ \hline'

        # Print the timeslot
        for time in times:
            out += r'\hline'
            out += "\n" + " " * 8 + "{}:00:00 & ".format(time)
            # Find out the number of lines for this time
            lines = 0
            for day in Days:
                try:
                    courses = len(self.days[day][time])
                except KeyError:
                    pass
                if courses > lines:
                    lines = courses

            for i in range(lines):
                if i > 0:
                    out += ' ' * 8 + ' & '
                for day in Days:
                    try:
                        print(self.days[day][time][i])
                        out += self.days[day][time][i]['course'].name
                    except KeyError:
                        pass
                    if day != Days.FRIDAY:
                        out += ' & '
                out += '\\\\ \n'

        out += end.substitute()
        return out


start = Template(r"""
\begin{table}
    \centering
    \caption{Resulting schedule}
    \begin{tabular}{l$cols}
""")
end = Template(r"""
    \end{tabular}
\end{table}""")
day_header = Template(r"""\multicolumn{$width}{|c|}{$name}""")
