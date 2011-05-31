# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class SomeTestCase(TestCase):
    fixtures = ["test1.json", "test2.json", "test3.json", "test4.json"]
    
    def test_func(self):
        response = self.client.get(reverse("main:index"))
        self.failUnlessEqual(response.status_code, 200)
        
        response = self.client.get(reverse("main:create"))
        self.assertRedirects(response, reverse("login")+u"?next=/create/")
        
        response = self.client.get(reverse("login"), {'next': '/create/'})
        self.failUnlessEqual(response.status_code, 200)
        
