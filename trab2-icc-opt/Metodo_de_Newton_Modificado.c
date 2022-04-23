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

#include "SistLinear.h"
#include "Metodo_de_Newton_Modificado.h"

//função para aplicar o pivoteamento
void pivotLU(S_FatLU *LU, int n, int i, double**hes, double * grad) {
  double max = fabs(hes[i][i]);
  int max_i = i;
   //verifica qual posição tem o maior valor na coluna i, linha j (i+1)
  for (int j = i+1; j < n; ++j) {
    double v = fabs(hes[j][i]);
    if (v > max) {
      max = v;
      max_i = j;
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

    tmp = LU->L[i];
    LU->L[i] = LU->L[max_i];
    LU->L[max_i] = tmp;

    aux = LU->z[i];
    LU->z[i] = LU->z[max_i];
    LU->z[max_i] = aux;
  }
} 

//função para triangularizar a matriz hessiana
void triangLU(S_FatLU *LU, int n, double**hes, double * grad) {
  for (int i = 0; i < n; ++i) {

    pivotLU(LU, n, i, hes, grad);
    
    LU->L[i][i] = 1;
    
    for (int k = i+1; k < n; k++) {
      double m = hes[k][i] / hes[i][i];
      if (isnan(m))
        printf("ERRO DE DIV POR 0 (TRIANG): %d %g\n", i, hes[i][i]);

      LU->L[k][i] = m;

      for (int j = i+1; j < n; ++j)
        hes[k][j] -= hes[i][j] * m;
    }
  }
}

//função para calcular o vetor z
void retrossubpz(S_FatLU *LU, int n, double * grad) {
  for (int i = 0; i < n; ++i) {
    LU->z[i] = grad[i];
    for (int j = 0; j < i; j++)
      LU->z[i] -= LU->L[i][j] * LU->z[j];
  }
}

//função para calcular o delta
void retrossubs2(double *z, int n, double**hes, double *delta) {
  for (int i = n-1; i >=0; --i) {
    delta[i] = z[i];
    for (int j = i+1; j < n; j++)
      delta[i] -= hes[i][j] * delta[j];
    delta[i] /= hes[i][i];
    if (isnan(hes[i][i]))
      printf("ERRO DE DIV POR 0 (RETRO): %d %g\n", i, hes[i][i]);
  }
}

//função com a chamada para o procedimento fatoração LU
double * FatLU(S_FatLU *LU, int n, double *delta, double**hes, double * grad) {
  triangLU(LU, n, hes, grad);
  retrossubpz(LU, n, grad);
  retrossubs2(LU->z, n, hes, delta);
  return delta;
}

//função principal para o metodo newton Modificado
double ** Newton_Modificado(SistLinear_t *SL, S_FatLU *LU, double *Xlu, double *TderivadasLU, double *TslLU, double ** m_aux)
{
  // aloca um vetor de LIN ponteiros para linhas
  double ** m_res = malloc ((SL->max_iter+1) * sizeof (double*));
  if (!(m_res)){
    free(SL);
    printf("ERRO");
    return NULL;
  }
 
  // aloca um vetor com todos os elementos da matriz
  m_res[0] = malloc ((SL->max_iter+1) * SL->num_v * sizeof (double));
  if (!(m_res[0])){
    free(SL);
    printf("ERRO");
    return NULL;
  }
 
  // ajusta os demais ponteiros de linhas (i > 0)
  for (int i = 1; i < SL->max_iter+1; i++)
    m_res[i] = m_res[0] + i * SL->num_v;

  //iteração zero
  for(int z = 0; z < SL->num_v; z++)
    m_res[0][z] = Xlu[z];

  int i;

  //for principal
  for (i = 0; i < SL->max_iter; i++)
  {
    double aux = 0.0;

    //atualiza o gradiente
    double * grad = calc_grad(SL->num_v, Xlu, TderivadasLU);

    //atualiza a matriz hessiana a cada has steps (numero de variaveis)
    if(i % SL->num_v == 0)
      calc_hes(SL->num_v, Xlu, TderivadasLU, m_aux);
  
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
    delta = FatLU(LU, SL->num_v, delta, m_aux, grad);
    *TslLU += timestamp() - tTotal;

    for (int l = 0; l < SL->num_v; l++)
      Xlu[l] += delta[l];

    aux = 0.0;

    for (int i = 0; i < SL->num_v; i++)
      aux += delta[i]*delta[i];
    aux = sqrt(aux);

    //iteração i+1
    for(int z = 0; z < SL->num_v; z++)
      m_res[i+1][z] = Xlu[z];

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