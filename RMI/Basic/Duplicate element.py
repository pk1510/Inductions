arr = []
dict={}
duplicate = []
n = int(input("enter the number of elements"))
for i in range(0,n):
    element = int(input("enter elementwise"))
    arr.insert(i, element)

for i in arr:
    if i in dict.keys():
        duplicate.append(i)
    else:
        dict[i] = i
    if arr[i] not in dict.keys():
        dict[arr[i]] = 1
    else:
        duplicate.append(arr[i])
print("the duplicate elements are: ", duplicate)

#time complexity is 0(n)
