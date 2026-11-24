# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile

# Android WebView
-keepclassmembers class android.webkit.WebView {
    native <methods>;
}

# Native module
-keepclassmembers class * {
    native <methods>;
}

# Keep WinTune classes
-keep class com.wintune.** { *; }

# Don't verify
-dontwarn com.chaquo.python.**

# WebView settings
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}