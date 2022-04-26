/* Código escrito por
    Anderson Aparecido do Carmo Frasão 
    GRR 20204069
    Erick Eckermann Cardoso 
    GRR 20186075
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <likwid.h>

#include "Metodo_de_Newton_Padrao.h"
#include "SistLinear.h"
#include "utils.h"

//função para aplicar o pivoteamento na matriz hessiana
void pivot(int n, double**hes, double * grad, int i) {
  double max = fabs(hes[i][i]);
  int max_i = i;

  //verifica qual posição tem o maior valor na coluna i, linha j (i+1)
  for (int j = i+1; j < n; ++j) {
    double v = fabs(hes[j][i]);
    if (v > max) {
      max = v;        // NAO DA PRA TIRAR ESSE IF
      max_i = j;      // POIS ESSAS DUAS VARIAVEIS PODEM MUDAR MAIS DE UMA VEZ
    }
  }

  //pivoteamento
  if (max_i != i) {
    double *tmp = hes[i];
    hes[i] = hes[max_i];
    hes[max_i] = tmp;

    double aux = grad[i];
    grad[i] = grad[max_i];
    grad[max_i] = aux;
  }
} 

//função para calcular o delta
void retrossubs(int n, double *delta, double**hes, double * grad) {
  for (int i = n-1; i >=0; --i) {
    delta[i] = grad[i];           // NAO DA PARA FAZER LOOP UNROLLING
    for (int j = i+1; j < n; j++) // POIS DELTA[I] MUDA DE UM EM UM
      delta[i] -= hes[i][j] * delta[j];
    delta[i] /= hes[i][i];
  }
}

//função para triangularizar a matriz hessiana
void triang(int n, double**hes, double * grad) {
  double m = 0.0;
  for (int i = 0; i < n && (!isnan(m)); ++i) {
    pivot(n, hes, grad, i);
    for (int k = i+1; k < n && (!isnan(m)); ++k) {
      double m = hes[k][i] / hes[i][i];
      
      hes[k][i] = 0.0;                // DEPENDENCIA DE DADOS

      for (int j = i+1; j < n; ++j)
        hes[k][j] -= hes[i][j] * m;
      grad[k] -= grad[i] * m;
    }
  }
  if (isnan(m))                       // IF AGORA ESTA FORA DO FOR
    printf("ERRO: NAN\n");
}

//função com a chamada para o procedimento eliminação de gauss
double* eliminacaoGauss(int n, double *delta, double**hes, double * grad) {
    triang(n, hes, grad);
    retrossubs(n, delta, hes, grad);
    return delta;
}


//função principal para o metodo newton padrão 
double ** Newton_Padrao(SistLinear_t *SL, double *TderivadasEG, double *TslEG, double ** m_aux)
{
  int n = 0;
  int m = 0;
  if((SL->max_iter+1) / 2 == 0)
    n = SL->max_iter+2;
  else
    n = SL->max_iter+1;

  if(SL->num_v / 2 == 0)
    m = SL->num_v+1;
  else
    m = SL->num_v;

  // aloca um vetor de LIN ponteiros para linhas
  double ** m_res = malloc (n * sizeof (double*));
  if (!(m_res)){
    free(SL);
    printf("ERRO");
    return NULL;
  }
  // aloca um vetor com todos os elementos da matriz
  m_res[0] = malloc (n * m * sizeof (double));
  if (!(m_res[0])){
    free(SL);
    printf("ERRO");
    return NULL;
  }
  // ajusta os demais ponteiros de linhas (i > 0)
  for (int i = 1; i < n; i++)
    m_res[i] = m_res[0] + i * m;

  //iteração zero
  for(int z = 0; z < SL->num_v; z++)
    m_res[0][z] = SL->Respostas->Xeg[z];

  //for principal
  for (int i = 0; i < SL->max_iter; i++)
  {
    double aux = 0.0;
    //atualiza o gradiente e a hessiana
    char* name = markerName("Tderi_grad_Padrao_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    double * grad = calc_grad(SL->num_v, SL->Respostas->Xeg, TderivadasEG);
    LIKWID_MARKER_STOP(name);
    name = markerName("Tderi_hes_Padrao_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    calc_hes(SL->num_v, SL->Respostas->Xeg, TderivadasEG, m_aux);
    LIKWID_MARKER_STOP(name);
    for (int i = 0; i < SL->num_v; i++)
      aux += grad[i]*grad[i];
    aux = sqrt(aux);

    //verifica se o gradiente é menor que epsolon
    if(aux < SL->epsilon)
    {
      free(grad);
      for (int l = i+1; l < SL->max_iter+1; l++)
        for(int z = 0; z < SL->num_v; z++)
          m_res[l][z] = NAN;
      return m_res;
    }

    double * delta = (double*) calloc(SL->num_v, sizeof(double));
    if (!(delta)){
      free(SL);
      printf("ERRO");
      return NULL;
    }

    //calcula o vetor delta e o tempo de execução do calculo
    double tTotal = timestamp();
    name = markerName("T_Sist_Lin_Padrao_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    delta = eliminacaoGauss(SL->num_v, delta, m_aux, grad);
    LIKWID_MARKER_STOP(name);
    *TslEG += timestamp() - tTotal;

    for (int l = 0; l < SL->num_v; l++)
      SL->Respostas->Xeg[l] += delta[l];

    aux = 0.0;

    for (int i = 0; i < SL->num_v; i++)
      aux += delta[i]*delta[i];
    aux = sqrt(aux);

    //iteração i+1
    for(int z = 0; z < SL->num_v; z++)
      m_res[i+1][z] = SL->Respostas->Xeg[z];

    free(delta);

    //verifica se delta é menor que epsolon
    if(aux < SL->epsilon)
    {
      free(grad);
      for (int l = i+1; l < SL->max_iter; l++)
        for(int z = 0; z < SL->num_v; z++)
          m_res[l+1][z] = NAN;
      return m_res;
    }
    free(grad);
  }
  return m_res;
}