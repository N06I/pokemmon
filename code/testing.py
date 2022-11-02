dika = {"a": [1, 2, 4],
        "ve": [1, 2],
        "she": [7, 3, 6, 4]}

dikbe = {"a": [1, 2, 4, 6],
         "ve": [1, 3],
         "ze": [4, 7, 8]}

for key in dikbe.keys():
    if key in dika:
        dikbe[key] = list(set(dikbe[key] + dika[key]))
for key in dika.keys():
    if key not in dikbe:
        dikbe[key] = dika[key]

print(dikbe)