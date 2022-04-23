#include <stdio.h>
#include <string.h>
#include <math.h>
#include "utils.h"

/*  Retorna tempo em milisegundos

    Forma de uso:
 
    double tempo;
    tempo = timestamp();
    <trecho de programa do qual se deseja medir tempo>
    tempo = timestamp() - tempo;
*/

char* markerName(char* baseName, int n)
{
  char* mark = (char*) malloc( (strlen(baseName)+1) + (log10(n)+1) + 1 );

  sprintf(mark, "%s_%u", baseName,n);

  // printf("*** %s\n", mark);

  return mark;

}

double timestamp(void)
{
  struct timeval tp;
  gettimeofday(&tp, NULL);
  return((double)(tp.tv_sec*1000.0 + tp.tv_usec/1000.0));
}

void prnVetorFloat(float *v, int n) {
	for (int i = 0; i < n; ++i)
		printf("%g ", v[i]);
	printf("\n");
}

void prnVetorDouble(double *v, int n) {
	for (int i = 0; i < n; ++i)
		printf("%lg ", v[i]);
	printf("\n");
}

void prnVetorLongDouble(long double *v, int n) {
	for (int i = 0; i < n; ++i)
		printf("%Lg ", v[i]);
	printf("\n");
}
