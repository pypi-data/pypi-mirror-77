# Fermata

一个 OpenAPI 3.0 的 Server 端实现, 作为 [swagger-py-codegen](https://github.com/guokr/swagger-py-codegen) 的代替方案, 类似的项目如: [Connexion](https://github.com/zalando/connexion).

Fermata 认同 [API First](https://opensource.zalando.com/restful-api-guidelines/#api-first) 原则, 尽量实现 OpenAPI 所定义的功能, 而不是反过来通过代码文档生成一份兼容的 OpenAPI 文档.

Fermata 为延音符号 [𝄐](https://zh.wikipedia.org/wiki/%E5%BB%B6%E9%9F%B3), 表示「[华彩乐段](https://zh.wikipedia.org/wiki/%E8%A3%9D%E9%A3%BE%E6%A8%82%E6%AE%B5)」的开始, 在这里表示开发者无需关注 OpenAPI Specification 中定义路由/校验/安全等像乐谱一样固定的部分, 而只需要对华彩乐段进行编程.

Fermata 将仅作为 RESTful API Server 而存在, 不支持常见的 web framework 功能, 如: 正则路由, 静态文件, 文件上传, 流式输出, 模版, Session, Cookies, redirect.. 等等.


## 上手

安装:

```bash
# git clone <fermata>
cd fermata
pip install .
```

运行例子:

```bash
cd examples/petstore
python app.py
```

## 功能

- [x] routing: OpenAPI 3.0 paths routing
- [x] resolver: `package.module.class.function` style operation id resolve
- [x] exception: 异常
- [x] application.exception_handle: 异常处理
- [x] specification: OpenAPI 3.0 Spec request validate
- [x] request
- [x] response
- [ ] config
- [x] OAuth: JWT, scope
- [ ] event handlers: before_request..
- [ ] logger
- [ ] APM
- [ ] sentry
- [ ] mock server

## 不支持

1. 不需要 response validator, 而是将其用于 api tests
2. 不支持 stream response / request, 没有这个必要, 需要这个场景的应该考虑 websocket
3. 暂不支持通配符 path, 因为 OpenAPI 就不支持, 也许在某些情况下是有必要的(比如外部回调要求了 path), 遇到的时候再考虑
4. 不支持 xml 等 response 格式, 仅支持 json, 因为通常用不到
5. 不支持 thread local request. 全局 request 并不容易理解, 用函数调用栈来解释 request 的处理不是很自然吗? 不实现全局 request 自然也就不用考虑 request 的线程问题, 例如不必加锁实现 cached_property.
6. 不支持常见的 web framework 的功能


## 使用

### Fermata

Fermata 的构造参数

- spec: 加载后的 OpenAPI 的字典, 这个参数将会废弃, 将通过 `app.load_from(file)` 来加载多个 yaml 文件, 或者 `app.load_all(path)` 加载全部文件.
- lazy_load: 懒加载 operaionId 对应的模块, 打开后可以提高线上应用启动速度, 开发时可以关闭, 便于发现加载错误.
- default_package: 加载 operaionId 时的默认包, 在 operaionId 为相对路径时有效
- scopes_fetcher: 见“认证和授权”
- exception_captors: 用于自定义异常处理

WSGI 中间件或 decorator

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

示例代码见 `examples/petstore` 和 `tests/openapi/test_operater.py`.


### 认证和授权

可以通过自定义 `scopes_fetcher()` 来实现认证和授权, 函数签名如下:

```python
def scopes_fetcher(request, security):
    return True, []

app = Fermata(scopes_fetcher=scopes_fetcher)
```

参数:

- request: fermata.request.Request
- security: string, 为 OpenAPI 定义的 `Security Requirement Object` 的 `name`, 如果定义了多种校验方式, security 可以用于区分当前请求的校验方式

返回值:

- 是否通过认证
- 获得哪些 scopes

### 内置 JWT

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


### 默认值

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

## 思考和探讨

- 要不要优先选择实现 ASGI 而非 WSGI? #1
- 校验功能选择哪个库来实现? #2
- 同步还是异步? #3
- 错误处理 #4
