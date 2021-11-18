import datetime


def font_color(val):
    color = 'rgb(9, 171, 59)' if val > 0 else 'rgb(255, 43, 43)'
    return f'color: {color}'


def font_size(val):
    return f'font-size: 18px'
