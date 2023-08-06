from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

GENDER_STATUS = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class student(models.Model):
    student_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    dob = models.DateField()
    parent_name1 = models.CharField(max_length=80)
    parent_name2 = models.CharField(max_length=80)
    phone = models.CharField(max_length=14)
    contact_number2 = models.CharField(max_length=14, blank=True)
    joining_date = models.DateField()
    email_id = models.CharField(max_length=360)
    upload_student_image = models.ImageField(upload_to="student_student_image_url/")
    grade_while_joining = models.CharField(max_length=50)
    gender = models.TextField(choices=GENDER_STATUS)

    def __str__(self):
        return self.first_name

    def Student(self):
        if self.upload_student_image:
            return mark_safe('<img src="/media/%s" width="70" height="70" />' % (self.upload_student_image))
        else:
            return mark_safe('<img src="/media/document/default.jpg" width="50" height="50" />')

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name


class course(models.Model):
    course_name = models.CharField(max_length=500)
    course_fee = models.FloatField()

    def __str__(self):
        return self.course_name

class attendance(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    date = models.DateField()
    presence = models.BooleanField()


class enrollment(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    fees_paid = models.FloatField()
    enrolled = 'ENR'
    in_progress = 'IPR'
    discontinued = 'DSC'
    completed = 'CMP'

    STATUS_CHOICES = [
        (enrolled, 'Enrolled'),
        (in_progress, 'In-progress'),
        (discontinued, 'Discontinued'),
        (completed, 'Completed'),
    ]

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=enrolled,
    )



