![Ravioli](ravioli.png "Ravioli")

A tool for calculating simple, useful complexity metrics -- notably the [Koopman Spaghetti Factor (KSF)](https://betterembsw.blogspot.com/2017/08/the-spaghetti-factor-software.html) -- for C.

> I've had to review code that has spaghetti-level complexity in control flow (too high cyclomatic complexity).  And I've had to review code that has spaghetti-level complexity its data flow (too many global variables mixed together into a single computation).  And I've had to review procedures that just go on for page after page with no end in sight. But the stuff that will really make your brain hurt is code that has all of these problems. -- Phil Koopman

This tool is designed to work especially on embedded software written for compilers with non-standard extensions.
It works without a compiler or any preprocessing required.

## Installation

Ravioli is built in Python, and the easiest way to install it is with the Python packaging tool `pip`. First install Python and then run `pip`:

```
$ pip install ravioli
```

## Usage

You can run this on a single file and it will compute metrics for it. Pass it a folder however and it will calculate metrics on all c files it finds in there.

Use it in the current folder like this:

```
$ ravioli .
```

And you'll get a list of all modules sorted by Koopman Spaghetti Factor (KSF):

```
-------------------------------------------------------------------------------
File                                         complexity   globals   lines   ksf
-------------------------------------------------------------------------------
motobox\Sources\FreeRTOS\tasks.c                     12         0    1387    81
motobox\Sources\datapage.c                            1         0    1242    63
motobox\Sources\FreeRTOS\queue.c                     15         0     930    61
motobox\Sources\command_processor.c                  19         2     243    41
motobox\Sources\rtos.c                                5         6     135    41
motobox\Sources\vehicle_comm.c                        8         1     432    34
motobox\Sources\vehicle_comm_sim.c                   11         0     373    29
motobox\Sources\Start12.c                             1         1     337    22
motobox\Sources\can.c                                 7         0     289    21
motobox\Sources\iso15765.c                           12         0     187    21
motobox\Sources\flash.c                               7         0     268    20
motobox\Sources\j1979.c                              10         0     201    20
motobox\Sources\Cpu.C                                 2         2      40    14
motobox\Sources\leds.c                                2         2      26    13
motobox\Sources\log.c                                 3         1     117    13
motobox\Sources\rti.c                                 2         2      23    13
```

There is also a `-f` flag that you can select, that will list all global variables and all functions, sorted by complexity:

```
$ ravioli -f .

-------------------------------------------------------------------------------
Globals
-------------------------------------------------------------------------------
motobox\Sources\Cpu.C:58 CCR_reg
motobox\Sources\Cpu.C:59 CpuMode
motobox\Sources\leds.c:11 zLEDDelay
motobox\Sources\leds.c:11 zLEDDelay
motobox\Sources\log.c:23 TestLog
motobox\Sources\rti.c:13 RTIInterruptCount
motobox\Sources\rti.c:14 TimeInSec
-------------------------------------------------------------------------------
Functions                                                            complexity
-------------------------------------------------------------------------------
motobox\Sources\command_processor.c:198
     zRunCommand                                                             19
motobox\Sources\FreeRTOS\queue.c:824
     xQueueGenericReceive                                                    15
motobox\Sources\FreeRTOS\queue.c:647
     xQueueAltGenericReceive                                                 14
motobox\Sources\iso15765.c:232
     zParseCANMessage                                                        12
motobox\Sources\FreeRTOS\tasks.c:386
     xTaskGenericCreate                                                      12
motobox\Sources\vehicle_comm_sim.c:112
     VehicleSimControlCommand                                                11
motobox\Sources\j1979.c:153
     J1979SendTestMessageCommand                                             10
```

## To do

- Add better error handling. If the parser has an error, make it easy to find the code that broke it.
- If a file doesn't parse, don't let it prevent the other modules from being reported. Currently it looks like any parsing failure produces a error showing results.
- Try it on some other code.
