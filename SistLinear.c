/* Código escrito por
    Anderson Aparecido do Carmo Frasão 
    GRR 20204069
    Erick Eckermann Cardoso 
    GRR 20186075
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <matheval.h>
#include <string.h>
#include <assert.h>

#include "utils.h"
#include "SistLinear.h"

//criando matriz hessiana a partir da função original
void cria_hes(SistLinear_t *SL)
{
  char aux[10];
  char Xn[10];

  strtok(SL->eq_aux, "\n");
  for(int n = 0; n < SL->num_v; n++)
  {
    for(int l = 0; l < SL->num_v; l++)
    {
      void * f_aux1;
      void * f_aux2;
      memset(Xn, 0, sizeof(Xn));              
      memset(aux, 0, sizeof(aux));            
      f_aux1 = evaluator_create(SL->eq_aux); 
      assert(f_aux1);
      sprintf(aux, "%d", n+1);                //gerando a variave que sera usada na derivada
      strcat(strcpy(Xn, "x"), aux);           //
      f_aux2 = evaluator_derivative (f_aux1, Xn);
      assert(f_aux2);
      memset(Xn, 0, sizeof(Xn));
      memset(aux, 0, sizeof(aux));
      sprintf(aux, "%d", l+1);                //gerando a variave que sera usada na derivada
      strcat(strcpy(Xn, "x"), aux);           //
      SL->HESSIANA[n][l] = evaluator_derivative (f_aux2, Xn);
      assert(SL->HESSIANA[n][l]);
      evaluator_destroy(f_aux1);
      evaluator_destroy(f_aux2);
    }
  }
}

//criando vetor gradiente a partir da função original
void cria_grad(SistLinear_t *SL)
{
  char aux[10];
  char Xn[10];
    
  for(int l = 0; l < SL->num_v; l++)
  {
    void * f_aux;
    memset(Xn, 0, sizeof(Xn));
    memset(aux, 0, sizeof(aux));
    f_aux = evaluator_create(SL->eq_aux);
    assert(f_aux);
    sprintf(aux, "%d", l+1);        //gerando a variave que sera usada na derivada
    strcat(strcpy(Xn, "x"), aux);   //
    SL->GRADIENTE[l] = evaluator_derivative (f_aux, Xn);
    assert(SL->GRADIENTE[l]);
    evaluator_destroy(f_aux);
  }
}

//calcula o vetor gradiente 
double * calc_grad(SistLinear_t *SL, double * X, double *tempo)
{
  double *res = (double*)malloc(SL->num_v*sizeof(double));
  if (!(res)) {
    free(SL);
    printf("ERRO");
    return 0;
  }
  char **Xs = (char**) malloc(SL->num_v*sizeof(char*));
  if (!(Xs)) {
    free(SL);
    printf("ERRO");
    return 0;
  }
  for (int i = 0; i < SL->num_v; i++)
  {
    Xs[i] = (char*) malloc(10*sizeof(char));
    if (!(Xs[i])) {
      free(SL);
      printf("ERRO");
      return 0;
    }
  }
  
  char aux[10];

  for(int i = 0; i < SL->max_iter; i++)
  {
    for(int l = 0; l < SL->num_v; l++)
    {
      memset(aux, 0, sizeof(aux));
      sprintf(aux, "%d", l+1);          //gerando a variave que sera usada na derivada
      strcat(strcpy(Xs[l], "x"), aux);  //
    }
    for(int l = 0; l < SL->num_v; l++)
    {
      double tTotal = timestamp();
      res[l] = -evaluator_evaluate(SL->GRADIENTE[l], SL->num_v, Xs, X);
      *tempo += timestamp() - tTotal;   //calculando o tempo da derivação
    }
  }
  for (int i = 0; i < SL->num_v; i++)
  {
    free(Xs[i]);
  }
  free(Xs);
  
  return res;
}

//calculando a matriz hessiana
void calc_hes(SistLinear_t *SL, double * X, double *tempo, double ** m_aux)
{
  char aux[4];
  
  char **Xs = (char**) calloc(SL->num_v, sizeof(char*));
  if (!(Xs)) {
    free(SL);
    printf("ERRO");
    return;
  }
  for(int l = 0; l < SL->num_v; l++)
  {
    Xs[l] = (char*) malloc(10*sizeof(char));
    if (!(Xs[l])) {
      free(SL);
      printf("ERRO");
      return;
    }
  }

  for(int l = 0; l < SL->num_v; l++)
  {
    memset(aux, 0, sizeof(aux));
    sprintf(aux, "%d", l+1);          //gerando a variave que sera usada na derivada
    strcat(strcpy(Xs[l], "x"), aux);  //
  }

  for (int i = 0; i < SL->num_v; i++)
  {
    for(int l = 0; l < SL->num_v; l++)
    {
      double tTotal = timestamp();
      m_aux[i][l] = evaluator_evaluate(SL->HESSIANA[i][l], SL->num_v, Xs, X);
      *tempo += timestamp() - tTotal; //calculando o tempo da derivação
    }
  }
  for (int i = 0; i < SL->num_v; i++)
  {
    free(Xs[i]);
  }
  free(Xs);
  return;
}

//alocando espaço para o sistema linear
SistLinear_t *alocaSistLinear(unsigned int n) {

  SistLinear_t *SL = (SistLinear_t *) malloc(sizeof(SistLinear_t));

  if (SL) {
    SL->num_v = n;

    SL->GRADIENTE = (void**) calloc(n, sizeof(void*));
    if (!(SL->GRADIENTE)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }

    SL->HESSIANA = (void***) calloc(n, sizeof(void**));
    if (!(SL->HESSIANA)) {
      free(SL);
      printf("ERRO");
      return NULL;
    }
    for (int i = 0; i < n; i++)
    {
      SL->HESSIANA[i] = (void**) calloc(n, sizeof(void*));
      if (!(SL->HESSIANA[i])) {
        free(SL);
        printf("ERRO");
        return NULL;
      }
    }

    SL->eq_aux = (char*) calloc(4096, sizeof(char));
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
  for (int i = 0; i < SL->num_v; i++)
  {
    for (int z = 0; z < SL->num_v; z++)
      evaluator_destroy(SL->HESSIANA[i][z]);
    free(SL->HESSIANA[i]);
  }
  free(SL->HESSIANA);
  for (int i = 0; i < SL->num_v; i++)
    evaluator_destroy(SL->GRADIENTE[i]);
  free(SL->GRADIENTE);
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