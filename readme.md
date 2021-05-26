# create package

## reference
https://blog.heckel.io/2015/10/18/how-to-create-debian-package-and-debian-repository/
https://www.google.com/url?q=https://coderwall.com/p/urkybq/how-to-create-debian-package-from-source&sa=D&source=editors&ust=1620016687602000&usg=AOvVaw1FD6mls4KPf-AhL6yGMPjp

```
sudo apt install build-essential autoconf automake \
autotools-dev dh-make debhelper devscripts fakeroot \
xutils lintian pbuilder
```


```
dh_make \
  --native \
  --single \
  --packagename report_1.0.0 \
  --email nguyenhoainam@ioit.ac.vn
```

```
dpkg-buildpackage
```

# create python package
https://projects.raspberrypi.org/en/projects/packaging-your-code

## build package
```
python3 setup.py sdist
```

# SenseHat Emulator
https://sense-emu.readthedocs.io/en/v1.1/install.html