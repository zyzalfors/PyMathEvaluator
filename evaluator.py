from decimal import *
import re, sys

def isoperator(token):
 return token in ["^", "*", "/", "+", "-"]

def isnumber(token):
 return re.fullmatch("[-+]?\d+\.?\d*", token) is not None

def issign(token):
 return token in ["+", "-"]

def isnumpart(token):
 return token in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

def isopenbracket(token):
 return token in ["(", "[", "{"]

def isclosebracket(token):
 return token in [")", "]", "}"]

def gettokens(expr):
 tokens, number = [], []
 for char in re.sub(r"\s+", "", expr):
  if isnumpart(char): number.append(char)
  elif isoperator(char):
   if len(number) > 0:
    tokens.append("".join(number))
    number = []
    tokens.append(char)
   elif issign(char): number.append(char)
   else: tokens.append(char)
  elif isopenbracket(char):
   if len(number) > 0:
    if len(number) == 1 and issign(number[0]): number.append("1")
    tokens.append("".join(number))
    number = []
    tokens.append("*")
   tokens.append(char)
  elif isclosebracket(char):
   if len(number) > 0:
    tokens.append("".join(number))
    number = []
   tokens.append(char)
  else: return []
 if len(number) > 0: tokens.append("".join(number))
 return tokens

def getpostfix(tokens, debug):
 prec, stack, queue = {"^": 2, "*": 1, "/": 1, "+": 0, "-": 0}, [], []
 for token in tokens:
  if isnumber(token): queue.append(token)
  elif isoperator(token):
   while len(stack) > 0 and not isopenbracket(stack[-1]) and prec.get(stack[-1]) >= prec.get(token): queue.append(stack.pop())
   stack.append(token)
  elif isopenbracket(token): stack.append(token)
  elif isclosebracket(token):
   while len(stack) > 0 and not isopenbracket(stack[-1]): queue.append(stack.pop())
   if len(stack) > 0: stack.pop()
  else: return []
  if debug: print("Stack:", str(stack), "\nQueue:", str(queue))
 while len(stack) > 0: queue.append(stack.pop())
 return queue

def evaluate(value1, value2, operation):
 if operation == "+": return Decimal(value1) + Decimal(value2)
 elif operation == "-": return Decimal(value1) - Decimal(value2)
 elif operation == "*": return Decimal(value1) * Decimal(value2)
 elif operation == "/": return Decimal(value1) / Decimal(value2)
 elif operation == "^": return Decimal(value1) ** Decimal(value2)
 else: return None

def getvalue(postfix):
 stack = []
 for token in postfix:
  if isoperator(token):
   value2, value1 = stack.pop(), stack.pop()
   stack.append(evaluate(value1, value2, token))
  else: stack.append(token)
 return stack.pop()

def main(argv):
 try:
  argv.pop(0)
  argv = list(map(lambda arg: arg.lower(), argv))
  debug = "-d" in argv
  if debug: argv.remove("-d")
  expr = "".join(argv)
  tokens = gettokens(expr)
  postfix = getpostfix(tokens, debug)
  if debug: print("Tokens:", str(tokens), "\nPostfix:", "  ".join(postfix))
  value = getvalue(postfix)
  print(str(value))
 except: print("Error")

main(sys.argv)