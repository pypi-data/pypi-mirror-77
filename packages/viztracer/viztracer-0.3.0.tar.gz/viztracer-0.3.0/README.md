# VizTracer

[![build](https://github.com/gaogaotiantian/viztracer/workflows/build/badge.svg)](https://github.com/gaogaotiantian/viztracer/actions?query=workflow%3Abuild)  [![pypi](https://img.shields.io/pypi/v/viztracer.svg)](https://pypi.org/project/viztracer/)  [![support-version](https://img.shields.io/pypi/pyversions/viztracer)](https://img.shields.io/pypi/pyversions/viztracer)  [![license](https://img.shields.io/github/license/gaogaotiantian/viztracer)](https://github.com/gaogaotiantian/viztracer/blob/master/LICENSE)  [![commit](https://img.shields.io/github/last-commit/gaogaotiantian/viztracer)](https://github.com/gaogaotiantian/viztracer/commits/master)

VizTracer is a deterministic debugging/profiling tool that can trace and visualize your python code to help you intuitively understand your code better and figure out the time consuming part of your code.

VizTracer can display every function executed and the corresponding entry/exit time from the beginning of the program to the end, which is helpful for programmers to catch sporatic performance issues. VizTracer is also capable of generating traditional flamegraph which is a good summary of the execution of the program

You can take a look at the [demo](http://www.minkoder.com/viztracer/result.html) result of multiple example programs(sort algorithms, mcts, modulo algorithms, multithread tracing, etc.)

[![example_img](https://github.com/gaogaotiantian/viztracer/blob/master/img/example.png)](https://github.com/gaogaotiantian/viztracer/blob/master/img/example.png)

[trace viewer](https://chromium.googlesource.com/catapult) is used to display the stand alone html data.

VizTracer also supports json output that complies with Chrome trace event format, which can be loaded using [perfetto](https://ui.perfetto.dev/)

VizTracer generates HTML report for flamegraph using [d3-flamegraph](https://github.com/spiermar/d3-flame-graph)

## Requirements

VizTracer requires python 3.6+. No other package is needed. For now, VizTracer only supports CPython + Linux/MacOS. 

## Install

The prefered way to install VizTracer is via pip

```
pip install viztracer
```

You can also download the source code and build it yourself.

## Usage

There are a couple ways to use VizTracer

### Command Line

The easiest way to use VizTracer is through command line. Assume you have a python script to profile and the normal way to run it is:

```
python3 my_script.py
```

You can simply use VizTracer as 

```
python3 -m viztracer my_script.py
```

which will generate a ```result.html``` file in the directory you run this command. Open it in browser and there's your result.

If your script needs arguments like 

```
python3 my_script.py arg1 arg2
```

Just feed it as it is to VizTracer

```
python3 -m viztracer my_script.py arg1 arg2
```

You can also specify the tracer to be used in command line by passing --tracer argument. c tracer is the default value, you can use python tracer(deprecated) instead

```
python3 -m viztracer --tracer c my_script.py
python3 -m viztracer --tracer python my_script.py
```

You can specify the output file using -o or --output_file argument. The default output file is result.html. Two types of files are supported, html and json.
```
python3 -m viztracer -o other_name.html my_script.py
python3 -m viztracer -o other_name.json my_script.py
```

By default, VizTracer only generates trace file, either in HTML format or json. You can have VizTracer to generate a flamegraph as well by 

```
python3 -m viztracer --save_flamegraph my_script.py
```

### Inline

Sometimes the command line may not work as you expected, or you do not want to profile the whole script. You can manually start/stop the profiling in your script as well.

First of all, you need to import ```VizTracer``` class from the package, and make an object of it.

```python
from viztracer import VizTracer

tracer = VizTracer()
```

If your code is executable by ```exec``` function, you can simply call ```tracer.run()```

```python
tracer.run("import random;random.randrange(10)")
```

This will as well generate a ```result.html``` file in your current directory. You can pass other file path to the function if you do not like the name ```result.html```

```python
tracer.run("import random; random.randrange(10)", output_file="better_name.html")
```

When you need a more delicate profiler, you can manually enable/disable the profile using ```start()``` and ```stop()``` function.

```python
tracer.start()
# Something happens here
tracer.stop()
tracer.save() # also takes output_file as an optional argument
```

Or, you can do it with ```with``` statement

```python
with VizTracer(output_file="optional.html") as tracer:
    # Something happens here
```

You can record only the part that you are interested in

```python
# Some code that I don't care
tracer.start()
# Some code I do care
tracer.stop()
# Some code that I want to skip
tracer.start()
# Important code again
tracer.stop()
tracer.save()
```

**It is higly recommended that ```start()``` and ```stop()``` function should be in the same frame(same level on call stack). Problem might happen if the condition is not met**

### Display Result

By default, VizTracer will generate a stand alone HTML file which you can simply open with Chrome(maybe Firefox?). The front-end uses trace-viewer to show all the data. 

However, you can generate json file as well, which complies to the chrome trace event format. You can load the json file on [perfetto](https://ui.perfetto.dev/), which will replace the deprecated trace viewer in the future. 

At the moment, perfetto does not support locally stand alone HTML file generation, so I'm not able to switch completely to it. The good news is that once you load the perfetto page, you can use it even when you are offline. 


### Trace Filter

Sometimes your code is really complicated or you need to run you program for a long time, which means the parsing time would be too long and the HTML/JSON file would be too large. There are ways in VizTracer to filter out the data you don't need. 

The filter mechanism only works in C tracer, and it works at tracing time, not parsing time. That means, using filters will introduce some extra overhead while your tracing, but will save significant memory, parsing time and disk space. 

Currently we support the following kinds of filters:

#### max_stack_depth

```max_stack_depth``` is a straight forward way to filter your data. It limits the stack depth VizTracer will trace, which cuts out deep call stacks, including some nasty recursive calls. 

You can specify ```max_stack_depth``` in command line:

```
python3 -m viztracer --max_stack_depth 10 my_script.py
```

Or you can pass it as an argument to the ```VizTracer``` object:

```python
from viztracer import VizTracer

tracer = VizTracer(max_stack_depth=10)
```


#### include_files and exclude_files

There are cases when you are only interested in functions in certain files. You can use ```include_files``` and ```exclude_files``` feature to filter out data you are not insterested in. 

When you are using ```include_files```, only the files and directories you specify are recorded. Similarly, when you are using ```exclude_files```, files and directories you specify will not be recorded. 

**IMPORTANT: ```include_files``` and ```exclude_files``` can't be both spcified. You can only use one of them.**

**If a function is not recorded based on ```include_files``` or ```exclude_files``` rules, none of its descendent functions will be recorded, even if they match the rules**

You can specify ```include_files``` and ```exclude_files``` in command line, but they can take more than one argument, which will make the following command ambiguous:

```
# Ambiguous command which should NOT be used
python3 -m viztracer --include_files ./src my_script.py
```

Instead, when you are using ```--include_files``` or ```--exclude_files```, ```--run``` should be passed for the command that you actually want to execute:

```
# --run is used to solve ambiguity
python3 -m viztracer --include_files ./src --run my_script.py
```

However, if you have some other commands that can separate them and solve ambiguity, that works as well:

```
# This will work too
python3 -m viztracer --include_files ./src --max_stack_depth 5 my_script.py
```

You can also pass a ```list``` as an argument to ```VizTracer```:

```python
from viztracer import VizTracer

tracer = VizTracer(include_files=["./src", "./test/test1.py"])
```

#### ignore_c_function

By default, ```VizTracer``` will record all the C functions called by python script. You can turn it off by:

```
python3 -m viztracer --ignore_c_function my_script.py
```

You can turn it off in your script as well:

```python
tracer = VizTracer(ignore_c_function=True)
```

#### ignore_function

Unlike ```ignore_c_function```, ```ignore_function``` is a decorator which you can apply to any function to skip tracing it and its descendants. 

```
from viztracer import ignore_function
@ignore_function
def some_function():
    # nothing inside will be traced
```

### Choose Tracer

The default tracer for current version is c tracer, which introduces a relatively small overhead(worst case 2-3x) but only works for CPython on Linux. However, if there's other reason that you would prefer a pure-python tracer, you can use python tracer using ```tracer``` argument when you initialize ```VizTracer``` object.

```python
tracer = VizTracer(tracer="python")
```

**python tracer will be deprecated because of the performance issue in the future**
**No filter feature is supported with python tracer**

#### Cleanup of c Tracer

The interface for c trace is almost exactly the same as python tracer. However, to achieve lower overhead, some optimization is applied to c tracer so it will withhold the memory it allocates for future use to reduce the time it calls ```malloc()```. If you want the c trace to free all the memory it allocates while collecting trace, use

```python
tracer.cleanup()
```

### Add Custom Event

```VizTracer``` supports custom event added while the program is running. This works like a print debug, but you can know when this print happens while looking at trace data. 

When your code is running with ```VizTracer``` on, you can use 

```python
tracer.add_instant(name, args, scope)
```

to add an event that will be shown in the report. In trace viewer, you would be able to see what ```args``` is.

```name``` should be a ```string``` for this event. 
```args``` should be a json serializable object(dict, list, string, number).
```scope``` is an optional argument, default is ```"g"``` for global. You can use ```p``` for process or ```t``` for thread. This affects how long the event shows in the final report.

### Log Print

```VizTracer``` can log your print to the report using instant events. In this way, you can simply add ```print``` functions in your code just like you are doing print debug and see what happens on the timeline.

You can specify ```--log_print``` on the command line

```
python -m viztracer --log_print my_script.py
```

Or do it when you initialize your ```VizTracer``` object

```python
tracer = VizTracer(log_print=True)
```

### Multi Thread Support

```VizTracer``` supports python native ```threading``` module without the need to do any modification to your code. Just start ```VizTracer``` before you create threads and it will just work.

[![example_img](https://github.com/gaogaotiantian/viztracer/blob/master/img/multithread_example.png)](https://github.com/gaogaotiantian/viztracer/blob/master/img/example.png)


### Multi Process Support

VizTracer can support multi process with some extra steps. The current structure of VizTracer keeps one single buffer for one process, which means the user will have to produce multiple results from multiple processes and combine them together. 

If you are using ```os.fork()``` or libraries using similiar mechanism, you can use VizTracer the normal way you do, with an extra option ```pid_suffix```.

```
python -m viztracer --pid_suffix multi_process_program.py
```

This way, the program will generate mutliple ```json``` files in current working directory. Notice here, if ```--pid_suffix``` is passed to VizTracer, the default output format will be ```json``` because this is only expected to be used by multi-process programs. 

You can specify the output directory if you want

```
python -m viztracer --pid_suffix --output_dir ./temp_dir multi_process_program.py
```

After generating ```json``` files, you need to combine them

```
python -m viztracer --combine ./temp_dir/*.json
```

This will generate the HTML report with all the process info. You can specify ```--output_file``` when using ```--combine```.

Actually, you can combine any json reports together to an HTML report. 

If your code is using ```subprocess``` to spawn processes, the newly spawned process won't be traced(We could do something to ```PATH``` but that feels sketchy). There are a couple ways to deal with that:

* You can change the ```subprocess``` or ```popen``` code manually, to attach VizTracer to sub-process. You will have json results from differnt processes and you just need to combine them together. This is a generic way to do multi-process tracing and could work pretty smoothly if you don't have many entries for your subprocess

* Or you can hack your ```PATH``` env to use ```python -m viztracer <args>``` to replace ```python```. This will make VizTracer attach your spawned process automatically, but could have other side effects. 

### JSON alternative 

VizTracer needs to dump the internal data to json format. It is recommended for the users to install ```orjson```, which is much faster than the builtin ```json``` library. VizTracer will try to import ```orjson``` and fall back to the builtin ```json``` library if ```orjson``` does not exist.

## Performance

Overhead is a big consideration when people choose profilers. VizTracer now has a similar overhead as native cProfiler. It works slightly worse in the worst case(Pure FEE) and better in easier case because even though it collects some extra information than cProfiler, the structure is lighter. 

Admittedly, VizTracer is only focusing on FEE now, so cProfiler also gets other information that VizTracer does not acquire.

An example run for test_performance with Python 3.8 / Ubuntu 18.04.4 on Github VM

```
fib       (10336, 10336): 0.000852800 vs 0.013735200(16.11)[py] vs 0.001585900(1.86)[c] vs 0.001628400(1.91)[cProfile]
hanoi     (8192, 8192): 0.000621400 vs 0.012924899(20.80)[py] vs 0.001801800(2.90)[c] vs 0.001292900(2.08)[cProfile]
qsort     (10586, 10676): 0.003457500 vs 0.042572898(12.31)[py] vs 0.005594100(1.62)[c] vs 0.007573200(2.19)[cProfile]
slow_fib  (1508, 1508): 0.033606299 vs 0.038840998(1.16)[py] vs 0.033270399(0.99)[c] vs 0.032577599(0.97)[cProfile]
```

## Limitations

VizTracer uses ```sys.setprofile()``` for its profiler capabilities, so it will conflict with other profiling tools which also use this function. Be aware of it when using VizTracer.

## Bugs/Requirements

Please send bug reports and feature requirements through [github issue tracker](https://github.com/gaogaotiantian/viztracer/issues). VizTracer is currently under development now and it's open to any constructive suggestions.

## License

Copyright Tian Gao, 2020.

Distributed under the terms of the  [Apache 2.0 license](https://github.com/gaogaotiantian/viztracer/blob/master/LICENSE).