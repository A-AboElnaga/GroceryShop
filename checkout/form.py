from django.forms import CharField, IntegerField, Form, ModelForm, ValidationError, DateField, SelectDateWidget
from .models import CheckoutLine
#from django.core.validators import RegexValidator


class CheckoutLineForm(ModelForm):
    class Meta:
        model = CheckoutLine
        exclude = ('product', 'checkout')
        
    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        super(CheckoutLineForm, self).__init__(*args, **kwargs)
        
    
    def clean(self):
        super(CheckoutLineForm, self).clean()
        quantity = self.cleaned_data.get('quantity')
        
        product_stock = self.product.stock
        
        if product_stock < quantity:
            self.add_error('quantity', 'insufficient stock')
            
        return self.cleaned_data

class MonthYearWidget(SelectDateWidget):
    def create_select(self, name, field, value, val, choices):
        # Override create_select method to display only month and year
        if field.widget.attrs['name'] == self.month_field % name:
            choices = [(x, x) for x in range(1, 13)]
        elif field.widget.attrs['name'] == self.year_field % name:
            choices = [(x, x) for x in range(self.years[0], self.years[1] + 1)]
        return super().create_select(name, field, value, val, choices)


def clean_card_number(card_number):
    if not card_number.isdigit():
        raise ValidationError("Card number should contain only digits.")
    if len(card_number) < 16:
        raise ValidationError("Card number should contain exactly 16 digits.")
    return card_number

def clean_cvv(cvv):
    if not cvv.isdigit():
        raise ValidationError("CVV should contain only digits.")
    if len(cvv) < 3:
        raise ValidationError("CVV should contain 3 to 4 digits.")
    return cvv
    


class PaymentCardForm(Form):
    
    card_number = CharField(label='Card Number', max_length=16, validators=[clean_card_number])
    expiration_date = DateField(widget=MonthYearWidget(years=range(2000, 2030), empty_label=("Choose Year", "Choose Month", "")))
    cvv = CharField(label='CVV', max_length=4, validators=[clean_cvv])
    cardholder_name = CharField(label='Cardholder Name', max_length=100)
