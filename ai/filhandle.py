#file handle
print("filehandle")
user = input ("enter the number:")
try :
    num = int(user)
    print("the number is:",num)
except ValueError:
    print("invalid input")