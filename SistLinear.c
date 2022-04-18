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
double * calc_grad(SistLinear_t *SL, double * X, double *tempo)
{
  double *res = (double*)malloc(SL->num_v*sizeof(double));
  if (!(res)) {
    free(SL);
    printf("ERRO");
    return 0;
  }

  for(int l = 0; l < SL->num_v; l++)
  {
    double tTotal = timestamp();
    res[l] = -rosenbrock_dx(l, X, SL->num_v);
    *tempo += timestamp() - tTotal;   //calculando o tempo da derivação
  }
  
  return res;
}

//calculando a matriz hessiana
void calc_hes(SistLinear_t *SL, double * X, double *tempo, double ** m_aux)
{
  for (int i = 0; i < SL->num_v; i++)
  {
    for(int l = 0; l < SL->num_v; l++)
    {
      double tTotal = timestamp();
      m_aux[i][l] = rosenbrock_dxdy(i, l, X, SL->num_v);
      *tempo += timestamp() - tTotal; //calculando o tempo da derivação
    }
  }
}

//alocando espaço para o sistema linear
SistLinear_t *alocaSistLinear(unsigned int n) {

  SistLinear_t *SL = (SistLinear_t *) malloc(sizeof(SistLinear_t));

  if (SL) {
    SL->num_v = n;

    SL->eq_aux = (char*) calloc(136000, sizeof(char));
    if (!(SL->eq_aux)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }

    SL->L = (double**) calloc(n, sizeof(double*));
    if (!(SL->L)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }
    for (int i = 0; i < n; i++)
    {
      SL->L[i] = (double*) calloc(n, sizeof(double));
      if (!(SL->L[i])) {
        free(SL);
        printf("ERRO");
        return NULL;
      }
    }

    SL->z = (double*) calloc(n, sizeof(double));
    if (!(SL->z)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }
  
    SL->Xeg = (double*) calloc(n, sizeof(double));
    if (!(SL->Xeg)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }

    SL->Xlu = (double*) calloc(n, sizeof(double));
    if (!(SL->Xlu)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }

    SL->Xgs = (double*) calloc(n, sizeof(double));
    if (!(SL->Xgs)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }
  }

  return SL;
}

//liberando a alocação de memoria
void liberaSistLinear(SistLinear_t *SL) {
  for(int i = 0; i < SL->num_v; i++)
    free(SL->L[i]);
  free(SL->L);
  free(SL->eq_aux);
  free(SL->z);
  free(SL->Xeg);
  free(SL->Xlu);
  free(SL->Xgs);
  free(SL);
}

//lendo o sistema linear
SistLinear_t *lerSistLinear() {

  unsigned int n;

  SistLinear_t *SL = NULL;
  
  if (scanf("%d",&n) != EOF) {  
    
    SL = alocaSistLinear(n);
    scanf("%s", SL->eq_aux);
    double aux = 0.0;
    for (int l = 0; l < SL->num_v; l++)
    {
      scanf("%le", &(aux));
      SL->Xeg[l] = aux;
      SL->Xlu[l] = aux;
      SL->Xgs[l] = aux;
    }
    
    scanf("%le", &(SL->epsilon));
    scanf("%i", &(SL->max_iter));
  }

  return SL;
}