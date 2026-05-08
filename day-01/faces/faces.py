def main():
    text = input("Enter the text :")
    print(convert(text))

def convert(text):
    text = text.replace(":)","🙂")
    text = text.replace(":(", "🙁")
    return text

main()
