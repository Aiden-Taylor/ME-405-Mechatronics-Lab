import csv_reader
val = ['34,32,33,27,26,28,28,20,25,28,27,21,20,25,21,20,24,41,27,40,22,50,26,47,28,54,30,53,31,78,32,78',
'50,38,46,41,47,33,38,32,44,31,34,34,38,27,32,30,32,30,33,33,41,29,41,31,52,27,45,36,67,37,64,40',
'42,40,43,33,38,36,36,29,36,31,36,26,34,35,30,27,30,48,36,49,35,61,34,52,33,61,36,67,36,91,37,83']
reed = csv_reader.CSV(val)
print(reed.readdata())
print(reed.col_largest())