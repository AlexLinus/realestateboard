from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Classified, ClassifiedImage
from .forms import AddClassifiedForm, ImageClassifiedForm, ComplaintsForm, SearchClassifiedForm
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse, Http404
import random

# Create your views here.

class ClassifiedView(View):
    def get(self, request, flat_slug):
        classified = Classified.objects.get(is_active=True, slug__iexact=flat_slug)
        image_iteration_list = [i for i in range(1, classified.classified_images.count())]
        related_classifieds = Classified.objects.filter(is_active=True, nmb_rooms__iexact=classified.nmb_rooms).order_by("?")[:2] #order_by нужно, чтобы выбирать рандомно объекты. А не 3 последних.
        feautered_classifieds = Classified.objects.filter(is_active=True, nmb_rooms__iexact=classified.nmb_rooms).order_by("-flat_price")[:3]
        #Присваиваем в сессию переменную, для дальнейшего повышения просмотров
        try:
            views_slug = request.session['views_id_{}'.format(classified.id)]
        except:
            request.session['views_id_{}'.format(classified.id)] = classified.id
            classified.views += 1
            classified.save()

        return render(request, 'classified_detail.html', context={'classified': classified, 'image_iteration_list': image_iteration_list, 'related_classifieds': related_classifieds, 'feautered_classifieds': feautered_classifieds})

class AddClassidiedView(View):

    def get(self, request):
        ImageFormset = modelformset_factory(ClassifiedImage, form=ImageClassifiedForm, fields=('image',), extra=1)
        form = AddClassifiedForm()
        formset = ImageFormset(queryset=ClassifiedImage.objects.none())
        context = {
            'form': form,
            'formset': formset,
        }
        return render(request, 'add_classified.html', context={'form': form, 'formset': formset,})

    def post(self, request):
        ImageFormset = modelformset_factory(ClassifiedImage, form=ImageClassifiedForm, fields=('image',), extra=1)
        form = AddClassifiedForm(request.POST)
        formset = ImageFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            #commit=False нужно для того, чтобы объект создался но не сохранялся в базу.
            classified = form.save(commit=False)
            classified.author = request.user
            classified.is_active = True
            classified.save()
            print('Сейчас будет принт формсет клианед дата')
            print(formset.cleaned_data)
            for f in formset.cleaned_data:
                try:
                    print('Сейчас будет print F')
                    print(f)
                    print('Сейчас будет print(f[image])')
                    f['image']
                    print(f['image'])
                    #РАБОТАЕТ, НО НУЖНО РАЗОБРАТЬСЯ, ПОЧЕМУ ДУБЛИРУЕТ ИЗОБРАЖЕНИе. ЕСЛИ ОДНО НЕ ЗАПОЛНЕНО.
                    photo = ClassifiedImage(classified=classified, image=f['image'], author=request.user)
                    photo.save()
                except Exception as e:
                    print('Ошибка')
            return redirect(classified)
        else:
           return render(request, 'add_classified.html', context={'form': form, 'formset': formset, })


class ClassifiedEdit(View):
    def get(self, request, flat_slug):
        classified = Classified.objects.get(slug__iexact=flat_slug)
        if request.user == classified.author:
            ImageFormset = modelformset_factory(ClassifiedImage, form=ImageClassifiedForm, fields=('image',), extra=1)
            form = AddClassifiedForm(instance=classified)
            formset = ImageFormset(queryset=ClassifiedImage.objects.none())
            return render(request, 'edit_classified.html', context={'form': form, 'formset': formset, 'classified': classified})
        else:
            raise Http404('Извините, но данное объявление Вам не принадлежит!')

    def post(self, request, flat_slug):
        classified = Classified.objects.get(slug__iexact=flat_slug)
        if request.user == classified.author:
            if request.is_ajax():
                image_id_list = request.POST.getlist('image_id_list')
                #Если один элемент то get(), а если массив, чтобы выводился весь список, то getlist
                #print(request.__dict__) Это нужно для проверки что передается в запросе и какой тип запроса
                for image_id in image_id_list:
                    image = ClassifiedImage.objects.filter(id__iexact=image_id).delete()
                return JsonResponse({'OK': 'Готово!'})

            ImageFormset = modelformset_factory(ClassifiedImage, form=ImageClassifiedForm, fields=('image',), extra=1)
            form = AddClassifiedForm(request.POST, instance=classified)
            formset = ImageFormset(request.POST, request.FILES)
            if form.is_valid() and formset.is_valid():
                updated_classified = form.save()
                for f in formset.cleaned_data:
                    try:
                        is_image = ClassifiedImage.objects.filter(classified=classified, image__iexact=f['image']).exists()
                        print('был try is image')
                    except:
                        is_image = True
                        print('был except is image True')
                    if not is_image:
                        try:
                            print('Сработал not is image сейчас будет сохранение фото.')
                            photo = ClassifiedImage(classified=classified, image=f['image'], author=request.user)
                            photo.save()
                            print('Фото, сохранилось!')
                        except Exception as e:
                            print('Ошибка')
                return redirect(updated_classified)
        else:
            raise Http404('Извините, но данное объявление Вам не принадлежит!')


#Узнать, стоит ли при POST запросе проверять авторство.


class DeleteClassifiedView(View):
    def get(self, request, flat_slug):
        classified = Classified.objects.get(slug__iexact=flat_slug)
        if request.user == classified.author:
            return render(request, 'delete_classified.html', context={'classified': classified})
        else:
            raise Http404('Извините, но данное объявление Вам не принадлежит!')

    def post(self, request, flat_slug):
        classified = Classified.objects.get(slug__iexact=flat_slug).delete()
        return redirect('user_classifieds_url')

class ComplaintsView(View):
    questions_answers = {'На какой планете мы находимся?': 'земля', '30 минус 27': '3', 'Вы робот? - Напишите: Нет': 'нет', '51 минут 10': '41'}
    questions_list = list(questions_answers.keys())
    rand_choice = random.choice(questions_list)
    def get(self, request, flat_slug):
        form = ComplaintsForm()
        classified = Classified.objects.get(slug__iexact=flat_slug)
        print(ComplaintsView.questions_list)
        return render(request, 'complaint.html', context={'form': form, 'classified': classified, 'rand_choice': ComplaintsView.rand_choice, 'answer': ComplaintsView.questions_answers[ComplaintsView.rand_choice]})

    def post(self, request, flat_slug):
        form = ComplaintsForm(request.POST)
        classified = Classified.objects.get(slug__iexact=flat_slug)
        if form.is_valid() and ComplaintsView.questions_answers[ComplaintsView.rand_choice] == form.cleaned_data['captcha_answer'].lower():
                complaint = form.save(commit=False)
                complaint.classified = classified
                complaint.save()
                return redirect(classified)
        else:
            raise Http404('Извините, но произошла ошибка!!')

class SearchClassifiedView(View):
    def get(self, request):
        search_form = SearchClassifiedForm(request.GET)
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        flat_type = request.GET.get('nmb_rooms')
        classifieds = Classified.objects.filter(flat_price__gt=min_price, flat_price__lte=max_price, is_active=True, nmb_rooms=flat_type)
        return render(request, 'classified_search_detail.html', context={'search_form': search_form, 'classifieds': classifieds})