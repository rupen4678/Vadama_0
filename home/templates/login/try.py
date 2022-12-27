
account = {'ronaldo':[7777,12000],'messi':[3030,13000],'neymar':[1010,14000]}

print('Welcome to Boke Bank\nInsert your card')

attempts = 0
boolem = True
pins = []
for i,j in account.items():
    pins.append(j[0])


while boolem != False and attempts < 3:
    result = attempts - 3
    if result != 0:
        print('you have {} attempts left'.format(result))    
    else:
        print('Try again in 24 hours')

    digits = 0
    pin = int(input('Enter your 4 digits pin-\n'))
    if len(str(pin)) > 4 and len(str(pin)) < 4:
        print("Sorry the pin must be 4")
        attempts += 1
    else:
        if pin not in pins:
            print('Incorrect pin!')
            attempts += 1
        else:
            opt=input('Choose your options:\nA=Saving\nB=Balance check\n').lower()  
            if opt=='b':
                print('You have 12000$')
                break
            elif opt=='a':
                amt=int(input('How much money do u want to withdraw?\n'))
                print('You have withdrawn Rs.',amt)
                break
                boolem = False
        
