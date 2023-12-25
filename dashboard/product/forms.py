from django import forms 
from product.models import ProductImage
from django_countries.fields import CountryField
from product.models import Brand

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        exclude = ('product','alt')
        
          
class FilterForm(forms.Form):
    min_price = forms.FloatField(label='Min Price', required=False)
    max_price = forms.FloatField(label='Max Price', required=False)
    brand_Nationality = CountryField(blank_label='Any Nationality', blank=True).formfield()
    brand_name = forms.CharField(required = False, label = 'Brand Name')
    

    brand_name_choice = forms.ModelChoiceField(label = 'Brand Name Choice',queryset= Brand.objects.all(),
                                               widget = forms.Select, empty_label= "All Brands",
                                               to_field_name = 'name',required=False)
    
    product_name = forms.CharField(required = False, label = 'Product Name')

    