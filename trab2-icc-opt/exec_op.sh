#!/bin/sh
likwid-perfctr -C 3 -g L3 -m -O ./newtonPC < funcoes.dat > L3-opt.log
likwid-perfctr -C 3 -g L2CACHE -m -O ./newtonPC < funcoes.dat > L2CACHE-opt.log
likwid-perfctr -C 3 -g FLOPS_DP -m -O ./newtonPC < funcoes.dat > FLOPS_DP-opt.log
likwid-perfctr -C 3 -g CLOCK -m -O ./newtonPC < funcoes.dat > CLOCK-opt.log

