package com.wintune;

import android.content.ComponentName;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.webkit.WebView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    
    private static final int PERMISSIONS_REQUEST_CODE = 1001;
    private static final String[] REQUIRED_PERMISSIONS = new String[] {
        "android.permission.INTERNET",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_EXTERNAL_STORAGE"
    };
    
    private WebView webView;
    private boolean termuxLaunched = false;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        setupWebView();
        checkPermissions();
        extractWinTuneFiles();
        checkTermuxInstallation();
        
        // Load the PWA after setup
        webView.loadUrl("file:///android_asset/index.html");
    }
    
    private void setupWebView() {
        webView = new WebView(this);
        setContentView(webView);
        
        // Enable JavaScript
        webView.getSettings().setJavaScriptEnabled(true);
        
        // Enable DOM storage
        webView.getSettings().setDomStorageEnabled(true);
        
        // Enable file access
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setAllowContentAccess(true);
        
        // Cache settings
        webView.getSettings().setAppCacheEnabled(true);
        webView.getSettings().setCacheMode(android.webkit.WebSettings.CACHE_ALL);
        
        // Enable cleartext traffic for localhost
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            webView.getSettings().setMixedContentMode(android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        }
        
        // Set WebChromeClient for debugging
        webView.setWebChromeClient(new android.webkit.WebChromeClient());
        
        // Set WebViewClient to handle navigation securely
        webView.setWebViewClient(new android.webkit.WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(android.webkit.WebView view, android.webkit.WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (url.startsWith("http://127.0.0.1:8000") || 
                    url.startsWith("http://localhost:8000") ||
                    url.startsWith("file:///android_asset")) {
                    return false;
                }
                return true;
            }
        });
    }
    
    private void checkPermissions() {
        List<String> permissionsNeeded = new ArrayList<>();
        
        for (String permission : REQUIRED_PERMISSIONS) {
            if (ContextCompat.checkSelfPermission(this, permission) 
                != PackageManager.PERMISSION_GRANTED) {
                permissionsNeeded.add(permission);
            }
        }
        
        if (!permissionsNeeded.isEmpty()) {
            String[] permissionsArray = permissionsNeeded.toArray(new String[0]);
            ActivityCompat.requestPermissions(this, permissionsArray, PERMISSIONS_REQUEST_CODE);
        }
    }
    
    private void extractWinTuneFiles() {
        try {
            File targetDir = new File(getFilesDir(), "wintune");
            if (!targetDir.exists()) {
                targetDir.mkdirs();
            }
            
            // Extract Python backend
            String[] files = {"wintune_android.py", "settings.json"};
            for (String file : files) {
                try {
                    java.io.InputStream in = getAssets().open(file);
                    File outFile = new File(targetDir, file);
                    java.io.OutputStream out = new java.io.FileOutputStream(outFile);
                    byte[] buffer = new byte[1024];
                    int read;
                    while ((read = in.read(buffer)) != -1) {
                        out.write(buffer, 0, read);
                    }
                    in.close();
                    out.close();
                } catch (Exception e) {
                    Log.w("MainActivity", "Could not extract " + file);
                }
            }
        } catch (Exception e) {
            Log.e("MainActivity", "Failed to extract files", e);
        }
    }
    
    private void checkTermuxInstallation() {
        try {
            PackageManager pm = getPackageManager();
            pm.getPackageInfo("com.termux", PackageManager.GET_ACTIVITIES);
            checkWinTuneStatus();
        } catch (PackageManager.NameNotFoundException e) {
            showInstallTermuxDialog();
        }
    }
    
    private void checkWinTuneStatus() {
        new Thread(() -> {
            try {
                java.net.URL url = new java.net.URL("http://127.0.0.1:8000/version");
                java.net.HttpURLConnection conn = (java.net.HttpURLConnection) url.openConnection();
                conn.setConnectTimeout(2000);
                
                runOnUiThread(() -> {
                    if (conn.getResponseCode() == 200) {
                        Toast.makeText(this, "WinTune server connected", Toast.LENGTH_SHORT).show();
                    } else {
                        showStartTermuxDialog();
                    }
                });
                
            } catch (Exception e) {
                runOnUiThread(() -> showStartTermuxDialog());
            }
        }).start();
    }
    
    private void showInstallTermuxDialog() {
        new AlertDialog.Builder(this)
            .setTitle("Install Termux")
            .setMessage("This app requires Termux to run the MP3 downloader backend.\n\nWould you like to install it from F-Droid?")
            .setPositiveButton("Install from F-Droid", (d, w) -> {
                Intent intent = new Intent(Intent.ACTION_VIEW);
                intent.setData(Uri.parse("https://f-droid.org/packages/com.termux/"));
                startActivity(intent);
            })
            .setNegativeButton("Cancel", null)
            .show();
    }
    
    private void showStartTermuxDialog() {
        new AlertDialog.Builder(this)
            .setTitle("Start WinTune Server")
            .setMessage("WinTune server is not running. Start it now?")
            .setPositiveButton("Start", (d, w) -> startWinTuneServer())
            .setNegativeButton("Cancel", null)
            .show();
    }
    
    private void startWinTuneServer() {
        if (termuxLaunched) {
            Toast.makeText(this, "Server starting...", Toast.LENGTH_SHORT).show();
            return;
        }
        
        try {
            Intent intent = new Intent();
            intent.setComponent(new ComponentName(
                "com.termux",
                "com.termux.app.TermuxActivity"
            ));
            intent.putExtra("com.termux.intent.bootstrap.SHELL", "" +
                "cd ~/wintune\n" +
                "export PATH=$PATH:/data/data/com.termux/files/usr/bin\n" +
                "if [ ! -f wintune_android.py ]; then\n" +
                "  echo 'Downloading WinTune...'\n" +
                "  curl -s https://raw.githubusercontent.com/frikkieshagger/wintune/main/wintune_android.py > wintune_android.py\n" +
                "fi\n" +
                "python wintune_android.py &");
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK;
            
            startActivity(intent);
            termuxLaunched = true;
            
            Toast.makeText(this, "Starting WinTune server...\nCheck Termux for output", Toast.LENGTH_LONG).show();
            
            new android.os.Handler(getMainLooper()).postDelayed(() -> {
                checkWinTuneStatus();
            }, 5000);
            
        } catch (Exception e) {
            Log.e("MainActivity", "Error starting WinTune", e);
            Toast.makeText(this, "Failed to start WinTune. Check if Termux is installed.", 
                          Toast.LENGTH_LONG).show();
        }
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, 
                                          @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PERMISSIONS_REQUEST_CODE) {
            if (grantResults.length > 0 && grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Storage permissions required for downloads", 
                              Toast.LENGTH_LONG).show();
            }
        }
    }
    
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
    
    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }
}