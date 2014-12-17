

Build RPM Packages of your python project

Usage
-----

```bash
sudo pip2 install rpm_fab
rpm.py build -H root@your-build-server.lan
rpm.py install -H root@your-run-server.lan
```

It assume that:
- The current project has a `make install` target configured, it must be evironment free.
- The current project has a `make migrate` target configured, it will be run on running server in post-install.
- Path should only be prensent into `bin` and `lib` directories, using virtualenv, it should be runned with `virtualenv .`


add this in your `Makefile`:

```
rpm:
    bin/pip install git+git://github.com/CIRB/rpm-fab.git --upgrade
    bin/rpm.py build
```



