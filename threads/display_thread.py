import threading
import time

from RPLCD.lcd import CharLCD, BacklightMode

import services.twitter_service as twitter_service
import services.vvs_service as vvs_service


def init_display(lcd):
    lcd.clear()
    lcd.backlight_enabled = True
    lcd.display_enabled = True
    a_umlaut = (
        0b01010,
        0b00000,
        0b00100,
        0b01010,
        0b10001,
        0b11111,
        0b10001,
        0b10001)
    o_umlaut = (
        0b01010,
        0b00000,
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    )
    u_umlaut = (
        0b01010,
        0b00000,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110
    )
    heart = (
        0b00000,
        0b00000,
        0b01010,
        0b11111,
        0b11111,
        0b01110,
        0b00100,
        0b00000)
    lcd.create_char(0, a_umlaut)
    lcd.create_char(1, o_umlaut)
    lcd.create_char(2, u_umlaut)
    lcd.create_char(3, heart)


def display_departure_on_lcd(lcd, departure_string, is_disruption):
    lcd.write_string(departure_string)
    if is_disruption:
        lcd.cursor_pos = (1, 15)
        lcd.write_string('!')
    time.sleep(3)
    lcd.clear()


def display_disruption_on_lcd(lcd, disruption_message):
    framebuffer = [_replace_umlauts(' ' + chr(3) + 'VVS Störung!' + chr(3) + ' '), '']
    _loop_string(lcd, disruption_message, framebuffer, 1, 16)


def _loop_string(lcd, string, framebuffer, row, num_cols, delay=0.1):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i:i + num_cols]
        _write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)


def _write_to_lcd(lcd, framebuffer, num_cols):
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')


def _replace_umlauts(umlaut_str):
    return umlaut_str.replace('ä', '\xe1').replace('ö', '\xef').replace('ü', '\xf5') \
        .replace('ß', '\xe2') \
        .replace('Ä', chr(0)).replace('Ö', chr(1)).replace('Ü', chr(2))


def turn_off_display(lcd):
    lcd.display_enabled = False
    lcd.backlight_enabled = False


class DisplayThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lcd = CharLCD(pin_rs=26, pin_rw=38, pin_e=29, pins_data=[31, 32, 33, 35],
                           pin_backlight=36, backlight_mode=BacklightMode.active_high, cols=16, rows=2)
        self.daemon = True
        self.start()

    def run(self):
        init_display(self.lcd)

        disruption_message = twitter_service.fetch_disruption_message()
        departures = vvs_service.fetch_departures_from_station()

        for departure in departures:
            display_departure_on_lcd(self.lcd, _replace_umlauts(departure),
                                     twitter_service.is_disruption(disruption_message))

        if twitter_service.is_disruption(disruption_message):
            display_disruption_on_lcd(self.lcd, _replace_umlauts(disruption_message))

        turn_off_display(self.lcd)
