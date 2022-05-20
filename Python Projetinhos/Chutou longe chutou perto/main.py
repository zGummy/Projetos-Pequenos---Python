from random import randrange, uniform

a=randrange(0,9)
#print("Random Number= ",a)

print("Advinhe um numero de 0 a 10")
tentativas=1

while True:
  n=int(input("Digite:"))

  if(n==a):
    print("")
    print("ACERTOU!")

    if(tentativas == 1):
      print("Com ",tentativas,' tentativa')

    else:
     print("Com ",tentativas,' tentativas')
    
    break  

  elif(n==a+2 or n==a-2 or n==a+1 or n==a-1):
    print('Chutou perto')

  else:
    print('Chutou longe')

  tentativas=tentativas+1