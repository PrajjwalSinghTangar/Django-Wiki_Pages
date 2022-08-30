from django.shortcuts import render
from . import util
from django import forms


## Search Class
class search_form(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'myfieldclass'}))

## New Page Forms

class title_form(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'mytitleclass'}))

class content_form(forms.Form):
    content = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'mycontentclass'}))

## Index Page 

def index(request):
    query=""
    response=[]

    if request.method == "POST":
        form = search_form(request.POST)

        if form.is_valid():
            query = form.cleaned_data["search"]

            for title in util.list_entries():
                if query.lower() == title.lower():
                    return wiki(request,title)
                
                if query.lower() in title.lower():
                    response.append(title)
        
        if response != []:
            return render(request, "encyclopedia/searchbar.html", {
                "results": response,
                "form": search_form()
            })
        else:
            return wiki(request, title)

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": search_form()
        })

## Wiki page search with error 404 page when not found!

def wiki(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/404.html", {
            "title": title.upper(),
            "message": "Page not found, Error:404!",
            "form": search_form()
        })
    else:
        return render(request, "encyclopedia/pages.html",{
            "title": title.upper(),
            "body": util.get_entry(title),
            "form": search_form()
        })

## Create New Page

def newpage(request):
    titleform = title_form(request.POST)
    contentform = content_form(request.POST)
    if request.method == "POST":
        if titleform.is_valid():
            querytitle = titleform.cleaned_data["title"]
        if contentform.is_valid():
            querycontent = contentform.cleaned_data["content"]

            if util.get_entry(querytitle) != None:
                return render(request, "encyclopedia/404.html", {
                "message": "Entry has already been done for this particular topic!"})
            else:
                util.save_entry(querytitle, '#' + querytitle + '\n' + querycontent)
                return wiki(request, querytitle)

    else:
        return render(request, "encyclopedia/newpage.html", {
            "title": title_form(),
            "body": content_form(),
            "form": search_form()
    })