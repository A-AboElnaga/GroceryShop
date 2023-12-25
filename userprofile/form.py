from django import forms
from .models import Addresses, UserProfile


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = "__all__"


class VisitorShippingAddressForm(ShippingAddressForm):
    email = forms.EmailField()
    
class EditShippingAddress(forms.Form):
    addresses = forms.ModelChoiceField(queryset=Addresses.objects.none())
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditShippingAddress, self).__init__(*args, **kwargs)
        self.fields['addresses'].queryset = UserProfile.objects.get(user=self.user).user_addresses.all()