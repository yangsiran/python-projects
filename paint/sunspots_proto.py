from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF

data = [
    #  YR  MO    PREDICTED     HIGH      LOW
    (2012, 10,        59.3,    60.3,    58.3),
    (2012, 11,        61.6,    63.6,    59.6),
    (2012, 12,        63.6,    66.6,    60.6),
    (2013, 01,        65.6,    70.6,    60.6),
    (2013, 02,        67.7,    72.7,    62.7),
    (2013, 03,        69.9,    75.9,    63.9),
    (2013, 04,        72.5,    79.5,    65.5),
    (2013, 05,        75.1,    82.1,    68.1),
    (2013, 06,        78.1,    86.1,    70.1),
    (2013, 07,        81.0,    90.0,    72.0)
    ]

drawing = Drawing(200, 150)

pred = [row[2]-40 for row in data]
high = [row[3]-40 for row in data]
low = [row[4]-40 for row in data]
times = [200*(row[0] +row[1]/12.0 - 2012)-150 for row in data]

drawing.add(PolyLine(zip(times, pred), strokeColor=colors.blue))
drawing.add(PolyLine(zip(times, high), strokeColor=colors.red))
drawing.add(PolyLine(zip(times, low), strokeColor=colors.green))

drawing.add(String(65, 115, 'Sunspots', fontSize=18, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'report1.pdf', 'Sunspots')
