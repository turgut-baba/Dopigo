from django import forms


class AddItem(forms.Form):
    name = forms.CharField(label='Item_name', max_length=50)
    quantity = forms.IntegerField(label='Quantity')
    price = forms.IntegerField(label='Price')
    cost = forms.IntegerField(label='Cost')

