import argparse
from ast import arg
import pathlib
import sys
import os
import yaml
from lib.tsproxy.proxy import tsproxy

class ConfigFile():

    def exit_help(self):
        print("""
The config should contain two keys matching -l and -f arguments.

For example:
---
listen: 9999
forward: https://webhook.talkspirit.com/v1/incoming/XXXXXX
ident:
    title: "Post title"
    name: "Talkspirit Proxy"
    url: "http://mypost_link.com"
    icon: ""
---
""")
        sys.exit(1)

    def __init__(self, path):
        if not os.path.isfile(path):
            raise Exception("{} is not a regular file. Check config file.".format(path))

        try:
            with open(path, 'r') as f:
                self._conf =yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

        if not "listen" in self._conf or not "forward" in self._conf:
            self.exit_help()

        if "ident" in self._conf:
            expected = ["title", "name", "url", "icon"]
            for e in expected:
                if e not in self._conf["ident"]:
                    self.exit_help()

    @property
    def listen(self):
        return self._conf["listen"]

    @property
    def forward(self):
        return self._conf["forward"]

    @property
    def ident(self):
        if "ident" in self._conf:
            return self._conf["ident"]
        return None


class ArgParse():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self._reg_args()
        self._args = self.parser.parse_args()

    def _reg_args(self):
        self.parser.add_argument('-l', '--listen', nargs=1, type=int, help='Port to listen on for Slack Webhooks', required=False)
        self.parser.add_argument('-f', '--forward', nargs=1, type=str, help='Webhook to forward to', required=False)
        self.parser.add_argument('-c', '--config', nargs=1, type=pathlib.Path, help='Path to config-file', required=False)

    @property
    def listen(self):
        return self._args.listen

    @property
    def forward(self):
        return self._args.forward

    @property
    def config(self):
        return self._args.config

    @property
    def config(self):
        return self._args.config

def cli_entry():
    args = ArgParse()

    listen=None
    forward=None
    ident=None

    if args.config:
        # Config based
        config = ConfigFile(args.config[0])
        listen = config.listen
        forward = config.forward
        ident = config.ident
    else:
        # Argument based
        if not args.listen or not args.forward:
            print("You must provide both a listen port AND a forward webhook to CLI\n"\
                "Or consider using a configuration file and the -c flag.")
            sys.exit(1)
        else:
            listen = args.listen
            forward = args.forward

    print("tsproxy listening on {}\nForwarding to {}".format(listen, forward))

    prox = tsproxy(listen,forward, ident)