while True:
    try:
        x = input("Fraction :")

        a, b = x.split("/")

        a = int(a)
        b = int(b)

        if a > b :
            continue
        
        fuel = round((a / b) * 100) 

    except ValueError:
        pass
    except ZeroDivisionError:
        pass
    else:
        break

if fuel <= 1:
    print("E")
elif fuel >= 99:
    print("F")
else:
    print(f"{fuel}%")