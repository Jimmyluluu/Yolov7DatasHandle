# import the time module
import time
  
# define the countdown func.
def timer(t):
    n = 0
    while n < t:
        mins, secs = divmod(n, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        n += 1
      
    print('Fire in the hole!!')
  
  
# input time in seconds
t = input("Enter the time in seconds: ")
  
# function call
timer(int(t))