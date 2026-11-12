[app]
title = PasswordGen
package.name = passwordgen
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

# Принудительно указываем скачать свежую ветку p4a архивом
p4a.branch = develop
p4a.url = https://github.com/kivy/python-for-android/archive/refs/heads/develop.zip
