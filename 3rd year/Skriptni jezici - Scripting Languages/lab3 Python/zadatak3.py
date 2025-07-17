import os
import sys

def get_students(filepath):
    students = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            line = line.split(' ')
            jmbag = line[0]
            lastname = line[1]
            name = line[2]
            students[jmbag] = (lastname, name)
    return students

def get_scores(path):
    exercises = set()
    scores = {}
    for lab in os.listdir(path):
        if lab.startswith('Lab_') and lab.endswith('.txt'):
            num = lab.split('_')
            exercise_number = int(num[1])
            exercises.add(exercise_number)
            with open(os.path.join(path, lab), 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    lab_result = line.split(' ')
                    jmbag = lab_result[0]
                    if jmbag not in scores:
                        scores[jmbag] = {}
                    bod = lab_result[1]
                    if exercise_number in scores[jmbag]:
                        print(f"Student {jmbag} appears twice in the list for the same exercise")
                    else:
                        scores[jmbag][exercise_number] = bod
    return scores, sorted(exercises)


entry = sys.argv
path = entry[1]
students_file = os.path.join(path, 'studenti.txt')
students = get_students(students_file)
#print(students)
scores, exercises = get_scores(path)

print(f"{'JMBAG':<11} {'Prezime, Ime':<20}", end='')
for v in exercises:
    lab = 'L' + str(v)
    print(f"{lab:>6}", end='')
print()

for jmbag in students:
    lastname, name = students[jmbag]
    lastname_name = lastname + ', ' + name
    print(f"{jmbag:<11} {lastname_name:<20}", end='')
    for v in exercises:
        if v in scores[jmbag]:
            bod = scores[jmbag][v]
        else:
            bod = '-'
        print(f"{bod:>6}", end='')
    print()


