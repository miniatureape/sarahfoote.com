from main.forms import *
from main.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.html import escape
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail

def home(request):
    if request.user.is_authenticated():
        posts = BlogPost.objects.all().reverse()[:3]
    else:
        posts = BlogPost.objects.filter(published=True).reverse()[:3]
    return render_to_response('front-blog.html', {'posts_list': posts},
                              context_instance=RequestContext(request))

@login_required
def add_photo(request):
    "Wrapper to handle Add Photo popup"
    form = PhotoForm
    return handle_pop_up(request, form, 'Photo')

@login_required
def add_file(request):
    "Wrapper to hander Add File Popup"
    form = FileForm
    return handle_pop_up(request, form, 'File')

@login_required
def publish_post(request, object_id):
    "Toggles the published boolean on object and redirects to object detail"
    import datetime
    post = BlogPost.objects.get(id=object_id)
    post.published = not post.published
    if post.published:
        post.published_on = datetime.datetime.now()
    post.save()        
    return HttpResponseRedirect(reverse('main_post_detail', args=[post.slug]))
    
def buy_category(request, category=None):
    categories = select_attr(Item, 'category')    
    items = Item.objects.all().filter(category=category)
    return render_to_response('items.html', {'categories': categories, 'item_list': items, 'category': category},
                              context_instance=RequestContext(request))

def contact(request):
    "Contact Page. Sends Email to email address in latest about object."
    msg = None    
    if request.method == 'POST':
        form = ContactForm(request.POST) 
        if form.is_valid():
            # Get Sarah's Email from her About obj
            try:
                about = About.objects.latest()
                email = about.email
            except About.DoesNotExist:
                email = 'sarah.signe@gmail.com'
            # Get data from form and mail to sarah
            name = form.cleaned_data['name']
            sender = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']            
            recipients = ['sarahsigne@gmail.com']
    
            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            
            msg = "Thank you for contacting Sarah"
            form = None
    else:
        form = ContactForm()
    return render_to_response('contact.html', {
        'msg': msg,
        'form': form,
    }, context_instance=RequestContext(request))
    
def about(request):
    "About page. Shows latest about object."
    try:
        aboutobj = About.objects.latest()
    except About.DoesNotExist:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('main_add_about'))
        else:
            raise Http404
    return render_to_response('about.html', {'aboutobj': aboutobj},
                              context_instance=RequestContext(request))

def items(request):
   items = select(Item)
   categories = select_attr(Item, 'category')
   extra = {'categories': categories}
   return list_detail.object_list(
           request,
           queryset = items,
           template_name = 'items.html',
           template_object_name = 'item',
           extra_context = extra
   )

def items_by_category(request, category=None):
    "Filters item list by category"
    items = Item.objects.all().filter(category=category)
    categories = select_attr(Item, 'category')    
    extra = {'category': category, 'categories': categories}
    return list_detail.object_list(
           request,
           queryset = items,
           template_name = 'items.html',
           template_object_name = 'item',
           extra_context = extra
    )

def handle_pop_up(request, form_class, field):
    "Mimics Django admin Add Another Pop Up"
    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_object = form.save()
            except forms.ValidationError, error:
                new_object = None
            if new_object:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                            (escape(new_object._get_pk_val()), escape(new_object)))
    else:
        form = form_class()
    page_context = {'form': form, 'field': field}
    return render_to_response("popup.html", page_context, context_instance=RequestContext(request))
