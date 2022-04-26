#!/bin/python3
from tokenize import Double
import matplotlib.pyplot as plt
import pandas as pd

"""
    script para gerar plots em python
    tem como extrair informacao para plot de .csv com pandas
    
    especificacao .csv == separador ( ; ) ponto e virgula
    para cada csv gerado, utilizar estas colunas:
    Aplicacao_metodo_Newton; Calculo_Gradiente; Calculo_Hessiana; Resolucao_Sistema_Linear
    TUDO                     .                  .                 .
    .                        .                  .                 .
    .                        .                  .                 .
    dataframe.plot() plota todas as colunas do csv
    dataframe["Nome Coluna"].plot() plota a Coluna do csv
    
    usar plt.scatter pra funcao que plota com pontos
    
    plt.show() mostra o grafico mas nao salva
    plt.savefig("nome_do_plot.png") salva o grafico em file
    
    rodar: $> python3 plotter.py
    rodar(todo): $> python3 plotter.py nomeMetodo nomeMedicao entrada.csv saida.csv
links pra ver como faz as parada:
pandas[1]: https://pandas.pydata.org/docs/getting_started/intro_tutorials/04_plotting.html
pyplot[0]: https://matplotlib.org/3.1.1/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py
"""

def plotter(input_file, out_plot, nameMetodo, metrica, log, save_plot, dp):
    #saida_grafico = out_plot
    input_csv = open(input_file, 'r')

    if dp == 0:
        legenda = ["Não Otimizado", "Otimizado"]
    if dp == 1:
        legenda = ["DP Não Otimizado", "DP Otimizado", "AVX Não Otimizado", "AVX Otimizado"]

    # diferentes dataframes
    df = pd.read_csv(sep=';', filepath_or_buffer=input_csv)

    # No eixo das abcissas os gráficos representam a dimensão N da Função de Rosenbrock
    x = [10, 32, 50, 64, 100, 128, 200, 250, 256, 300, 400, 512, 600, 1000, 1024, 2000, 2048, 3000, 4096]
    # fazer um grafico por vez

    # cores = list(islice(cycle(['b', 'g', 'orange', 'r']), None, len(df)))
    # df.plot(style='.-', color=cores)
    df.plot(style='.-')

    # o que vai ser medido
    plt.ylabel(metrica)
    # titulo do grafico
    plt.title(f'{nameMetodo}')    # nome do grafico gerado, aparece na img dpois

    # NAO MUDA DAKI PRA BAIXO
    plt.subplots_adjust(bottom=0.14)
    plt.xticks(df.index, x[:len(df.index)], rotation=50) # magica em python  
    plt.legend(legenda)
    plt.xlabel("dimensão N da Função de Rosenbrock")
    if log:
        plt.yscale('log')                                               # especificado no Inexatotrabalho

    if (save_plot):
        plt.savefig(out_plot)  # salvar grafico em:
    else:
        plt.show()  # mostra grafico
        
        
    
if __name__ == "__main__":
    DP_AVX_SL_I_csv = '../trab2-resul/dp-avx_sl_i.csv'
    DP_AVX_SL_P_csv= '../trab2-resul/dp-avx_sl_p.csv'
    DP_AVX_M_I_csv = '../trab2-resul/dp-avx_m_i.csv'
    DP_AVX_M_P_csv= '../trab2-resul/dp-avx_m_p.csv'
    DP_AVX_H_I_csv = '../trab2-resul/dp-avx_h_i.csv'
    DP_AVX_H_P_csv= '../trab2-resul/dp-avx_h_p.csv'
    DP_AVX_G_I_csv= '../trab2-resul/dp-avx_g_i.csv'
    DP_AVX_G_P_csv= '../trab2-resul/dp-avx_g_p.csv'

    TIME_SL_I_csv = '../trab2-resul/time_sl_i.csv'
    TIME_SL_P_csv= '../trab2-resul/time_sl_p.csv'
    TIME_M_I_csv = '../trab2-resul/time_m_i.csv'
    TIME_M_P_csv= '../trab2-resul/time_m_p.csv'
    TIME_H_I_csv = '../trab2-resul/time_h_i.csv'
    TIME_H_P_csv= '../trab2-resul/time_h_p.csv'
    TIME_G_I_csv= '../trab2-resul/time_g_i.csv'
    TIME_G_P_csv= '../trab2-resul/time_g_p.csv'

    MISS_SL_I_csv = '../trab2-resul/miss_sl_i.csv'
    MISS_SL_P_csv= '../trab2-resul/miss_sl_p.csv'
    MISS_M_I_csv = '../trab2-resul/miss_m_i.csv'
    MISS_M_P_csv= '../trab2-resul/miss_m_p.csv'
    MISS_H_I_csv = '../trab2-resul/miss_h_i.csv'
    MISS_H_P_csv= '../trab2-resul/miss_h_p.csv'
    MISS_G_I_csv= '../trab2-resul/miss_g_i.csv'
    MISS_G_P_csv= '../trab2-resul/miss_g_p.csv'

    BAND_SL_I_csv = '../trab2-resul/band_sl_i.csv'
    BAND_SL_P_csv= '../trab2-resul/band_sl_p.csv'
    BAND_M_I_csv = '../trab2-resul/band_m_i.csv'
    BAND_M_P_csv= '../trab2-resul/band_m_p.csv'
    BAND_H_I_csv = '../trab2-resul/band_h_i.csv'
    BAND_H_P_csv= '../trab2-resul/band_h_p.csv'
    BAND_G_I_csv= '../trab2-resul/band_g_i.csv'
    BAND_G_P_csv= '../trab2-resul/band_g_p.csv'

    dp = 0
    salve = True
    log = True
    metric = 'Tempo de Execução'
    plotter(TIME_G_I_csv, './time_g_i.png', 'Gradiente, Newton Inexato', metric, log, salve, dp)
    plotter(TIME_G_P_csv, './time_g_p.png', 'Gradiente, Newton Padrão', metric, log, salve, dp)
    plotter(TIME_H_I_csv, './time_h_i.png', 'Hessiana, Newton Inexato', metric, log, salve, dp)
    plotter(TIME_H_P_csv, './time_h_p.png', 'Hessiana, Newton Padrão', metric, log, salve, dp)
    plotter(TIME_SL_I_csv, './time_sl_i.png', 'Sistema Linear, Newton Inexato', metric, log, salve, dp)
    plotter(TIME_SL_P_csv, './time_sl_p.png', 'Sistema Linear, Newton Padrão', metric, log, salve, dp)
    plotter(TIME_M_I_csv, './time_m_i.png', 'Método Newton Inexato', metric, log, salve, dp)
    plotter(TIME_M_P_csv, './time_m_p.png', 'Método Newton Padrao', metric, log, salve, dp)

    log = False
    metric = 'Memory bandwidth [MBytes/s]'
    plotter(BAND_G_I_csv, './band_g_i.png', 'Gradiente, Newton Inexato', metric, log, salve, dp)
    plotter(BAND_G_P_csv, './band_g_p.png', 'Gradiente, Newton Padrão', metric, log, salve, dp)
    plotter(BAND_H_I_csv, './band_h_i.png', 'Hessiana, Newton Inexato', metric, log, salve, dp)
    plotter(BAND_H_P_csv, './band_h_p.png', 'Hessiana, Newton Padrão', metric, log, salve, dp)
    plotter(BAND_SL_I_csv, './band_sl_i.png', 'Sistema Linear, Newton Inexato', metric, log, salve, dp)
    plotter(BAND_SL_P_csv, './band_sl_p.png', 'Sistema Linear, Newton Padrão', metric, log, salve, dp)
    plotter(BAND_M_I_csv, './band_m_i.png', 'Método Newton Inexato', metric, log, salve, dp)
    plotter(BAND_M_P_csv, './band_m_p.png', 'Método Newton Padrao', metric, log, salve, dp)

    metric = 'data cache miss ratio'
    plotter(MISS_G_I_csv, './miss_g_i.png', 'Gradiente, Newton Inexato', metric, log, salve, dp)
    plotter(MISS_G_P_csv, './miss_g_p.png', 'Gradiente, Newton Padrão', metric, log, salve, dp)
    plotter(MISS_H_I_csv, './miss_h_i.png', 'Hessiana, Newton Inexato', metric, log, salve, dp)
    plotter(MISS_H_P_csv, './miss_h_p.png', 'Hessiana, Newton Padrão', metric, log, salve, dp)
    plotter(MISS_SL_I_csv, './miss_sl_i.png', 'Sistema Linear, Newton Inexato', metric, log, salve, dp)
    plotter(MISS_SL_P_csv, './miss_sl_p.png', 'Sistema Linear, Newton Padrão', metric, log, salve, dp)
    plotter(MISS_M_I_csv, './miss_m_i.png', 'Método Newton Inexato', metric, log, salve, dp)
    plotter(MISS_M_P_csv, './miss_m_p.png', 'Método Newton Padrao', metric, log, salve, dp)

    dp = 1
    metric = 'FLOPS DP/AVX'
    plotter(DP_AVX_G_I_csv, './dp_avx_g_i.png', 'Gradiente, Newton Inexato', metric, log, salve, dp)
    plotter(DP_AVX_G_P_csv, './dp_avx_g_p.png', 'Gradiente, Newton Padrão', metric, log, salve, dp)
    plotter(DP_AVX_H_I_csv, './dp_avx_h_i.png', 'Hessiana, Newton Inexato', metric, log, salve, dp)
    plotter(DP_AVX_H_P_csv, './dp_avx_h_p.png', 'Hessiana, Newton Padrão', metric, log, salve, dp)
    plotter(DP_AVX_SL_I_csv, './dp_avx_sl_i.png', 'Sistema Linear, Newton Inexato', metric, log, salve, dp)
    plotter(DP_AVX_SL_P_csv, './dp_avx_sl_p.png', 'Sistema Linear, Newton Padrão', metric, log, salve, dp)
    plotter(DP_AVX_M_I_csv, './dp_avx_m_i.png', 'Método Newton Inexato', metric, log, salve, dp)
    plotter(DP_AVX_M_P_csv, './dp_avx_m_p.png', 'Método Newton Padrao', metric, log, salve, dp)