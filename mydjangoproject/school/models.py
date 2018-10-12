from django.db import models


# class Subject(models.Model):
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name
#
# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     subjects = models.ManyToManyField(Subject)
#     def __str__(self):
#         return self.name



class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject,through="Score",through_fields=("student","subject"))
    def __str__(self):
        return self.name
    # subjects = models.ManyToManyField(Subject,through="Score",through_fields=("subject","student"))


class Score(models.Model):
    subject = models.ForeignKey(Subject)
    student = models.ForeignKey(Student)
    num = models.IntegerField()




