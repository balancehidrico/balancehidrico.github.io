#!/usr/bin/env python
# coding: utf-8

# # Playa Potrero, Santa Cruz, Guanacaste (Zona Bosques 4). Junio 2011.

# ## Resumen
# 
# Este programa en Python recibe como entradas, para un área geográfica y un período de tiempo determinados:
# 
# - Un archivo CSV con datos de suelo (ej. capacidad de infiltración, densidad, profundidad de raíces, capacidad de campo).
# - Un archivo CSV con datos mensuales meteorológicos de precipitación y evapotranspiración.
# 
# Como salida, el programa genera:
# - Un modelo de balance hídirico de suelo basado en el método de Gunther Schosinsky {cite}`schosinsky_calculo_2006`, el cual muestra la recarga potencial de acuíferos, y otros datos relacionados, para cada mes del período en el área geográfica de estudio.

# ## Simbología
# 
# `fc`: Capacidad de Infiltración.  
# `I`: Infiltración.  
# `CC`: Capacidad de Campo.  
# `PM`: Punto de Marchitez.  
# `PR`: Profundidad de Raices.  
# `(CC-PM)`: Rango de Agua Disponible.  
# `DS`: Densidad de Suelo.  
# `C1`: Factor de ETP, por cierre de estomas, antes que ocurra ETR.  
# `C2`: Factor de ETP, por cierre de estomas, después que ocurre ETR.  
# `Kp`: Factor por pendiente.  
# `Kv`: Factor por vegetación.  
# `Kfc`: Factor estimado con base a la prueba de infiltración. 
# `P`: Precipitación Media Mensual.  
# `Pi`: Precipitación que infilta.  
# `ESC`: Escorrentía Superficial.  
# `ETP`: Evapotranspiración Potencial.  
# `ETR`: Evapotranspiración Real.  
# `HSi`: Humedad de Suelo Inicial.  
# `HD`: Humedad Disponible.  
# `HSf`: Humedad de Suelo Final.  
# `DCC`: Déficit de Capacidad de Campo.  
# `Rp`: Recarga Potencial.  
# `NR`: Necesidad de Riego.  
# `Ret`: Retención de lluvia.

# In[1]:


import math
import pandas as pd
import plotly.express as px


# ## Datos de suelo

# In[2]:


# Cálculos de textura

def kfc(row):
    if (row['fc'] < 16):
        return 0.0148*row['fc']/16
    else:
        if (row['fc'] > 1568):
            return 1
        else:
            return 0.267 * math.log(row['fc']) - 0.000154 * (row['fc']) - 0.723
        
def i(row):
    if (row['kp'] + row['kv'] + row['kfc'] > 1):
        return 1
    else:
        return row['kp'] + row['kv'] + row['kfc']
    
def cc_pm(row):
    return row['cc'] - row['pm']


# In[3]:


textura = pd.read_csv("datos/textura.csv")

textura['kfc'] = textura.apply (lambda row: kfc(row), axis=1)
textura['i'] = textura.apply (lambda row: i(row), axis=1)
textura['cc_pm'] = textura.apply (lambda row: cc_pm(row), axis=1)

textura


# In[4]:


lluvia_retenida = textura.iloc[0, 12]
print("lluvia_retenida =", lluvia_retenida)


# In[5]:


i = textura.iloc[0, 4]
print("i =", i)


# In[6]:


mes_inicial = textura.iloc[0, 11]
print("mes_inicial =", mes_inicial)


# In[7]:


hsi = textura.iloc[0, 7]
print("hsi =", hsi)


# ## Datos meteorológicos

# In[8]:


# Cálculos de meses

def ret(row):
    if (row['p'] <= 5):
        return row['p']
    else:
        if (row['p'] * lluvia_retenida > 5):
            return row['p']*lluvia_retenida
        else:
            return 5
        
def pi(row):
    return (row['p'] - row['ret']) * i

def esc(row):
    return row['p'] - row['ret'] - row['pi']

def etr(row):
    if (row['hd'] >= (row['c1'] + row['c2'])/2 * row['etp']):
        return (row['c1'] + row['c2'])/2 * row['etp']
    else:
        row['hd']
        
def rp(row):
    return row['pi'] + row['hsi'] - row['hsf'] - row['etr']

def nr(row):
    return row['dcc'] - row['etr'] + row['etp']


# In[9]:


meses = pd.read_csv("datos/meses.csv")

meses['ret'] = meses.apply(lambda row:ret(row), axis=1)
meses['pi'] = meses.apply(lambda row:pi(row), axis=1)
meses['esc'] = meses.apply(lambda row:esc(row), axis=1)

meses['etr'] = meses.apply(lambda row:etr(row), axis=1)

meses['rp'] = meses.apply(lambda row:rp(row), axis=1)
meses['nr'] = meses.apply(lambda row:nr(row), axis=1)


# ## Modelo de balance hídrico

# In[10]:


meses


# In[11]:


fig = px.line(meses, x="mes", y=meses.columns[[1,2,3,4,5,6,9,10,11,12,13,14]])

fig.show()


# ## Referencias bibliográficas
# ```{bibliography}
# :filter: docname in docnames
# ```

# In[ ]:




