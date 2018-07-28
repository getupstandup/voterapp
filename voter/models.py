from django.contrib.gis.db import models


class District(models.Model):
    statefp = models.CharField(max_length=2)
    districtid = models.CharField(max_length=2)
    boundary = models.MultiPolygonField(srid=4326)

    def get_polygon(self):
        return str(self.boundary.coords)

    def get_polygon_lst(self):
        result = []
        for ii in self.boundary.coords:
            result_ = []
            for iii in ii[0]:
                result_.append([iii[1], iii[0]])
            result.append(result_)
        return result

    def __str__(self):
        return self.districtid


class Voter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    birthday = models.DateField()
    statefp = models.CharField(max_length=150, null=True, blank=True)
    cd115fp = models.CharField(max_length=250, null=True, blank=True)
    persuasion = models.CharField(max_length=250, null=True, blank=True)
    num_voters_in_household = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Email(models.Model):
    email = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.email


class Issue(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    question1 = models.CharField(max_length=300)
    question2 = models.CharField(max_length=300)
    question3 = models.CharField(max_length=300)
    question4 = models.CharField(max_length=300, null=True, blank=True)
    question5 = models.CharField(max_length=300, null=True, blank=True)
    jurisdiction = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title


class VoterResponse(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
    questions = models.CharField(max_length=50)

    def __str__(self):
        return self.issue.title


class Representative(models.Model):
    prefix = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_4 = models.CharField(max_length=100)
    st_dis_115 = models.CharField(max_length=100)
    bioguideid = models.CharField(max_length=20, null=True, blank=True)
    party = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
