from django import forms


class NameOfNewRestaurant(forms.Form):
    name = forms.CharField(label="Name", max_length=25, empty_value='42',
                           widget=forms.TextInput(attrs={'placeholder': 'W'}))


class NewMenuItem(forms.Form):
    CHOICES = [('Entree', 'Entree'), ('Appetizer', 'Appetizer'), ('Beverage', 'Beverage'), ('Dessert', 'Dessert')]
    name = forms.CharField(label="Name", max_length=30, empty_value='42',
                           widget=forms.TextInput(attrs={'placeholder': 'W'}))
    price = forms.CharField(label="Price", max_length=8, widget=forms.TextInput(attrs={'placeholder': '0.99'}))
    description = forms.CharField(label='Description', max_length=300,
                                  widget=forms.Textarea(attrs={'placeholder': 'description', 'cols': 27}))
    course = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

# class SetNameForm(forms.Form):
#     user_name = forms.CharField(label="Your name", max_length=25, empty_value='NoName', required=False)
