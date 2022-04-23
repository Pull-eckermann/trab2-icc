#ifndef __UTILS__
#define __UTILS__

#include <stdlib.h>
#include <sys/time.h>

char* markerName(char* baseName, int n);

double timestamp(void);

void prnVetorFloat(float *x, int n);

void prnVetorDouble(double *x, int n);

void prnVetorLongDouble(long double *x, int n);

#endif
