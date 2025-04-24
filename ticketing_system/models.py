from django.contrib.auth.models import User
from django.db import models

# Create your models here.
def ticket_attachment_upload_path(instance, filename):
    return f'tickets/{instance.ticket.id}/{filename}'

class TicketStausEnum(models.IntegerChoices):
    DRAFT= 1,'DRAFT'
    ONGOING = 2,'ONGOING'
    COMPLETED = 3,'COMPLETED'
    ARCHIVED= 4,'ARCHIVED'

class CommonFields(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True)
    name = models.CharField(max_length=40,unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Ticket(CommonFields):
    status = models.PositiveIntegerField(choices=TicketStausEnum.choices,default=TicketStausEnum.DRAFT)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='tickets')


class Project(CommonFields):
    status = models.PositiveIntegerField(choices=TicketStausEnum.choices, default=TicketStausEnum.DRAFT)
    # assigned_to = models.ManyToManyField(User,through='LinkingUserToProject',related_name='assigned_projects')


class LinkingUserToProject(models.Model):
    user = models.ForeignKey(to=User,related_name='projects',on_delete=models.PROTECT)
    project = models.ForeignKey(to=Project,related_name='projects',on_delete=models.PROTECT)

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=ticket_attachment_upload_path)
    uploaded_date = models.DateTimeField(auto_now_add=True)