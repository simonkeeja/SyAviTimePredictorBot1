[app]
title = SyAvi Time Predictor
package.name = syavitimepredictor
package.domain = org.syavi

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt

version = 1.0

# IMPORTANT — pyjnius is required for your AndroidMachineLock
requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

# Your app uses Android file APIs → allow access
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# UPDATE API LEVELS (API 31 is outdated)
android.api = 33
android.minapi = 21
android.ndk = 25c

# Architecture
android.archs = arm64-v8a,armeabi-v7a

# Reduce noise in logs
android.logcat_filters = *:S python:D

# Add this to avoid file access crash on Android 13+
android.extra_args = --force-build

[buildozer]
log_level = 2
warn_on_root = 1
