camel = input("camelCase: ").strip()

result = ""

for char in camel:
    if char.isupper():     
        result += "_" + char.lower()
    else:
        result += char

print(result)