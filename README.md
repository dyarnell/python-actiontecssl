====================
Python Actiontec SSL
====================

Code inspired by http://github.com/larsks/python-actiontec but wanted to
not have to think plaintext passwords and finding a external SSL Telnet
client.

Requirements
============

- You need to enable the secure telnet administration interface on your
  router.

  - Log in to your router.

  - Select "Advanced".

  - "Yes", you want to proceed.

  - Select "Local Administration", located in the menu under the
    toolbox icon.

  - Under "Allow local telnet access", enable "Using Secure Telnet over
    SSL Port (992)".

  - Click "Apply".

Testing
=======

You can run the following to test things out.

```
python test.py 192.168.1.1 992 mypassword
```
