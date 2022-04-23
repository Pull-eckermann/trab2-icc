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

def plotter(input_file, out_plot, nameMetodo, metrica, log, save_plot):
    #saida_grafico = out_plot
    input_csv = open(input_file, 'r')

    legenda = ["Total Metodo", "Gradiente", "Hessiana", "Sist. Linear"]

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
    # metrica eh tempo
    TnoOptP = '../trab2-original/noOPT_CLOCKPadrao.csv'
    TnoOptI = '../trab2-original/noOPT_CLOCKInexato.csv'
    TOptP   = '../trab2-icc-opt/OPT_CLOCKPadrao.csv'
    TOptI   = '../trab2-icc-opt/OPT_CLOCKInexato.csv'
    
    # metrica eh L3
    L3noOptP = '../trab2-original/noOPT_L3Padrao.csv'
    L3noOptI = '../trab2-original/noOPT_L3Inexato.csv'
    L3OptP   = '../trab2-icc-opt/OPT_L3Inexato.csv'
    L3OptI   = '../trab2-icc-opt/OPT_L3Inexato.csv'
    
    # metrica eh L2
    L2P  = '../trab2-original/noOPT_L2Padrao.csv'
    L2I  = '../trab2-original/noOPT_L2Inexato.csv'
    L2oP = '../trab2-icc-opt/OPT_L2Inexato.csv'
    L2oI = '../trab2-icc-opt/OPT_L2Inexato.csv'

    # metrica eh DP
    DPP  = '../trab2-original/noOPT_FLOPS_DPPadrao.csv'
    DPI  = '../trab2-original/noOPT_FLOPS_DPInexato.csv'
    DPoP = '../trab2-icc-opt/OPT_FLOPS_DPInexato.csv'
    DPoI = '../trab2-icc-opt/OPT_FLOPS_DPInexato.csv'

    # metrica eh AVX
    AVXP  = '../trab2-original/noOPTPadrao_FLOPS_AVX.csv'
    AVXI  = '../trab2-original/noOPTInexat_FLOPS_AVX.csv'
    AVXoP = '../trab2-icc-opt/OPTPadrao_FLOPS_AVX.csv'
    AVXoI = '../trab2-icc-opt/OPTInexat_FLOPS_AVX.csv'

    salve = True
    log = True
    metric = 'Tempo de Execução'
    plotter(TnoOptP, './noOpt_tempoPadrao.png', 'Newton Padrao não Otimizado', metric, log, salve)
    plotter(TnoOptI, './noOpt_tempoInexato.png', 'Newton Inexato não Otimizado', metric, log, salve)
    plotter(TOptP, './Opt_tempoPadrao.png', 'Newton Padrao Otimizado', metric, log, salve)
    plotter(TOptI, './Opt_tempoInexato.png', 'Newton Inexato Otimizado', metric, log, salve)

    log = False
    metric = 'Memory bandwidth [MBytes/s]'
    plotter(L3noOptP, './noOpt_L3Padrao.png', 'Newton Padrao não Otimizado', metric, log, salve)
    plotter(L3noOptI, './noOpt_L3Inexato.png', 'Newton Inexato não Otimizado', metric, log, salve)
    plotter(L3OptP, './Opt_L3Padrao.png', 'Newton Padrao Otimizado', metric, log, salve)
    plotter(L3OptI, './Opt_L3Inexato.png', 'Newton Inexato Otimizado', metric, log, salve)

    metric = 'data cache miss ratio'
    plotter(L2P, './noOpt_L2Padrao.png', 'Newton Padrao não Otimizado', metric, log, salve)
    plotter(L2I, './noOpt_L2Inexato.png', 'Newton Inexato não Otimizado', metric, log, salve)
    plotter(L2oP, './Opt_L2Padrao.png', 'Newton Padrao Otimizado', metric, log, salve)
    plotter(L2oI, './Opt_L2Inexato.png', 'Newton Inexato Otimizado', metric, log, salve)

    metric = 'FLOPS DP'
    plotter(DPP, './noOpt_DP_Padrao.png', 'Newton Padrao não Otimizado', metric, log, salve)
    plotter(DPI, './noOpt_DP_Inexato.png', 'Newton Inexato não Otimizado', metric, log, salve)
    plotter(DPoP, './Opt_DP_Padrao.png', 'Newton Padrao Otimizado', metric, log, salve)
    plotter(DPoI, './Opt_DP_Inexato.png', 'Newton Inexato Otimizado', metric, log, salve)

    metric = 'FLOPS AVX'
    plotter(AVXP, './noOpt_AVX_Padrao.png', 'Newton Padrao não Otimizado', metric, log, salve)
    plotter(AVXI, './noOpt_AVX_Inexato.png', 'Newton Inexato não Otimizado', metric, log, salve)
    plotter(AVXoP, './Opt_AVX_Padrao.png', 'Newton Padrao Otimizado', metric, log, salve)
    plotter(AVXoI, './Opt_AVX_Inexato.png', 'Newton Inexato Otimizado', metric, log, salve)