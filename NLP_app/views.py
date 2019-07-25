from django.shortcuts import render
from django.http import HttpResponse
from . import forms, parcer


def index(request):
    my_dict = {'insert_me':"Ok,it's from views somehow. And it's from views ."}
    return render(request, 'NLP_app/index.html')


# Create your views here.
def input(request):
    inp_form = forms.InputForm()
    if request.method == 'POST':
        inp_form = forms.InputForm(request.POST)
    if inp_form.is_valid():
        print("YEP")
        print(inp_form)
        print(inp_form.cleaned_data['input'])
        adress = "C:\\Dima\\NLP\\shinbun_analyse\\07.11.2019__shakai.txt"
        file = adress.split('\\')[-1]
        string = parcer.freq_from_one_file(adress,inp_form.cleaned_data['input'])
        kanji = inp_form.cleaned_data['input']
        translation = parcer.dict_mult_symbol(inp_form.cleaned_data['input'])
        return render(request, 'NLP_app/index.html', {'inp_form':inp_form, 'text':file, 'word': kanji, 'frequency':string, 'translate': translation[0], 'pron': translation[1]})
    else:
        return render(request, 'NLP_app/index.html', {'inp_form': inp_form})


def output(request):
    out_form = forms.OutputForm()
    return render(request, 'NLP_app/index.html', {'out_form':out_form})
