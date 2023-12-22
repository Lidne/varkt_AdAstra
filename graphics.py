import csv
import matplotlib.pyplot as plt

with open("data.txt") as f:
    reader = csv.reader(f, delimiter=";", quotechar='"')
    for i in reader:
        print(i)