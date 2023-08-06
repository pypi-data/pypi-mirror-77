# ODR Stream Router

[![Build Status](https://travis-ci.org/digris/odr-stream-router.svg?branch=master)](https://travis-ci.org/digris/odr-stream-router)

A tool to route ODR-AudioEnc zmq streams.

The aim of `odroute` is to achieve two goals:

 - Provide a way to handle a fallback for DAB+ streams generated with
   [ODR-AudioEnc](https://github.com/Opendigitalradio/ODR-AudioEnc),
   e.g. in the situation when running a dedicated encoder box in the studio, but in case of connection- or
   encoder-failure an automatic failover to a central encoder instance (encoding a webstream) is desired.
 - Provide a way to distribute DAB+ streams through a single connection from an encoder to multiple instances
   of [ODR-DabMux](https://github.com/Opendigitalradio/ODR-DabMux).

The tool can be configured while running, adding/removing inputs without interruptions.

## Installation

### Via PyPi

    pip install odroute


### From GitHub

    pip install -e git+https://github.com/digris/odr-stream-router.git#egg=odroute


### From Source

    git clone https://github.com/digris/odr-stream-router.git
    cd odr-stream-router

    # pip
    pip install -e .

    # or setup.py
    python setup.py develop

## Usage

    odroute run --help

### Simple CLI Example

Listen on ports *5001* and *5002* and output the active port to *tcp://localhost:9001* - switching
inputs after 0.5 seconds of 'inactivity/activity'.

`-s/--source` and `-o/--output` can both be specified multiple times.

The priority of the input ports is specified through the order. So in this example port *5001* is forwarded if
available, else packages from the socket on *5002* are used.

    odroute -v run -s 5001 -s 5002 -o tcp://localhost:9001 -d 0.5

### Telnet Interface

Version `0.0.2` provides a telnet interface that can list the configured inputs
and outputs and the currently *active* input.
Further it provides functionality fo *force* an input to be used (instead of
relying on the fallback behaviour).


use option `--telnet` resp. `-t` with either *port* to listen on or in
*ip:port* to bind.  See `odroute run --help`

    odroute run -s 5001 -s 5002 -o tcp://localhost:9001 -t 127.0.0.1:4001

Connect with telnet and run `help` to see the available commands

    telnet 127.0.0.1 4001

Or use `netcat`:

    echo help             | nc 127.0.0.1 4001
    echo input.list       | nc 127.0.0.1 4001
    echo input.force 5002 | nc 127.0.0.1 4001
    echo input.current    | nc 127.0.0.1 4001


### UNIX Socket interface

Version `0.0.17` provides a UNIX socket interface, with the same commands as the telnet one.
Example client in python, with `thesocket` as path:

    import socket
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("./thesocket")
    s.send("help\n".encode())
    print(s.recv(1024).decode())

Using netcat is also possible

    echo input.list | nc -U ./thesocket

### Configuration via .yml file

Alternatively odroute can read its configuration from file.
When specifying a config file (in .yml format) all other CLI options are
ignored in favour of options in config-file resp. their defaults.

All options in the .yml file are optional - if not given the corresponding defaults will be used.

#### Config file example

    # config.yml
    version: 1
    name: my-router-instance-name
    source_ports:
     - 7000
     - 7001
    
    destinations:
     - tcp://127.0.0.1:7010
     - tcp://127.0.0.1:7011
    
    nodata_failover_delay: 1.0
    nodata_recover_delay: 10.0
    noaudio_failover_delay: 20
    noaudio_recover_delay: 20
    audio_threshold: -90
    
    socket: ./thesocket
    
    log_level: debug
    log_format: '%(asctime)s [%(levelname)s] %(name)s: %(message)s'


#### Run with file-based config

    odroute run -c ./config.yml


#### 'Hot-reloading' config

When running `odroute` with a file-based config you have the possibility to
'hot-reload' the settings, if you have configured a control-interface via
socket or telnet.

To reload the configuration invoke a 'reload' command via any suitable
control-interface. Assuming you have a socket interface on `./thesocket`:

    echo reload | nc -U ./thesocket

This will re-read the config file and update the inputs and outputs as well as
updating the values for 'no-data' / 'no-audio' failover settings.

Please note: You *cannot* change the control-interface on-the-fly! To change
the socket or telnet interface you have to restart the odroute process.


### Testing

Run the `./test.sh` script to run a few automated tests.
