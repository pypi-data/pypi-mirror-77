# Fermata CLI

Fermata 开发工具, 线上环境不要安装.

## Install

```bash
git clone ..
cd fermata-cli
pip install .
```

## Features

- [x] debug: 启动调试模式的 fermata app
    - [x] debugger
    - [x] reload: 自动重启
    - [ ] logger: 控制台 logger
    - [ ] ui: swagger ui
    - [ ] editor: swagger editor
- [ ] validate: 验证 OpenAPI Specification
- [x] generate: 代码生成
    - [x] operate: 按自动路由生成函数
    - [ ] model: 生成某种 ORM 的 Model 定义


## Usages

### Init

初始化项目, 例如:

```bash
$ fermata init
> app created.
$ cat <<EOF >> specs/a.yml
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
$ fermata complete
$ fermata debug
```

### Complete

1. 自动补全函数签名
2. 自动创建包和模块
3. 自动将包改为模块或相反

```bash
$ fermata complete
```

### Debug

`fermata debug <app> --host --port`

- <app>: fermata application instance 所在位置, 如: `some_module.app`; 如果没有 `.` 则默认实例名为 `app`; 如果传入文件名, 则自动忽略 `.py` 后缀; 如果为空则默认为 `app.app`.
- --host: 监听主机, 默认值 `127.0.0.0`
- --port: 监听端口, 默认值 `8000`

以下两者等价:
```bash
$ fermata debug
$ fermata debug app.app
```

以下三者等价:
```bash
$ fermata debug pet.app
$ fermata debug pet
$ fermata debug pet.py
```
