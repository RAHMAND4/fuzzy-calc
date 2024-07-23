import matplotlib.pyplot as plt
import numpy as np
import io
import base64

class FuzzySet:
    def __init__(self, name, domain, method):
        self.name = name
        self.domain = domain
        self.method = method
        if method == "triangular":
            self.membership_function = self.triangular
        elif method == "trapezoidal":
            self.membership_function = self.trapezoidal
        elif method == "linear up":
            self.membership_function = self.linear_up
        elif method == "linear down":
            self.membership_function = self.linear_down
        else:
            raise ValueError("Metode tidak dikenali.")

    def get_membership_degree(self, x):
        return self.membership_function(x)

    def triangular(self, x):
        a, b, c = self.domain
        if a <= x <= b:
            return (x - a) / (b - a)
        elif b <= x <= c:
            return (c - x) / (c - b)
        elif x==b:
            return 1
        else:
            return 0

    def trapezoidal(self, x):
        a, b, c, d = self.domain
        if x <= a or x >= d:
            return 1
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x <= c:
            return 1
        elif c < x < d:
            return (d - x) / (d - c)
        else:
            return 0
    
    def linear_up(self, x):
        a, b = self.domain
        if x >= b:
            return 1
        elif a <= x < b:
            return (x - a) / (b - a)
        else:
            return 0
    
    def linear_down(self, x):
        a, b = self.domain
        if x <= a:
            return 1
        elif a < x <= b:
            return (b - x) / (b - a)
        else:
            return 0

def plot_membership_functions(himpunan_list, x_value, min_value, max_value):
    x = np.linspace(min_value, max_value, 400)
    
    plt.figure()
    
    for himpunan in himpunan_list:
        y = [himpunan.get_membership_degree(val) for val in x]
        plt.plot(x, y, label=himpunan.name)
        
    for himpunan in himpunan_list:
        y_value = himpunan.get_membership_degree(x_value)
        plt.scatter(x_value, y_value, marker='o', color='red')  
        
    plt.axvline(x=x_value, color='red', linestyle='--')
    
    plt.xlabel('Semesta pembicaraan')
    plt.ylabel('Derajat keanggotaan')
    plt.title('Fuzzy Membership Functions')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Pindahkan legenda ke luar plot
    plt.grid(True)
    
    # Simpan plot ke dalam buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')  # Tambahkan bbox_inches='tight' untuk memastikan semua elemen plot disimpan
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    
    return plot_url

def main():
    print("Input Nama Kasus:")
    nama_kasus = input()

    print("Input Nama Variabel:")
    nama_variabel = input("Nama Variabel: ")
    
    print("Masukkan jumlah record:")
    jumlah_record = int(input())
    
    x_values = []
    for i in range(jumlah_record):
        x_value = float(input(f"Masukkan Kasus {nama_variabel} untuk record ke- {i+1}: "))
        x_values.append(x_value)
    
    himpunan_list = []

    print("Masukkan jumlah kategori himpunan:")
    jumlah_kategori = int(input())

    for i in range(jumlah_kategori):
        print(f"Input Nama Himpunan dan Domain untuk kategori {i+1}:")
        nama_himpunan = input(f"Nama Himpunan ke-{i+1}: ")
        
        method = input(f"Pilih metode untuk {nama_himpunan} (linear up, linear down, triangular, trapezoidal): ").strip().lower()

        if method == "linear up" or method == "linear down":
            rendah = float(input(f"Input batas rendah dari himpunan {nama_himpunan}: "))
            tinggi = float(input(f"Input batas tinggi dari himpunan {nama_himpunan}: "))
            himpunan_list.append(FuzzySet(nama_himpunan, [rendah, tinggi], method))
        elif method == "triangular":
            rendah = float(input(f"Input batas rendah dari himpunan {nama_himpunan}: "))
            puncak = float(input(f"Input nilai puncak dari himpunan {nama_himpunan}: "))
            tinggi = float(input(f"Input batas tinggi dari himpunan {nama_himpunan}: "))
            himpunan_list.append(FuzzySet(nama_himpunan, [rendah, puncak, tinggi], method))
        elif method == "trapezoidal":
            a = float(input(f"Input batas rendah dari himpunan {nama_himpunan}: "))
            b = float(input(f"Input nilai naik pertama dari himpunan {nama_himpunan}: "))
            c = float(input(f"Input nilai naik kedua dari himpunan {nama_himpunan}: "))
            d = float(input(f"Input batas tinggi dari himpunan {nama_himpunan}: "))
            himpunan_list.append(FuzzySet(nama_himpunan, [a, b, c, d], method))
        else:
            raise ValueError("Metode tidak dikenali.")

    min_value = float(input("Masukkan nilai minimal dari semesta pembicaraan: "))
    max_value = float(input("Masukkan nilai maksimal dari semesta pembicaraan: "))
    print(f"Range diagram: {min_value} sampai {max_value}")
    
    x_value = float(input("Masukkan nilai X yang ingin diuji: "))
    print(f"Nilai X = {x_value}:")
    for himpunan in himpunan_list:
        degree = himpunan.get_membership_degree(x_value)
        print(f"  Himpunan {himpunan.name}: {degree}")

    plot_url = plot_membership_functions(himpunan_list, x_value, min_value, max_value)

if __name__ == "__main__":
    main()