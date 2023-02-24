from Gui import GUI

print("ASCII image converter")
print("Enter a name of file to convert")
file_name = input()
print("Enter scale of conversion(default: 0.1)")
scale = float(input() or "0.1")
GUI(file_name, scale)