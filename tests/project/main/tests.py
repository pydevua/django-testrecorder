# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

class TestClass(TestCase):
    def setUp(self):
        self.auth = {
            "username": u"admin",
            "password": u"admin"
        }
    
    def test_func(self):
        self.client.login(**self.auth)
        
        response = self.client.get(reverse("main:create"))
        self.failUnlessEqual(response.status_code, 200)
        
        response = self.client.get(reverse("main:create"))
        self.failUnlessEqual(response.status_code, 200)
        
        data = {
            "content": u"",
            "name": u"",
            "image": u""
        }
        response = self.client.post(reverse("main:create"), data)
        self.failUnlessEqual(response.status_code, 200)
        self.failIf(response.context["form"].is_valid())
        
        data = {
            "content": u"dfgdfg",
            "name": u"dfgdfg",
            "image": u""
        }
        response = self.client.post(reverse("main:create"), data)
        self.failUnlessEqual(response.status_code, 200)
        self.failUnless(response.context["form"].is_valid())