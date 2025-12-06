# https://www.freecodecamp.org/news/how-to-use-defaultdict-python/

letters = {}

for letter in "Mississippi":
    if letter not in letters:
        letters[letter] = 1
    else:
        letters[letter] +=1

print(letters)
# {'M': 1, 'i': 4, 's': 4, 'p': 2}


from collections import defaultdict

letters = defaultdict(int)

for letter in "Mississippi":
    letters[letter] += 1

print(letters)
# defaultdict(<class 'int'>, {'M': 1, 'i': 4, 's': 4, 'p': 2})

d1 = defaultdict(int)

d1["Adding an entry!"]

print(d1)
# defaultdict(<class 'int'>, {'Adding an Entry!': 0})

# from collections import defaultdict

my_word = "Mississippi"

d1 = defaultdict(list)

for index, letter in enumerate(my_word):
    if letter == "i":
        d1[letter].append(index)

print(d1)
# defaultdict(<class 'list'>, {'i': [1, 4, 7, 10]})


def return_hello():
    return "Hello!"

d1 = defaultdict(return_hello)

d1[1]
d1[2]
d1[3]

print(d1)

