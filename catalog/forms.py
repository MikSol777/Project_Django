from django import forms
from .models import Product, Category

FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control-file'

            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название продукта'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание продукта'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = 'Введите цену продукта'
            elif field_name == 'category':
                field.widget.attrs['class'] += ' form-select'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Название продукта не может содержать слово '{word}'.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise forms.ValidationError(f"Описание продукта не может содержать слово '{word}'.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена продукта не может быть отрицательной.")
        return price


