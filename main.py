import graph_gen
import os

banner = """
[1] Generate tables for Gephi
[2] Analyze Chat

[clear] Clear Console
"""
os.system('clear')
print(banner)
while True:
    
    option = input("  Enter option: ")
    if option == '1':
        filename = input("Input path to file: ")
        graph_gen.one(filename)
    elif option == '2':
        os.system('python words_analyze.py')
    elif option == 'clear':
        os.system('clear')
        print(banner)
    