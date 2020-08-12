from web_scraping import populate_data,get_driver

def get_days(month,Months):
    Days = [30,31]
    index = Months.index(month)+1
    if(index == 2):
        days = 29
    elif(index == 8):
        days = 31
    elif(index > 8):
        days = Days[::-1][index%2]
    else:
        days = Days[index%2]
    return days

def main():
    Months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    year = '2020'
    webdriver1 = get_driver()
    dri = get_driver()
    for month in Months:
        res = populate_data('All',month,year,webdriver1,dri)
        if(res == 'Stop'):
            break
        break
    dri.close()
    webdriver1.close()

if __name__ == '__main__':
    main()
