from datetime import datetime
from BMMatching import bmMatching
import database
import re


#def executeCommand(s):

def getKataPenting(s):
    penting = database.getAllKataPenting()
    for kata in penting:
        if (bmMatching(kata[0].lower(), s)):
            return kata[0]
    return False

def getMatkul(s):
    x = re.search(r"\b[A-Z]{2}[1-4][0-2][0-9]{2}\b", s)
    if (x):
        return x.group()
    else:
        return False

def getDeadline(s):
    #x = re.search(r"\b[0-9]{4}-0[1-9]-[0-2][0-9]\b|\b[0-9]{4}-0[1-9]-3[0-1]\b|\b[0-9]{4}-1[0-2]-[0-2][0-9]\b|\b[0-9]{4}-1[0-2]-[3][0-1]\b", s)
    x = re.search(r"\b[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])\b", s)
    if (x):
        return x.group()
    else:
        return False

def getTopik(s):
    x = re.search("topik", s)
    if (x):
        return x.group()
    else:
        return False

def createTask(s):
    jenis = getKataPenting(s)
    matkul = getMatkul(s)
    deadline = getDeadline(s)
    topik = getTopik(s)
    if (jenis and matkul and deadline and topik):
        return database.InsertTask(deadline, matkul, jenis, topik)
    else:
        return False

def updateTask(s):
    x = bmMatching("menjadi", s)
    if (x):
        id = re.search(r"\b[0-9]+\b",s)
        deadline = getDeadline(s)
        if (x and deadline):
            return database.UpdateTask(int(id.group()), deadline)
    else:
        return False

def getTask(s):
    if (bmMatching("deadline", s)):
        jenis = getKataPenting(s)
        if (jenis):
            x = re.search(r"[0-9]+ (hari|minggu)", s)
            if (x):
                n = x.group().split(" ")
                date = str(datetime.date(datetime.now()))
                if (n[1] == "hari"):
                    return database.PrintTaskNHariKataPenting(date, int(n[0]), True, jenis)
                else:
                    return database.PrintTaskNHariKataPenting(date, int(n[0]), False, jenis)
            else:
                date = re.findall(r"\b[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])\b", s)
                if (len(date) == 2):
                    return database.PrintTaskBetweenKataPenting(date[0], date[1], jenis)
                else:
                    date = re.search(r"hari ini", s)
                    if (date):
                        return database.PrintTaskTodayKataPenting(jenis)
                    else:
                        return database.PrintAllTaskKataPenting(jenis)
        else:
            x = re.search(r"[0-9]+ (hari|minggu)", s)
            if (x):
                n = x.group().split(" ")
                date = str(datetime.date(datetime.now()))
                if (n[1] == "hari"):
                    return database.PrintTaskNHari(date, int(n[0]), True)
                else:
                    return database.PrintTaskNHari(date, int(n[0]), False)
            else:
                date = re.findall(r"\b[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])\b", s)
                if (len(date) == 2):
                    return database.PrintTaskBetween(date[0], date[1])
                else:
                    date = re.search(r"hari ini", s)
                    if (date):
                        return database.PrintTaskToday()
                    else:
                        return False
    else:
        return False
        



database.CreateTable()

s = "deadline 16 minggu ke depan" 
print(getTask(s))
