## NZBget file opener

This scripts sends .nzb files to the specified host. You can specify many options, like deleting the files after upload.
Also, it ensures that NZBGet is running before sending the files, launching it if necessary (Auto-detected on macOS. Windows users have to manually specify app path).

### Install

```shell script
pip install nzbget-file-opener
```

### Usage

```
nzbget-file-opener [-h]
                   [-n HOSTNAME] [-u USERNAME] [-p PASSWORD]
                   [-l CONFIG] [-d DOMAIN]
                   [-c CATEGORY] [-P PRIORITY]
                   [--add-top] [--add-paused]
                   [-D]
                   [--app-path NZBGET_PATH]
                   files [files ...]


positional arguments:

  files                 the files to send


optional arguments:

  -h, --help            show this help message and exit

  -n HOSTNAME, --hostname HOSTNAME
                        the nzbget hostname to reach
  -u USERNAME, --username USERNAME
                        your nzbget username
  -p PASSWORD, --password PASSWORD
                        your nzbget password

  -l CONFIG, --load-config CONFIG
                        your nzbget config
  -d DOMAIN, --domain DOMAIN
                        the domain target defined in your nzbget config

  -c CATEGORY, --category CATEGORY
                        the category to use for the nzb files download
  -P PRIORITY, --priority PRIORITY
                        the category to use for the nzb files download

  --add-top             add the files to the top of queue
  --add-paused          add the files in pause state

  --app-path NZBGET_PATH
                        specify the nzbget app path to launch it if not
                        already running

  -D, --delete-files    to delete the files sent to NZBget
```


### Scripts

Available `pipenv run` scripts :

- `install` - installs the package in pipenv
- `app` - runs the application
- `test` - runs the tests with [pytest](https://docs.pytest.org/en/latest/)
- `build` - build the app artifacts
- `clean` - clean the artifacts created with the `build` script
- `deploy-test` - deploy to [test.pypi](https://test.pypi.org)
- `deploy` - deploy to [pypi](https://pypi.org)



> In order to properly run the deploy scripts, you should :
> - have **[twine](https://pypi.org/project/twine/)** installed.
> - have a `~/.pypirc` file filled according to the template below

### Configurations templates

`~/.nzbgetrc` configuration (recommended) :
```toml
[localhost]
username = local-username
password = local-password

[remote.domain.tld]
port = 6790
username = remote-username
password = remote-password

```  
> you can use defaut by not mentioning the field  

---

`.env` configuration :
```toml
NZBGET_URL='[http|https]://hostname:port'
NZBGET_USERNAME='username'
NZBGET_PASSWORD='password'
```
  
> url scheme and port are optional

> you can also set these variables in your environment

---

`.pypirc`    
```toml
[distutils]
index-servers=
    pypi
    testpypi

[pypi]
username: your_username
password: your_password

[testpypi]
repository: https://test.pypi.org/legacy/
username: your_username
password: your_password
```

Note: `pypi.org` and `test.pypi.org` uses two distinct databases for user accounts. You need to create an account for both domains
