import argparse

def is_number(item):
    try:
        float(item)
        return True
    except ValueError:
        return False


def set_up_list(ex):
    ex = ex.replace(" ", "")
    if (ex[0] in ["-", "+"]):
        ex = "0" + ex

    #Then it creates the list and adds each individual character to the list
    a_list = []
    for item in ex:
        a_list.append(item)
    count = 0
    #Finally it combines individual numbers into actual numbers based on user input
    while count < len(a_list) - 1:
        if is_number(a_list[count]) and a_list[count + 1] == "(":
            print("[WARN ]parentheses directly after number, inserting ×.")
            a_list.insert(count + 1, "*")
        if is_number(a_list[count]) and is_number(a_list[count + 1]):
            a_list[count] += a_list[count + 1]
            del a_list[count + 1]
        count = count + 1
    return a_list


def perform_operation(n1, operand, n2):
    if operand == "+":
        return str(float(n1) + float(n2))
    elif operand == "-":
        return str(float(n1) - float(n2))
    elif operand == "*":
        return str(float(n1) * float(n2))
    elif operand == "/":
        try:
            n = str(float(n1) / float(n2))
            return n
        except ZeroDivisionError:
            print("You tried to divide by 0.")
            print("Just for that I am going to terminate myself")
            exit()

def eval_expression_string(ex):
    expression = set_up_list(ex)
    eval_expression_list(expression)
    return expression[0]

def eval_expression_list(expression):
    emergency_count = 0
    P = ["(", ")"]
    # When only one item remains we have evaluated expression
    while len(expression) != 1:
        #If there are parentheses around a single list item, the list item is obviously just a number, eliminate parentheses
        #Will check to see if the first parentheses exists first so that it does not throw an index error
        count = 0
        while count < len(expression) - 1:
            if expression[count] == "(":
                if expression[count + 2] == ")":
                    del expression[count + 2]
                    del expression[count]
            count = count + 1
        #After that is done, it will multiply and divide what it can
        count = 0
        while count < len(expression) - 1:
            if expression[count] in ["*", "/"] and not (expression[count+1] in P or expression[count-1] in P):
                expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
                del expression[count + 1]
                del expression[count]
            count = count + 1
        #Then it will add and subtact what it can
        count = 0
        while count < len(expression) - 1:
            if expression[count] in ["+", "-"] and not (expression[count+1] in P or expression[count-1] in P):
                expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
                del expression[count + 1]
                del expression[count]
            count = count + 1

        #The steps will repeat until only one character is left. Operations that fail will be stopped by emergency count.
        emergency_count += 1
        if emergency_count >= 1000:
            print("Operation was too long or was bugged")
            exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '')
    parser.set_defaults(ex = "2+2")
    parser.add_argument( 'ex', action = 'store', type = str, help = 'expression' )
    args = parser.parse_args()
    result = eval_expression_string(args.ex)
    print(result)