from django import forms
from shop.models import ProductModel


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = [
            "title",
            "slug",
            "image",
            "proudct_category",
            "stock",
            "price",
            "discount_percent",
            "status",
            "description",
            "brif_description",
        ]
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['slug'].widget.attrs['class'] = 'form-control'
        self.fields['proudct_category'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['brif_description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['type'] = 'number'
        self.fields['status'].widget.attrs['class'] = 'form-select'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['discount_percent'].widget.attrs['class'] = 'form-control'
            

            