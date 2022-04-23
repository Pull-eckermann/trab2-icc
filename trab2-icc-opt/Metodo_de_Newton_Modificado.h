/* Código escrito por
    Anderson Aparecido do Carmo Frasão 
    GRR 20204069
    Erick Eckermann Cardoso 
    GRR 20186075
*/

#ifndef __METODO_DE_NEWTON_MODIFICADO__
#define __METODO_DE_NEWTON_MODIFICADO__

#include "SistLinear.h"

//função para aplicar o pivoteamento na matriz hessiana
void pivotLU(S_FatLU *LU, int n, int i, double**hes, double * grad);

//função para calcular o vetor z
void retrossubpz(S_FatLU *LU, int n, double * grad);

//função para calcular o delta
void retrossubs2(double *z, int n, double**hes, double *delta);

//função para triangularizar a matriz hessiana
void triangLU(S_FatLU *LU, int n, double**hes, double * grad);

//função com a chamada para o procedimento fatoração LU
double * FatLU(S_FatLU *LU, int n, double *delta, double**hes, double * grad);

//função principal para o metodo newton Modificado
double ** Newton_Modificado(SistLinear_t *SL, S_FatLU *LU, double *Xlu, double *TderivadasLU, double *TslLU, double ** m_aux);

#endif