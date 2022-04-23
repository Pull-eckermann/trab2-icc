#!/bin/sh
likwid-perfctr -C 3 -g L3 -m -o L3.csv ./newtonPC < funcoes.dat 
likwid-perfctr -C 3 -g L2CACHE -m -o L2CACHE.csv ./newtonPC < funcoes.dat
likwid-perfctr -C 3 -g FLOPS_DP -m -o FLOPS_DP.csv ./newtonPC < funcoes.dat
likwid-perfctr -C 3 -g CLOCK -m -o CLOCK.csv ./newtonPC < funcoes.dat
