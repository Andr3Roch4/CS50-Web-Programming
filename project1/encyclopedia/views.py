from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from markdown2 import Markdown


from . import util



def index(request):
    if request.method == "POST":
        searchtitle = request.GET.get("q")
        if util.get_entry(searchtitle):
            return render(request, "encyclopedia/title.html", {
                "titletext": util.get_entry(searchtitle),
                "title": searchtitle
            })
        elif not util.get_entry(searchtitle):
            return render(request, "encyclopedia/titlenotfound.html")

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
        if util.get_entry(title):
            markdowner = Markdown()
            titletext = markdowner.convert(util.get_entry(title))
            return render(request, "encyclopedia/title.html", {
                "titletext": titletext,
                "title": title
            })
        elif not util.get_entry(title):
            return render(request, "encyclopedia/titlenotfound.html")
        
def searchresult(request):
    searchtitle = request.GET.get("q")
    if util.get_entry(searchtitle):
            return HttpResponseRedirect(f"/{searchtitle}")
    elif not util.get_entry(searchtitle):
        results = []
        for entrie in util.list_entries():
            if str.lower(searchtitle) in str.lower(entrie):
                results.append(entrie)
        return render(request, "encyclopedia/searchresult.html", {
            "results": results
        })
    
def createnew(request):
    content = request.GET.get("content")
    title = request.GET.get("title")
    if str.lower(title) in str.lower(util.list_entries()):
        return render(request, "encyclopedia/titleexists.html", {
             "content": content
        })
    else:
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/{title}")
    
def editpage(request):
    title = request.GET.get("title")
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "content": content,
            "title": title
        })
    elif request.method == "POST":
        newcontent = request.POST.get("newcontent")
        util.save_entry(title, newcontent)
        return HttpResponseRedirect(f"/{title}")

def randomtitle(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(f"/{title}")