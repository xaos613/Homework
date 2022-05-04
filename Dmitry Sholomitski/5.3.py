import csv

def file_to_list(file_path):
    students_list = []
    with open(file_path) as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            students_list.append(row)
    return students_list


def get_top_performers(file_path, number_of_top_students=5):
    students_list = file_to_list(file_path)
    sorted_keys = sorted(students_list, key= lambda x: float(x["average mark"]), reverse=True)

    return [x['student name'] for x in sorted_keys[:number_of_top_students]]

def get_by_age(file_path):
    students_list = sorted(file_to_list(file_path), key= lambda x: int(x["age"]), reverse=True)

    with open('data/result.csv','x', newline='') as csvfile:


        fieldnames = ['student name','age','average mark']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in students_list:
            writer.writerow(x)




print(get_top_performers("data/students.csv"))

get_by_age("data/students.csv")