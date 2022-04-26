/* Código escrito por
    Anderson Aparecido do Carmo Frasão 
    GRR 20204069
    Erick Eckermann Cardoso 
    GRR 20186075
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <likwid.h>
#include "SistLinear.h"
#include "utils.h"
#include <inttypes.h>
#include <assert.h>
#include "Metodo_de_Newton_Inexato.h"
#include "Metodo_de_Newton_Padrao.h"
#include "Rosenbrock.h"

int main (){
  LIKWID_MARKER_INIT;
  SistLinear_t *SL;

  double TtotalEG = 0;
  double TtotalGS = 0;
  double TderivadasEG = 0; 
  double TderivadasGS = 0;
  double TslEG = 0;
  double TslGS = 0;
  
  while (SL = lerSistLinear())
  {
    int m = 0;

    if(SL->num_v / 2 == 0)
      m = SL->num_v+1;
    else
      m = SL->num_v;

    // aloca um vetor de LIN ponteiros para linhas
    double ** m_aux = malloc (m * sizeof (double*));
    if (!(m_aux)){
      printf("ERRO");
      return 0;
    }
 
    // aloca um vetor com todos os elementos da matriz
    m_aux[0] = malloc (m * m * sizeof (double));
    if (!(m_aux[0])){
      free(m_aux);
      printf("ERRO");
      return 0;
    }
 
    // ajusta os demais ponteiros de linhas (i > 0)
    for (int i = 1; i < m; i++)
      m_aux[i] = m_aux[0] + i * m;
    
    //Newton Padrão
    double tTotal = timestamp();
    char* name = markerName("T_Newton_Padrao_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    double ** m_reseg = Newton_Padrao(SL, &TderivadasEG, &TslEG, m_aux);
    LIKWID_MARKER_STOP(name);
    TtotalEG = timestamp() - tTotal;    //calculando o tempo total do newton padrao
    
    //Metodo de Newton Inexato

    tTotal = timestamp();
    name = markerName("T_Newton_Inexato_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    double ** m_resgs = Newton_Inexato(SL, &TderivadasGS, &TslGS, m_aux);
    LIKWID_MARKER_STOP(name);
    TtotalGS = timestamp() - tTotal;    ////calculando o tempo total do newton inexato

    //inicio do processamento de impressão
    // cabeçalho
    
    printf("%d\n", SL->num_v);
    printf("%s\n", SL->eq_aux);
    printf("#Iteração \t| Newton Padrão \t| Newton Inexato\n");
    double final[2];
    // para cada iteração
    for (int i = 0; i <= SL->max_iter; i++) {
      final[0] = final[1] = NAN;

      final[0] = rosenbrock(m_reseg[i], SL->num_v);
      final[1] = rosenbrock (m_resgs[i], SL->num_v);
      if (isnan(final[0]) && isnan(final[1]))
        break;
      
      printf("%d \t\t| ", i); // imprime iteração
      
      if (final[0] != NAN) {  // se nesta iteração o valor da primeira coluna existe, imprime
        if (isnan(final[0]) || isinf(final[0]))
          printf("\t\t\t| ");
        else
          printf("%1.14e\t| ", final[0]);
      }
      else
        printf("\t\t\t| ");

      if (final[1] != NAN) {  // se nesta iteração o valor da primeira coluna existe, imprime
        if (isnan(final[1]) || isinf(final[1]))
          printf("\t\t\t ");
        else
          printf("%1.14e\t ", final[1]);
      }
      else
        printf("\t\t\t ");
      printf("\n");
    }

    // imprimir os tempos
    printf("Tempo total \t| %1.14e\t| %1.14e\n", TtotalEG, TtotalGS);
    printf("Tempo derivadas | %1.14e\t| %1.14e\n", TderivadasEG, TderivadasGS);
    printf("Tempo SL \t| %1.14e\t| %1.14e\n", TslEG, TslGS);
    printf("#\n");
    printf("\n");
    
    libera_aux(m_aux, m_reseg, m_resgs, SL->num_v, SL->max_iter);
    liberaSistLinear(SL);
  }
  LIKWID_MARKER_CLOSE;
}