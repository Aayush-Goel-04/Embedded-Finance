import configparser
import pandas as pd

fileA = pd.read_csv('fileA.csv')
fileB = pd.read_csv('fileB.csv')

# print("FileA contents:")
# print(fileA.head())
# print()

# print("FileB contents:")
# print(fileB.head())
# print()

config_obj = configparser.ConfigParser()

config_obj.read("config.ini")
validation = config_obj["validation"]
data_transform = config_obj["data_transform"]
generate_map = config_obj["generate_map"]
matching = config_obj["matching"]

old_bal = eval(validation["old_bal"])
new_bal = eval(validation["new_bal"])
rules = eval(validation["rules"])
limitsA = eval(data_transform["limitsA"])
limitsB = eval(data_transform["limitsB"])
new_colsA = eval(data_transform["new_colsA"])
new_colsB = eval(data_transform["new_colsB"])
uniqueA = eval(generate_map["uniqueA"])
uniqueB = eval(generate_map["uniqueB"])
sumA = eval(generate_map["sumA"])
sumB = eval(generate_map["sumB"])

match_dict = eval(matching["match_dict"])



def Validation(rules):
    truth_val = {}
    for _ in rules.keys():
        truths = []
        for i in rules[_]:
            truths.append(eval(i))
        truth_val[_] = truths
    return truth_val
        
    
def Data_transform(limitsA, limitsB, new_colsA, new_colsB):
    global fileA, fileB
    for _ in limitsA.keys():
        fileA[_] = fileA[_].str[limitsA[_][0]: limitsA[_][1]]
        try:
            fileA[_] = fileA[_].apply(eval)
        except (SyntaxError, NameError, ValueError):
            pass

    for _ in limitsB.keys():
        fileB[_] =  fileB[_].str[limitsB[_][0]: limitsB[_][1]]
        try:
            fileB[_] = fileB[_].apply(eval)
        except (SyntaxError, NameError, ValueError):
            pass

    for _ in new_colsA.keys():
        expression = ""
        for i in new_colsA[_]:
            if i in ["+", "-", "*", "/", "(", ")"]:
                expression += i
            else:
                expression += "fileA['"+i+"']"
        fileA[_] = eval(expression)

    for _ in new_colsB.keys():
        expression = ""
        for i in new_colsB[_]:
            if i in ["+", "-", "*", "/"]:
                expression += i
            else:
                expression += "fileB['"+i+"']"
        
        fileB[_] = eval(expression)

def Generate_map(uniqueA, uniqueB, sumA, sumB):
    global fileA, fileB
    for _ in uniqueA.keys():
        fileA = fileA.drop_duplicates(subset=[_, uniqueA[_]])
        sizeA = len(fileA)
        fileA = fileA.drop_duplicates(subset=[_])
        if sizeA != len(fileA):
            print("Unique UID can't be established in file A!")

    for _ in uniqueB.keys():
        fileB = fileB.drop_duplicates(subset=[_, uniqueB[_]])
        sizeB = len(fileB)
        fileB = fileB.drop_duplicates(subset=[_])
        if sizeB != len(fileB):
            print("Unique UID can't be established in file B!")

    for _ in sumA.keys():
        fileA[sumA[_]] = fileA.groupby(_)[sumA[_]].transform('sum')
        fileA = fileA.drop_duplicates(subset=[_])

    for _ in sumB.keys():
        fileB[sumB[_]] = fileB.groupby(_)[sumB[_]].transform('sum')
        fileB = fileB.drop_duplicates(subset=[_])

def Matching(match_dict):
    global fileA, fileB
    closed_records, open_records = None, None
    for _ in match_dict.keys():
        match_type = match_dict[_].pop(-1)
        if match_type == "ALL_A":
            closed_records = pd.merge(fileA, fileB, left_on=[_]*(len(match_dict[_])), right_on=match_dict[_], how='left')
            unmatched_records = closed_records[closed_records.isna().any(axis=1)]
            matched_records = closed_records.dropna()
            if closed_records.isna().any().any():
                print()
                print("Couldn't match all records !!! Following are open/unmatched records")
                print()
                print(unmatched_records)
            else:
                print()
                print("Records closed/matched !!")
            print()
            print("Closed/Matched records")
            print()
            print(matched_records)
        
        if match_type == "ALL_B":
            closed_records = pd.merge(fileB, fileA, left_on=[_]*(len(match_dict[_])), right_on=match_dict[_], how='left')
            unmatched_records = closed_records[closed_records.isna().any(axis=1)]
            matched_records = closed_records.dropna()
            if closed_records.isna().any().any():
                print()
                print("Couldn't match all records !!! Following are open/unmatched records")
                print()
                print(unmatched_records)
            else:
                print()
                print("Records closed/matched !!")
            print()
            print("Closed/Matched records")
            print()
            print(matched_records)




print("------------------------------ Validate all rules ------------------------------")
print()
print(Validation(rules))
print()
Data_transform(limitsA, limitsB, new_colsA, new_colsB)
print("------------------------------ After Data Transform ------------------------------")
print()
print(fileA.head())
print()
print(fileB.head())
print()
Generate_map(uniqueA, uniqueB, sumA, sumB)
print("------------------------------ After Map Generation ------------------------------")
print()
print(fileA.head())
print()
print(fileB.head())
print()
print("------------------------------ After Matching ------------------------------")
print()
Matching(match_dict)
print()

