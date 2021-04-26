def bmMatching(p, T):
    L = last(p)
    i = len(p)-1
    j = i
    count = 0;
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
        print(count)
    return found;


def last(p):
    alfabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    lastoccur = {}
    for a in alfabet:
        i = len(p) - 1
        while (p[i] != a and i >= 0):
            i -=1
        if (p[i] == a):
            lastoccur[a] = i
        else:
            lastoccur[a] = -1
    return lastoccur
