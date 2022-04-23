#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd

"""
    script para extrair metricas do .log
    
    formato:
    recebe .log de metrica
    
    devolve:
    sobre uma metrica (L3/L2/FLOPS)
               |  csv_P  |  csv_I  |
    -----------+---------+---------+
    Tmetodo    |    ~    |    ~    |
    Gradiente  |    ~    |    ~    |
    Hessiana   |    ~    |    ~    |
    Sist lin   |    ~    |    ~    |
    -----------+---------+---------+
    
""" 

def parse_LOG(csv_in, padrao_out, inexat_out, line_of_interest):
    padrao_out.write("METODO; GRAD; HESS; SISTLIN\n")
    inexat_out.write("METODO; GRAD; HESS; SISTLIN\n")
    lines = csv_in.readlines()

    metricsP = {"T_Newton_Padrao":0,"Tderi_grad_Padrao":0, "Tderi_hes_padrao":0, "T_Sist_Lin_Padrao":0}
    metricsI = {"T_Newton_Inexato":0,"Tderi_grad_Inexato":0, "Tderi_hes_Inexato":0, "T_Sist_Lin_Inexato":0}
    keys = ["T_Newton_Padrao","Tderi_grad_Padrao","Tderi_hes_padrao","T_Sist_Lin_Padrao", "T_Newton_Inexato", "Tderi_grad_Inexato", "Tderi_hes_Inexato", "T_Sist_Lin_Inexato"]
    Keyspadrao = ["T_Newton_Padrao","Tderi_grad_Padrao", "Tderi_hes_padrao", "T_Sist_Lin_Padrao"]
    Keysinexato = ["T_Newton_Inexato","Tderi_grad_Inexato", "Tderi_hes_Inexato", "T_Sist_Lin_Inexato"]
    for pos, line in enumerate(lines):
        if "Group 1 Metric" in line and "Raw" not in line:
            # for metric in metrics:
            # print(line, lines[pos+line_of_interest])
# """
            Nth = line.split(',')[1].split(' ')
            value = lines[pos+line_of_interest].split(',')[1]
            # print(Nth, ":  ", value)
            
            for key in keys:
                if key in Nth[1] and "Padrao" in Nth[1]:
                    metricsP[key] = value
                if key in Nth[1] and "padrao" in Nth[1]:
                    metricsP[key] = value
                if key in Nth[1] and "Inexato" in Nth[1]:
                    metricsI[key] = value

            # se preencheu dict PADRAO, write && zera
            if all(val != 0 for val in metricsP.values()):  
                m = metricsP.get(keys[0])
                g = metricsP.get(keys[1])
                h = metricsP.get(keys[2])
                s = metricsP.get(keys[3])
                padrao_out.write(f"{m}; {g}; {h}; {s}\n".format(m, g, h, s))

                metricsP = dict.fromkeys(Keyspadrao, 0)
                # print("padrao:", metricsP, end='\n')

            # se preencheu dict INEXATO, write && zera
            if all(val != 0 for val in metricsI.values()):
                # print("METRICA i: ",metricsI.values())
                m = metricsI.get(keys[4])
                g = metricsI.get(keys[5])
                h = metricsI.get(keys[6])
                s = metricsI.get(keys[7])
                inexat_out.write(f"{m}; {g}; {h}; {s}\n".format(m, g, h, s))
                metricsI = dict.fromkeys(Keysinexato, 0)
                # print("inexato:", metricsI, end='\n')
# """

def parse_L3(csv_in, padrao_out, inexat_out):
    parse_LOG(csv_in, padrao_out, inexat_out, 10)
                    
def parse_L2(csv_in, padrao_out, inexat_out):
    parse_LOG(csv_in, padrao_out, inexat_out, 8)

def parse_FLOPS(csv_in, padraoDP_out, inexatDP_out):
    parse_LOG(csv_in, padraoDP_out, inexatDP_out, 6)

def parse_TIME(csv_in, padrao_out, inexat_out):
    parse_LOG(csv_in, padrao_out, inexat_out, -9)

def parse_AVX(csv_in, padraoAVX_out, inexatAVX_out):
    parse_LOG(csv_in, padraoAVX_out, inexatAVX_out, 7)
    


if __name__ == "__main__":
    # data de nao otimizado
    raw_L3 = open("../trab-original/L3.csv", "r")
    raw_L2 = open("../trab-original/L2CACHE.csv", "r")
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_AVX = open("../trab-original/FLOPS_DP.csv", "r")
    raw_TIME = open("../trab-original/CLOCK.csv", "r")

    L3padrao_csv = open("../trab-original/noOPT_L3Padrao.csv", "w")
    L3inexato_csv= open("../trab-original/noOPT_L3Inexato.csv", "w")
    L2padrao_csv = open("../trab-original/noOPT_L2Padrao.csv", "w")
    L2inexato_csv= open("../trab-original/noOPT_L2Inexato.csv", "w")
    DPpadrao_csv = open("../trab-original/noOPT_FLOPS_DPPadrao.csv", "w")
    DPinexato_csv= open("../trab-original/noOPT_FLOPS_DPInexato.csv", "w")
    AVXpadrao_csv= open("../trab-original/noOPTPadrao_FLOPS_AVX.csv", "w")
    AVXinexat_csv= open("../trab-original/noOPTInexat_FLOPS_AVX.csv", "w")
    CLOCKpadrao_csv = open("../trab-original/noOPT_CLOCKPadrao.csv", "w")
    CLOCKinexato_csv= open("../trab-original/noOPT_CLOCKInexato.csv", "w")

    # data de otimizado
    raw_L3O = open('../trab2-icc-opt/L3-opt.csv', "r")
    raw_L2O = open('../trab2-icc-opt/L2CACHE-opt.csv', "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    raw_AVXO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    raw_TIMEO = open('../trab2-icc-opt/CLOCK-opt.csv', "r")

    L3P = open("../trab2-icc-opt/OPT_L3Padrao.csv", "w")
    L3I = open("../trab2-icc-opt/OPT_L3Inexato.csv", "w")
    L2P = open("../trab2-icc-opt/OPT_L2Padrao.csv", "w")
    L2I = open("../trab2-icc-opt/OPT_L2Inexato.csv", "w")
    DPoP= open("../trab2-icc-opt/OPT_FLOPS_DPPadrao.csv", "w")
    DPoI= open("../trab2-icc-opt/OPT_FLOPS_DPInexato.csv", "w")
    AVXP= open("../trab2-icc-opt/OPTPadrao_FLOPS_AVX.csv", "w")
    AVXI= open("../trab2-icc-opt/OPTInexat_FLOPS_AVX.csv", "w")
    CLKP = open("../trab2-icc-opt/OPT_CLOCKPadrao.csv", "w")
    CLKI = open("../trab2-icc-opt/OPT_CLOCKInexato.csv", "w")

    # gera csv para plotter
    parse_L3(raw_L3, L3padrao_csv, L3inexato_csv)
    parse_L2(raw_L2, L2padrao_csv, L2inexato_csv)
    parse_FLOPS(raw_DP, DPpadrao_csv, DPinexato_csv)
    parse_TIME(raw_TIME, CLOCKpadrao_csv, CLOCKinexato_csv)
    parse_AVX(raw_AVX, AVXpadrao_csv, AVXinexat_csv)

    parse_L3(raw_L3O, L3P, L3I)
    parse_L2(raw_L2O, L2P, L2I)
    parse_FLOPS(raw_DPO, DPoP, DPoI)
    parse_TIME(raw_TIMEO, CLKP, CLKI)
    parse_AVX(raw_AVXO, AVXP, AVXI)