[app]
title = TransportApp
package.name = transportapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,db
version = 1.0
requirements = python3,kivy==2.1.0,android,pandas,openpyxl,sqlite3
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 30
android.ndk = 19b
android.wakelock = True