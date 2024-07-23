from flask import Flask, request, render_template
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from fuzzy_set import FuzzySet, plot_membership_functions  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama_kasus = request.form["nama_kasus"]
        nama_variabel = request.form["nama_variabel"]
        
        himpunan_list = []
        jumlah_kategori = request.form["jumlah_kategori"]
        if not jumlah_kategori.isdigit():
            return "Jumlah kategori harus berupa angka.", 400
        jumlah_kategori = int(jumlah_kategori)
        
        for i in range(jumlah_kategori):
            nama_himpunan = request.form[f"nama_himpunan_{i}"]
            method = request.form[f"method_{i}"].strip().lower()
            
            if method == "linear up" or method == "linear down":
                rendah = float(request.form[f"rendah_{i}"])
                tinggi = float(request.form[f"tinggi_{i}"])
                himpunan_list.append(FuzzySet(nama_himpunan, [rendah, tinggi], method))
            elif method == "triangular":
                rendah = float(request.form[f"rendah_{i}"])
                puncak = float(request.form[f"puncak_{i}"])
                tinggi = float(request.form[f"tinggi_{i}"])
                himpunan_list.append(FuzzySet(nama_himpunan, [rendah, puncak, tinggi], method))
            elif method == "trapezoidal":
                a = float(request.form[f"a_{i}"])
                b = float(request.form[f"b_{i}"])
                c = float(request.form[f"c_{i}"])
                d = float(request.form[f"d_{i}"])
                himpunan_list.append(FuzzySet(nama_himpunan, [a, b, c, d], method))
            else:
                raise ValueError("Metode tidak dikenali.")
        
        min_value = float(request.form["min_value"])
        max_value = float(request.form["max_value"])
        x_value = float(request.form["x_value"])
        
        plot_url = plot_membership_functions(himpunan_list, x_value, min_value, max_value)
        
        results = [(himpunan.name, himpunan.get_membership_degree(x_value)) for himpunan in himpunan_list]
        
        return render_template("index.html", 
                            nama_kasus=nama_kasus, 
                            nama_variabel=nama_variabel, 
                            x_value=x_value, 
                            results=results, 
                            plot_url=plot_url)
    
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)