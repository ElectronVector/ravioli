![Ravioli](ravioli.png "Ravioli")

A tool for calculating simple, useful complexity metrics for C.

This tool is designed to work especially on embedded software written for compilers with non-standard extensions.
It works without a compiler or any preprocessing required.

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
```

## To do

- Clean up output format on -f option. Only provide filename, not full path?
- Provide coordinates for functions when using the -f option.
- Add better error handling. If the parser has an error, make it easy to find the code that broke it.
- Try it on some other code.