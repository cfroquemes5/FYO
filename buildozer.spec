cat <<EOT > buildozer.spec
[app]
title = MyApp
package.name = myapp
package.domain = org.example
source.dir = .
version = 1.0  # <--- Asegúrate de que esta línea esté presente
requirements = python3,kivy,sqlite3,pandas
android.ndk_path = \$ANDROID_HOME/ndk/27.2.12479018
android.sdk_path = \$ANDROID_HOME
android.sdk_build_tools = 34.0.0
android.api = 34
android.minapi = 21
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
EOT
