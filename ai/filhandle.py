#file handle
print("filehandle")
user = input ("enter the number:")
try :
    if int(user)>18:
        print("you are above 18")
        inp = input("enter the file name:")
        with open(inp, 'r') as f:
            data = f.read()
            print(data)

    else:        
        print("you are below 18")
except ValueError:
    print("invalid input")