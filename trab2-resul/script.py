#!/bin/python3

from os import close
import matplotlib.pyplot as plt
import pandas as pd

def parse_LOG(metri, csv1_in, csv2_in, inexat_out, padrao_out, line_of_interest1):
    padrao_out.write("NÃO OTIMIZADO; OTIMIZADO\n")
    inexat_out.write("NÃO OTIMIZADO; OTIMIZADO\n")
    lines1 = csv1_in.readlines()
    lines2 = csv2_in.readlines()

    aux1 = metri + '_Padrao_NOpt'
    aux2 = metri + '_Padrao_Opt'
    aux3 = metri + '_Inexato_NOpt'
    aux4 = metri + '_Inexato_Opt'

    print(aux1, aux2, aux3, aux4)

    metricsP = {aux1:0, aux2:0}
    metricsI = {aux3:0, aux4:0}
    keys = [aux1, aux2, aux3, aux4]
    Keyspadrao = [aux1, aux2]
    Keysinexato = [aux3, aux4]
    for pos, line in enumerate(lines1):
        if metri in line and "Raw" not in line:
            # for metric in metrics:
            # print(line, lines[pos+line_of_interest])
            
            Nth = line.split(',')[1].split(' ')
            Nth2 = line.split(',')[1].split(' ')
            Nth2[1] = Nth2[1].replace("NOpt", "Opt")
            value1 = lines1[pos+line_of_interest1].split(',')[1]
            value2 = lines2[pos+line_of_interest1].split(',')[1]
            print(Nth, ":  ", value1)
            print(Nth2, ":  ", value2)

            for key in keys:
                if key in Nth[1] and "Padrao_NOpt" in Nth[1]:
                    metricsP[key] = value1
                if key in Nth2[1] and "Padrao_Opt" in Nth2[1]:
                    metricsP[key] = value2
                if key in Nth[1] and "Inexato_NOpt" in Nth[1]:
                    metricsI[key] = value1
                if key in Nth2[1] and "Inexato_Opt" in Nth2[1]:
                    metricsI[key] = value2

            # se preencheu dict PADRAO, write && zera
            if all(val != 0 for val in metricsP.values()):  
                m = metricsP.get(keys[0])
                g = metricsP.get(keys[1])
                padrao_out.write(f"{m}; {g}\n".format(m, g))

                metricsP = dict.fromkeys(Keyspadrao, 0)
                # print("padrao:", metricsP, end='\n')

            # se preencheu dict INEXATO, write && zera
            if all(val != 0 for val in metricsI.values()):
                # print("METRICA i: ",metricsI.values())
                m = metricsI.get(keys[2])
                g = metricsI.get(keys[3])
                inexat_out.write(f"{m}; {g}\n".format(m, g))
                metricsI = dict.fromkeys(Keysinexato, 0)
                # print("inexato:", metricsI, end='\n')
    
def DP_SL(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Sist_Lin", csv1_in, csv2_in, inexat_out, padrao_out, 6)
                
def DP_M(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Newton", csv1_in, csv2_in, inexat_out, padrao_out, 6)

def DP_H(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_hes", csv1_in, csv2_in, inexat_out, padrao_out, 6)

def DP_G(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_grad", csv1_in, csv2_in, inexat_out, padrao_out, 6)

def AVX_SL(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Sist_Lin", csv1_in, csv2_in, inexat_out, padrao_out, 7)
                
def AVX_M(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Newton", csv1_in, csv2_in, inexat_out, padrao_out, 7)

def AVX_H(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_hes", csv1_in, csv2_in, inexat_out, padrao_out, 7)

def AVX_G(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_grad", csv1_in, csv2_in, inexat_out, padrao_out, 7)

def TIME_SL(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Sist_Lin", csv1_in, csv2_in, inexat_out, padrao_out, -9)

def TIME_M(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Newton", csv1_in, csv2_in, inexat_out, padrao_out, -9)
                    
def TIME_H(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_hes", csv1_in, csv2_in, inexat_out, padrao_out, -9)

def TIME_G(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_grad", csv1_in, csv2_in, inexat_out, padrao_out, -9)

def MISS_SL(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Sist_Lin", csv1_in, csv2_in, inexat_out, padrao_out, 8)

def MISS_M(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Newton", csv1_in, csv2_in, inexat_out, padrao_out, 8)
                    
def MISS_H(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_hes", csv1_in, csv2_in, inexat_out, padrao_out, 8)

def MISS_G(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_grad", csv1_in, csv2_in, inexat_out, padrao_out, 8)

def BAND_SL(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Sist_Lin", csv1_in, csv2_in, inexat_out, padrao_out, 10)

def BAND_M(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("T_Newton", csv1_in, csv2_in, inexat_out, padrao_out, 10)

def BAND_H(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_hes", csv1_in, csv2_in, inexat_out, padrao_out, 10)

def BAND_G(csv1_in, csv2_in, inexat_out, padrao_out):
    parse_LOG("Tderi_grad", csv1_in, csv2_in, inexat_out, padrao_out, 10)

if __name__ == "__main__":
    DP_SL_I_csv = open("../trab2-resul/dp_sl_i.csv", "w")
    DP_SL_P_csv= open("../trab2-resul/dp_sl_p.csv", "w")
    DP_M_I_csv = open("../trab2-resul/dp_m_i.csv", "w")
    DP_M_P_csv= open("../trab2-resul/dp_m_p.csv", "w")
    DP_H_I_csv = open("../trab2-resul/dp_h_i.csv", "w")
    DP_H_P_csv= open("../trab2-resul/dp_h_p.csv", "w")
    DP_G_I_csv= open("../trab2-resul/dp_g_i.csv", "w")
    DP_G_P_csv= open("../trab2-resul/dp_g_p.csv", "w")

    AVX_SL_I_csv = open("../trab2-resul/avx_sl_i.csv", "w")
    AVX_SL_P_csv= open("../trab2-resul/avx_sl_p.csv", "w")
    AVX_M_I_csv = open("../trab2-resul/avx_m_i.csv", "w")
    AVX_M_P_csv= open("../trab2-resul/avx_m_p.csv", "w")
    AVX_H_I_csv = open("../trab2-resul/avx_h_i.csv", "w")
    AVX_H_P_csv= open("../trab2-resul/avx_h_p.csv", "w")
    AVX_G_I_csv= open("../trab2-resul/avx_g_i.csv", "w")
    AVX_G_P_csv= open("../trab2-resul/avx_g_p.csv", "w")

    DP_AVX_SL_I_csv = open("../trab2-resul/dp-avx_sl_i.csv", "w")
    DP_AVX_SL_P_csv= open("../trab2-resul/dp-avx_sl_p.csv", "w")
    DP_AVX_M_I_csv = open("../trab2-resul/dp-avx_m_i.csv", "w")
    DP_AVX_M_P_csv= open("../trab2-resul/dp-avx_m_p.csv", "w")
    DP_AVX_H_I_csv = open("../trab2-resul/dp-avx_h_i.csv", "w")
    DP_AVX_H_P_csv= open("../trab2-resul/dp-avx_h_p.csv", "w")
    DP_AVX_G_I_csv= open("../trab2-resul/dp-avx_g_i.csv", "w")
    DP_AVX_G_P_csv= open("../trab2-resul/dp-avx_g_p.csv", "w")

    TIME_SL_I_csv = open("../trab2-resul/time_sl_i.csv", "w")
    TIME_SL_P_csv= open("../trab2-resul/time_sl_p.csv", "w")
    TIME_M_I_csv = open("../trab2-resul/time_m_i.csv", "w")
    TIME_M_P_csv= open("../trab2-resul/time_m_p.csv", "w")
    TIME_H_I_csv = open("../trab2-resul/time_h_i.csv", "w")
    TIME_H_P_csv= open("../trab2-resul/time_h_p.csv", "w")
    TIME_G_I_csv= open("../trab2-resul/time_g_i.csv", "w")
    TIME_G_P_csv= open("../trab2-resul/time_g_p.csv", "w")

    MISS_SL_I_csv = open("../trab2-resul/miss_sl_i.csv", "w")
    MISS_SL_P_csv= open("../trab2-resul/miss_sl_p.csv", "w")
    MISS_M_I_csv = open("../trab2-resul/miss_m_i.csv", "w")
    MISS_M_P_csv= open("../trab2-resul/miss_m_p.csv", "w")
    MISS_H_I_csv = open("../trab2-resul/miss_h_i.csv", "w")
    MISS_H_P_csv= open("../trab2-resul/miss_h_p.csv", "w")
    MISS_G_I_csv= open("../trab2-resul/miss_g_i.csv", "w")
    MISS_G_P_csv= open("../trab2-resul/miss_g_p.csv", "w")

    BAND_SL_I_csv = open("../trab2-resul/band_sl_i.csv", "w")
    BAND_SL_P_csv= open("../trab2-resul/band_sl_p.csv", "w")
    BAND_M_I_csv = open("../trab2-resul/band_m_i.csv", "w")
    BAND_M_P_csv= open("../trab2-resul/band_m_p.csv", "w")
    BAND_H_I_csv = open("../trab2-resul/band_h_i.csv", "w")
    BAND_H_P_csv= open("../trab2-resul/band_h_p.csv", "w")
    BAND_G_I_csv= open("../trab2-resul/band_g_i.csv", "w")
    BAND_G_P_csv= open("../trab2-resul/band_g_p.csv", "w")

    # gera csv para plotter
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    DP_SL(raw_DP, raw_DPO, DP_SL_I_csv, DP_SL_P_csv)
    raw_DP.close()
    raw_DPO.close()
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    DP_M(raw_DP, raw_DPO, DP_M_I_csv, DP_M_P_csv)
    raw_DP.close()
    raw_DPO.close()
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    DP_H(raw_DP, raw_DPO, DP_H_I_csv, DP_H_P_csv)
    raw_DP.close()
    raw_DPO.close()
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    DP_G(raw_DP, raw_DPO, DP_G_I_csv, DP_G_P_csv)
    raw_DP.close()
    raw_DPO.close()
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    AVX_SL(raw_DP, raw_DPO, AVX_SL_I_csv, AVX_SL_P_csv)
    raw_DP.close()
    raw_DPO.close()
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    AVX_M(raw_DP, raw_DPO, AVX_M_I_csv, AVX_M_P_csv)
    raw_DP.close()
    raw_DPO.close()
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    AVX_H(raw_DP, raw_DPO, AVX_H_I_csv, AVX_H_P_csv)
    raw_DP.close()
    raw_DPO.close()
    raw_DP = open("../trab-original/FLOPS_DP.csv", "r")
    raw_DPO = open('../trab2-icc-opt/FLOPS_DP-opt.csv', "r")
    AVX_G(raw_DP, raw_DPO, AVX_G_I_csv, AVX_G_P_csv)
    raw_DP.close()
    raw_DPO.close()

    raw_TIME = open("../trab-original/CLOCK.csv", "r")
    raw_TIMEO = open('../trab2-icc-opt/CLOCK-opt.csv', "r")
    TIME_SL(raw_TIME, raw_TIMEO, TIME_SL_I_csv, TIME_SL_P_csv)
    raw_TIME.close()
    raw_TIMEO.close()
    raw_TIME = open("../trab-original/CLOCK.csv", "r")
    raw_TIMEO = open('../trab2-icc-opt/CLOCK-opt.csv', "r")
    TIME_M(raw_TIME, raw_TIMEO, TIME_M_I_csv, TIME_M_P_csv)
    raw_TIME.close()
    raw_TIMEO.close()
    raw_TIME = open("../trab-original/CLOCK.csv", "r")
    raw_TIMEO = open('../trab2-icc-opt/CLOCK-opt.csv', "r")
    TIME_H(raw_TIME, raw_TIMEO, TIME_H_I_csv, TIME_H_P_csv)
    raw_TIME.close()
    raw_TIMEO.close()
    raw_TIME = open("../trab-original/CLOCK.csv", "r")
    raw_TIMEO = open('../trab2-icc-opt/CLOCK-opt.csv', "r")
    TIME_G(raw_TIME, raw_TIMEO, TIME_G_I_csv, TIME_G_P_csv)
    raw_TIME.close()
    raw_TIMEO.close()

    raw_L3 = open("../trab-original/L3.csv", "r")
    raw_L3O = open('../trab2-icc-opt/L3-opt.csv', "r")
    BAND_SL(raw_L3, raw_L3O, BAND_SL_I_csv, BAND_SL_P_csv)
    raw_L3.close()
    raw_L3O.close()
    raw_L3 = open("../trab-original/L3.csv", "r")
    raw_L3O = open('../trab2-icc-opt/L3-opt.csv', "r")
    BAND_M(raw_L3, raw_L3O, BAND_M_I_csv, BAND_M_P_csv)
    raw_L3.close()
    raw_L3O.close()
    raw_L3 = open("../trab-original/L3.csv", "r")
    raw_L3O = open('../trab2-icc-opt/L3-opt.csv', "r")
    BAND_H(raw_L3, raw_L3O, BAND_H_I_csv,BAND_H_P_csv)
    raw_L3.close()
    raw_L3O.close()
    raw_L3 = open("../trab-original/L3.csv", "r")
    raw_L3O = open('../trab2-icc-opt/L3-opt.csv', "r")
    BAND_G(raw_L3, raw_L3O, BAND_G_I_csv, BAND_G_P_csv)
    raw_L3.close()
    raw_L3O.close()

    raw_L2 = open("../trab-original/L2CACHE.csv", "r")
    raw_L2O = open('../trab2-icc-opt/L2CACHE-opt.csv', "r")
    MISS_SL(raw_L2, raw_L2O, MISS_SL_I_csv, MISS_SL_P_csv)
    raw_L2.close()
    raw_L2O.close
    raw_L2 = open("../trab-original/L2CACHE.csv", "r")
    raw_L2O = open('../trab2-icc-opt/L2CACHE-opt.csv', "r")
    MISS_M(raw_L2, raw_L2O, MISS_M_I_csv, MISS_M_P_csv)
    raw_L2.close()
    raw_L2O.close
    raw_L2 = open("../trab-original/L2CACHE.csv", "r")
    raw_L2O = open('../trab2-icc-opt/L2CACHE-opt.csv', "r")
    MISS_H(raw_L2, raw_L2O, MISS_H_I_csv, MISS_H_P_csv)
    raw_L2.close()
    raw_L2O.close()
    raw_L2 = open("../trab-original/L2CACHE.csv", "r")
    raw_L2O = open('../trab2-icc-opt/L2CACHE-opt.csv', "r")
    MISS_G(raw_L2, raw_L2O, MISS_G_I_csv, MISS_G_P_csv)
    raw_L2.close()
    raw_L2O.close()

    DP_SL_I_csv.close()
    DP_SL_P_csv.close()
    DP_M_I_csv.close()
    DP_M_P_csv.close()
    DP_H_I_csv.close()
    DP_H_P_csv.close()
    DP_G_I_csv.close()
    DP_G_P_csv.close()

    AVX_SL_I_csv.close()
    AVX_SL_P_csv.close()
    AVX_M_I_csv.close()
    AVX_M_P_csv.close()
    AVX_H_I_csv.close()
    AVX_H_P_csv.close()
    AVX_G_I_csv.close()
    AVX_G_P_csv.close()

    DP_SL_I_csv = open("../trab2-resul/dp_sl_i.csv", "r")
    DP_SL_P_csv= open("../trab2-resul/dp_sl_p.csv", "r")
    DP_M_I_csv = open("../trab2-resul/dp_m_i.csv", "r")
    DP_M_P_csv= open("../trab2-resul/dp_m_p.csv", "r")
    DP_H_I_csv = open("../trab2-resul/dp_h_i.csv", "r")
    DP_H_P_csv= open("../trab2-resul/dp_h_p.csv", "r")
    DP_G_I_csv= open("../trab2-resul/dp_g_i.csv", "r")
    DP_G_P_csv= open("../trab2-resul/dp_g_p.csv", "r")

    AVX_SL_I_csv = open("../trab2-resul/avx_sl_i.csv", "r")
    AVX_SL_P_csv= open("../trab2-resul/avx_sl_p.csv", "r")
    AVX_M_I_csv = open("../trab2-resul/avx_m_i.csv", "r")
    AVX_M_P_csv= open("../trab2-resul/avx_m_p.csv", "r")
    AVX_H_I_csv = open("../trab2-resul/avx_h_i.csv", "r")
    AVX_H_P_csv= open("../trab2-resul/avx_h_p.csv", "r")
    AVX_G_I_csv= open("../trab2-resul/avx_g_i.csv", "r")
    AVX_G_P_csv= open("../trab2-resul/avx_g_p.csv", "r")

    #juntando as duas
    aux1 = DP_SL_I_csv.readlines()
    aux2 = AVX_SL_I_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_SL_I_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))

    aux1 = DP_SL_P_csv.readlines()
    aux2 = AVX_SL_P_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_SL_P_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))

    aux1 = DP_M_I_csv.readlines()
    aux2 = AVX_M_I_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_M_I_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))

    aux1 = DP_M_P_csv.readlines()
    aux2 = AVX_M_P_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_M_P_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))

    aux1 = DP_H_I_csv.readlines()
    aux2 = AVX_H_I_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_H_I_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))

    aux1 = DP_H_P_csv.readlines()
    aux2 = AVX_H_P_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_H_P_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))

    aux1 = DP_G_I_csv.readlines()
    aux2 = AVX_G_I_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_G_I_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))

    aux1 = DP_G_P_csv.readlines()
    aux2 = AVX_G_P_csv.readlines()
    for z in range(20):
        aux2[z] = aux2[z].rstrip('\n')
        aux1[z] = aux1[z].rstrip('\n')
    for z in range(20):
        DP_AVX_G_P_csv.write(f"{aux1[z]}; {aux2[z]}\n".format(aux1[z], aux2[z]))