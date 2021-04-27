from datetime import datetime
from BMMatching import bmMatching
import database
import re


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
    x = re.search(r"\b[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])\b", s)
    if (x):
        return x.group()
    else:
        return False

def getTopik(s, matkul):
    regex = matkul + " .+ pada"
    x = re.search(regex, s)
    if (x):
        regex = " pada|"+matkul + " "
        topik = re.sub(regex, "", x.group())
        return topik
    else:
        return False

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
    #belum ada liat tugas spesifik
    if (bmMatching("deadline", s)):
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
            x = re.search(r"\b[0-9]+ (hari|minggu)", s)
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
                        return database.PrintAllTask()
    else:
        return False
        
def removeTask(s):
    if (bmMatching("selesai", s)):
        x = re.search(r"\b[0-9]+\b", s)
        if (x):
            return database.DeleteTask(int(x.group()))
        else:
            return False
    else:
        return False

def showHelp(s):
    x = re.search(r"(A|a)pa .*assistant | (A|a)ssistant .*apa", s)
    if (x):
        return database.help()
    else:
        return False


if __name__ == "__main__":
    database.CreateTable()

    s = "deadline apa saja?" 
    print(executeCommand(s))
