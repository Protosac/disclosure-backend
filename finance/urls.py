from django.contrib import admin
from django.conf.urls import patterns, url

from . import views


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'committee/(?P<committee_id>[0-9]+)$',
        views.CommitteeViewSet.as_view(actions={'get': 'retrieve'}),
        name='committee_get'),

    url(r'committee/(?P<committee_id>[0-9]+)/contributions/summary',
        views.BeneficiaryViewSet.as_view(actions={'get': 'summary'}),
        name='contributors_summary'),

    url(r'committee/(?P<committee_id>[0-9]+)/contributors',
        views.BeneficiaryViewSet.as_view(actions={'get': 'contributors'}),
        name='contributors_list'),

    url(r'committee/(?P<committee_id>[0-9]+)/contributions_received$',
        views.BeneficiaryViewSet.as_view(actions={'get': 'contributions_received'}),
        name='contributions_received_list'),

    url(r'committee/(?P<committee_id>[0-9]+)/contributions$',
        views.BenefactorViewSet.as_view(actions={'get': 'contributions'}),
        name='contributions_list'))
