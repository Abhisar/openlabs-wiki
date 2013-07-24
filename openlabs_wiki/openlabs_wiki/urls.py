from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url('wiki/create/$', 'wiki.views.create_page'),
    url('wiki/save/$', 'wiki.views.save'),
    url(r'^wiki/(?P<page_id>[^/]+)/$', 'wiki.views.view_page'),
    url(r'^wiki/(?P<page_id>[^/]+)/edit/$', 'wiki.views.edit_page'),
    url(r'^wiki/(?P<page_id>[^/]+)/save_edit/$', 'wiki.views.save_edit'),
    url('accounts/login/$', 'openlabs_wiki.views.login'),
    url('accounts/logout/$', 'openlabs_wiki.views.logout'),
    url('accounts/auth/$', 'openlabs_wiki.views.auth_view'),
    url('accounts/loggedin/$', 'openlabs_wiki.views.loggedin'),
    url('accounts/invalid/$', 'openlabs_wiki.views.invalid_login'),
    url('accounts/register/$', 'openlabs_wiki.views.register_user'),
    url('accounts/register_success/$', 'openlabs_wiki.views.register_success'),
    # Examples:
    # url(r'^$', 'openlabs_wiki.views.home', name='home'),
    # url(r'^openlabs_wiki/', include('openlabs_wiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
