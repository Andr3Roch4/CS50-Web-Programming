from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


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
            return render(request, "encyclopedia/title.html", {
                "titletext": util.get_entry(title),
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