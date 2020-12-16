from django.forms import ModelForm, Textarea
from django import forms
from .models import Auction, Category
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime
class ListingForm(forms.Form):
    title = forms.CharField(max_length= 64, label= 'Listing title')
    category = forms.ModelChoiceField(queryset= Category.objects)
    # category = forms.ChoiceField(choices= Category.objects.values_list())
    description = forms.CharField(widget= forms.Textarea)
    #start_time = forms.DateTimeField(widget= DateTimePickerInput)
    start_time = forms.DateTimeField(initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), required=False)
    price = forms.IntegerField(min_value= 0)
    img_rul = forms.URLField(label= 'Image URL')
    # class Meta:
    #     model = Auction
    #     exclude = ('user',)

    #     widgets = {
    #         'description': Textarea(attrs={'cols': 80, 'rows': 5}),
    #     }
    #     labels = {
    #         'title': ('Listing title'),
    #     }
    #     help_texts = {
    #         'title': ('Some useful help text.'),
    #     }
    #     error_messages = {
    #         'title': {
    #             'max_length': ("This writer's name is too long."),
    #         },
    #     }

    
    # def __init__(self, *args, **kwargs):
    #     self._user = kwargs.pop('user')
    #     super(ListingForm, self).__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     inst = super(ListingForm, self).save(commit=False)
    #     inst.author = self._user
    #     if commit:
    #         inst.save()
    #         self.save_m2m()
    #     return inst
