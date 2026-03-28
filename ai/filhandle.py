#file handle
print("filehandle")
user = input ("enter the number:")
try :
    if int(user)>18:
        print("you are above 18")
    else:        
        print("you are below 18")
except ValueError:
    print("invalid input")