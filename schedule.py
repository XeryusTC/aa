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

    def add(self, room, course, agent):
        if room.start_time not in self.days[room.day].keys():
            self.days[room.day][room.start_time] = []

        self.days[room.day][room.start_time].append({
            'room': room.name,
            'course': course,
            'agent': agent,
        })

    def as_plain(self):
        out = ""
        for day in Days:
            out = out + '\n' + str(day);
            for time in sorted(self.days[day]):
                out = "{}\n    {}:00:00".format(out, time)
                for course in self.days[day][time]:
                    out = "{}\n        ({}) {} by {}".format(out,
                        course['room'], course['course'].name,
                        course['agent'].name)
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
                    courses = 0
                if courses > lines:
                    lines = courses

            for i in range(lines):
                if i > 0:
                    out += ' ' * 8 + ' & '
                for day in Days:
                    try:
                        course = self.days[day][time][i]
                        out += bla.substitute(
                            room=course['room'],
                            course=course['course'].name,
                            teacher=course['agent'].name,
                        )
                    except (KeyError, IndexError):
                        pass
                    if day != Days.FRIDAY:
                        out += ' & '
                out += '\\\\ \n'

        out += end.substitute()
        return out

    def as_tex_multi_table(self):
        # Find the timeslots
        times = set()
        for day in Days:
            for time in self.days[day]:
                times.add(time)
        times = sorted(list(times))
        out = ""

        for day in Days:
            out += mt_start.substitute(day=str(day))
            for time in times:
                out += r'\hline'
                out += "\n" + " " * 8 + "{}:00:00 & ".format(time)
                first = True
                try:
                    for course in self.days[day][time]:
                        if not first:
                            out += "\n" + " " * 8 + "& "
                        first = False
                        out += bla.substitute(
                            room=course['room'],
                            course=course['course'].name,
                            teacher=course['agent'].name
                        )
                        out += r"\\"
                except KeyError:
                    out += r"\\"

            out += mt_end.substitute()

        return out


mt_start = Template(r"""
\begin{table}
    \centering
    \caption{$day}
    \begin{tabular}{l|l}
""")

mt_end = Template(r"""
    \end{tabular}
\end{table}
""")

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
bla = Template(r"""($room) $course by $teacher""")
