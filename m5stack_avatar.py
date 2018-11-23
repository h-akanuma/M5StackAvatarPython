from m5stack import lcd

import random
import time
import _thread

class M5StackAvatar:
    FONT_COLOR = lcd.WHITE
    FONT = lcd.FONT_DejaVu24
    
    def __init__(self):
        lcd.setColor(self.FONT_COLOR)
        lcd.font(self.FONT)

        self.fw, self.fh        = lcd.fontSize()
        self.ww, self.wh        = lcd.winsize()
        self.eye_x              = 90
        self.eye_y              = 80
        self.eye_r              = 10
        self.eye_close_x        = 70
        self.eye_close_width    = 40
        self.eye_close_height   = 5
        self.blink_term_ms      = 500
        self.mouth_x            = 135
        self.mouth_y            = 150
        self.mouth_width        = 50
        self.mouth_height       = 5
        self.mouth_close        = True
        self.mouth_close_height = 20
        self.exclamation_x      = 280
        self.exclamation_y      = 20
        self.exclamation_width  = 10
        self.exclamation_height = 30
        self.exclamation_space  = 8
        
        self.spaces = ' '
        while lcd.textWidth(self.spaces) < self.ww:
            self.spaces += ' '

    def _blink(self):
        _thread.allowsuspend(True)
        while True:
            self._eye_close()
            time.sleep_ms(self.blink_term_ms)
            self._eye_open()
            time.sleep(random.randint(2, 6))

    def _eye_close(self):
        lcd.circle(self.eye_x, self.eye_y, self.eye_r, lcd.BLACK, lcd.BLACK)
        lcd.circle(self.ww - self.eye_x, self.eye_y, self.eye_r, lcd.BLACK, lcd.BLACK)
        lcd.rect(self.eye_close_x, self.eye_y, self.eye_close_width, self.eye_close_height, lcd.WHITE, lcd.WHITE)
        lcd.rect(
            self.ww - self.eye_close_x - self.eye_close_width,
            self.eye_y, self.eye_close_width,
            self.eye_close_height,
            lcd.WHITE,
            lcd.WHITE
        )

    def _eye_open(self):
        lcd.rect(self.eye_close_x, self.eye_y, self.eye_close_width, self.eye_close_height, lcd.BLACK, lcd.BLACK)
        lcd.rect(
            self.ww - self.eye_close_x - self.eye_close_width,
            self.eye_y,
            self.eye_close_width,
            self.eye_close_height,
            lcd.BLACK,
            lcd.BLACK
        )
        lcd.circle(self.eye_x, self.eye_y, self.eye_r, lcd.WHITE, lcd.WHITE)
        lcd.circle(self.ww - self.eye_x, self.eye_y, self.eye_r, lcd.WHITE, lcd.WHITE)

    def _lipsync(self):
        if self.mouth_close:
            self._lip_open()
        else:
            self._lip_close()

    def _lip_close(self):
        lcd.rect(
            self.mouth_x,
            self.mouth_y - (self.mouth_close_height // 2),
            self.mouth_width,
            self.mouth_height + self.mouth_close_height, 
            lcd.BLACK,
            lcd.BLACK
        )
        lcd.rect(self.mouth_x, self.mouth_y, self.mouth_width, self.mouth_height, lcd.WHITE, lcd.WHITE)
        self.mouth_close = True

    def _lip_open(self):
        lcd.rect(self.mouth_x, self.mouth_y, self.mouth_width, self.mouth_height, lcd.BLACK, lcd.BLACK)
        lcd.rect(
            self.mouth_x,
            self.mouth_y - (self.mouth_close_height // 2),
            self.mouth_width,
            self.mouth_height + self.mouth_close_height,
            lcd.WHITE,
            lcd.WHITE
        )
        self.mouth_close = False

    def _speak(self, text):
        lcd.setColor(lcd.BLACK, lcd.WHITE)
        lcd.arc((self.eye_x + self.mouth_x) // 2, (self.wh - self.fh) - 5, 25, 25, 270, 360, lcd.WHITE, lcd.WHITE)
        lcd.rect(0, (self.wh - self.fh) - 5, self.ww + 5, self.fh + 5, lcd.WHITE, lcd.WHITE)
        lcd.textClear(0, (self.wh - self.fh) - 1, self.spaces, lcd.WHITE)
        lcd.print(text, 0, lcd.BOTTOM, lcd.BLACK)
        self._lipsync()
        time.sleep_ms(2000)
        while lcd.textWidth(text) > 0:
            text = text[1:]
            lcd.textClear(0, (self.wh - self.fh) - 1, self.spaces, lcd.WHITE)
            lcd.print(text, 0, lcd.BOTTOM, lcd.BLACK)
            self._lipsync()
            time.sleep_ms(200)
        lcd.rect(0, (self.wh - self.fh) - 5, self.ww, self.fh + 5, lcd.BLACK, lcd.BLACK)
        lcd.arc((self.eye_x + self.mouth_x) // 2, (self.wh - self.fh) - 5, 25, 25, 270, 360, lcd.BLACK, lcd.BLACK)
        self._lip_close()

    def _mouth(self):
        lcd.rect(self.mouth_x, self.mouth_y, self.mouth_width, self.mouth_height, lcd.WHITE, lcd.WHITE)
        while True:
            typ, sender, msg = _thread.getmsg()
            if msg:
                self._speak(msg)
            time.sleep_ms(200)

    def _display(self):
        self.eye_blink_thread_id = _thread.start_new_thread('eye_blink', self._blink, ())
        self.mouth_thread_id     = _thread.start_new_thread('mouth', self._mouth, ())
        while True:
            typ, sender, msg = _thread.getmsg()
            if msg:
                _thread.sendmsg(self.mouth_thread_id, msg)
            time.sleep_ms(200)

    def _exclamation_color(self, color):
        lcd.rect(self.exclamation_x, self.exclamation_y, self.exclamation_width, self.exclamation_height, color, color)
        lcd.rect(
            self.exclamation_x, 
            self.exclamation_y + self.exclamation_height + self.exclamation_space,
            self.exclamation_width,
            self.exclamation_width,
            color,
            color
        )

    def _pale_color(self, color):
        lcd.rect(200, 0, 5, 40, color, color)
        lcd.rect(220, 0, 5, 45, color, color)
        lcd.rect(240, 0, 5, 50, color, color)
        lcd.rect(260, 0, 5, 55, color, color)
        lcd.rect(40, 100, 5, 40, color, color)
        lcd.rect(60, 103, 5, 35, color, color)
        lcd.rect(80, 106, 5, 30, color, color)
        lcd.rect(100, 109, 5, 25, color, color)

    def start(self):
        lcd.setCursor(0, 0)
        lcd.clear()
        self.face_thread_id = _thread.start_new_thread('face', self._display, ())

    def speak(self, text):
        _thread.sendmsg(self.face_thread_id, text)

    def exclamation_on(self):
        self._exclamation_color(lcd.RED)

    def exclamation_off(self):
        self._exclamation_color(lcd.BLACK)

    def pale_on(self):
        self._pale_color(lcd.BLUE)

    def pale_off(self):
        self._pale_color(lcd.BLACK)
