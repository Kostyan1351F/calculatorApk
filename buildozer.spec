[app]
package.name = calculator
package.domain = org.test

title = Calculator

version = 1.0.0

source.dir = calc
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy,sqlite3,Cython<3.0

orientation = portrait

icon.filename = %(source.dir)s/pics/icon.png

android.accept_sdk_license = True

p4a.branch = develop
android.api = 36
android.ndk = 29
