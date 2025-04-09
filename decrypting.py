import sys
sys.setrecursionlimit(10000)

def mod_mult(a,b,m):
    return(a*b)%m

def mod_square(a,m):
    return mod_mult(a,a,m)

def fast_pow_mod(a,b,m):
    if(b ==0):
        return 1
    elif(b%2 ==0):
        y = fast_pow_mod(a,b//2,m)
        z = mod_square(y,m)
        if (z==1 and y != 1 and y != m-1):
            return 0
        else:
            return z
    else:
        return mod_mult(a,fast_pow_mod(a,b-1,m),m)

def xgcd(a,b):
    if b ==0:
        return (a,1,b)
    else:
        d,x,y = xgcd(b,a%b)
        return (d,y,x-(a//b)*y)

def main():

    f1 = open("a.txt","r")
    a = int(f1.readline()) #getting a from assingment 4 plain text
    f1.close()

    f2 = open("a3.pubkeys.txt","r")
    prime = f2.readline()
    primelist = prime.split(" ")
    P = int(primelist[2])
    generator = f2.readline()
    generatorlist = prime.split(" ")
    G = int(generatorlist[2])
    mask = f2.readline()
    masklist = prime.split(" ")
    B = int(primelist[2])
    f2.close()

    plaintext = ""

    f3 = open("a3.cipher.txt","r")
    while(True):
        ctext = f3.readline()

        if ctext == "":
            break

        clist = ctext.split(",")
        halfmask = int(clist[0])
        c = int(clist[1])

        temp = fast_pow_mod(halfmask,a,P)
        #print(temp)
        gcd,x,y = xgcd(P,temp)
        m = (c*y) %P
        plaintext = plaintext + chr(m)

    print(plaintext)







if __name__ == "__main__":
    main()