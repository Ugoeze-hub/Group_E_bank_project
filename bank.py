print("Welcome to spark financial organisation \n Please how can i halp you")
print('''
   _____
   |#$|||
   @!#$%|
''')
print("Please provide the needed information")
pin = '1357'
c = 0
while c <=5 :
    u_pin = input('Enter your pin') 
    c += 1
    if u_pin != pin:
        print('Invalid Pin ', c, "Trial left")
        if c == 5:
            print('Account blocked, visit service handler')
            break
        continue
    else:
        print("correct, You are log into our plaatform")
        print("PLease press 1 for finacial service \n press 2 for customer care \n and 3 for others")
        C = int(input("Please how can we be of help"))
        if C == 1:
            print("financial service")
            
        elif C == 2:13