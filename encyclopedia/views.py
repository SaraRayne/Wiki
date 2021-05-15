import markdown2
import random
from django.shortcuts import render
from django.shortcuts import redirect

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    # Look for entry title entered
    entry = util.get_entry(title)
    # If entry doesn't exist, take to error page
    if entry == None:
        return render(request, "encyclopedia/error.html")
    # If entry exists, display in HTML
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry), "title": title
        })

def search(request):
    # Get query
    query = request.POST['q']

    # Get list of all entries in encyclopedia
    entries = util.list_entries()

    if request.method == "POST":
        # Compare query to see if it's in the list of entries
        if query in entries:
            # If it is, send them to the corresponding entry
            return redirect('title', title=query)
        # If query does not match existing entry, send them to a resutls page
        else:
            # Create empty list to store all possible results matching query
            results = []
            # Loop through all entries to compare to query
            for entry in entries:
                # Check if query is a substring of an entry
                if query in entry:
                    # If it is a substring, add it to the possible results list
                    results.append(entry)
            # If results list is empty, "no matches" message is shown
            if not results:
                return render(request, "encyclopedia/none.html")
            # If the list is not empty, results page is shown
            else:
                return render(request, "encyclopedia/search.html", {
                    "results": results
                    })

def new_page(request):
    if request.method == "POST":
        # Retrieve title
        title = request.POST['title']
        # Retrieve text
        text = request.POST['new_entry']
        # Retrieve current entries
        entries = util.list_entries()
        # Check if entry exists based on title
        if title in entries:
            # If it already exists, display error
            return render(request, "encyclopedia/invalid.html")
        else:
            # Send info to save_entry function
            util.save_entry(title, text)

            # Then send info to title function to render page
            return redirect('title', title=title)

    else:
        return render(request, "encyclopedia/new_page.html")

def edit(request):
    if request.method == "POST":
        title = request.POST['title']

        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "page": page, "title": title
        })

def save_edits(request):
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['edit_entry']
        util.save_entry(title, text)

        return redirect('title', title=title)

def random_choice(request):
    # when link for random is clicked, list of all entries should be pulled
    # somehow, from that list, a random page should be grabbed and title function should run
    entries = util.list_entries()

    random_choice = random.choice(entries)

    return redirect('title', title=random_choice)
