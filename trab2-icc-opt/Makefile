# Código escrito por
#    Anderson Aparecido do Carmo Frasão 
#    GRR 20204069
#    Erick Eckermann Cardoso 
#    GRR 20186075

CFLAGS = -Wall -g -DLIKWID_PERFMON -I /usr/local/include -O3 -mavx -march=native
LFLAGS = -lm -L /usr/local/lib -llikwid 

objs = main.o utils.o SistLinear.o Metodo_de_Newton_Inexato.o Metodo_de_Newton_Modificado.o Metodo_de_Newton_Padrao.o Rosenbrock.o

all: newtonPC

newtonPC: $(objs)
	gcc $(objs) -o newtonPC $(CFLAGS) $(LFLAGS)
        
main.o: main.c
	cc -c main.c $(CFLAGS)
utils.o: utils.c
	cc -c utils.c $(CFLAGS) 
SistLinear.o: SistLinear.c
	cc -c SistLinear.c $(CFLAGS)  
Metodo_de_Newton_Inexato.o: Metodo_de_Newton_Inexato.c
	cc -c Metodo_de_Newton_Inexato.c $(CFLAGS) 
Metodo_de_Newton_Modificado.o: Metodo_de_Newton_Modificado.c
	cc -c Metodo_de_Newton_Modificado.c $(CFLAGS)
Metodo_de_Newton_Padrao.o: Metodo_de_Newton_Padrao.c
	cc -c Metodo_de_Newton_Padrao.c $(CFLAGS) 
Rosenbrock.o: Rosenbrock.c
	cc -c Rosenbrock.c $(CFLAGS) 
                        
clean:
	-rm -f *.o *~ 
        
purge: clean
	-rm -f newtonPC