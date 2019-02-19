from django.shortcuts import render
from django.views.generic import (ListView, CreateView, DeleteView,
                                    UpdateView, DetailView)
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Records, Comments
from .forms import CreateRecordForm, CommentsForm

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
# Create your views here.

class index_views(ListView):
    model = Records
    paginate_by = 5
    context_object_name = 'record_users'
    template_name = 'entradas/index.html'


def tags_list(request, tag_slug=None):
    #function list for tags
    object_list = Records.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'entradas/list_tags.html',
                  {'page': page,
                   'record_users': posts,
                   'tag': tag})


class up_Record_views(LoginRequiredMixin, CreateView):
    model = Records
    form_class = CreateRecordForm
    template_name = 'entradas/up_record.html'
    success_url = reverse_lazy('entradas:index')

    #Receive file and asigned user
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            Record = form.save(commit=False)
            Record.author = User.objects.get(username=request.user)
            Record.save()
            #use to save tags
            form.save_m2m()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class Record_views(DetailView):
    model = Records
    template_name = 'entradas/view_record.html'
    form_class = CommentsForm

    def get_context_data(self, **kwargs):
        context =super(Record_views, self).get_context_data(**kwargs)
        sumaVistas = context['object']
        sumaVistas.views += 1
        sumaVistas.save()
        if 'form' not in context:
            context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            pk = kwargs['pk']  
            slug = kwargs['slug']
            comentario = form.save(commit=False)
            comentario.author = User.objects.get(username=request.user)
            comentario.recordOwn = self.model.objects.get(pk=pk)
            comentario.save()
        return HttpResponseRedirect(comentario.recordOwn.get_absolute_url())

class Record_edit_views(LoginRequiredMixin, UpdateView):
    model = Records
    form_class = CreateRecordForm
    template_name = 'entradas/edit_record.html'

    def get_success_url(self):
    # if you are passing 'pk' from 'urls'
    # capture that 'pk' and pass it to 'reverse_lazy()' function
    #send this slug because edit the title else send slug = self.kwargs['slug']
        slug=self.object.slug
        pk=self.object.id 
        return reverse_lazy('entradas:record_view', kwargs={'pk': pk, 'slug': slug })
