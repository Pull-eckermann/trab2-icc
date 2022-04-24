/* Código escrito por
    Anderson Aparecido do Carmo Frasão 
    GRR 20204069
    Erick Eckermann Cardoso 
    GRR 20186075
*/

#ifndef __METODO_DE_NEWTON_PADRAO__
#define __METODO_DE_NEWTON_PADRAO__

#include "SistLinear.h"

//função para aplicar o pivoteamento na matriz hessiana
void pivot(int n, double**hes, double * grad, int i);

//função para calcular o delta
void retrossubs(int n, double *delta, double**hes, double * grad);

//função para triangularizar a matriz hessiana
void triang(int n, double**hes, double * grad);

//função com a chamada para o procedimento eliminação de gauss
double* eliminacaoGauss(int n, double *delta, double**hes, double * grad);

//função principal para o metodo newton padrão
double ** Newton_Padrao(SistLinear_t *SL, double *TderivadasEG, double *TslEG, double ** m_aux);

#endif