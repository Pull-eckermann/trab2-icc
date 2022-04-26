/*Alunos:
Anderson Aparecido do Carmo Frasão
GRR 20204069

Erick Eckermann Cardoso
GRR20186075
*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <likwid.h>

#include "Metodo_de_Newton_Inexato.h"
#include "SistLinear.h"
#include "utils.h"

//Recebe os independentes da iteração e retorna os valores convergindo para a raiz
double * calcula_independentes(int n, double **m_aux, double *grad, double * res)
{
  double result = 0.0;
  //Vetor que guarda os valores x1 .. xn
  double *indep = (double*) calloc(n, sizeof(double));
  if (!(indep)){
    printf("ERRO");
    return NULL;
  }
  for (int i = 0; i < n; i++)
    indep [i] = res[i];

  double m = 0.0;

  for(int i = 0; i < n && !isnan(m); i++){     //Alterna os valores x1 .. xn para cálculo dos seus resultados
    for(int j = 0; j < n; j++)
      result += m_aux[i][j] * indep[j];   //Calcula xi, avaliando os outros termos do poinômio de acordo com indep[]
    result -= m_aux[i][i] * indep[i];
    result = grad[i] - result; 
    m = m_aux[i][i];                      // NAO DA PARA FAZER LOOP UNROLLING
    result /= m;                          // DEVIDO A DEPENDENCIA DO PRIMEIRO FOR PARA OUTRAS VARIAVEIS
    indep[i] = result;                    //Guarda o resulado de xi para o calculo de xi+1
    result = 0.0; 
  }
  if (isnan(m))                           //Confere se não é divisão por zero
    printf("ERRO: NAN\n");                // TIRANDO IF DO FOR
  return indep;
}

// Método Gauss-Seidel para resolução de sistemas lineares
double * gaussSeidel(int num_v, double epsilon, double **m_aux, double *grad)
{
  double *res = (double*) calloc(num_v, sizeof(double));
  if (!(res)){
    printf("ERRO");
    return NULL;
  }
  double *prox_res;

  int i = 0;
  double num_maior = 0.0;
  double sub = 0.0;

  do{
    //Função que calcula valores de x1 .. xn da próxima iteração
    prox_res = calcula_independentes(num_v, m_aux, grad, res);
    for(int j = 0; j < num_v; j++){
      sub = prox_res[j] - res[j];
      if(sub >= num_maior){
        num_maior = sub;        // NAO DA PRA TIRAR ESSE IF POIS NUM_MAIOR 
      }                         // PODE MUDAR MAIS DE UMA VEZ
    }
    free(res);
    res = prox_res;  
    
    i++;
  //Critério de parada, vai no máximo até 50 iterações
  }while((i <= 50) && (num_maior > epsilon));

  return res;
}

//função principal para o metodo newton Inexato
double ** Newton_Inexato(SistLinear_t *SL, double *TderivadasGS, double * TlsGS, double ** m_aux)
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
    m_res[0][z] = SL->Respostas->Xgs[z];

  //for principal
  for (int i = 0; i < SL->max_iter; i++)
  {
    double aux = 0.0;

    //atualiza o vetor gradiente e a matriz hessiana
    char* name = markerName("Tderi_grad_Inexato_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    double * grad = calc_grad(SL->num_v, SL->Respostas->Xgs, TderivadasGS);
    LIKWID_MARKER_STOP(name);
    name = markerName("Tderi_hes_Inexato_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    calc_hes(SL->num_v, SL->Respostas->Xgs, TderivadasGS, m_aux);
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
          m_res[l][z] = NAN;                // NAO DA PRA TIRAR ESSE IF POIS
      return m_res;                         // POIS O METODO MANDA TER UM TESTE AQUI
    }
    
    double * delta;
    
    //calcula o vetor delta e o tempo de execução do calculo
    double tTotal = timestamp();
    name = markerName("T_Sist_Lin_Inexato_Opt", SL->num_v);
    LIKWID_MARKER_START(name);
    delta = gaussSeidel(SL->num_v, SL->epsilon, m_aux, grad);
    LIKWID_MARKER_STOP(name);
    *TlsGS += timestamp() - tTotal;

    for (int l = 0; l < SL->num_v; l++)
      SL->Respostas->Xgs[l] += delta[l];

    aux = 0.0;

    for (int i = 0; i < SL->num_v; i++)
      aux += delta[i]*delta[i];
    aux = sqrt(aux);

    //iteração i+1
    for(int z = 0; z < SL->num_v; z++)
      m_res[i+1][z] = SL->Respostas->Xgs[z];

    free(delta);

    //verifica se delta é menor que epsolon
    if(aux < SL->epsilon)
    {
      free(grad);
      for (int l = i+1; l < SL->max_iter; l++)
        for(int z = 0; z < SL->num_v; z++)
          m_res[l+1][z] = NAN;                // IDEM PRIMEIRO IF
      return m_res;
    }
    free(grad);
  }
  return m_res;
}