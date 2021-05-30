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

# generate ssh keys

```
ssh-keygen -t rsa
```


```
Enter file in which to save the key (/home/namnguyen/.ssh/id_rsa): /home/namnguyen/django/cs20.10_v2/packages/pi_temp/configuration/ssh_keys/device1
```

# set remote origin

```
git remote set-url origin ubuntu@git.namnguyenhoai.com-device1:/home/ubuntu/git-update-versions.git
```

# set SSH config

```
Host git.namnguyenhoai.com-device1
  HostName git.namnguyenhoai.com
  ForwardAgent yes
  AddKeysToAgent yes
  User device1
  IdentityFile ~/django/cs20.10_v2/packages/pi_temp/configuration/ssh_keys/device1
```

# install local package
https://stackoverflow.com/questions/15031694/installing-python-packages-from-local-file-system-folder-to-virtualenv-with-pip

# execution time
https://stackoverflow.com/questions/45492786/find-execution-time-for-subprocess-popen-python