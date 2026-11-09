# Restoring an AXIS Companion Classic site on Android without the cloud

If you've cleared storage on (or reinstalled) the **AXIS Companion Classic** Android app, your site and cameras are gone from the phone. Axis has switched off the Companion cloud login, so the app can't download the site again and the **+** button only shows "Can't create site".

This repo shows how to get your cameras back into the app using its hidden **local site import** (`.accs` file). It works without an Axis account or internet access.

## Background
I have 13 Axis cameras that record to a NAS on my home network, viewed with AXIS Companion Classic on Windows and Android. I cleared the Android app's storage and reinstalled it, and my site was gone. With the cloud switched off there was no way to sign in and download it again, and the app wouldn't let me create a new site.

I didn't want to move to AXIS Camera Station Edge because I'd lose recording to the NAS (see below). So I decompiled the app and found it can still import a site from a small text file. I built that file from the Windows app's camera list, imported it, and the phone showed all 13 cameras again with working live view.

## Quick steps
1. Make a `.accs` file listing your cameras: run [make_accs.py](make_accs.py) on a PC that has the Windows desktop app, or write it by hand.
2. Copy it to the phone's **Downloads** folder.
3. Open it in AXIS Companion Classic (from the Files app, or with the adb command below).
4. Tap **Local site** in the app and enter your site password.

## Why not just move to AXIS Camera Station Edge?
Axis wants Companion users to move to [AXIS Camera Station Edge](https://www.axis.com/products/axis-camera-station-edge). Its product page lists three ways to record:
- an Axis SD card in each camera
- an AXIS S30 recorder
- AXIS Camera Station Cloud Storage

**Recording to your own NAS or network share isn't listed.** If your cameras record to a NAS and you want to keep it that way, staying on Companion Classic for local viewing is the option left. This guide keeps the phone app working on the home network (or remotely over a VPN).

## What you get
- The Android app shows **"Local site – N cameras"** and live view works after you enter the site password.
- **Home network, or remotely over a VPN.** Axis's own remote access ended with the cloud shutdown, but a VPN or Tailscale gets you onto the home network from anywhere. See [Remote access](#remote-access-over-a-vpn-or-tailscale).
- The app talks to the cameras over **plain HTTP on port 80**, not HTTPS.
- No camera limit found in the app's code (tested with 13 cameras).

## Key facts about the Android app
- Package: `com.axis.acc` (AXIS Companion Classic). Tested with version **6.0.1** on a Pixel 9 running Android 17. Version 5.1.17 also has the import.
- The phone keeps the site in a private database. **Android backup doesn't include it** (the app turns backup off). Clearing storage or uninstalling deletes it for good.
- The phone app can't log in or create sites any more. The `.accs` import is the only way to add a site.

## The `.accs` file format
The import screen is `com.axis.acc/.LocalSiteImportActivity`. The file is plain text:
- Line 1 is `1.0`.
- Every other line is one camera: `IP:port;video source;serial number;name`
- Names must not contain `;`.
- Save as **UTF-8 without a BOM**. With a BOM the app can't read the `1.0` line.

See [example.accs](example.accs):

```
1.0
192.168.1.20:80;0;ACCC8E000001;Front door
192.168.1.21:80;0;ACCC8E000002;Driveway
```

- **Video source** is `0` for a normal single-sensor camera.
- **Serial number** is the camera's MAC address without separators (on the label and in the camera's web page).
- A hostname works in place of the IP. IPv6 addresses don't, because the app splits the address on `:`.
- The `:port` part is required.
- Windows line endings (CRLF) are fine.

### What the app does with a bad file
- A camera line with the wrong number of fields, no `:port` or a port that isn't a number is skipped with no message.
- If no camera lines are usable, the app shows "There are no cameras to import."
- If the first line isn't `1.0` or `2.0`, or the app can't read the file, it shows "Can't open the file."
- Importing the same file twice creates a second site. The app doesn't check for duplicates.

### Version 2.0 format
The app also reads a second layout. Each line has exactly 6 fields:

```
2.0
Camera;192.168.1.20:80;0;ACCC8E000001;Front door;No RVP link
```

- The first field must be `Camera`. The app skips lines for other device types.
- The last field must be `No RVP link`. The app skips cameras that have a remote-access link.

Older exports may use this layout. Version `1.0` is simpler for new files.

## Making the file

### From the Windows desktop app (easiest)
If AXIS Companion Classic still works on a Windows PC, it has your camera list in:

`C:\ProgramData\Axis Communications\AXIS Companion\ApplicationSiteSettings.xml`

Run [make_accs.py](make_accs.py) on that PC (Python 3, no extra packages):

```
python make_accs.py
```

It writes `site.accs` in the current folder. You can pass a different input or output file:

```
python make_accs.py path\to\ApplicationSiteSettings.xml mysite.accs
```

- **If the desktop app has several sites,** the script writes one file per site, named after the site (for example `Home.accs`). It ignores the output file name in that case and skips sites with no cameras.
- **The script reads the local camera list (`CameraList`),** the one the desktop app shows. The same XML also holds a cloud copy (`InternetSite > Cameras`). Since the cloud shutdown that copy can be out of date. Mine still listed 4 removed cameras and was missing a new one. Don't switch the script to the cloud list.

Don't share `ApplicationSettings.xml` from the same folder. It holds your (encrypted) cloud login token.

### By hand
Write the file in a text editor using the format above. Find each camera's IP and serial in your router or the camera's web page.

## Importing the file on the phone

### Option A: phone only (not tested)
1. Put the `.accs` file in the phone's **Downloads** folder.
2. Open the Files app, tap the file and choose **AXIS Companion Classic** under "Open with".
3. Open the app, tap "Local site" and enter the site password.

### Option B: from a PC with adb (tested on a Pixel 9, Android 17)
You need [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) and USB debugging turned on.

Always pass `-s <serial>` so commands go to the right device.

1. Find the phone's serial:
   ```
   adb devices -l
   ```
2. Copy the file to the phone:
   ```
   adb -s <serial> push site.accs /sdcard/Download/site.accs
   ```
3. Open a shell on the phone:
   ```
   adb -s <serial> shell
   ```
4. Find the file's media ID and note the `_id` number:
   ```
   content query --uri content://media/external/file --projection _id:_data --where "_data LIKE '%site.accs'"
   ```
   On the Pixel, Android had already indexed the pushed file, so this returned a row straight away. If you get "No result found", give the phone a moment and try again. I haven't tested other phones.

   Run this inside the phone shell, as shown. Typed straight into Windows PowerShell as `adb shell "..."`, the quotes get mangled.
5. Open it in the app's import screen (replace `<ID>`):
   ```
   am start -a android.intent.action.VIEW -d content://media/external/file/<ID> -t application/octet-stream --grant-read-uri-permission -n com.axis.acc/.LocalSiteImportActivity
   ```
6. Type `exit`, open the app, tap **Local site** and enter the site password.

### After importing
- **Site password:** the import doesn't ask for or check the password. The app asks the first time you tap the site, then remembers it. It's the site password from the desktop app, the one it set on the cameras.
- **Getting back to the Sites list:** with only one site and a saved password, the app skips the Sites list and opens the cameras directly. Press Back to reach the Sites list.
- **Importing again:** delete the old site first (long-press it in the Sites list), or you'll get two copies.

## Remote access over a VPN or Tailscale
The imported site connects straight to the cameras' local IP addresses. If the phone can reach those addresses, the app works, wherever you are. Any tunnel that puts the phone on your home network will do:
- **Tailscale:** run a [subnet router](https://tailscale.com/kb/1019/subnets) on an always-on device at home (a NAS, Raspberry Pi or PC) and advertise the camera subnet, e.g. `192.168.1.0/24`. Approve the route in the Tailscale admin console and turn on the Tailscale app on the phone. The cameras can't run Tailscale themselves, so the subnet router is needed.
- **WireGuard or OpenVPN:** many routers and NAS boxes have a VPN server built in. Make sure the camera subnet is included in the phone's allowed IPs or routes.
- **ZeroTier** or similar: same idea; route the camera subnet through a device at home.

Notes:
- Your home subnet must not clash with the network the phone is on (e.g. both `192.168.1.x`). If it does, change the home subnet or use a less common one.
- **Don't port-forward the cameras to the internet instead.** The app uses plain HTTP, so the password and video would cross the internet unencrypted. A VPN encrypts everything inside the tunnel.

## If the app disappears from the Play Store
Save a copy of the installed app now while you still have it. On Play Store installs it's split into several APK files that must be installed together:

```
adb -s <serial> shell pm path com.axis.acc
adb -s <serial> pull <each path listed>
adb -s <serial> install-multiple base.apk split_config.*.apk
```

Notes:
- 64-bit phones (such as Pixels) need the `arm64_v8a` split. Older 32-bit tablets need `armeabi_v7a`. A copy from one won't install on the other.
- APKPure lists older versions. Its 6.0.1 download only had the 64-bit split and its 5.1.17 download only had the 32-bit split.
- **Don't install version 1.1.x on a phone or tablet.** That's the Android TV app (NVIDIA SHIELD). Its internal version number is higher than 6.0.1's, so Android treats it as an update and replaces the working phone app.
- All the builds I checked are signed with the same Axis certificate (SHA-256 starts `59FA96F7FAA29C4D`). If Android reports a different signature, the copy came from somewhere else.

## What Axis removed in 6.0
Compared with 5.1.17, version 6.0.1 drops push notifications, answering door station calls, Firebase crash reporting and analytics, Google Sign-In and the "What's new" screen. All of them depended on cloud services. The `.accs` import and local live view are still there.

## Things that don't work
- **`adb backup`:** the app blocks backups.
- **Folders under `Android/data/com.axis.acc` shown by some file managers:** they weren't real on my phone.
- **Opening the `.accs` file from `Android/data/com.axis.acc/files`:** the app says "Can't open the file". If adb created that folder, the folder belongs to adb, and the app can't read it. Use Downloads.

  As a precaution, delete the folder afterwards: `adb -s <serial> shell rm -rf /sdcard/Android/data/com.axis.acc`. The app recreates it when it needs it. I haven't confirmed that leaving it causes problems.
- **Copying the site from another device:** reading another app's private data needs root.

## How the format was found
I pulled the installed APK with adb and decompiled it with [jadx](https://github.com/skylot/jadx) to read `LocalSiteImportActivity`. No Axis code is included here.

## FAQ
**My AXIS Companion Classic site disappeared from the Android app. Can I get it back?**
Yes. Clearing storage or reinstalling deletes the site from the phone, and the cloud can't restore it any more. Import it again from a `.accs` file as described above.

**The app says "Can't create site". What can I do?**
The app no longer creates sites. Importing a `.accs` file is the only way to add one.

**Can I keep recording to a NAS after the AXIS Companion cloud shutdown?**
The cameras keep recording to the NAS on their own; that's set on each camera. What stops is the cloud login in the app. Importing a local site gets live view on the phone working again. AXIS Camera Station Edge doesn't list NAS recording.

**Do I need an Axis account or internet access?**
No. The imported site talks directly to the cameras on your network.

**Can I view my cameras away from home?**
Yes, over a VPN or Tailscale. See [Remote access](#remote-access-over-a-vpn-or-tailscale).

**Does this work on iPhone?**
Not tested. This guide only covers Android.

**What is the site password?**
The password the Windows desktop app set on the cameras when you created the site. The import doesn't include it; the app asks the first time you open the site.

## Disclaimer
Not affiliated with or endorsed by Axis Communications. AXIS, AXIS Companion and AXIS Camera Station are trademarks of Axis AB. Use at your own risk. This only uses features already in the app.
