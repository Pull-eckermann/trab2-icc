#!/bin/sh
likwid-perfctr -C 3 -g L3 -m -o L3-opt.csv ./newtonPC < funcoes.dat 
likwid-perfctr -C 3 -g L2CACHE -m -o L2CACHE-opt.csv ./newtonPC < funcoes.dat
likwid-perfctr -C 3 -g FLOPS_DP -m -o FLOPS_DP-opt.csv ./newtonPC < funcoes.dat
likwid-perfctr -C 3 -g CLOCK -m -o CLOCK-opt.csv ./newtonPC < funcoes.dat

