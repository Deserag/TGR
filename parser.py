from openpyxl import load_workbook
import re
book = load_workbook(filename="C:/Users/Deserag/Downloads/Telegram Desktop/10%2013.03-18.03.xlsx")

# 65-90 A-Z

sheet = book['Колледж ВятГУ']
pattern = r"Группа .{1,2}к"
for i in range(65,91):
     print( sheet[chr(i)+'24'].value)
     if  sheet[chr(i)+'24'].value and re.match(pattern,sheet[chr(i)+'24'].value):
        begin_value = chr(i)+'24'
        print(sheet[chr(i)+'24'].value)
        break
print(begin_value)

