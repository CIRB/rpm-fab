

Build RPM Packages of your python project

Usage
-----

```bash
sudo pip2 install rpm_fab
rpm.py build -H root@yourbuildserver.lan
rpm.py install -H root@yourbuildserver.lan
```

`build` will run make install


self-dist with rpm
------------------

```bash
$ env/bin/rpm_fab
$ ls dist
```


dist egg with rpm
------------------

```bash
$ cd /path/to/your/project-folder
$ /path/to/rpm_fab/env/bin/rpm_fab
$ ls dist
```
