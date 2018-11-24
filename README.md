# M5StackAvatarPython

 MicroPython module for M5Stack to render avatar face.

![M5StackAvatarPython](m5stack_avatar_python_original.gif)

## Features

* Show avatar face with blinking eyes
* Show text with lip sync
* Show exclamation mark
* Show pale face

## Installation

 Download m5stack_avatar.py and put it to the flash directory.

## Usage

### Initialize

```python
from m5stack_avatar import M5StackAvatar

avatar = M5StackAvatar()
avatar.start()
```

### Show text

```python
avatar.speak('Hello from M5StackAvatarPython!!')
```

### Turn on/off exclamation mark

```python
avatar.exclamation_on()
```

```python
avatar.exclamation_off()
```

### Turn on/off pale face

```python
avatar.pale_on()
```

```python
avatar.pale_off()
```

## Example

```python
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
```

## Licence
Copyright (c) 2018 Akanuma Hiroaki  
Released under the MIT license  
https://opensource.org/licenses/mit-license.php
