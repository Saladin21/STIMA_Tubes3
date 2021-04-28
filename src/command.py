from datetime import datetime
from BMMatching import bmMatching
import database
import re

bulan = {}
bulan["januari"] = "01"
bulan["februari"] = "02"
bulan["maret"] = "03"
bulan["april"] = "04"
bulan["mei"] = "05"
bulan["juni"] = "06"
bulan["juli"] = "07"
bulan["agustus"] = "08"
bulan["september"] = "09"
bulan["oktober"] = "10"
bulan["november"] = "11"
bulan["desember"] = "12"



# Menjalankan fitur sesuai masukan user atau memberikan pesan error jika perintah user tidak dikenali
def executeCommand(s):
    task = getTask(s)
    if (task):
        return task
    newtask = createTask(s)
    if (newtask):
        return newtask
    remove = removeTask(s)
    if (remove):
        return remove
    update = updateTask(s)
    if (update):
        return update
    help = showHelp(s)
    if (help):
        return help
    return "Maaf, command kamu tidak dikenali"

# Mengekstrak kata penting yang terdapat pada suatu string
def getKataPenting(s):
    penting = database.getAllKataPenting()
    for kata in penting:
        if (bmMatching(kata[0].lower(), s)):
            return kata[0]
    return False

# Mengekstrak kode mata kuliah dari suatu string
def getMatkul(s):
    x = re.search(r"\b[A-Z]{2}[1-4][0-2][0-9]{2}\b", s)
    if (x):
        return x.group()
    else:
        return False

# Mengekstrak tanggal deadline dari suatu string
def getDeadline(s):
    # Format YYYY-MM-DD, YYYY MM DD, YYYY/MM/DD
    x = re.search(r"\b[0-9]{4}[-\s\/](0[1-9]|1[0-2])[-\s\/](0[1-9]|[1-2][0-9]|3[0-1])\b", s)
    if (x):
        xRet = re.sub(" |/", "-", x.group())
        return xRet
    else:
        # Format <DD> <nama_bulan> <YYYY>, <DD>-<nama_bulan>-<YYYY>, <DD>/<nama_bulan>/<YYYY>
        y = re.search(r"\b(0*[1-9]|[1-2][0-9]|3[0-1])[-\s\/][A-Z|a-z]+[-\s\/][0-9]{4}\b", s)
        if(y):
            y = re.sub(" |/", "-", y.group()).split("-")
            result = f"{y[2]}-{bulan[y[1].lower()]}-{y[0]}"
            return result
        else:
            # Format DD-MM-YYYY, DD MM YYYY, DD/MM/YYYY
            z = re.search(r"\b(0[1-9]|[1-2][0-9]|3[0-1])[-\s\/](0[1-9]|1[0-2])[-\s\/][0-9]{4}\b", s)
            if (z):
                zRet = re.sub(" |/", "-", z.group()).split("-")
                return f"{zRet[2]}-{zRet[1]}-{zRet[0]}"
        return False

# Mengekstrak topik dari suatu string
def getTopik(s, matkul):
    regex = matkul + " .+ pada"
    x = re.search(regex, s)
    if (x):
        regex = " pada|"+matkul + " "
        topik = re.sub(regex, "", x.group())
        return topik
    else:
        return False

# Membuat sebuah task baru jika string masukan memiliki 4 komponen yakni kata penting, kode matkul,
# topik, dan tanggal deadline
def createTask(s):
    jenis = getKataPenting(s)
    matkul = getMatkul(s)
    deadline = getDeadline(s)
    if (matkul):
        topik = getTopik(s, matkul)
        if (jenis and deadline and topik):
            return database.InsertTask(deadline, matkul, jenis, topik)
        else:
            return False
    else:
        return False

# Memperbarui suatu task 
def updateTask(s):
    if (bmMatching("jadi", s)):
        id = re.search(r"\b[0-9]+\b",s)
        deadline = getDeadline(s)
        if (id and deadline):
            return database.UpdateTask(int(id.group()), deadline)
    else:
        return False

# Menampilkan luaran sesuai dengan fitur
def getTask(s):
    if (bmMatching("kapan", s)):
        jenis = getKataPenting(s)
        matkul = getMatkul(s)
        if (jenis in ["Tucil", "Tubes"] and matkul):
            return database.PrintTaskSpesifik(jenis, matkul)
    getTask=re.search(r"(a|A)pa saja", s)
    if (getTask):
        jenis = getKataPenting(s)
        if (jenis):
            x = re.search(r"\b[0-9]+ (hari|minggu)", s)
            if (x):
                n = x.group().split(" ")
                date = str(datetime.date(datetime.now()))
                if (n[1] == "hari"):
                    return database.PrintTaskNHariKataPenting(date, int(n[0]), True, jenis)
                else:
                    return database.PrintTaskNHariKataPenting(date, int(n[0]), False, jenis)
            else:
                date = []
                for match in re.finditer(r"\b([0-9]{4}[-\s\/](0[1-9]|1[0-2])[-\s\/](0[1-9]|[1-2][0-9]|3[0-1]))|((0[1-9]|[1-2][0-9]|3[0-1])[-\s\/][A-Z|a-z]+[-\s\/][0-9]{4})|((0[1-9]|[1-2][0-9]|3[0-1])[-\s\/](0[1-9]|1[0-2])[-\s\/][0-9]{4})\b", s):
                     date.append(getDeadline(match.group()))
                if (len(date) == 2):
                    return database.PrintTaskBetweenKataPenting(date[0], date[1], jenis)
                else:
                    date = re.search(r"hari ini", s)
                    if (date):
                        return database.PrintTaskTodayKataPenting(jenis)
                    else:
                        return database.PrintAllTaskKataPenting(jenis)
        elif(bmMatching("deadline", s)):
            x = re.search(r"\b[0-9]+ (hari|minggu)", s)
            if (x):
                n = x.group().split(" ")
                date = str(datetime.date(datetime.now()))
                if (n[1] == "hari"):
                    return database.PrintTaskNHari(date, int(n[0]), True)
                else:
                    return database.PrintTaskNHari(date, int(n[0]), False)
            else:
                date = []
                for match in re.finditer(r"\b([0-9]{4}[-\s\/](0[1-9]|1[0-2])[-\s\/](0[1-9]|[1-2][0-9]|3[0-1]))|((0[1-9]|[1-2][0-9]|3[0-1])[-\s\/][A-Z|a-z]+[-\s\/][0-9]{4})|((0[1-9]|[1-2][0-9]|3[0-1])[-\s\/](0[1-9]|1[0-2])[-\s\/][0-9]{4})\b", s):
                     date.append(getDeadline(match.group()))
                if (len(date) == 2):
                    return database.PrintTaskBetween(date[0], date[1])
                else:
                    date = re.search(r"hari ini", s)
                    if (date):
                        return database.PrintTaskToday()
                    else:
                        return database.PrintAllTask()
        else:
            return False
    else:
        return False

# Menghapus task        
def removeTask(s):
    if (bmMatching("selesai", s)):
        x = re.search(r"\b[0-9]+\b", s)
        if (x):
            return database.DeleteTask(int(x.group()))
        else:
            return False
    else:
        return False

# Menampilkan fitur-fitur dan daftar kata penting
def showHelp(s):
    x = re.search(r"(A|a)pa .*assistant|(A|a)ssistant .*apa", s)
    if (x):
        return database.help()
    else:
        return False

# Testing
if __name__ == "__main__":
    database.CreateTable()
    while(True):
        s = input("> ")
        print(executeCommand(s))
