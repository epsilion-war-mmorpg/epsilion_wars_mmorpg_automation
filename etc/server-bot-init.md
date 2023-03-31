Server setup
---
```shell

adduser epsa-twink2
usermod -a -G supervisor epsa-twink2
vi /etc/supervisor/conf.d/epsa-twink2.conf
service supervisor restart
# run deploy here

```