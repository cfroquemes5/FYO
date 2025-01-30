[app]
# (str) Title of your application
title = MyApp

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py is located
source.dir = .

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3, kivy, sqlite3, pandas

# (str) Supported orientation (one of: landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Android NDK version to use ▋
