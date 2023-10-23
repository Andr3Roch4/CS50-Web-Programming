from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
import markdown2


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
        if util.get_entry(title):
            titletext = markdown2.markdown(util.get_entry(title))
            return render(request, "encyclopedia/title.html", {
                "titletext": titletext,
                "title": title
            })
        elif not util.get_entry(title):
            return render(request, "encyclopedia/titlenotfound.html")
        
def searchresult(request):
    searchtitle = request.GET.get("q")
    if util.get_entry(searchtitle):
            return HttpResponseRedirect(reverse("title", args=[searchtitle]))
    elif not util.get_entry(searchtitle):
        results = []
        for entrie in util.list_entries():
            if str.lower(searchtitle) in str.lower(entrie):
                results.append(entrie)
        return render(request, "encyclopedia/searchresult.html", {
            "results": results
        })
    
def createnew(request):
    if request.method == "GET":
        return render(request, "encyclopedia/createnew.html")
    elif request.method == "POST":
        post = request.POST
        content = post["content"]
        title = post["title"]
        for entrie in util.list_entries():
            if str.lower(title) == str.lower(entrie):
                errormessage = f"A page already exists for {title}, try editing it!"
                return render(request, "encyclopedia/createnewerror.html", {
                    "content": content,
                    "error": errormessage
                })
        if not content:
            errormessage = "Must write something to save a new Encyclopedia page!"
            return render(request, "encyclopedia/createnewerror.html", {
                    "content": content,
                    "error2": errormessage
                })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=[title]))
    
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
        return HttpResponseRedirect(reverse("title", args=[title]))

def randomtitle(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", args=[title]))