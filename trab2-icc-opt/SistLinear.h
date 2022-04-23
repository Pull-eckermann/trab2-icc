/* Código escrito por
    Anderson Aparecido do Carmo Frasão 
    GRR 20204069
    Erick Eckermann Cardoso 
    GRR 20186075
*/

#ifndef __SIST_LINEAR__
#define __SIST_LINEAR__

#include "utils.h"
#include <assert.h>

typedef struct {
  double *Xeg;          //vetor de resultados finais eliminacao
  double *Xlu;          //vetor de resultados finais fat LU
  double *Xgs;          //vetor de resultados finais Gauss
} Res_SL;

typedef struct {
  unsigned int num_v;   // numero de variaveis
  char *eq_aux;         //strings com equacao auxiliar pra montagem da matriz
  double epsilon;       //tolerancia no metodo de gauss seidel
  int max_iter;         //numero maximo de iterações
  Res_SL *Respostas;
} SistLinear_t;

typedef struct {
  double **L;           // matriz dos multiplicadores (LESS)
  double *z;            // vetor z para Fatoração LU
} S_FatLU;

//calcula o vetor gradiente
double * calc_grad(int n, double * X, double *tempo);

//calculando a matriz hessiana
void calc_hes(int n, double * X, double *tempo, double ** m_aux);

S_FatLU *alocaFatLU(unsigned int n);

Res_SL *alocaRes(int n);

//alocando espaço para o sistema linear
SistLinear_t *alocaSistLinear(unsigned int n);

void liberaFatLU(S_FatLU *LU, int n);

void libera_aux(double **m_aux, double **m_reseg, double **m_resgs, int num_v, int max_iter);

//liberando a alocação de memoria
void liberaSistLinear(SistLinear_t *SL);

//lendo o sistema linear
SistLinear_t *lerSistLinear();

#endif