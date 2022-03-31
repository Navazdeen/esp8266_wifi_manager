from machine import Pin, I2C
import machine
import ssd1306
import network
import gc
import time
import gfx

p0 = Pin(2, Pin.IN)

char_width = 8
char_height = 9

oled_width = 128
oled_height = 64

wlan = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

i2c = I2C(scl=Pin(5), sda=Pin(4))
display = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

graphics = gfx.GFX(oled_width, oled_height, display.pixel)


def draw_lock(i):
    graphics.fill_rect(15*char_width, i*8, char_width, char_height, 1)
    graphics.fill_circle(15*char_width+char_width //
                         2, i*8+char_height//2, 2, 0)
    graphics.fill_rect(15*char_width+char_width //
                       2-1, i*8+char_height//2, 3, 4, 0)


def wifi_connect(username, password):
    i = 0
    j = 9
    if ap.active():
        ap.active(False)
    if not wlan.active():
        wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(username, password)
        # print(wlan.isconnected())
        display.fill(0)
        display.text("connecting", 0, 0, 1)
        while not wlan.isconnected():
            display.text(".", i, j, 1)
            display.show()
            i += 5
            time.sleep(1)
            if i > 50:
                display.fill(0)
                display.text("unable to conne", 0, 0, 1)
                display.text("ct. check pass", 0, char_height, 1)
                display.show()
                wlan.active(False)
                return
    display.fill(0)
    display.text('Connected to ', 0, 0, 1)
    display.text(username, 0, char_height, 1)
    print(wlan.ifconfig())
    display.show()


def show_wifi(p):
    wifi_list = wlan.scan()
    print(wifi_list)
    display.fill(0)
    if wifi_list:
        for i, wifi in enumerate(wifi_list):
            print(wifi)
            name = wifi[0].decode('utf-8')
            mode = wifi[4]
            display.text(name[0:min(7, (len(name)-1))]+"...", 0, i*8, 1)
            if mode > 0:
                draw_lock(i)
            else:
                graphics.rect(15*char_width, i*8, char_width, char_height, 1)
            display.show()
    else:
        display.text('no device found', 0, 0, 1)
        display.text('', 0, 9, 1)
        display.show()

    # wifi_connect('Mi 10T Pro', '12345678')


show_wifi('p')
p0.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_FALLING, handler=show_wifi)
