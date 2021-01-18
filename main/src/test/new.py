a = "datetime.date(2014, 3, 1)"

def main(string):
    for ch in string:
        nums = []
        check = len(string)
        try:
            int(ch)
            nums.append(ch)

        except:
            continue

        if check == 25:
            M, Y, D = nums[:4], nums[4:5], nums[5:]
        
        
        return M, Y, D

main(a)