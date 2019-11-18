# jwt_demo
#### Jwt:一般用于用户认证

​	传统的token认证是用户进行登陆，服务端返回token给浏览器，并将token保存在服务端

​	jwt 是用户登陆，服务端给用户返回一个token，但是服务端不保存，以后用户再来访问的时候需要携带着token，服务端再做校验，jwt优势在于无需在服务端保存token

jwt实现过程：用户提交用户名和密码给服务端，如果登陆成功，使用jwt创建一个token返回给用户，jwt生成的token由三部分组成并且用点连接

第一部分：header 包括加密算法 和token类型,转换成json后进行base64url加密

```
{
	"alg":"hs256",
	"typ":"JWT"
}
```

第二部分：payload 包括自定义值 比如说id  name,转化成json字符串，再base64url加密

```
{
"id":"123",
"name":"anwen",
"exp":超时时间
}
```

第三部分：将第一和第二部分的加密字符串拼接起来，再进行hs256加密+加盐，对加密后的hs256串，在进行base64url加密

以后用户再来访问的时候，需要携带token，后端对token进行校验，

​	校验过程：

​	第一步：对token进行切割 

​	第二步：对第二段base64url 解密，并获取payload信息，检测token是否已经超时

​	第三步：把第1，2段拼接再次执行hs256加密+加盐，如果第1,2段密文 = 第3段通过base64解密的值，表示token未被修改过则认证通过

jwt.encode 生成token

jwt.decode 解密token
