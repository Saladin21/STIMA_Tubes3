import sqlite3
import datetime

# CATATAN: Query buat fitur 3 masih belum diimplementasi soalnya bingung maksud suatu task tuh apanya

connection = sqlite3.connect('../test/database.db')
cursor = connection.cursor()

def CreateTable():
    command = '''CREATE TABLE IF NOT EXISTS daftar_kata_penting(kata_penting VARCHAR)'''
    cursor.execute(command)
    kata_penting = ["Kuis", "Ujian", "Praktikum", "Tucil", "Tubes"]
    cursor.execute(f"SELECT * FROM daftar_kata_penting")
    result = cursor.fetchall()
    if(len(result) == 0):
        for kata in kata_penting:
            cursor.execute(f"INSERT INTO daftar_kata_penting VALUES('{kata}')")
    connection.commit
    command = '''CREATE TABLE IF NOT EXISTS daftar_task(id INT PRIMARY KEY, deadline DATE, matkul VARCHAR, jenis VARCHAR, topik VARCHAR)'''
    cursor.execute(command)
    connection.commit()

def getAllTask():
    cursor.execute(f"SELECT * FROM daftar_task")
    result = cursor.fetchall()
    return result

def getTaskByID(idTask):
    cursor.execute(f"SELECT * FROM daftar_task WHERE id = '{idTask}'")
    result = cursor.fetchall()
    return result

def getTaskBetween(date_1, date_2):
    cursor.execute(f"SELECT * FROM daftar_task WHERE deadline BETWEEN '{date_1}' AND '{date_2}'")
    result = cursor.fetchall()
    return result

# isHari True jika N merupakan N hari, False jika N merupakan N minggu
def getTaskNhari(date1, N, isHari):
    date2 = datetime.date.fromisoformat(date1)
    if(isHari):
        date2 += datetime.timedelta(days=N)
    else:
        date2 += datetime.timedelta(days=7*N)
    return getTaskBetween(date1, date2)

def getTaskToday(today):
    cursor.execute(f"SELECT * FROM daftar_task WHERE deadline = '{today}'")
    result = cursor.fetchall()
    return result

def getTaskKataPenting(kata_penting):
    cursor.execute(f"SELECT * FROM daftar_task WHERE jenis = '{kata_penting}'")
    result = cursor.fetchall()
    return result

def getTaskSpesifik(kata_penting, matkul):
    cursor.execute(f"SELECT * FROM daftar_task WHERE jenis = '{kata_penting}' and matkul = '{matkul}'")
    result = cursor.fetchall()
    return result

def getAllKataPenting():
    cursor.execute(f"SELECT * FROM daftar_kata_penting")
    result = cursor.fetchall()
    return result

def getTaskBetweenKataPenting(date_1, date_2, kata_penting):
    cursor.execute(f"SELECT * FROM daftar_task WHERE jenis = '{kata_penting}' AND deadline BETWEEN '{date_1}' AND '{date_2}'")
    result = cursor.fetchall()
    return result

def getTaskNhariKataPenting(date1, N, isHari, kata_penting):
    date2 = datetime.date.fromisoformat(date1)
    if(isHari):
        date2 += datetime.timedelta(days=N)
    else:
        date2 += datetime.timedelta(days=7*N)
    return getTaskBetweenKataPenting(date1, date2, kata_penting)

def getTaskTodayKataPenting(today, kata_penting):
    cursor.execute(f"SELECT * FROM daftar_task WHERE jenis = '{kata_penting}' AND deadline = '{today}'")
    result = cursor.fetchall()
    return result

def GenerateID():
    alltask = getAllTask()
    if(len(alltask) == 0):
        return 1
    else:
        idMaks = alltask[0][0]
        for tupple in alltask:
            if(idMaks < tupple[0]):
                idMaks = tupple[0]
        return idMaks+1

def InsertTask(deadline, matkul, jenis, topik):
    cursor.execute(f"SELECT * FROM daftar_task WHERE deadline = '{deadline}' and matkul = '{matkul}' and jenis = '{jenis}' and topik = 'topik'")
    result = cursor.fetchall()
    if (len(result) == 0):
        idTask = GenerateID()
        cursor.execute(f"INSERT INTO daftar_task(id, deadline, matkul, jenis, topik) VALUES ('{idTask}', '{deadline}', '{matkul}', '{jenis}', '{topik}')")
        connection.commit()
        strRet = f"[TASK BERHASIL DICATAT]\n(ID: {idTask}) {deadline} - {matkul} - {jenis} - {topik}"
        
    else:
        strRet = f"[TASK SUDAH TERCATAT]\n(ID: {result[0][0]}) {deadline} - {matkul} - {jenis} - {topik}"
    return strRet

def DeleteTask(idTask):
    strRet = ""
    if(isIDvalid(idTask)):
        cursor.execute(f"DELETE FROM daftar_task WHERE id = {idTask}")
        connection.commit()
        strRet += "[Task Berhasil Diselesaikan]\n"
    else:
        strRet += "[Tidak dapat menyelesaikan task karena task tidak dikenali]"
    return strRet

def UpdateTask(idTask, newDeadline):
    strRet = ""
    if(isIDvalid(idTask)):
        cursor.execute(f"UPDATE daftar_task SET deadline = '{newDeadline}' WHERE id = '{idTask}'")
        connection.commit()
        strRet += "[Berhasil memperbarui deadline] " + PrintTaskByID(idTask)
    else:
        strRet += "Tidak dapat memperbarui task karena task tidak dikenali"
    return strRet

def PrintTask(alltask):
    strRet = ""
    if(len(alltask) == 0):
        strRet += "Tidak ada"
    else:
        strRet += "[DAFTAR DEADLINE]\n"
        i = 1
        for tupple in alltask:
            strRet += f"{i}. (ID: {tupple[0]}) {tupple[1]} - {tupple[2]} - {tupple[3]} - {tupple[4]} \n"
            i += 1
    return strRet

def PrintTaskByID(idTask):
    taskbyID = getTaskByID(idTask)[0]
    strRet = f"(ID: {taskbyID[0]}) {taskbyID[1]} - {taskbyID[2]} - {taskbyID[3]} - {taskbyID[4]}\n"
    return strRet

def PrintAllTask():
    alltask = getAllTask()
    return PrintTask(alltask)

def PrintTaskSpesifik(kata_penting, matkul):
    alltask = getTaskSpesifik(kata_penting, matkul)
    strRet = ""
    if(len(alltask) == 0):
        strRet += "Tidak ada"
    else:
        strRet += "[DEADLINE]\n"
        for tupple in alltask:
            strRet += f"{tupple[4]} : {tupple[1]} \n"
    return strRet

def PrintTaskBetween(date_1, date_2):
    alltask = getTaskBetween(date_1, date_2)
    return PrintTask(alltask)

# isHari = True jika N merupakan N hari, isHari = False jika N merupakan N minggu
def PrintTaskNHari(date1, N, isHari):
    alltask = getTaskNhari(date1, N, isHari)
    return PrintTask(alltask)

def PrintTaskToday():
    alltask = getTaskToday(datetime.date.today())
    return PrintTask(alltask)

def PrintAllTaskKataPenting(kata_penting):
    alltask = getTaskKataPenting(kata_penting)
    return PrintTask(alltask)

def PrintTaskBetweenKataPenting(date_1, date_2, kata_penting):
    alltask = getTaskBetweenKataPenting(date_1, date_2, kata_penting)
    return PrintTask(alltask)

# isHari = True jika N merupakan N hari, isHari = False jika N merupakan N minggu
def PrintTaskNHariKataPenting(date1, N, isHari, kata_penting):
    alltask = getTaskNhariKataPenting(date1, N, isHari, kata_penting)
    return PrintTask(alltask)

def PrintTaskTodayKataPenting(kata_penting):
    alltask = getTaskTodayKataPenting(datetime.date.today(), kata_penting)
    return PrintTask(alltask)

def isIDvalid(idTask):
    alltask = getAllTask()
    for tupple in alltask:
        if(idTask == tupple[0]):
            return True
    return False

def help():
    fitur = ["Menambahkan task baru", "Melihat daftar task yang harus dikerjakan", "Menampilkan deadline dari suatu task tertentu", "Memperbarui task tertentu", "Menandai bahwa suatu task sudah selesai dikerjakan"]
    katapenting = getAllKataPenting()
    strRet = "[Fitur]\n"
    i = 1
    for ftr in fitur:
        strRet += str(i) + ". " + ftr + "\n"
        i += 1
    strRet += "[Daftar Kata Penting]\n"
    i = 1
    for kt in katapenting:
        strRet += str(i) + ". " + kt[0] + "\n"
        i += 1
    return strRet

if __name__ == "__main__":
    CreateTable()
    print(help())
    print(InsertTask('2021-04-26', 'PBO', 'TUBES', 'Tugas Besar 2 Engimon'))
    print(InsertTask('2021-04-28', 'STIMA', 'TUBES', 'Tugas Besar 3 String Matching'))
    print(InsertTask('2021-05-11', 'IF2211', 'MAKALAH', 'Makalah stima'))
    print("="*10, "All Task", "="*10)
    print(PrintAllTask())
    print("="*10, "Task between", "="*10)
    print(PrintTaskBetween('2021-04-20', '2021-04-30'))
    print("="*10, "Task N hari", "="*10)
    print(PrintTaskNHari('2021-04-20', 7, True))
    print("="*10, "Task N minggu", "="*10)
    print(PrintTaskNHari('2021-04-20', 2, False))
    print("="*10, "Task today", "="*10)
    print(PrintTaskToday())
    print("="*10, "Update", "="*10)
    print(UpdateTask(3, '2021-06-01'))
    print(PrintAllTask())
    print("="*10, "Delete", "="*10)
    print(DeleteTask(1))
    print(PrintAllTask())