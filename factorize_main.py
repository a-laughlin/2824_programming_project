# Your names:
#
#
#
#

# Did you copy and paste code from any online source?

# Note: you are not allowed to do so for this assignment.
# Your answer should generally be "no". But if you did,
# mark the code clearly and explain here why you needed to do so.

# Did you collaborate with someone outside your team?
# If yes, explain what you obtained from the collaboration.

# Did you post queries on online forums (such as stackoverflow, ..)
# related to this assignment?
# If yes, post the links here.

#----------- IMPORTS ---------------------

# If you have import statements, please explain in comments
# why you need them. You can be very brief.

from __future__ import print_function
# I import this just for compatibility with python2 please use python3
# though.

import sys
import math
# sys has useful utilities I need.




from time import clock as time_clock
# Time is being imported to measure
# running time for the factorize
# function.

from functools import reduce # for pipe
from random import randrange # to generate complexity analysis nums
from time import perf_counter,sleep # timing, and sleep for test fns
from multiprocessing import Pool # to run fns in different processes
from os import getpid # to check that the fns are running in different processes
from types import SimpleNamespace # dict property access is annoying

# -------------------------------------------

# fn composition ltr
pipe = lambda fn1,*fns: lambda arg,*args: reduce(lambda a,f: f(a), fns, fn1(arg,*args))



#
# test setup
# 
def gen_nums(digits=1,samples=None,fixed_num=None):
  if(fixed_num):
    if(samples==None): return [fixed_num]
    return [fixed_num for r in range(samples)]

  min_num = 10**(digits-1)
  max_num = 10**digits
  sample_len = range(samples or int(10**(digits/2)))
  return [randrange(min_num,max_num) for s in sample_len]

def summarizeFnResults(summary_list):
  summaries = {}
  for result in summary_list:
    if(not (result.name in summaries)):
      summaries[result.name] = SimpleNamespace(
        min=999999999999,
        max=0,
        mean=0,
        durations=[],
        results=[],
        name='',
      )
    summary = summaries[result.name]

    if(result.duration<summary.min):summary.min=result.duration
    if(result.duration>summary.max):summary.max=result.duration
    summary.durations.append(result.duration)
    summary.results.append(result)
    summary.name=result.name
    del result.name

  for name in summaries:
    summaries[name].mean = sum(summaries[name].durations)/len(summaries[name].durations)
    del summaries[name].durations
  [print('{} \nmean: {} \nmax: {}'.format(s.name,s.mean,s.max)) for s in summaries.values()]
  return;
  # return summaries

def execTest(tup):
  name,fn,num = tup;
  start = perf_counter()
  output = fn(num)
  end = perf_counter()
  print('pid',getpid(),'time',end-start,'{}({})={}'.format(name,num,output))
  return SimpleNamespace(
    duration=end-start,
    name=name,
    output=output,
  )

pool = Pool()
execTests = lambda nums:pipe(
  lambda *fns:[(fn.__name__,fn,num)  for num in nums for fn in fns],
  lambda tups:pool.map(execTest,tups),
  summarizeFnResults,
  lambda x:(pool.close(),pool.join(),x.duration)[2]
)

# test runners for specific nums of digits
# gen7_20_rand = execTests(gen_nums(digits=7,samples=20))
# gen7_5_fixed_prime = execTests(gen_nums(fixed_num=5515927,samples=5))

# run a test comparing functions side by side on the same numbers
# test_7digit_fixed_prime = execTests(gen_nums(fixed_num=5515927,samples=5))
# test_7digit_fixed_prime(factorize,factorize1)



# This is the brute force algorithm.
# You are being asked to improve upon this
def factorize(n):
    for i in range(2, n-1):
        if n % i == 0:
            return i
    assert False, 'You gave me a prime number to factor'
    return -1


# Improve on factorize function above:
# Call your functions factorize1, factorize2, ...
# Please write a brief comment before each function to describe
# the improvements you are trying out.

# def factorize1(n): Iterate only until n//2 and test only prime numbers.  
def factorize1(n):
    for i in range(2, math.sqrt(n) + 1):
        if n % i == 0:
            return i
    assert False, 'You gave me a prime number to factor'
    return -1

def factorize3(n):
    for i in range(2, math.sqrt(n) + 1):
        if n % i == 0:
            return i
        x = x + 1
    assert False, 'You gave me a prime number to factor'
    return -1

# too many primes to create a sieve: how does the running time compare to the brute force
# generate lots of plots etc. 
# complexity analysis = is this too many? 
    # each digit you add, the space for search multiplies by 5


#def factorize2(n): this function creates a list and edits it after each prime
# factor has been considered and ruled out. 
# turns out to not be a time efficient way to do factorization. 
# create a counter i from 2 to sqrt(n)
    # counter i 2, starts at 0, goes to 1, everytime it goes to 0, skip the number
    # counter i3, starts at 0, goes to 2, everytime it gets to 0, skip the number
    # counter i4
import math
def factorize2(n):
    p = int(math.sqrt(n))
    list_primes = list(range(2, p + 1))
    i = 2
    for i in list_primes:
        if n % i == 0:
            return i
        j = 2 * i
        while j < p:
            if j in list_primes:
                list_primes.remove(j)
            j = j + i
    assert False, 'You gave me a prime number to factor'
    return -1
        
import math
def fermfact(n):
    a = int(math.ceil(math.sqrt(n)))
    bsq = a ** 2 - n
    while math.sqrt(bsq) != int(math.sqrt(bsq)):
        a = a + 1
        bsq = a ** 2 - n
    return a - math.sqrt(bsq)

def fermfact1(n):
    a = int(math.ceil(math.sqrt(n)))
    if n % 4 == 1:
        if a % 2 == 0:
            a = a + 1
    if n % 4 == 3:
        if a % 2 != 0:
            a = a + 1
    bsq = a ** 2 - n
    while math.sqrt(bsq) != int(math.sqrt(bsq)):
        a = a + 2
        bsq = a ** 2 - n
    return a - math.sqrt(bsq)
# ...

#def factorize3(n):
# ...
import math
from math import sqrt
def fermfact2(n):
    p = n % 10
    a = int(math.ceil(math.sqrt(n)))
    bmodeven = [0, 4, 6]
    bmododd = [1, 5, 9]
    bsq = a ** 2 - n
    zero = 0.0
    if n % 4 == 1:
        if a % 2 == 0:
            a = a + 1
            bsq = a ** 2 - n
        if sqrt(bsq)%1 == zero:
            return a - sqrt(bsq)
        while bsq % 10 not in bmodeven:
            a = a + 2
            bsq = a ** 2 - n
            if sqrt(bsq)%1 == 0:
                return a - sqrt(bsq)
        while sqrt(bsq) % 1 is not zero:
            if n % 10 == 1:
                if a % 10 == 1:
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 5:
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                if a % 10 == 9:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 3:
                if a % 10 == 3:
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a + a + 6
                    bsq = a ** 2 - n
                if a % 10 == 7:
                    a = a + 6
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 5:
                a = a + 2
                bsq = a ** 2 - n
            if n % 10 == 7:
                if a % 10 == 1:
                    a = a + 8
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 9:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
            if n % 10 == 9:
                if a % 10 == 3:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 10 == 5:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 7:
                    a = a + 6
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
        return a - sqrt(bsq)
    if n % 4 == 3:
        if a % 2 != 0:
            a = a + 1       
            bsq = a ** 2 - n
        if sqrt(bsq)%1 == zero:
            return a - sqrt(bsq)
        while bsq % 10 not in bmododd:
            a = a + 2
            bsq = a ** 2 - n
            if sqrt(bsq)%1 == zero:
                return a - sqrt(bsq)
        while sqrt(bsq)%1 is not zero:
            if n % 10 == 1:
                if a % 10 == 6:
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 0:
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                if a % 10 == 4:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 3:
                if a % 10 == 2:
                    a = a + 6
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a + a + 4
                    bsq = a ** 2 - n
                if a % 10 == 8:
                    a = a + 4
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
            if n % 10 == 5:
                a = a + 2
                bsq = a ** 2 - n
            if n % 10 == 7:
                if a % 10 == 4:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
                if a % 10 == 6:
                    a = a + 8
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
            if n % 10 == 9:
                if a % 10 == 8:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 10 == 0:
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 2:
                    a = a + 6
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if sqrt(bsq)%1 == zero:
                        return a - sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
        return a - sqrt(bsq) 

#def factorize4(n):
# ...
import random
import fractions
def pollard_rho(n):
    x = (random.randint(1, n) % (n - 2)) + 2
    y = 0
    c = (random.randint(1, n) % (n - 1)) + 1
    d = 1
    while x != y:
        y = x
        x = (x ** 2 + c) % n
        y = (x ** 2 + c) % n
        d = fractions.gcd(abs(x - y), n)
        if d > 1:
            return d
        if d == n:
            pollard_rho(n)
    
# ...
def fermfact4(n):
    p = n % 10
    a = int(math.ceil(math.sqrt(n)))
    bmodeven = [0, 4, 6]
    bmododd = [1, 5, 9]
    bsq = a ** 2 - n
    if n % 4 == 1:
        if a % 2 == 0:
            a = a + 1
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                    return a - math.sqrt(bsq)
        while bsq % 10 not in bmodeven:
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)):
            if n % 10 == 1:
                if a % 10 == 1:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 5:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                if a % 10 == 9:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 3:
                if a % 10 == 3:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a + a + 6
                    bsq = a ** 2 - n
                if a % 10 == 7:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 5:
                a = a + 2
                bsq = a ** 2 - n
            if n % 10 == 7:
                if a % 10 == 1:
                    a = a + 8
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 9:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
            if n % 10 == 9:
                if a % 10 == 3:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 10 == 5:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 7:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
        return a - math.sqrt(bsq)
    if n % 4 == 3:
        if a % 2 != 0:
            a = a + 1       
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
        while bsq % 10 not in bmododd:
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)):
            if n % 10 == 1:
                if a % 10 == 6:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 0:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                if a % 10 == 4:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 3:
                if a % 10 == 2:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a + a + 4
                    bsq = a ** 2 - n
                if a % 10 == 8:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
            if n % 10 == 5:
                a = a + 2
                bsq = a ** 2 - n
            if n % 10 == 7:
                if a % 10 == 4:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
                if a % 10 == 6:
                    a = a + 8
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
            if n % 10 == 9:
                if a % 10 == 8:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 10 == 0:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 2:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
        return  a - math.sqrt(bsq)  
def fermfact5(n):
    p = n % 10
    a = int(math.ceil(math.sqrt(n)))
    bmodeven = [0, 4]
    bmododd = [1, 9]
    bsq = a ** 2 - n
    if n % 4 == 1:
        if a % 2 == 0:
            a = a + 1
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                    return a - math.sqrt(bsq)
        while bsq % 16 not in bmodeven:
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)):
            if n % 16 == 1 or n % 16 == 13:
                if a % 16 == 1 or a % 16 == 9:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 16 == 7 or a % 16 == 15:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
            if n % 16 == 9 or n % 16 == 5:
                if a % 16 == 3 or a % 16 == 11:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 16 == 5 or a % 16 == 13:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
        return a - math.sqrt(bsq)
    if n % 4 == 3:
        if a % 2 != 0:
            a = a + 1       
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
        while bsq % 16 not in bmododd:
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)):
            if n % 16 == 3 or n % 16 == 11:
                if a % 16 == 1 or a % 16 == 9:
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 16 == 7 or n % 16 == 15:
                if a % 16 ==  4:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
                if a % 16 == 8:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                if a % 16 == 12:
                    a = a + 8
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n   
        return  a - math.sqrt(bsq)  


# Below we have test code:
# to test your function say factorize2, you would simply call

# python3 factorize_main.py factorize2

if __name__ == '__main__':
    # First parse command line arguments and figure out which
    # function we want to test
    if len(sys.argv) <= 1:
        fun = fermfact5
    else:
        fun_to_call_string = sys.argv[1]
        assert fun_to_call_string in globals(), ('You did not implement '+fun_to_call_string)
        globals_copy= globals().copy()
        fun = globals_copy.get(fun_to_call_string)
    # Open the file with list of numbers
    # test_7digit_fixed_prime = execTests(gen_nums(fixed_num=5515927,samples=5))
    # test_7digit_fixed_prime(factorize,factorize1)
    
    f = open('composite_list.txt', 'r')
    # test each number
    for line in f:
        n = int(line)
        print('Factoring', n, '(', len(line), 'digits ): ', end='')
        time_elapsed = execTests([n])(fun)
#         t1 = time_clock() # Record time
#         p = fun(n)
#         t2 = time_clock() # Record time
#         time_elapsed = t2 - t1  # seconds
        print('Factor = ', p, ' other factor = ', n/p, ' Time Elapsed: ', time_elapsed)
        if n % p != 0:
            print('Factorization failed for: ', n)
            sys.exit(1)
    f.close()
