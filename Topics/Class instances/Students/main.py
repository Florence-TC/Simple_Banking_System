class Student:

    def __init__(self, name, last_name, birth_year):
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        # calculate the student_id here
        self.student_id = name[0] + last_name + str(birth_year)


student_1 = Student(input(), input(), int(input()))
print(student_1.student_id)
  