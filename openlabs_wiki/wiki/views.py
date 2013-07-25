from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.core.context_processors import csrf
from wiki.models import Article, history
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.http import HttpResponseRedirect


def create_page(request):
    """creates a new page if user is logged in """
    if request.user.is_authenticated():
        content = ""
        return render_to_response(
            "create.html", {"content": content},
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect('/accounts/login')


def save(request):
    """saves the page created"""
    title = request. POST["title"]
    checkvalue = request.POST.get('check', False)
    owner = request.user.username
    try:
        page = Article.objects.get(title=title, user=owner)
        return render_to_response("alreadyexists.html")
    except Article.DoesNotExist:
        page = Article(title=title, user=owner, flag=checkvalue)
    page.save()
    getpage = Article.objects.get(title=title, user=owner)
    content = request.POST["content"]
    savecontent = history(page_id=getpage, content=content, edited_by=owner)
    savecontent.save()
    return HttpResponseRedirect("/wiki/"+str(getpage.id)+"/")


def view_page(request, page_id):
    """to view a page based on page_id"""
    page = Article.objects.get(id=page_id)
    page_title = page.title
    page_content = history.objects.filter(page_id=page_id) \
        .latest('edited').content
    return render_to_response(
        "view.html", {
            "page_title": page_title,
            "content": page_content,
            "page_id": page_id
        }
    )


def edit_page(request, page_id):
    """function edits the existing page"""
    page = Article.objects.get(id=page_id)
    page_title = page.title
    page_content = history.objects.filter(page_id=page_id) \
        .latest('edited').content
    return render_to_response(
        "edit.html", {
            "page_title": page_title, "content": page_content,
            "page_id": page_id
            }, context_instance=RequestContext(request)
    )


def save_edit(request, page_id):
    """saves the page after edit"""
    page = Article.objects.get(id=page_id)
    page_title = page.title
    page_content = request.POST["content"]
    loggedin_user = request.user.username
    newchange = history(
        page_id=page, content=page_content, edited_by=loggedin_user
    )
    newchange.save()
    content = history.objects.filter(page_id=page_id).latest('edited').content
    return render_to_response(
        "view.html", {
            "page_title": page_title, "content": content,
            "page_id": page_id}
    )
