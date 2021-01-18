a = "datetime.date(2014, 3, 1)"

def main(string):
    check = len(string)
    nums = []
    if check == 25:
      for ch in string:
        try:
          int(ch)
          nums.append(ch)
        except:
          continue

      return nums
  
    elif check == 26:
    Y = nums[:4]
    M = nums[4:5]
    D = nums[5:]


out = main(a)
Y = out[:4]
M = out[4:5]
D = out[5:]
print(D)