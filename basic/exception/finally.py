try:
    f=open("text.txt", 'r')
    k=f.read()
    print(k)
except Exception as e:
    print(e)
finally:
    try:
        f.close()
    except Exception as e:
        print(e)