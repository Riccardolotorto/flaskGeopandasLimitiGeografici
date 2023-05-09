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
province3857 = province.to_crs(3857)
rip3857 = ripartizioni_geografiche.to_crs(3857)
regioni3857 = regioni.to_crs(3857)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/es1')
def es1():
    listaRegioni = list(set(regioni["DEN_REG"]))
    listaRegioni.sort()
    return render_template('risultato.html', lista = listaRegioni)

@app.route('/es2')
def es2():
    regioni_ripartizioni = regioni.groupby("COD_RIP")[["DEN_REG"]].count().reset_index()
    regioni_ripartizioni = regioni_ripartizioni.merge(ripartizioni_geografiche, on = "COD_RIP")
    dizionario = dict(zip(regioni_ripartizioni["DEN_RIP"], regioni_ripartizioni["DEN_REG"]))
    return render_template('risultato.html', dizionario = dizionario)

@app.route('/es3', methods = ["GET"])
def es3():
    regione = request.args.get("regione")
    regione_scelta = regioni[regioni["DEN_REG"] == regione.capitalize()].to_crs(3857)
    ax = regione_scelta.plot(figsize = (12, 8), edgecolor = "k", facecolor = "none")
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "graf1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('mappa.html', immagine = file_name)

@app.route('/es4', methods = ["GET"])
def es4():
    regione = request.args.get("regione2")
    regione_scelta = regioni[regioni["DEN_REG"] == regione.capitalize()].to_crs(3857)
    province_regioni = province3857[province3857.within(regione_scelta.geometry.item())]
    ax = province_regioni.plot(figsize = (12, 8), edgecolor = "red", facecolor = "none")
    regione_scelta.plot(ax = ax, edgecolor = "k", facecolor = "none")
    ctx.add_basemap(ax)
    
    dir = "static/images"
    file_name = "graf2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('mappa.html', immagine = file_name)

@app.route('/es5', methods = ["GET"])
def es5():
    regione = request.args.get("regione3")
    regione_scelta = regioni[regioni["DEN_REG"] == regione.capitalize()].to_crs(3857)
    province_regioni = province3857[province3857.within(regione_scelta.geometry.item())]
    from shapely.ops import cascaded_union
    itaOggetto = cascaded_union(rip3857.geometry)
    italia = gpd.GeoSeries(itaOggetto)
    ax = province_regioni.plot(figsize = (12, 8), edgecolor = "red", facecolor = "none")
    regione_scelta.plot(ax = ax, edgecolor = "k", facecolor = "none")
    italia.plot(ax = ax, facecolor = "none", edgecolor = "blue", linewidth = 2)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "graf3.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('mappa.html', immagine = file_name)

@app.route('/es6', methods = ["GET"])
def es6():
    regione = request.args.get("regione4")
    regione_scelta = regioni[regioni["DEN_REG"] == regione.capitalize()].to_crs(3857)
    regioniConfinanti = regioni3857[regioni3857.touches(regione_scelta.geometry.item())]
    ax = regioniConfinanti.plot(figsize = (12, 8), edgecolor = "k", facecolor = "none")  
    ctx.add_basemap(ax)
    r = regioniConfinanti[["DEN_REG"]].to_html()

    dir = "static/images"
    file_name = "graf4.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('mappa.html', immagine = file_name, tabella = r)

@app.route('/es7')
def es7():
    regioni3857["Shape_Area"] = regioni3857["Shape_Area"] / 1000000
    reg = regioni3857[["DEN_REG", "Shape_Area"]].sort_values(by = "Shape_Area", ascending = False).to_html()
    return render_template('mappa.html', tabella = reg)

@app.route('/es8')
def es8():
    reg = regioni3857[["DEN_REG", "Shape_Area"]].sort_values(by = "Shape_Area", ascending = False).reset_index()
    labels = reg["DEN_REG"]
    dati = reg["Shape_Area"]

    
    fig, ax = plt.subplots(figsize=(15,11))
    ax.bar(labels, dati, label='estensione per ogni regione italiana')
    plt.xticks(rotation = 80)
    ax.set_ylabel('estensione (kmQ)')
    ax.set_title('regioni')
    ax.legend()

    dir = "static/images"
    file_name = "g1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)

    fig, ax = plt.subplots(figsize=(15,11))
    ax.barh(labels, dati, label='estensione per ogni regione italiana')
    ax.set_ylabel('regione')
    ax.set_title('estensione (kmQ)')
    ax.legend()

    dir = "static/images"
    file_name = "g2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)

    plt.figure(figsize=(16, 8))
    plt.pie(dati, labels=labels, autopct='%1.1f%%')

    dir = "static/images"
    file_name = "g3.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('grafici.html')

@app.route('/es9', methods = ["GET"])
def es9():
    regione = request.args.get("regione5")
    regione_scelta = regioni[regioni["DEN_REG"] == regione.capitalize()].to_crs(3857)
    regioniNONConfinanti = regioni3857[~regioni3857.touches(regione_scelta.geometry.item())]
    ax = regioniNONConfinanti.plot(figsize = (12, 8), edgecolor = "k", facecolor = "none")  
    ctx.add_basemap(ax)
    r = regioniNONConfinanti[["DEN_REG"]].to_html()

    dir = "static/images"
    file_name = "graf5.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('mappa.html', immagine = file_name, tabella = r)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)