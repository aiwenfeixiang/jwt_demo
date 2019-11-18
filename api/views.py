from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
import uuid


class Login(APIView):
	def post(self, request, *args, **kwargs):
		user = request.data.get("username")
		pwd = request.data.get("password")
		user_object = models.UserInfo.objects.filter(username=user, password=pwd).first()

		if not user_object:
			return Response({"code": 1000, "error": "用户名密码错误"})
		random_string = str(uuid.uuid4())
		user_object.token = random_string
		user_object.save()
		return Response({"code": 1001, "data": "登录成功", "token": random_string})


class OrderView(APIView):
	def get(self, request, *args, **kwargs):
		token = request.query_params.get('token')
		if not token:
			return Response({"code": 2000, "error": '登录后才能访问'})
		user_object = models.UserInfo.objects.filter(token=token).first()
		if not user_object:
			return Response({"code": 2001, "error": 'token无效'})
		return Response("订单列表")


class JwtLogin(APIView):
	def post(self, request):
		user = request.data.get("username")
		pwd = request.data.get("password")
		user_object = models.UserInfo.objects.filter(username=user, password=pwd).first()
		if not user_object:
			return Response({"code": 3000, "error": "用户名密码错误"})

		import jwt
		import datetime
		salt = "!@#$%^&*(#QWE"
		headers = {
			"typ": 'jwt',
			"alq": "HS256"
		}
		payload = {
			'user_id': user_object.id,
			'username': user_object.username,
			'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
		}
		token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)
		return Response({'code': 3001, "data": token})


class JwtOrderView(APIView):
	def get(self, request):
		token = request.query_params.get('token')

		import jwt
		from jwt import exceptions

		salt = "!@#$%^&*(#QWE"
		payload = None
		msg = None
		try:
			payload = jwt.decode(token, salt, True)
		except exceptions.ExpiredSignatureError:
			msg = 'token已失效'
		except jwt.DecodeError:
			msg = 'token认证失败'
		except jwt.InvalidTokenError:
			msg = '非法的token'
		if not payload:
			return Response({'code': 1003, 'error': msg})

		print(payload['user_id'], payload['username'])
		return Response('订单列表')


from api.utils.jwt_auth import create_token
class ProLoginView(APIView):
	authentication_classes = []

	def post(self, request, *args, **kwargs):
		user = request.data.get('username')
		pwd = request.data.get('password')
		user_object = models.UserInfo.objects.filter(username=user, password=pwd).first()
		if not user_object:
			return Response({'code': 1000, 'error': '用户名或密码错误'})
		token = create_token({'id': user_object.id, 'name': user_object.username})
		return Response({'code': 1001, 'data': token})


class ProOrderView(APIView):
	def get(self, request, *args, **kwargs):
		print(request.user)
		return Response('订单列表')
