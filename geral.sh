#!/bin/bash
cd trab-original/
make 
sh gera_rosenbrock.sh > funcoes.dat
sh exec_nop.sh
cd ../trab2-icc-opt/
make
sh gera_rosenbrock.sh > funcoes.dat
sh exec_nop.sh
cd ../trab2-resul/
python3 script.py
python3 scri.py