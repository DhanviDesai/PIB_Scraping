Months = ['January','February','March','April','May','June','July','August','September','October','November','December']
Days = [30,31]

def get_days(month):
    index = Months.index(month)+1
    if(index == 2):
        days = 29
    elif(index == 8):
        days = 31
    elif(index > 8):
        days = Days[::-1][index%2]
    else:
        days = Days[index%2]
    print(days)

get_days('September')
