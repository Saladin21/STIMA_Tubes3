# Tugas Besar 3 IF2211 Strategi Algoritma
Penerapan String Matching dan Regular Expression dalam Pembangunan Deadline Reminder Assistant
* [Penjelasan Singkat Program](#penjelasan-singkat-program)
* [Requirement](#requirement)
* [Penggalan Kode Program](#penggalan-kode-program)
* [Cara Menggunakan Program](#cara-menggunakan-program)
* [Fitur Program](#fitur-program)
* [Status](#status)
* [Author](#author)

## Penjelasan Singkat Program
ENDGAMEBOT adalah aplikasi *chatbot Deadline Reminder Assistant* berbahasa Python berbasis web dengan menggunakan perkakas *website* Flask. *Chatbot* ini berfungsi untuk membantu pengguna mengingat berbagai *deadline*, tanggal penting, dan *task*-*task* kuliah. Aplikasi ini memanfaatkan algoritma *String Matching* dan *Regular Expression* untuk menghasilkan luaran *chatbot* yang sesuai dengan perintah masukan pengguna.

## Requirement
- Python versi 3 :https://www.python.org/downloads/
- Flask
`pip3 install flask`
- sqlite3
`pip3 install sqlite3`

## Penggalan Kode Program
Algoritma Booyer-Moore Matching
```
def bmMatching(p, T):
    L = last(p)
    i = len(p)-1
    j = i
    count = 0
    found = False
    while (i < len(T) and not found):
        if (p[j].lower() == T[i].lower() and j >= 0):
            i -= 1
            if (j==0):
                found = True
            else:
                j -= 1
        else:
            if ((T[i].lower() in L.keys()) and L[T[i].lower()] < j):
                i += len(p) - L[T[i].lower()] - 1
            else:
                if ((T[i].lower() in L.keys()) and L[T[i].lower()] != -1):
                    i += (len(p)-1 - j) + 1
                else:
                    i += len(p)
            j = len(p) - 1
        count += 1
    return found
```

## Cara Menggunakan Program
* Melalui Terminal
1. Buka Terminal
2. Cari direktori src
3. Ketik perintah `python app.py`
4. Salin link localhost dan buka pada browser seperti Google Chrome
5. Program dibuka dan dapat dijalankan

* Melalui Website Hasil Deployment

Buka link https://endgamebot.herokuapp.com untuk mengakses website EndgameBot hasil web deploy

## Fitur Program
1. Menambahkan task baru
2. Melihat daftar task yang harus dikerjakan
3. Menampilkan deadline dari suatu task tertentu
4. Memperbarui task tertentu
5. Menandai bahwa suatu task sudah selesai dikerjakan

## Status
Finished

## Author
| Nama | NIM |
|------|-----|
| [Epata Tuah](https://github.com/epata) | 13519120 |
| [Ahmad Saladin](https://github.com/Saladin21) | 13519187 |
| [Prana Gusriana](https://github.com/pranagusriana) | 13519195|
