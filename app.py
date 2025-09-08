import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "perpus.db" #Mendefinisikan nama database

def connectdb():#: Membuat koneksi ke database
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():# Membuat tabel jika belum ada dengan kolom:
    conn = connectdb()
    conn.execute('''CREATE TABLE IF NOT EXISTS peminjaman (
                        id_peminjaman INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama_peminjam VARCHAR(100) NOT NULL,
                        nama_buku VARCHAR(100) NOT NULL,
                        tanggal_peminjaman TEXT NOT NULL,
                        tanggal_pengembalian TEXT NOT NULL
                    );''')
    conn.commit()
    conn.close()

#Halaman utama
@app.route('/')
def index():
    conn = connectdb()
    pinjam = conn.execute("SELECT * FROM peminjaman").fetchall()#Menampilkan semua data peminjaman dari database
    conn.close()
    return render_template('index.html', pinjam=pinjam)#Mengirim data buku ke template index.html

#Halaman tambah
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama_peminjam = request.form['nama_peminjam']
        nama_buku = request.form['nama_buku']
        tanggal_peminjaman = request.form['tanggal_peminjaman']
        tanggal_pengembalian = request.form['tanggal_pengembalian']
        conn = connectdb()
        conn.execute("INSERT INTO peminjaman (nama_peminjam, nama_buku, tanggal_peminjaman, tanggal_pengembalian ) VALUES (?, ?, ?, ?)", (nama_peminjam, nama_buku, tanggal_peminjaman, tanggal_pengembalian))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    conn = connectdb()
    peminjaman = conn.execute("SELECT * FROM peminjaman WHERE id_peminjaman = ?", (id,)).fetchone()
    if not peminjaman:
        return "Data peminjaman tidak ditemukan", 404
    
    if request.method == 'POST':
        nama_peminjam = request.form['nama_peminjam']
        nama_buku = request.form['nama_buku']
        tanggal_peminjaman = request.form['tanggal_peminjaman']
        tanggal_pengembalian = request.form['tanggal_pengembalian']
        conn.execute("UPDATE peminjaman SET nama_peminjam = ?, nama_buku = ?, tanggal_peminjaman = ?, tanggal_pengembalian = ?  WHERE id_peminjaman = ?", (nama_peminjam, nama_buku, tanggal_peminjaman, tanggal_pengembalian, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', peminjaman=peminjaman)

@app.route('/delete/<int:id>')
def delete(id):
    conn = connectdb()
    conn.execute("DELETE FROM peminjaman WHERE id_peminjaman = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)