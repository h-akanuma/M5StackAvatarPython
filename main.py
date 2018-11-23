from m5stack_avatar import M5StackAvatar

import time

avatar = M5StackAvatar()
avatar.start()

while True:
    avatar.speak('Hello from M5StackAvatarPython!!')
    time.sleep(10)
    avatar.exclamation_on()
    time.sleep(5)
    avatar.exclamation_off()
    time.sleep(5)
    avatar.pale_on()
    time.sleep(5)
    avatar.pale_off()
    time.sleep(5)