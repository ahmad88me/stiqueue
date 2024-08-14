#!/bin/sh
cd stiqueue; ls -ltra; echo "running client ... " ; echo "stiqueue host: " ; echo stq ; python src/stiqueue/sqclient.py stq 1234
