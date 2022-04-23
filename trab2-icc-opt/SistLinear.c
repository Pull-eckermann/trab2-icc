/* Código escrito por
    Anderson Aparecido do Carmo Frasão 
    GRR 20204069
    Erick Eckermann Cardoso 
    GRR 20186075
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#include <likwid.h>

#include "utils.h"
#include "SistLinear.h"
#include "Rosenbrock.h"

//calcula o vetor gradiente 
double * calc_grad(int n, double * X, double *tempo)
{
  double *res = (double*)malloc(n*sizeof(double));
  if (!(res)) {
    printf("ERRO");
    return 0;
  }

  for(int l = 0; l < n; l++)
  {
    double tTotal = timestamp();
    res[l] = -rosenbrock_dx(l, X, n);
    *tempo += timestamp() - tTotal;   //calculando o tempo da derivação
  }
  
  return res;
}

//calculando a matriz hessiana
void calc_hes(int n, double * X, double *tempo, double ** m_aux)
{
  for (int i = 0; i < n; i++)
  {
    for(int l = 0; l < n; l++)
    {
      double tTotal = timestamp();
      m_aux[i][l] = rosenbrock_dxdy(i, l, X, n);
      *tempo += timestamp() - tTotal; //calculando o tempo da derivação
    }
  }
}

S_FatLU *alocaFatLU(unsigned int n){

  S_FatLU *LU = (S_FatLU *) calloc(1, sizeof(S_FatLU));

  if (n / 2 == 0)
    n += 1;

  if(LU){
    // aloca um vetor de LIN ponteiros para linhas
    LU->L = malloc (n * sizeof (double*));
    if (!(LU->L)){
      free(LU);
      printf("ERRO");
      return NULL;
    }
 
    // aloca um vetor com todos os elementos da matriz
    LU->L[0] = malloc (n * n * sizeof (double));
    if (!(LU->L[0])){
      free(LU->L);
      printf("ERRO");
      return NULL;
    }
 
    // ajusta os demais ponteiros de linhas (i > 0)
    for (int i = 1; i < n; i++)
      LU->L[i] = LU->L[0] + i * n;

    LU->z = (double*) calloc(n, sizeof(double));
    if (!(LU->z)) {
      free(LU);
      printf("ERRO");
      return NULL;
    }
  }

  return LU;
}

Res_SL *alocaRes(int n){

  Res_SL *Res = (Res_SL*) malloc(sizeof(Res_SL));

  if (n / 2 == 0)
    n += 1;

  if(Res){
    Res->Xeg = (double*) calloc(n, sizeof(double));
    if (!(Res->Xeg)) {
      free(Res);
      printf("ERRO");
      return NULL;
    }

    Res->Xlu = (double*) calloc(n, sizeof(double));
    if (!(Res->Xlu)) {
      free(Res);
      printf("ERRO");
      return NULL;
    }

    Res->Xgs = (double*) calloc(n, sizeof(double));
    if (!(Res->Xgs)) {
      free(Res);
      printf("ERRO");
      return NULL;
    }
  }
  return Res;
}

//alocando espaço para o sistema linear
SistLinear_t *alocaSistLinear(unsigned int n) {

  SistLinear_t *SL = (SistLinear_t *) calloc(1, sizeof(SistLinear_t));

  if (SL) {
    SL->num_v = n;
    
    SL->eq_aux = (char*) calloc(136000, sizeof(char));
    if (!(SL->eq_aux)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }
  }

  return SL;
}

void liberaFatLU(S_FatLU *LU, int n){
  free(LU->L[0]);
  free(LU->L);
  free(LU->z);
  free(LU);
}

//liberando a alocação de memoria
void liberaSistLinear(SistLinear_t *SL) {
  free(SL->eq_aux);
  free(SL->Respostas->Xeg);
  free(SL->Respostas->Xlu);
  free(SL->Respostas->Xgs);
  free(SL->Respostas);
  free(SL);
}

void libera_aux(double **m_aux, double **m_reseg, double **m_resgs, int num_v, int max_iter){
  free(m_resgs[0]);
  free(m_resgs);
  free(m_reseg[0]);
  free(m_reseg);
  free(m_aux[0]);
  free(m_aux);
}

//lendo o sistema linear
SistLinear_t *lerSistLinear() {

  unsigned int n;

  SistLinear_t *SL = NULL;
  
  if (scanf("%d",&n) != EOF) {  
    
    SL = alocaSistLinear(n);
    SL->Respostas = alocaRes(n);

    scanf("%s", SL->eq_aux);
    double aux = 0.0;
    for (int l = 0; l < SL->num_v; l++)
    {
      scanf("%le", &aux);
      SL->Respostas->Xeg[l] = SL->Respostas->Xlu[l] = SL->Respostas->Xgs[l] = aux;
    }

    scanf("%le", &SL->epsilon);
    scanf("%i", &SL->max_iter);
  }

  return SL;
}