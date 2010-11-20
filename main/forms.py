from django import forms
from main.models import *
from django.template.loader import render_to_string
from ckeditor.widgets import CKEditorWidget
from django.core.urlresolvers import reverse

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()        
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'credit', 'alt')

class FileForm(forms.ModelForm):
    class Meta:
        model = File

class MTMultiSelect(forms.SelectMultiple):
    class Media:
        js = ('js/mtmultiselect.js',)
    
    def render(self, name, value, *args, **kwargs):
        html = super(MTMultiSelect, self).render(name, value,  *args, **kwargs)
        mtmulti = render_to_string("forms/MTMultiSelect.html")
        return html+mtmulti
    
class MTMultiSelectPlus(MTMultiSelect):
    def render(self, name, value, *args, **kwargs):
        html = super(MTMultiSelectPlus, self).render(name, value, *args, **kwargs)
        plus = render_to_string("forms/MultiSelectWithPopup.html", {'field': name, 'addurl': self.addurl})
        return html + plus

class ItemForm(forms.ModelForm):
    "Add the Model class to the widget so it knows the url for the popup"
    widget = MTMultiSelectPlus()
    widget.addurl = '/photos/add'
    photos = forms.ModelMultipleChoiceField(Photo.objects, required=False, widget=widget)
    
    class Meta:
        model = Item
        exclude = ('slug',)

class BlogPostForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(Item.objects, required=False, widget=MTMultiSelect)
    text = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'items']

class SelectPlus(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectPlus, self).render(name, *args, **kwargs)
        plus = render_to_string("forms/MultiSelectWithPopup.html", {'field': name, 'addurl': self.addurl})
        return html + plus

class PressForm(forms.ModelForm):
    widget = SelectPlus()
    widget.addurl = '/file/add'
    file = forms.ModelChoiceField(File.objects, required=False, widget=widget)

    class Meta:
        model = Press

