from django import forms
from .models import workAssignments, Requests

class workform(forms.ModelForm):
    class Meta:
        model=workAssignments
        widgets={
            "assignDate" : forms.DateInput(attrs={'type':'datetime-local'}),
            "dueDate" : forms.DateInput(attrs={'type':'datetime-local'}),
            }

        fields=[
            "work",
            "assignDate",
            "dueDate",
            "taskerId",

        ]

class makeRequestForm(forms.ModelForm):
    class Meta:
        model=Requests
        widgets={
            "requestDate" : forms.DateInput(attrs={'type':'datetime-local'}),
            }

        fields=[
            "requestMessage",
            "requestDate",
            "destinationEmployeeId",
        ]