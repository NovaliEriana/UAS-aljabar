from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'


@app.route('/')
def beranda():
    return render_template('index.html')


@app.route('/unggah', methods=['POST'])
def unggah_gambar():
    # Jika ada file yang diunggah
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Simpan gambar yang diunggah
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Proses refleksi berdasarkan pilihan
            jenis_refleksi = request.form.get('reflection_type')
            gambar_terproses_path = proses_refleksi(filepath, jenis_refleksi)

            # Kirim nama gambar yang diproses ke template
            return render_template('index.html', processed_image=gambar_terproses_path)

    # Jika ada gambar yang sudah dipilih untuk refleksi (tanpa unggah file baru)
    elif 'previous_image' in request.form:
        gambar_sebelumnya = request.form.get('previous_image')
        jenis_refleksi = request.form.get('reflection_type')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], gambar_sebelumnya)
        
        gambar_terproses_path = proses_refleksi(filepath, jenis_refleksi)

        # Kirim nama gambar yang diproses ke template
        return render_template('index.html', processed_image=gambar_terproses_path)


def proses_refleksi(filepath, jenis_refleksi):
    img = cv2.imread(filepath)

    # Proses refleksi berdasarkan jenis
    if jenis_refleksi == 'horizontal':
        gambar_refleksi = cv2.flip(img, 1)  # Refleksi horizontal
    elif jenis_refleksi == 'vertical':
        gambar_refleksi = cv2.flip(img, 0)  # Refleksi vertikal
    elif jenis_refleksi == 'both':
        gambar_refleksi = cv2.flip(img, -1)  # Refleksi horizontal dan vertikal
    else:
        gambar_refleksi = img  # Jika jenis tidak valid, tampilkan gambar asli

    # Simpan hasil refleksi
    nama_file = 'reflected_' + os.path.basename(filepath)
    gambar_terproses_path = os.path.join(app.config['UPLOAD_FOLDER'], nama_file)
    cv2.imwrite(gambar_terproses_path, gambar_refleksi)

    # Kembalikan path gambar hasil
    return nama_file


@app.route('/static/images/<filename>')
def tampilkan_gambar(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
