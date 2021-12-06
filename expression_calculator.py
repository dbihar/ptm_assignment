import argparse

from numpy import nan

def is_number(item):
    try:
        float(item)
        return True
    except ValueError:
        return False


def set_up_list(ex):
    # Preparing string  for calculation

    ex = ex.replace(" ", "")
    ex = ex.replace("x", "*")
    ex = ex.replace("X", "*")
    ex = ex.replace("×", "*")
    ex = ex.replace("+++", "+")
    ex = ex.replace("++", "+")
    
    if (ex[0] in ["-", "+"]):
        ex = "0" + ex

    #Then it creates the list and adds each individual character to the list
    a_list = []
    #print("ex is", ex)
    a_list.append("")
    for i in range(len(ex)):
        if ex[i] in ["+", '*', '/', '-', '(', ')']:
            a_list.append(ex[i])
            a_list.append("")
        else:
            a_list[-1] = a_list[-1] + ex[i]
    
    if(a_list[-1] == ""):
        del a_list[-1]

    #print("a list", a_list)
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
    try:
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
                print("[ERROR] Division by 0")
                return "nan"
    except ValueError:
        print("Value error, expression probably read incorrectly ")
        return "nan"

def eval_expression_string(ex):
    if(ex==""):
        return nan
    expression = set_up_list(ex)
    print("String" , ex)
    print(expression)
    result = eval_expression_list(expression)
    return result

def eval_expression_list(expression):
    emergency_count = 0
    P = ["(", ")"]
    M = ["/", "*"]
    # When only one item remains we have evaluated expression
    while len(expression) != 1:
        expression = [item for item in expression if (item!="")]
        print(' '.join(expression)) 
        #If there are parentheses around a single list item, the list item is obviously just a number, eliminate parentheses
        #Will check to see if the first parentheses exists first so that it does not throw an index error
        # - infront of number
        count = 0
        while count < len(expression) - 1:
            if (expression[count] == '-') and is_number(expression[count + 1]):
                expression[count] = '+'
                expression[count+1] = '-' +  expression[count+1]
            count = count + 1

        # Front boundary condition
        if expression[0] in ["+", "-"]:
            if expression[0] == '-':
                expression.insert(0, "0")
            else:
                del expression[0]
                break

        count = 0
        while count < len(expression) - 1:
            if is_number(expression[count]) and is_number(expression[count + 1]):
                expression.insert(count + 1, "+")
            count = count + 1
        
        count = 0
        while count < len(expression) - 1:
            if (expression[count] == "(") and (expression[count + 1]=="+"):
                expression.insert(count + 1, "0")
            count = count + 1

        #print(' '.join(expression)) 

        count = 0
        while count < len(expression) - 1:
            if is_number(expression[count]) and expression[count + 1] == '(':
                expression.insert(count + 1, "*")
            count = count + 1

        #print(' '.join(expression)) 

        count = 0
        while count < len(expression) - 1:
            if is_number(expression[count+1]) and expression[count] == ')':
                expression.insert(count + 1, "*")
            count = count + 1

        #print(' '.join(expression)) 

        count = 0
        while count < len(expression) - 2:
            if expression[count] == "(":
                if expression[count + 2] == ")":
                    del expression[count + 2]
                    del expression[count]
                    break
            count = count + 1
        #print(' '.join(expression)) 

        count = 0
        while count < len(expression) - 1:
            if expression[count] in ["*", "/"] and not (expression[count+1] in P or expression[count-1] in P):
                expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
                del expression[count + 1]
                del expression[count]
                break
            count = count + 1
        
        #Then it will add and subtact what it can
        count = 1
        #print(' '.join(expression)) 
        while count < len(expression) - 2:
            if expression[count] in ["+", "-"] and \
            not (expression[count+1] in P or expression[count-1] in P or expression[count+2] in M or expression[count-2] in M):
                expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
                del expression[count + 1]
                del expression[count]
                break
            count = count + 1
        
        # Boundary condition
        if(len(expression) > 3):
            if expression[1] in ["+", "-"] and \
            not (expression[2] in P or expression[0] in P or expression[3] in M):
                expression[0] = perform_operation(expression[0], expression[1], expression[2])
                del expression[2]
                del expression[1]
        elif len(expression) > 2:
            if expression[1] in ["+", "-"] and \
            not (expression[2] in P or expression[0] in P):
                expression[0] = perform_operation(expression[0], expression[1], expression[2])
                del expression[2]
                del expression[1]
        
        #print(' '.join(expression)) 
        if(len(expression) > 3):
            if expression[-2] in ["+", "-"] and \
            not (expression[-3] in P or expression[-1] in P or expression[-4] in M):
                expression[-3] = perform_operation(expression[-1], expression[-2], expression[-3])
                expression = expression[:-2]
                
        elif(len(expression) > 2):
            if expression[-2] in ["+", "-"] and \
            not (expression[-3] in P or expression[-1]):
                expression[-3] = perform_operation(expression[-1], expression[-2], expression[-3])
                expression = expression[:-2]

        #print(' '.join(expression)) 
        #The steps will repeat until only one character is left. Operations that fail will be stopped by emergency count.
        emergency_count += 1 
        if emergency_count >= 200:
            print("Operation was too long or was bugged")
            return nan
    return expression[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '')
    parser.set_defaults(ex = "2+2")
    parser.add_argument( 'ex', action = 'store', type = str, help = 'expression' )
    args = parser.parse_args()
    result = eval_expression_string(args.ex)
    print(result)