

""""
pos_x": -2087,
"pos_y": 3870,
"scale": 4.9,
"""

def translate(p, pos_x, pos_y):
    x, y = p
    return x - float(pos_x), float(pos_y) - y

def translate_scale(p):
    x_p, y_p, sc_m = -2087, 3870, 4.9

    x, y = translate(p, x_p, y_p)

    return x / float(sc_m), y / float(sc_m)