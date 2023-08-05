# Example

### Input

```
from AW9523B import EX_GPIO,Port0,Port1
import time

inputPin = [Port1.PIN7, Port1.PIN6, Port1.PIN5, Port1.PIN4, Port0.PIN7,
                    Port1.PIN0, Port1.PIN1, Port1.PIN2, Port1.PIN3, Port0.PIN0]

def inputCallback(pin):
    print("inputCallback", pin)

if __name__ == "__main__":
    for pin in inputPin:
        EX_GPIO.setup(pin, EX_GPIO.INPUT)
    EX_GPIO.inputCB = inputCallback
    while 1:
        time.sleep(1)

```

### OUTPUT

```
from AW9523B import EX_GPIO,Port0
import time

led1 = Port0.PIN5
led2 = Port0.PIN6

EX_GPIO.setup(led1, EX_GPIO.OUTPUT)
EX_GPIO.setup(led2, EX_GPIO.OUTPUT)



if __name__ == "__main__":
    while 1:
        time.sleep(5)
        EX_GPIO.output(led1,EX_GPIO.HIGH)
        EX_GPIO.output(led2,EX_GPIO.LOW)
        time.sleep(5)
        EX_GPIO.output(led1,EX_GPIO.LOW)
        EX_GPIO.output(led2,EX_GPIO.HIGH)

```