# Documentation

## Debugging

### Logs

When the api is running, the application is writing logs in the **workspace/logs** 
folder. There are logs of nginx, the gui and the api itself.

The usful logs are explained below:

#### api.run.log

In this file errors originating from the api will be displayed.

Here, infos about FastAPI, sqlalchemy or infos that are logged manually are saved.
If you want to log your own info or own erros, you can do this in **main.py**:

```python
logger.debug("debug")
logger.info("info")
logger.warn("warning")
logger.error("error")
```

**CAUTION**

If you don't find your logged messages, thats maybe because the 
displayed log level is not set to the appropiate level. You can take a 
way around this by logging at a higher level:

```
logger.info("")
```
becomes to
```
logger.error("")
```

**More about errors that occur in the api will be described in the api section.**

#### gui.run.log

This log will give you info about the vite dev server that runs the gui.
If the gui isn't running, you will see it here.

If the last message in the log looks like this...
```log
> rdp@0.0.0 dev
> vite


  VITE v4.4.9  ready in 1237 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```
... then it should mean that the dev server is running correctly. Sometimes
there will be some warnings printed below the message shown above.
But this shouldn't be any problem.

**INFO** If a message is displayed that looks likte this: _vite not found_,
probably means that the dependencies are not installed.

To fix this, navigate in the container to the gui folder and enter this command:
```bash
abc@4069ff6a4615:~/workspace$ cd gui
abc@4069ff6a4615:~/workspace/gui$ npm i
```
After this the dependecies should be installed and the server will be running again.

#### nginx_error.log

```log
2023/11/22 13:41:57 [error] 104#104: *174 connect() failed (111: Unknown error) while connecting to upstream, client: ...
```

If you see this sort of error, it propably means that the gui dev server isn't
running and thus nginx can't connect to it
