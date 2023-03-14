from django import forms
from phonenumber_field.formfields import PhoneNumberField

COUNTRY_CHOICE=[
('Pak','Pakistan')
]

CITY_CHOICES=[
('Islamabad','Islamabad'),
('Rawalpindi','Rawalpindi'),
('Faisalabad','Faisalabad'),
('Lahore','Lahore'),
('Multan','Multan'),
('Peshawar','Peshawar'),
]

#placehoolder in a drop down list
blank_choice1=[('b','(Select Country)'),]
blank_choice2=[('b','(Select City)'),]

class CheckoutForm(forms.Form):
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    street_address=forms.CharField(widget=forms.TextInput(attrs={
    'placeholder':'1234 Main St','class':'form-control'
    }))
    apartment_address=forms.CharField(required=False,widget=forms.TextInput(attrs={
    'placeholder':'Apartment or suite','class':'form-control'
    }))        #apartment address is not a required field (optional)
    country=forms.ChoiceField(choices=blank_choice1+COUNTRY_CHOICE,widget=forms.Select(attrs={
    'class':'custom-select d-block w-100'
    }))        #user can select any of the available choices
    city=forms.ChoiceField(choices=blank_choice2+CITY_CHOICES,widget=forms.Select(attrs={
    'class':'custom-select d-block w-100'
    }))        #user can select any of the available choices
    postal_code=forms.CharField(max_length=5,widget=forms.TextInput(attrs={
    'placeholder':'00000','class':'form-control','pattern':'[0-9]+', 'title':'Enter numbers Only ',
    }))         #constraint applied so that only numeric value can be entered
    phone=PhoneNumberField(widget=forms.TextInput(attrs={
    'placeholder':'+92 XXX XXXXXXX','class':'form-control','title':'Enter according to the pattern'
    }))         #phone number field prevents user from entering wrong phone number
