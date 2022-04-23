#!/bin/bash
cd trab-original/
make purge
make
sh gera_rosenbrock.sh > funcoes.dat
sh exec_nop.sh
cd ../trab2-icc-opt/
make purge
make
sh gera_rosenbrock.sh > funcoes.dat
sh exec_op.sh
cd ../trab2-resul/
python3 script.py
python3 scri.py