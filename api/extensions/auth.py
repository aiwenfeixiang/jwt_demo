# -*- coding: utf-8 -*-
# @Time    : 2019/11/14 22:04
# @Author  : AnWen
from rest_framework.authentication import BaseAuthentication
class JwtQueryParamsAuthentication(BaseAuthentication):
	def authenticate(self,request):pass