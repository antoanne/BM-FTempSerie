# -*- coding: latin-1 -*-
"""
@author: Antoanne Pontes
@description: Trabalho de Modelagem e Mineração de dados
@title: Análise de séries temporais
"""
from numpy import loadtxt
from matplotlib.pyplot import plot, scatter, boxplot, show, title, legend, figure
from scipy import linspace, polyval, polyfit, sqrt, stats, randn, array
from scipy.stats import describe, cumfreq
from scipy.stats.kde import gaussian_kde
from pylab import hist
import string
import csv

datapath = "/home/antoanne/Dropbox/Work-2011/Mestrado/Modelagem/trab1-bovespa/"
nome_dt_pres = "presidentes-br.csv"
nome_dt_bove = "bovespa.csv"
dolar_dataset = "dolar_venda.csv"

dt_bove = loadtxt(datapath+nome_dt_bove, delimiter=',', 
                  skiprows = 2, converters = {0: datestr2num},
                  dtype={
                      'names': ('date','open','high','low','close','volume','adj_close'),
                      'formats': ('i','f','f','f','f','f','f')
                  })

dt_pres = loadtxt(datapath+nome_dt_pres, delimiter=',', skiprows = 2, 
                  converters = {1: lambda s: string.replace(s,'"',''),
                                2: datestr2num, 
                                3: datestr2num}, 
                  usecols=(0,1,2,3,4),
                  dtype={
                      'names': ('id','nome','inicio','fim','partido'),
                      'formats': ('i4','S40','i4','i4','S10')
                  })


dolar = loadtxt(datapath+dolar_dataset, delimiter=';', 
                  skiprows = 1, converters = {0: datestr2num},
                  dtype={
                      'names': ('data','fechamento'),
                      'formats': ('i','f')
                  })


# ------------------------------

# Primeira avaliação - Day trading
max_date, alta = 0, 0
min_date, queda = 0, 0
count = 0
for o in dt_bove[:]['date']:
    if ((dt_bove[count]['close'] - dt_bove[count]['open']) >= alta):
        max_date = dt_bove[count]['date']
        alta = (dt_bove[count]['close'] - dt_bove[count]['open'])
    if ((dt_bove[count]['close'] - dt_bove[count]['open']) <= queda):
        min_date = dt_bove[count]['date']
        queda = (dt_bove[count]['close'] - dt_bove[count]['open'])
    count = count + 1

# maior alta no dia
num2date(max_date)
dt_bove[dt_bove[:]['date'] == max_date][:]
# maior queda no dia
num2date(min_date)
dt_bove[dt_bove[:]['date'] == min_date][:]

# ------------------------------

# Evolução Bovespa
plot(dt_bove[:]['date'], dt_bove[:]['open'],'r')

# ------------------------------

# Figura 1
# Evolução Bovespa sem corte
title('Mudanças presidenciais e Bovespa'.decode('utf-8'))
plot(dt_bove[3559:]['date'], dt_bove[3559:]['open'],'k')
plot(dt_bove[0:3559]['date'], dt_bove[0:3559]['open']*10,'k')
# Mudanças presidenciais
plot(dt_pres[0:1]['inicio'], [15000],'^r', label=dt_pres[0]['nome'].decode('utf-8') + " " + dt_pres[0]['partido'],
     markerfacecolor='r', markersize=16)
plot(dt_pres[1:2]['inicio'], [15000],'*r', label=dt_pres[1]['nome'].decode('utf-8') + " " + dt_pres[1]['partido'],
     markerfacecolor='r', markersize=16)
plot(dt_pres[2:3]['inicio'], [15000],'sb', label=dt_pres[2]['nome'].decode('utf-8') + " " + dt_pres[2]['partido'],
     markerfacecolor='b', markersize=14)
plot(dt_pres[3:4]['inicio'], [15000],'Dy', label=dt_pres[3]['nome'].decode('utf-8') + " " + dt_pres[3]['partido'],
     markerfacecolor='y', markersize=14)
xlabel('Data')
ylabel('Pontos')
legend(loc='upper left', numpoints=1)

# ------------------------------

# Figura 2
# Oscilações Bovespa
title('Oscilações Bovespa'.decode('utf-8'))
plot(dt_bove[:]['date'], dt_bove[:]['close'] - dt_bove[:]['open'])
# Mudanças presidenciais
plot(dt_pres[0:1]['inicio'], [0],'^r', label=dt_pres[0]['nome'].decode('utf-8') + " " + dt_pres[0]['partido'],
     markerfacecolor='r', markersize=16)
plot(dt_pres[1:2]['inicio'], [0],'*r', label=dt_pres[1]['nome'].decode('utf-8') + " " + dt_pres[1]['partido'],
     markerfacecolor='r', markersize=16)
plot(dt_pres[2:3]['inicio'], [0],'sb', label=dt_pres[2]['nome'].decode('utf-8') + " " + dt_pres[2]['partido'],
     markerfacecolor='b', markersize=14)
plot(dt_pres[3:4]['inicio'], [0],'Dy', label=dt_pres[3]['nome'].decode('utf-8') + " " + dt_pres[3]['partido'],
     markerfacecolor='y', markersize=14)
xlabel('Data')
ylabel('Pontos')
legend(loc='upper center', numpoints=1)

# ------------------------------

spamWriter = csv.writer(open(datapath+'bovespaV3.csv', 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='excel')
spamWriter.writerow(['inicio','fim','diff'])

# [data,pontos] len(dt_bove[:])-1
dados = []
positivo = True
inicio = max(dt_bove[:]['date'])
count, pontos = 0, 0
for o in dt_bove[:]['date']:
    row = ()
    if ((dt_bove[count]['close'] - dt_bove[count]['open']) >= 0):
        if (positivo):
            pontos = pontos + (dt_bove[count]['close'] - dt_bove[count]['open'])
            fim = dt_bove[count]['date']
        else:
            if (pontos):
                l = []
                l.append(fim)
                l.append(inicio)
                l.append(pontos)
                spamWriter.writerow(l)
            pontos = (dt_bove[count]['close'] - dt_bove[count]['open'])
            inicio = dt_bove[count]['date']
            fim = dt_bove[count]['date']
            positivo = True
    else:
        if (positivo):
            if (pontos):
                l = []
                l.append(fim)
                l.append(inicio)
                l.append(pontos)
                spamWriter.writerow(l)
            pontos = (dt_bove[count]['close'] - dt_bove[count]['open'])
            inicio = dt_bove[count]['date']
            fim = dt_bove[count]['date']
            positivo = False
        else:
            pontos = pontos - (dt_bove[count]['close'] - dt_bove[count]['open'])
            fim = dt_bove[count]['date']
    count = count + 1

dt_boveV3 = loadtxt(datapath+"bovespaV3.csv", delimiter=',', skiprows = 1,
                  dtype={
                      'names': ('inicio','fim','volume'), 'formats': ('i','i','f')
                      })

# Acumulado por "sinal"
plot(dt_boveV3[:]['inicio'],dt_boveV3[:]['volume'])
title('Acumulado, positivo e negativo'.decode('utf-8'))
xlabel('Data')
ylabel('Pontos')
grid()
legend(loc='upper center', numpoints=1)

dt_boveV3_neg = sorted(dt_boveV3[:], key=lambda x: x[2])
dt_boveV3_pos = sorted(dt_boveV3[:], key=lambda x: x[2], reverse=True)

# Melhores e piores dias
print "Início    | Fim        | Volume"
for d in dt_boveV3_pos[:10]:
    print num2date(d[0]).strftime("%d/%m/%y"), ' | ', num2date(d[1]).strftime("%d/%m/%y"), ' | ', d[2]

print "Início    | Fim        | Volume"
    for d in dt_boveV3_neg[:10]:
    print num2date(d[0]).strftime("%d/%m/%y"), ' | ', num2date(d[1]).strftime("%d/%m/%y"), ' | ', d[2]




# TODO: Incluir marcações nas faixas de dados
# ax.fill_between(x, y1, y2, where=y2>=y1, facecolor='green', interpolate=True)


    
# TODO: Criar plot das mudanças presidenciais
# Mudanças presidenciais
# plot(dt_pres[0:2]['inicio'], dt_pres[0:2]['id']*200,'*r', label=dt_pres[0]['partido'],
#      markerfacecolor='r', markersize=16)


