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
import difflib

def create_page(request):
    """creates a new page if user is logged  """
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
    if request.user.is_authenticated():
        loggedin_user = request.user.username
        page = Article.objects.get(id=page_id)
        page_title = page.title
        owner = page.user
        page_content = history.objects.filter(page_id=page_id) \
            .latest('edited').content
        return render_to_response(
            "edit.html", {
                "page_title": page_title,
                "content": page_content, "page_id": page_id,
                'loggedin_user': loggedin_user, 'owner': owner
                }, context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect('/accounts/login')


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


def all_articles(request):
    """shows all the articles based on if user is logged in or not"""
    status = request.user.is_authenticated()
    if request.user.is_authenticated():
        owner = request.user.username
        all_pages = Article.objects.filter(Q(user=owner) | Q(flag=False))
        return render_to_response(
            "articles.html", {
                'all_pages': all_pages, 'status': status}
        )
    else:
        all_pages = Article.objects.all().filter(flag=False)
        return render_to_response(
            "articles.html", {
                'all_pages': all_pages, 'status': status}
        )


def view_history(request, page_id):
    """
    shows the history of changes applied to a page
    """
    page = Article.objects.get(id=page_id)
    page_title = page.title
    page_history = history.objects.filter(page_id=page_id).order_by('-edited')
    return render_to_response(
        "history.html", {
            'page_history': page_history, 'page_title': page_title},context_instance=RequestContext(request)
    )


def view_change(request, page_id):
    """
    Shows the change made by a user
    """
    page_history = history.objects.get(id=page_id)
    return render_to_response(
        "view_change.html", {
            'page_history': page_history}
    )


def revert(request, page_id):
    """
    reverts back to the previous content of page
    """
    loggedin_user = request.user.username
    page_history = history.objects.get(id=page_id)
    page_num = page_history.page_id
    page = Article.objects.get(id=page_num.id)
    new_entry = history(
        page_id=page, content=page_history.content, edited_by=loggedin_user
    )
    new_entry.save()
    return HttpResponseRedirect('/wiki/'+str(page.id))


def view_diff(request):
    """
    compares two versions of an article
    """
    if request.method == 'POST':
        diff = difflib.Differ()
        article1 = history.objects.get(id=request.POST['id1'])
        article2 = history.objects.get(id=request.POST['id2'])
        values = {'content': list(diff.compare(article2.content.split('\n'),article1.content.split('\n')))}
        return render_to_response('compare-wiki.html', values, context_instance=RequestContext(request))
    else:
        return HttpResponse('error')






























