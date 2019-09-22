
# List
a = ["apple", "Microsoft", "Samsung"]
# Length function.
print(len(a))
# Append function. Adds items at the end of the list.
a.append("lenovo")
print(a)
# Extend the list by appending all items in a given list.
a.extend("foo")
print(a)
# Remove item in list.
a.pop(a.index("Samsung"))
print(a)
# Get index of item in list.
print(a.index("apple"))

a = ["apple", "Microsoft", "Samsung"]
# List reverse function. This can also be done using slicing.
# Python slicing. Start, stop, step.
print(a[::-1])
a.reverse()
print(a)
# Nested list
a = [["john", "smith", "GIS programmer", 60,000],
    ["Will", "Smith", "Actor", 1000000]]

# Create a list from a comma delimited string.
string = "John, Smith, GIS programmer"
w = string.split(",")
print(w)

# Make copy of variable. Allows one to change a variable without changing the
# original variable.
a = [1, 2, 3]
b = list(a)
b.append(4)
print(a)
print(b)

# Appends object at the end.
#https://stackoverflow.com/questions/252703/what-is-the-difference-between-pythons-list-methods-append-and-extend
x = [1, 2, 3]
x.append([4, 5])
print(x)

# Extends list by appending elements from the iterable.
x = [1, 2, 3]
x.extend([4, 5])
print(x)



