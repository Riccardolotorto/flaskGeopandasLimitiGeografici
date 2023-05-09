from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
import geopandas as gpd
import contextily as ctx
import os
import matplotlib.pyplot as plt

regioni = gpd.read_file("Regioni/Reg01012023_g_WGS84.dbf")
province = gpd.read_file("Province/ProvCM01012023_g_WGS84.dbf")
ripartizioni_geografiche = gpd.read_file("Ripartizioni/RipGeo01012023_g_WGS84.dbf")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/es1')
def es1():
    listaRegioni = list(set(regioni["DEN_REG"]))
    listaRegioni.sort()
    return render_template('risultato.html', lista = listaRegioni)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)