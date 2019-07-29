from django.shortcuts import render
from django.http import HttpResponse
from . import forms, parcer
from django.template import Template, Context
from django.template.loader import get_template, render_to_string

def index(request):
    my_dict = {'insert_me':"Ok,it's from views somehow. And it's from views ."}
    return render(request, 'NLP_app/translator_and_analyser.html')


# Create your views here.
def translator_input(request):
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
        return render(request, 'NLP_app/translator_and_analyser.html', {'inp_form':inp_form, 'text':file, 'word': kanji, 'frequency':string, 'translate': translation[0], 'pron': translation[1]})
    else:
        return render(request, 'NLP_app/translator_and_analyser.html', {'inp_form': inp_form})


def parser_input(request):
    parser_form = forms.OutputForm()
    return render(request, 'NLP_app/parser.html', {'out_form':parser_form})

def menu(request):
    context = {
        'contacts': [
            '<li class="menu_link"><a href="/parser/" class="parser">Parser</a></li>',
            '<li class="menu_link"><a href="/parser/" class="parser">Parser</a></li>',
            '<li class="menu_link"><a href="/parser/" class="parser">Parser</a></li>',
        ]
    }

    '''
    <ul class="menu">
    <h3>Menu:</h3>
    
    </ul>
    '''
    response_string = render_to_string()


def test_page(request):
    template = Template(
    '''
     <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>MY NLP APP</title>
    </head>
    <body>
            <div>
            <h1>Hello, this is test app I've made for HSE interview!</h1>
            <h2>'This is {{ name }} '</h2>
                <ul class="menu">
                    <h3>Menu:</h3>
                    <li class="menu_link">
                        <a href="/parser/" class="parser">Parser</a>
                    </li>
                    <li class="menu_link">
                        <a href="/" class="translator_and_analyser">Translator</a>
                    </li>
                     <li class="menu_link">
                        <a href="/test/" class="translator_and_analyser">Test page</a>
                    </li>
                </ul>
    </body>
    </html>

    '''
    )
    context = Context({'name': "TEST-ONE-TWO" })
    response_string = template.render(context)
    return HttpResponse(response_string)