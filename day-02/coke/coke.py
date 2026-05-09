due = 50

while due > 0:
    print(f"Amount : {due}")
    coin = int(input("Insert coin:"))

    if coin == 25 or coin == 10 or coin == 5:
        due = due - coin 

print(f"changed owned : {abs(due)}") 