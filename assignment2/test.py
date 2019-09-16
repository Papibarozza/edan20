
def fib(n,memo):
  
  if(n == 1 or n == 0):
    return 1
  else:
    if(memo[n-1] == 0):
        memo[n-1]=fib(n-1)
    else:
      return fib(n-1)+fib(n-2)



print(fib(5))