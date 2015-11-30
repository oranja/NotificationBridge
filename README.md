# NotifyBridge
## Introduction
I have been looking for a way to let Jenkins deliver pop-up notifications to my KDE desktop sessions. The *Hudson Tray Application* doesn't seem to be truly KDE-compatible. Previous attempts with alternative approaches failed, stemming mostly from the fact the Jenkins runs under a special *jenkins* user on the system. *export*-ing DBUS_SESSION_BUS_ADDRESS and DISPLAY allowed neither Groovy nor shell scripts running under *jenkins* to reach my desktop DBus session.

Eventually, the solution I chose is a simple Python script combined with Jenkins' Notification Plugin.  
It is provided here for your own convenience and as a request for further improvement.

## Usage
For one-time usage, configure Jenkins as described in steps 6-7 below and run the script:
```sh
$ python3 NotifyBridge.py
```
Exit the script by pressing `Ctrl+C` in the console it's running at.

## Installation
Installation can be mostly automated, but for now, you'll have to do things yourself and perhaps fiddle with things a bit until everything runs together.

#### Tested and built for
- [Fedora] Workstation 22 [4.1.6-200.fc22.x86_64]
- [KDE] Plasma 5.3.2
- [Jenkins] v1.628

### Requirements
* **[Jenkins]**
    * **[Notification Plugin]**
* **[Python 3+]**
    * **[Flask]** &nbsp;&nbsp;*(for a quick RESTful web application)*
    * **[Flask-JSON]** &nbsp;&nbsp;*(for easy JSON-based request/response format)*
    * **[python3-gobject]** &nbsp;&nbsp;*(for libnotify integration)*
* **[libnotify]** &nbsp;&nbsp;*(for sending notificiations to KDE)*

### Steps
1. Install dependencies:
  ```sh
  $ sudo dnf install python3-flask python3-gobject
  $ sudo pip3 install Flask-JSON
  ```

2. Copy the `NotifyBridge.py` script to `/usr/local/bin/` or similiar (you'll need root permissions).  
Make sure it has proper access rights.
  ```sh
  chmod a+x /usr/local/bin/NotifyBridge.py
  ```
   
3. Copy the `NotifyBridge@.service` systemd unit file to `/usr/lib/systemd/user/` (you'll need root permissions).

4. Add the following content to the end of your `~/.profile` file.
  ```sh
  systemctl --user import-environment DBUS_SESSION_BUS_ADDRESS
  systemctl --user import-environment DISPLAY
  systemctl --user start NotifyBridge@${USER}.service
  ```
**_Note:_** Also run these 3 commands now to *start the service* now (without restarting the session).

5. From the Jenkins dashboard, install the *Notification Plugin*. Restart Jenkins as required.

6. For each Jenkins job you want to get notifications for, *Configure* the job, such that under **Job Notifications** you will have two endpoints:

  Field | Value
  --- | ---
  Format | JSON
  Protocl | HTTP
  Event | Job Started
  URL | http://_localhost_:29876/notify/jenkins/build/start

  Field | Value
  --- | ---
  Format | JSON
  Protocl | HTTP
  Event | Job Finalized
  URL | http://_localhost_:29876/notify/jenkins/build/result


## Uninstallation
1. Stop the service:
  ```sh
  $ systemctl --user stop NotifyBridge@${USER}.service
  ```

2. Remove the script and unit file:
  ```sh
  $ sudo rm /usr/local/bin/NotifyBridge.py
  $ sudo rm /usr/lib/systemd/user/NotifyBridge@.service
  ```

3. Remove these lines from your `~/.profile`:
  ```sh
  systemctl --user import-environment DBUS_SESSION_BUS_ADDRESS
  systemctl --user import-environment DISPLAY
  systemctl --user start NotifyBridge@${USER}.service
  ```

## Troubleshooting
If something goes wrong, I'm personally sorry, but well, it was predictable. Maybe inevitable.  
First, I suggest that you try running the script as a stand-alone and watch the console's output.
```sh
$ python3 NotifyBridge.py
```
If this works but running as a service fails, try investigating whatever issue you're having by using:
```sh
$ systemctl --user status NotifyBridge@${USER}.service
```
and
```sh
$ journalctl --user
```

#### License
This software is released as a free and open source software under GNU/LGPLv3.  
Summary and full text can be found here:  
https://tldrlegal.com/license/gnu-lesser-general-public-license-v3-(lgpl-3)


[Fedora]: http://getfedora.org/
[KDE]: https://www.kde.org/
[Jenkins]: http://jenkins-ci.org/
[Notification Plugin]: https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin
[python 3+]: https://www.python.org/
[Flask]: http://flask.pocoo.org/
[Flask-JSON]: http://flask-json.readthedocs.org/en/latest/
[python3-gobject]: https://apps.fedoraproject.org/packages/pygobject3
[libnotify]: https://developer.gnome.org/libnotify/

