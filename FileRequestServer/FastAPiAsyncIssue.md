
Fastapi项目，在接口中调用同步方法，如果该同步方法，耗时较长(比如连接redis超时)，会造成整个项目接口的阻塞，这是任何接口的访问都会被阻塞超时

[FastApi框架异步调用同步问题 - 輪滑少年 - 博客园](https://www.cnblogs.com/ltyc/p/18664047)

一、为什么会阻塞

FastAPI 是基于异步框架（如 `asyncio` 或 `anyio`）构建的，它的核心是一个事件循环（Event Loop）。事件循环负责调度和执行所有的异步任务。当你在异步函数中直接调用同步阻塞代码时，事件循环会被阻塞，无法继续处理其他任务，直到同步代码执行完毕。

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

```
from fastapi import FastAPI
import time

app = FastAPI()

def sync_function():
    time.sleep(5)  # 模拟一个耗时的同步操作
    return "Done"

@app.get("/")
async def root():
    result = sync_function()  # 直接调用同步函数
    return {"result": result}
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

在这个例子中 `time.sleep(5)` 是一个同步阻塞操作，它会阻塞事件循环 5 秒钟。在这期间，FastAPI 无法处理其他请求，整个应用的并发性能会大幅下降。

二、如何避免阻塞

将同步代码放到线程池或进程池中执行，将同步代码改为异步实现。有以下几种常用解决方案

#### 1. 使用 `run_in_threadpool` 或 `asyncio.to_thread`

将同步代码放到线程池中执行，避免阻塞事件循环。

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

```
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
import time

app = FastAPI()

def sync_function():
    time.sleep(5)  # 模拟一个耗时的同步操作
    return "Done"

@app.get("/")
async def root():
    result = await run_in_threadpool(sync_function)  # 在线程池中运行
    return {"result": result}
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

#### 2 使用 `run_in_processpool`

对于 CPU 密集型的同步代码，可以使用进程池来避免阻塞事件循环。

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

```
from fastapi import FastAPI
from fastapi.concurrency import run_in_processpool
import time

app = FastAPI()

def cpu_intensive_function():
    # 模拟一个 CPU 密集型的操作
    result = sum(i * i for i in range(10**6))
    return result

@app.get("/")
async def root():
    result = await run_in_processpool(cpu_intensive_function)  # 在进程池中运行
    return {"result": result}
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

#### 3. 将同步代码改为异步实现

如果可能，尽量将同步代码改为异步实现。例如，使用 `asyncio.sleep` 代替 `time.sleep`，或者使用异步库代替同步库。

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

```
from fastapi import FastAPI
import asyncio

app = FastAPI()

async def async_function():
    await asyncio.sleep(5)  # 异步等待
    return "Done"

@app.get("/")
async def root():
    result = await async_function()  # 直接调用异步函数
    return {"result": result}
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

#### 4. 使用 `anyio.to_thread.run_sync`

如果你使用的是 `anyio` 库，可以使用 `anyio.to_thread.run_sync` 来运行同步代码。

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

```
from fastapi import FastAPI
import anyio
import time

app = FastAPI()

def sync_function():
    time.sleep(5)  # 模拟一个耗时的同步操作
    return "Done"

@app.get("/")
async def root():
    result = await anyio.to_thread.run_sync(sync_function)  # 在线程池中运行
    return {"result": result}
```

[![复制代码](https://assets.cnblogs.com/images/copycode.gif)](javascript:void(0); "复制代码")

### 总结

* **直接调用同步代码会阻塞事件循环** ，导致整个应用的性能下降。
* **解决方案** ：
* 对于 I/O 密集型任务，使用 `run_in_threadpool` 或 `asyncio.to_thread`。
* 对于 CPU 密集型任务，使用 `run_in_processpool`。
* 尽量将同步代码改为异步实现。
* **最佳实践** ：在 FastAPI 中，尽量避免直接调用同步阻塞代码，始终使用异步或线程池/进程池来处理同步任务。
