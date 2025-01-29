[app]
title = TransportApp
package.name = transportapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,db
version = 1.0
requirements = python3,kivy==2.2.1,android,pandas,openpyxl,sqlite3,python-for-android==2023.10.06
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.1
fullscreen = 0
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.2.12479018
android.archs = arm64-v8a
android.minapi = 21
android.wakelock = True
