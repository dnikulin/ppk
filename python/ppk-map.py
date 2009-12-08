#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

# Known bugs:
# * Termination does not propagate from broken pipe
#   Many fixes have been tried, none have worked

import ppk

import os
import sys

from subprocess import Popen, PIPE

if __name__ == '__main__':
    if len(sys.argv) < 2:
        ppk.printUsage("<program> [arguments ...]")

    args = sys.argv[1:]

    for _, ibody in ppk.readRaw():
        pipe = Popen(args, stdin = PIPE, stdout = PIPE, shell = False)

        try:
            with pipe.stdin as opipe:
                with pipe.stdout as ipipe:                    
                    pid = os.fork()

                    if pid == 0: # spawnee (read pipe, write stdout)
                        try:
                            # Don't pipe.wait() on exit
                            pipe = None

                            opipe.close()
                            obody = ipipe.read()
                            ipipe.close()

                            ppk.writeRaw(obody)
                        finally:
                            sys.exit(0)
                    else: # spawner (read stdin, write pipe)
                        try:
                            ipipe.close()
                            opipe.write(ibody)
                            opipe.close()
                        finally:
                            os.waitpid(pid, 0)
        finally:
            if pipe is not None:
                pipe.wait()
