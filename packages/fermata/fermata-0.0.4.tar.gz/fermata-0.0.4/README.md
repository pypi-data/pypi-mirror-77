# Fermata

一个 OpenAPI 3.0 的 Server 端实现, 作为 [swagger-py-codegen](https://github.com/guokr/swagger-py-codegen) 的代替方案, 类似的项目如: [Connexion](https://github.com/zalando/connexion).

Fermata 认同 [API First](https://opensource.zalando.com/restful-api-guidelines/#api-first) 原则, 尽量实现 OpenAPI 所定义的功能, 而不是反过来通过代码文档生成一份兼容的 OpenAPI 文档.

Fermata 为延音符号 [𝄐](https://zh.wikipedia.org/wiki/%E5%BB%B6%E9%9F%B3), 表示「[华彩乐段](https://zh.wikipedia.org/wiki/%E8%A3%9D%E9%A3%BE%E6%A8%82%E6%AE%B5)」的开始, 在这里表示开发者无需关注 OpenAPI Specification 中定义路由/校验/安全等像乐谱一样固定的部分, 而只需要对华彩乐段进行编程.

Fermata 将仅作为 RESTful API Server 而存在, 不支持常见的 web framework 功能, 如: 正则路由, 静态文件, 文件上传, 流式输出, 模版, Session, Cookies, redirect.. 等等.

## 安装

开发环境安装 fermata 命令行接口即可:

```bash
pip install fermata-cli
```

## 快速上手

### 第一个例子

创建项目文件夹并进入, 例如 petstore:

```bash
$ mkdir petstore
$ cd petstore
```

初始化项目:

```bash
$ fermata init
```

这会创建如下文件:

- app.py: 入口程序
- http.sh: 生产环境所用的启动命令行
- specs/api.yml: 接口描述文件

默认的 api.yml 内容为空, 需要自定义, 例如:

```bash
$ cat <<EOF >> specs/api.yml
paths:
  /users:
    get:
      parameters:
      - name: page
        in: query
        schema:
          default: 1
      - name: status
        in: query
        required: true
EOF
```

编辑 api.yml 后, 可以使用自动补全代码命令自动完成函数声明:

```bash
$ fermata complete
```

这会创建一个 python package, 默认为文件夹名, 即 `petstore`, 如需修改可以在 `app.py` 中指定: `Fermata(default_pakcage)`. 

以调试模式启动:

```bash
$ fermata debug
> * Fermata on: http://127.0.0.1:8000
```

访问测试:

```bash
$ curl -D - "http://127.0.0.1:8000/api/a"
HTTP/1.1 200 OK
Server: meinheld/1.0.2
Date: Wed, 19 Aug 2020 05:49:15 GMT
content-type: application/json;charset=utf-8
Transfer-Encoding: chunked
Connection: close

null
```

需要注意的是, 访问路径不是 `/a`, 而是 `/api/a`, 这是为了支持多个 spec 文件, 每个 spec 文件的文件名(不含后缀)会作为该 spec 的 base_path. 如果不需要这个功能可以修改 `app.py`:

```python
- app = Fermata('petstore', 'specs/*.yml')
+ app = Fermata('petstore').scan('specs/*.yml')
```


### 自动路由

Fermata 支持自动路由, 并且可以自动完成自动路由对应的函数定义, 在非必要的情况下不要手动指定路由. 开发人员需要了解一下自动路由规则, 这样就可以快速找到 path 对应的函数.

自动路由的规则很简单, 首先, 找到函数所在模块:

path 的所有非变量组成模块路径, 如 '/a/{b}/c', 其中 b 为变量, 忽略后得到模块路径为 `a.c` 即为函数所在模块. 当然, 对于 python 来说, 这可能表示 `a/c.py` 也可能表示 `a/c/__init__.py`, 这取决于 `c` 模块是否还有子模块.

然后找到函数, 分两种情况:

1. 如果 path 中没有变量, 那么函数名就是 http_method, 如 `get /a` 对应的函数就在 `a.py` 中, 函数名为 `def get(request):`
2. 如果 path 中有变量, 函数名则可以简单认为是 `{http_method}_by_{path_var}`, 如 `get /a/{b}` 对应的函数在 `a.py` 中, 函数名为 `def get_by__b(request):`

如果有多个 path 变量, 则每个变量名都会出现在函数名中, 掌握上述规则就可以快速找到自动路由对应的函数了.




### 内置 JWT 校验

fermata 内置了标准 JWT 的最小实现, 仅支持 `HS256` 签名, 可以自动校验 OpenAPI 中定义的 scopes, 名字约定为 `fermata.jwt`, 例如:

```yaml
paths:
  /pet:
    get:
      security:
        fermata.jwt:
          - read
          - write
```

access token 和 refresh token 的签发逻辑需要自行实现, 例子见 `examples/petstore`, 获取 token 的函数为 `petstore.user.login.get`, 刷新 token 为 `petstore.user.refresh.get`.


### 如何使用数据库

以 PonyORM 为例, 修改 `app.py`:

```python
+ from pony import orm
+ 
+ app.wsgi = orm.db_session(app.wsgi)
```


### 自定义认证和授权

可以通过自定义 `scopes_fetcher()` 来实现认证和授权, 函数签名如下:

```python
def scopes_fetcher(request, security, required_scopes):
    return True, []

app = Fermata(scopes_fetcher=scopes_fetcher)
```

参数:

- request: `fermata.request.Request`
- security: `string`, 为 OpenAPI 定义的 `Security Requirement Object` 的 `name`, 如果定义了多种校验方式, security 可以用于区分当前请求的校验方式
- required_scopes: `set[string]`, 需要的权限

返回值:

- 是否通过认证
- 获得哪些 scopes: `list[string]` or `set[string]`


## 主要机制说明

### Fermata 对象

Fermata 的构造参数

- default_package: 加载 operaionId 时的默认包, 在 operaionId 为相对路径时有效, 也会作为 app.name 的值
- spec_glob: 加载 spec 文件的路径, 支持 glob 语法, 如 `specs/*.yml`
- exception_captors: 用于自定义异常处理
- scopes_fetcher: 用于实现自定义鉴权, 详见“认证和授权”
- jwt_key: 使用内置 JWT 校验

使用 WSGI 中间件或 decorator

基本形式:

```python
app = Fermata()
app.wsgi = WSGIMiddleware(app.wsgi)
```

例如, 修正 X-Forwarded-For:
```
from werkzeug.middleware.proxy_fix import ProxyFix

app = Fermata()
app.wsgi = ProxyFix(app.wsgi, x_for=1, x_host=1)
```

例如, 使用 ponyorm:
```
from pony import orm

app = Fermata()
app.wsgi = orm.db_session(app.wsgi)
```


### 路由

路由支持手动指定和自动路由.

#### operationId 的格式

可以通过 OpenAPI 中规定的 `operationId` 来指定 path 到 function 的路由规则, 不指定时采用自动路由规则.

`operationId` 的格式为 `path.to.function`, 通过 `.` 分隔, 最后一项表示函数名, 前面表示 package 或 module, 暂不支持 `class.method` 的形式.

当 `operationId` 的第一个字符为 `.` 时, 表示相对于 `default_package` 的路径, `default_package` 是 `fermata.application.Fermata` 构造方法的参数.

#### 自动路由

自动路由的基本规则为:

```
.{path_segment}...{path_segment}.{method}
```

- path_segment: 通过 `/` 分割 path 得到的每一项
- method: HTTP METHOD, 即 OpenAPI 中的 operation 的名字

对于有 path params 的规则为:
```
.{path_segment}...{path_segment}.{method}_by{path_signature}
```

path_signature的值计算:
```python
import re

def path_signature(path):
    sign = re.sub(r'/\w', '/', path)  # 删除所有 path_segment
    sign = re.sub(r'[{}]', '', sign)  # 删除所有 `{}`
    sign = re.sub(r'/', '_', sign)    # `/` 替换为 `_`
    return sign
```

自动路由的例子(用 operationId 字段来表示自动路由后的值):

```yaml
paths:
  /a/b/c:
    get:
      operationId: .a.b.c.get
    delete:
      operationId: .a.b.c.delete
  /{a}/b/{c}:
    get:
      operationId: .b.get_by_a__c
  /a/{b}/c/{d}:
    get:
      operationId: .a.c.get_by__b__d
```

### 定义 operate

或者叫 request handler 或者 view function, 即要实现的业务函数, 基本的函数签名为:

```python
def operate(request, param1, param2):
    return resposne
```

其中 request 为 fermata.request.Request 类型, 提供 request.headers 等便捷方法, 但通常用不到.

其他参数为 OpenAPI 中所定义的参数, 非 required 的参数且没有定义 default 值, 那就需要在函数签名中指定默认值, 如:

```python
def operate(request, param1, param2=None):
    return resposne
```

response 如果不是 fermata.response.Response 类型, 那就会被被包装为 fermata.response.JSONResponse 类型, 通常情况下像普通函数一样返回基本类型即可:

```python
def operate(request, param1, param2=None):
    return {'a': 'A', 'b': 'B'}
```

当需要指定 header 或 status code 时, 可以返回 JSONResponse 对象:

```python
def operate(request, param1, param2=None):
    return JSONResponse({'a': 'A', 'b': 'B'}, 201, [
        ('x-total-page', '100'),
    ])
```

如果需要其他格式, 可以返回 Response 对象, 或者继承 Response 自行扩展:

```python
def operate(request, param1, param2=None):
    xml = '<xml></xml>'
    return Response(xml, 200, [
        ('x-total-page', '100'),
    ], 'application/xml')
```


### OpenAPI 中的默认值

可以通过 default 字段指定默认值, 但有三点需要注意:

1. 当 required 为 `True` 时, default 会被忽略, 因为这时 default 没有意义
2. 为 object 的字段指定 default 时, 需要先为 object 设置 default 为 `{}`, 否则 object 为 `None`, 不存在 attribute, 也就无法指定默认值
3. 暂不支持为 array 的 items.schema 的子 property 指定默认值

参考: 

- [Why doesn’t my schema’s default property set the default on my instance?](https://python-jsonschema.readthedocs.io/en/stable/faq/)
- [Common Mistakes](https://swagger.io/docs/specification/describing-parameters/)


### 自动反序列化

#### requestBody 的反序列化

fermata 默认 request.content_type 为 `application/json`, 所以在不指定 `Content-Type` 的情况下会自动按 json 格式反序列化.

除 json 外, fermata 还支持 `application/x-www-form-urlencoded` 格式, 其他格式暂不支持.

反序列化后的变量名固定为 body, 暂不支持自定义.

#### parameters 的反序列化

通过 content 属性可以指定 body 以外的参数自动反序列化, 同样支持 json / form 两种基本格式, 例如:

```yaml
paths:
  /location:
    post:
      parameters:
      - name: coordinates
        in: query
        content:
          application/json:
            schema:
              type: object
              required:
              - lat
              - long
              properties:
                lat:
                  type: number
                long:
                  type: number
```

发送请求 `/location?coordinates={%22lat%22:%20123,%20%22long%22:%20456}`, 得到的 coordinates 的值为 `{'lat': 123, 'long': 456}`.

### format

在校验实现上使用的是 [jsonschema](https://github.com/Julian/jsonschema), 采用的协议是 JSON Schema Draft 7, 比 OpenAPI 所定义的格式更为丰富, 支持更多的 [format](https://json-schema.org/understanding-json-schema/reference/string.html#format), 例如:

- date-time: `2018-11-13T20:20:39+00:00`
- date: `2018-11-13`
- time: `20:20:39+00:00`
- email
- hostname
- ipv4
- ipv6
- uri
- regex: 利用 regex 可以满足各种字符串校验的需求


## 部署

注意事项:

1. 不要安装 `fermata-cli`, 而仅需安装 `fermata` 包, 两个包分开的目的是为了避免开发配置干扰生产环境
2. 非 lambda 环境使用 `http.sh` 启动 http server


## 功能线路图

- [x] routing: OpenAPI 3.0 paths routing
- [x] resolver: `package.module.class.function` style operation id resolve
- [x] exception: 异常
- [x] application.exception_handle: 异常处理
- [x] specification: OpenAPI 3.0 Spec request validate
- [x] request
- [x] response
- [ ] config
- [x] OAuth: JWT, scope
- [x] event handlers: before_request..
- [ ] logger
- [x] APM
- [ ] sentry
- [ ] mock server

不会支持:

1. 不需要 response validator, 而是将其用于 api tests
2. 不支持 stream response / request, 没有这个必要, 需要这个场景的应该考虑 websocket
3. 暂不支持通配符 path, 因为 OpenAPI 就不支持, 也许在某些情况下是有必要的(比如外部回调要求了 path), 遇到的时候再考虑
4. 不支持 xml 等 response 格式, 仅支持 json, 因为通常用不到
5. 不支持全局 request 对象. 全局 request 并不容易理解, 用函数调用栈来解释 request 的处理不是很自然吗? 不实现全局 request 自然也就不用考虑 request 的线程问题, 例如不必加锁实现 cached_property.
6. 不支持常见的 web framework 的功能

## 思考和探讨

- 要不要优先选择实现 ASGI 而非 WSGI? #1
- 校验功能选择哪个库来实现? #2
- 同步还是异步? #3
- 错误处理 #4

