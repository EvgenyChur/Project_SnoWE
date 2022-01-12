#-------------------------------------------------------------------------------
#
# Current code owner:
#
#   Roshydromet
#
# Authors:
#
#   Hydrometeorological Research Center of Russia, 2015-2017
#   Ekaterina Kazakova, Mikhail Chumakov, Inna Rozinkina,
#   Vladimir Kopeykin, Evgeny Churiulin
#   phone:  +7(499)795-23-59
#   email:  catherine.kazakova@mail.ru, inna.rozinkina@mail.ru,
#   v.v.kopeykin@mail.ru, evgenychur@gmail.com
#
#-------------------------------------------------------------------------------

SOLUTION = smfecalc.ex

FC = ifort
FCFLAGS = -i4 -r8 -check bounds -Wl,--trace -extend_source
FLFLAGS =

LIBS =

COMMONPATH = ../common/
COMMONOBJS = $(wildcard $(COMMONPATH)*.o)

SOURCES = $(wildcard *.f90)
MODOBJS = $(patsubst %.f90, %.o, $(filter mod_%.f90, $(SOURCES)))
OBJS = $(patsubst %.f90, %.o, $(filter-out mod_%.f90, $(SOURCES)))

ALL: $(SOLUTION)

$(SOLUTION): $(COMMONOBJS) $(MODOBJS) $(OBJS)
	$(FC) -o $@ $(FCFLAGS) $(FLFLAGS) $^ $(LIBS)

%.o: %.f90
	$(FC) -c $(FCFLAGS) $(FLFLAGS) $< -I$(COMMONPATH)

clean:
	rm -rf *.o *.mod *.ex
