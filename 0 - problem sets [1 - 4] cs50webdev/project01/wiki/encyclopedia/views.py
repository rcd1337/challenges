from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from . import util
import random
import markdown2


def index(request):
    # Handles the search
    if request.method == "POST":
        entry = util.get_entry(request.POST['q'])
        if entry != None:
            # Return searched page
            return redirect(f"/wiki/{request.POST['q']}")
        else:
            entry = request.POST['q']
            entries = util.list_entries()
            matched_entries = []
            # Search for substring in entries
            for i in range(len(entries)):
                if entry.lower() in entries[i].lower():
                    matched_entries.append(entries[i])
            if not matched_entries:
                return render(request, "encyclopedia/search.html", {
        "entries": matched_entries
    })
            else:
                return render(request, "encyclopedia/search.html", {
        "entries": matched_entries
    })
    
    # Homepage
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, wikipage):
    # Checks if page exists and renders it
    if util.get_entry(wikipage) != None:
        html = markdown2.markdown(util.get_entry(wikipage))
        return render(request, "encyclopedia/wikipage.html", {
            "pagename": wikipage,
            "html": html
        })
    # Render an apalogy page if page not found
    else:
        return render(request, "encyclopedia/apology.html")

def new(request):
    if request.method == "POST":
        form = request.POST
        error = ""
        # Validates title
        if not form['np-title']:
            error = "Title must be provided"
            return render(request, "encyclopedia/newpageapology.html", {
            "error": error
        })
        if form['np-title'].lower() in [entry.lower() for entry in util.list_entries()]:
            error = "Title already exists"
            return render(request, "encyclopedia/newpageapology.html", {
            "error": error
        })
        
        # Validates text
        if not form['np-text']:
            error = "Text content must be provided"
            return render(request, "encyclopedia/newpageapology.html", {
            "error": error
        })
        
        # Saves new entry
        util.save_entry(form['np-title'], form['np-text'])
        return redirect(f"/wiki/{form['np-title']}")
    return render(request, "encyclopedia/newpage.html")
        
def edit(request):
    # Edits page coming from /wiki/<entry>
    if request.method == "GET":
        # Returns error if accessing directly /w/edit
        if not request.GET:
            return render(request, "encyclopedia/apology.html")
        
        # Reads entry content and renders edit page
        content = util.get_entry(request.GET['w-title'])
        return render(request, "encyclopedia/edit.html", {
            "title": request.GET['w-title'],
            "text": content
        })
    
    # Delivers changes to given entry
    if request.method == "POST":
        form = request.POST
        
        # Validates entry contet
        if not form['ed-text']:
            return HttpResponse("there must be something written")
        
        # Saves new entry content
        util.save_entry(form['ed-title'], form['ed-text'])
        return redirect(f"/wiki/{form['ed-title']}")

def randompage(request):
    # Chooses a random item from entries list and renders it's page
    randompage = random.choice(util.list_entries())
    return redirect(f"/wiki/{randompage}")
