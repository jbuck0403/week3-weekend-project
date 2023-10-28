import os


def clearTerminal():
    # Check the OS type to use the appropriate clear command
    if os.name == "posix":  # Unix/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")


def userInput(
    message,
    errorMessage="Invalid input, numbers only...",
    passCondition=lambda x: True,
    strInput=False,
    boolInput=False,
):
    if boolInput:
        message = f"{message} ('Yes' or 'No'): "
        errorMessage = "'Yes' or 'No' only..."
        passCondition = lambda x: x == "y" or x == "n"

    if strInput and passCondition == (lambda x: True):
        passCondition = lambda x: x != ""

    error = False
    while True:
        try:
            clearTerminal()

            if error:
                newMessage = f"{errorMessage}\n{message}"

            if strInput:
                userInput = input(newMessage if error else message).strip().lower()
            elif boolInput:
                userInput = input(newMessage if error else message).strip().lower()[0]
            else:
                userInput = int(input(newMessage if error else message).strip())

            if passCondition(userInput):
                if boolInput:
                    if userInput == "y":
                        return True
                    else:
                        return False
                return userInput
            else:
                error = True
                continue
        except:
            error = True
            continue
