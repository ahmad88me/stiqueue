#!/bin/sh
cd stiqueue; ls -ltra; echo "running client ... " ; echo "stiqueue host: " ; echo stq ; python -m stiqueue.sqclient stq 1234
