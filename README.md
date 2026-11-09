# Restoring an AXIS Companion Classic (version 3) site on Android without the cloud

If you've cleared the storage of the **AXIS Companion Classic** Android app, or reinstalled it, your cameras will have disappeared from the app. (The app calls your group of cameras a "site".) Axis has switched off its online login for Companion Classic, so the app can't download them again. Tapping **+** only shows "Can't create site".

This guide shows how to put your cameras back into the app. The app has a hidden way to load a list of cameras from a small text file (a `.accs` file). You don't need an Axis account or an internet connection.

## Which AXIS Companion is this about?
Axis has used the name "Companion" for two different products. **This guide is only about AXIS Companion Classic, also called AXIS Companion version 3 or V3.** That's the version that can record to your own NAS (network attached storage: a storage box on your home network).

| | **AXIS Companion Classic / version 3** (this guide) | AXIS Companion version 4, now **AXIS Camera Station Edge** |
|---|---|---|
| Recording to your own (3rd-party) NAS or network share | **Yes** ("selected third-party NAS devices") | **No** ("No third-party NAS support") |
| Other recording options | Axis SD card, AXIS Companion Recorder, AXIS S3008 (from 3.70.1, offline only, no mobile app) | AXIS Surveillance Card, AXIS Companion Recorder, AXIS S30 and S40 recorders, AXIS Camera Station Cloud Storage |
| Camera firmware (AXIS OS) | 5.50 or newer | 8.40 or newer. Older cameras only work with limits, and every camera must be factory reset first |
| Internet connection and My Axis account | Not needed | Needed to set up and manage the system |
| Viewing from outside the home through Axis's servers | Stopped: for cameras added after 31 March 2023, then for all cameras on 31 December 2024 | Yes |
| Windows app | AXIS Companion 3.x (latest 3.80) | AXIS Camera Station Edge |
| Android app | **AXIS Companion Classic** (`com.axis.acc`) | AXIS Camera Station Edge (`com.axis.companion`) |

Sources: [Axis: requirements for upgrading from Companion Classic](https://help.axis.com/en-us/axis-camera-station-edge#requirements), [Axis FAQ: Secure Remote Access discontinued](https://faq.axis.com/s/article/vms-axis-secure-remote-access-service-discontinued?language=en_US), Axis's "AXIS S3008 support in AXIS Companion Classic (Version 3)" disclaimer (April 2022, on the [Companion Classic support page](https://www.axis.com/products/axis-companion-classic/support)), [NetcamCenter: Remote access AXIS Camera Companion Classic](https://netcamcenter.com/en/remote-access-companion-classic-versie-3-2).

In this guide, "AXIS Companion" and "the app" always mean version 3 (Classic).

## What Axis says about Companion Classic
Axis's own FAQ, ["I use AXIS Companion Classic. What does it mean for me when the Axis Secure Remote Access service is discontinued?"](https://faq.axis.com/s/article/vms-axis-secure-remote-access-service-discontinued?language=en_US):

> When the Axis Secure Remote Access service is discontinued, you no longer have access to the cameras remotely, only on premises. If you need remote access after December 31, 2024, we recommend that you migrate to AXIS Camera Station Edge. [...] AXIS Companion Classic will continue to be supported on premises in offline scenarios after December 31, 2024.

In other words, Axis still supports using Companion Classic at home, which is what this guide does. The only thing that has gone is viewing your cameras from outside the home through Axis's servers.

## Why I wrote this
I have 13 Axis cameras that record to a NAS at home. I watch them with AXIS Companion Classic on Windows and Android. I cleared the Android app's storage, and my cameras disappeared from it. Axis had switched off its online service, so there was no way to sign in and get them back, and the app wouldn't let me set them up again.

I didn't want to move to AXIS Camera Station Edge. I'm a home user, not a business. My cameras are older models and they record to my own NAS. Edge can't record to a NAS at all. Moving would also mean resetting every camera, buying Axis memory cards or an Axis recorder and relying on an Axis account and an internet connection (see below).

So I looked inside the app's code and found it can still load a list of cameras from a small text file. I made that file from the camera list in the Windows app and loaded it into the phone. All 13 cameras came back, with live video working.

## Quick steps
1. Make a `.accs` file that lists your cameras. Either run [make_accs.py](make_accs.py) on a PC with the Windows app, or write the file yourself.
2. Copy the file to the phone's **Downloads** folder.
3. Open the file in AXIS Companion Classic, either from the phone's Files app or from a PC (see below).
4. In the app, tap **Local site** and enter your site password.

## Why not just move to AXIS Camera Station Edge (Companion version 4)?
Axis wants Companion Classic users to move to [AXIS Camera Station Edge](https://www.axis.com/products/axis-camera-station-edge), which used to be called AXIS Companion version 4. Its product page gives three places to record to:
- an Axis memory card (SD card) in each camera
- an AXIS S30 recorder
- AXIS Camera Station Cloud Storage (a paid online service)

**Your own NAS isn't one of them.** Axis's [upgrade requirements](https://help.axis.com/en-us/axis-camera-station-edge#requirements) say it plainly: "No third-party NAS support". Moving would also mean:
- **resetting every camera to factory settings** ("Any device that was used in AXIS Companion Classic must be hard reset")
- cameras with **AXIS OS 8.40 or newer**, where Classic works with 5.50 or newer
- a **My Axis account and an internet connection** to set up and manage the system

For a home user with older cameras and a NAS, that means buying new storage, possibly new cameras and relying on Axis's online services. Staying on Companion Classic avoids all of that. This guide keeps the phone app working at home, and from anywhere through a VPN.

## What you get
- The Android app shows **"Local site – N cameras"**. Live video works once you enter the site password.
- **It works at home, and away from home through a VPN.** Axis's own way of viewing from outside the home has stopped, but a VPN such as Tailscale connects your phone to your home network from anywhere. See [Viewing your cameras away from home](#viewing-your-cameras-away-from-home).
- The app connects to the cameras over **plain HTTP on port 80**. This isn't encrypted (it's not HTTPS).
- I found no limit on the number of cameras in the app's code. I've tested it with 13.

## Key facts about the Android app
- The app is AXIS Companion Classic (package name `com.axis.acc`). I tested version **6.0.1** on a Pixel 9 with Android 17. The older version 5.1.17 can also load the file.
- The app keeps your cameras in its own private storage. **Android's backup doesn't save it**, because the app opts out of backups. Clearing the app's storage or uninstalling the app deletes your cameras for good.
- The app can no longer sign in or set up new sites. Loading a `.accs` file is the only way to add cameras.

## The `.accs` file
The file is plain text:
- The first line is `1.0`.
- Every other line is one camera: `IP address:port;video source;serial number;name`
- Names mustn't contain `;`.
- Save it as **UTF-8 without a BOM**. A BOM is an invisible marker that some editors add to the start of a file, and the app can't read the file if it's there. In Notepad, choose "UTF-8", not "UTF-8 with BOM".

Example ([example.accs](example.accs)):

```
1.0
192.168.1.20:80;0;ACCC8E000001;Front door
192.168.1.21:80;0;ACCC8E000002;Driveway
```

- **Video source** is `0` for an ordinary camera with one lens.
- **Serial number** is the camera's MAC address without the colons or dashes. It's on the camera's label and on the camera's web page.
- You can use a hostname instead of an IP address. IPv6 addresses don't work, because the app splits the address at the `:`.
- The `:port` part must be there.
- Windows line endings are fine.

### What happens if the file has mistakes
- A camera line with the wrong number of parts, no `:port` or a port that isn't a number is skipped without any warning.
- If none of the camera lines can be used, the app says "There are no cameras to import."
- If the first line isn't `1.0` or `2.0`, or the app can't read the file, it says "Can't open the file."
- Loading the same file twice gives you two copies of the site. The app doesn't check.

### The older 2.0 layout
The app also reads a second layout. Each line has exactly 6 parts:

```
2.0
Camera;192.168.1.20:80;0;ACCC8E000001;Front door;No RVP link
```

- The first part must be `Camera`. Lines for other kinds of device are skipped.
- The last part must be `No RVP link`. Cameras that were set up for Axis's remote access are skipped.

Older exported files may use this layout. For a new file, `1.0` is simpler.

## Making the file

### From the Windows app (easiest)
If AXIS Companion Classic still works on a Windows PC, your camera list is in this file:

`C:\ProgramData\Axis Communications\AXIS Companion\ApplicationSiteSettings.xml`

Run [make_accs.py](make_accs.py) on that PC. You need Python 3 and nothing else:

```
python make_accs.py
```

It creates `site.accs` in the folder you run it from. You can also choose which file to read and what to call the new one:

```
python make_accs.py path\to\ApplicationSiteSettings.xml mysite.accs
```

- **If the Windows app has more than one site,** the script makes one file per site, named after the site (for example `Home.accs`). In that case it ignores the name you gave, and it skips sites with no cameras.
- **The script uses the camera list the Windows app shows** (`CameraList`). The same file also holds an old copy from Axis's online service (`InternetSite > Cameras`). Since the service closed, that copy can be out of date. Mine still listed 4 cameras I'd removed and was missing a new one. Don't change the script to use it.

Don't share `ApplicationSettings.xml` from the same folder. It holds your (encrypted) login for Axis's old online service.

### Writing it yourself
Use a text editor and the layout above. You can find each camera's IP address and serial number in your router or on the camera's web page.

## Loading the file on the phone

### Option A: on the phone only (not tested)
1. Put the `.accs` file in the phone's **Downloads** folder.
2. Open the Files app, tap the file and choose **AXIS Companion Classic** under "Open with".
3. Open the app, tap "Local site" and enter the site password.

### Option B: from a PC with adb (tested on a Pixel 9 with Android 17)
adb (Android Debug Bridge) is Google's free tool for controlling an Android phone from a PC over USB. Download [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) and turn on USB debugging on the phone.

Always include `-s <serial>` so the command goes to the right phone.

1. Find the phone's serial number:
   ```
   adb devices -l
   ```
2. Copy the file to the phone:
   ```
   adb -s <serial> push site.accs /sdcard/Download/site.accs
   ```
3. Open a command line on the phone:
   ```
   adb -s <serial> shell
   ```
4. Find the file's ID number and write down the `_id` value:
   ```
   content query --uri content://media/external/file --projection _id:_data --where "_data LIKE '%site.accs'"
   ```
   On my Pixel this found the file straight away. If you get "No result found", wait a moment and try again. I haven't tried other phones.

   Type this on the phone's command line, as shown. If you type it straight into Windows PowerShell as `adb shell "..."`, PowerShell breaks the quote marks.
5. Open the file in the app (replace `<ID>` with the number):
   ```
   am start -a android.intent.action.VIEW -d content://media/external/file/<ID> -t application/octet-stream --grant-read-uri-permission -n com.axis.acc/.LocalSiteImportActivity
   ```
6. Type `exit`. Open the app, tap **Local site** and enter the site password.

### After loading the file
- **Site password:** loading the file doesn't ask for the password or check it. The app asks the first time you tap the site, then remembers it. It's the password you chose when you first set up the site in the Windows app.
- **Getting back to the list of sites:** if you only have one site and the password is saved, the app goes straight to the cameras. Press Back to see the list of sites.
- **Loading the file again:** delete the old site first (press and hold it in the list of sites), or you'll end up with two copies.

## Windows app
The Windows app keeps its cameras in `C:\ProgramData\Axis Communications\AXIS Companion\ApplicationSiteSettings.xml`, so reinstalling the phone app doesn't affect it. If you lose your cameras on Windows too, you don't need to rebuild that file by hand.

The Windows app (I checked version 3.80) has its own **Import site** and **Export site** options. They use the same `.accs` file ("AXIS Companion Classic Site (*.accs)"), so the [example.accs](example.accs) layout and the file from [make_accs.py](make_accs.py) should work in both apps.

The login screen still has **Create new site** and **Import site** links under the LOG IN button, so the Windows app looks able to set up sites without Axis's online service. I haven't tested either since the service closed.

- **Import site** sets up a site from a `.accs` file. Not tested yet.
- **Export site** saves a working site as a `.accs` file. Use it to make a file for the phone or a spare copy. It won't export a site with a camera that was set up for Axis's remote access.
- **Back up** the `C:\ProgramData\Axis Communications\AXIS Companion\` folder before trying either.

## The site password
The site password isn't in the `.accs` file or in the Windows app's files. It's kept on the cameras:
- When you set up a site, AXIS Companion Classic adds a user called **`ACCAdmin`** to each camera, with the site password as its password.
- The apps log in to each camera as `ACCAdmin` with the password you type. That's why loading the file never asks for it: the app asks the first time you open the site.
- To check the password, open a camera's web page and log in as `ACCAdmin`. If the site has no password, the app uses `pass`.
- **If you lose the site password, you'll have to reset every camera to factory settings.** Keep it in a password manager.

The password doesn't unlock or decrypt any files. It's only the login for the cameras. The apps can remember it so you don't have to type it each time:
- **Windows:** if "Remember password" is ticked, it's saved in `%LOCALAPPDATA%\Axis Communications\AXIS Companion\UserSiteSettings.xml`. It's encrypted with Windows' built-in protection (DPAPI), so only the same Windows user on the same PC can read it. Copying the file to another PC won't bring the password with it.
- **Android:** it's saved in the app's private storage, and lost if you clear the app's storage.

## Viewing your cameras away from home
The app connects straight to each camera's address on your home network. If your phone can reach those addresses, the app works wherever you are. A VPN does this: it connects your phone to your home network over the internet. Any of these will work:
- **Tailscale:** set up a [subnet router](https://tailscale.com/kb/1019/subnets) on something at home that's always on (a NAS, Raspberry Pi or PC). Tell it to share your home network's address range, for example `192.168.1.0/24`. Approve this in the Tailscale admin page, then turn on Tailscale on the phone. The cameras can't run Tailscale themselves, which is why you need the subnet router.
- **WireGuard or OpenVPN:** many routers and NAS boxes have a VPN server built in. Make sure it gives the phone access to the cameras' address range.
- **ZeroTier** or similar: the same idea. Route the cameras' address range through a device at home.

Things to watch:
- Your home network and the network the phone is on mustn't use the same address range (for example, both `192.168.1.x`). If they do, change your home network to a less common range.
- **Don't open ports on your router to reach the cameras directly.** The app doesn't encrypt anything, so your password and video would travel across the internet for anyone to see. A VPN encrypts everything.

## If the app disappears from the Play Store
Save a copy of the app now, while it's still on your phone. Apps installed from the Play Store come as several APK files that have to be installed together:

```
adb -s <serial> shell pm path com.axis.acc
adb -s <serial> pull <each path listed>
adb -s <serial> install-multiple base.apk split_config.*.apk
```

Things to know:
- 64-bit phones (such as Pixels) need the `arm64_v8a` file. Older 32-bit tablets need `armeabi_v7a`. A copy from one won't install on the other.
- The APKPure website has older versions. Its 6.0.1 download only had the 64-bit file, and its 5.1.17 download only had the 32-bit file.
- **Don't install version 1.1.x on a phone or tablet.** That's the Android TV version (for the NVIDIA SHIELD). Android sees it as newer than 6.0.1 and replaces your working phone app with it.
- Every version I checked is signed with the same Axis certificate (its SHA-256 fingerprint starts `59FA96F7FAA29C4D`). If Android says the signature is different, the copy didn't come from Axis.

## What Axis removed in version 6.0
Compared with 5.1.17, version 6.0.1 no longer has notifications, answering calls from door stations, crash reporting, Google sign-in or the "What's new" screen. They all relied on online services. Loading a `.accs` file and watching live video still work.

## Things that don't work
- **`adb backup`:** the app blocks backups.
- **Folders under `Android/data/com.axis.acc` that some file managers show:** on my phone they didn't really exist.
- **Opening the `.accs` file from `Android/data/com.axis.acc/files`:** the app says "Can't open the file". If adb created that folder, adb owns it and the app can't read it. Use the Downloads folder instead.

  To be safe, delete the folder afterwards: `adb -s <serial> shell rm -rf /sdcard/Android/data/com.axis.acc`. The app makes it again when it needs it. I don't know for certain that leaving it causes problems.
- **Copying the site from another phone or tablet:** you can't read another app's private storage without rooting the device.

## How I worked out the file layout
I copied the app from my phone with adb and turned it back into readable code with [jadx](https://github.com/skylot/jadx). The part that loads the file is called `LocalSiteImportActivity`. None of Axis's code is included here.

## Links and archived copies
These are the official Axis pages and documents for AXIS Companion Classic, plus the ones I've quoted. Axis may take them down at some point, so each one has a link to the [Wayback Machine](https://web.archive.org/), a free public archive of web pages.

- **"copy from …"** opens the saved copy closest to 9 November 2026. Other dates may be available on the same page.
- **"search"** means I couldn't find a saved copy. You can save one yourself at [web.archive.org/save](https://web.archive.org/save) while the original still works.
- **SHA-256** is a fingerprint of each file as I downloaded it from Axis on 9 November 2026. If you find a copy elsewhere, you can check it's identical: in Windows PowerShell run `Get-FileHash <file>` and compare the result.

About the Windows installer: Axis's support page gives its SHA-256 as `743E6DBDF2B733ECC9D4A562DECDF932ABED57DB609E8FCE6FDB1F264A318DBF`, but the file I downloaded has a different value (below). My copy is digitally signed by Axis Communications AB and Windows says the signature is valid, so I think Axis updated the file without updating the page. The Wayback Machine copy may be an older build.

### Software
| Document | Wayback Machine | SHA-256 of the copy I downloaded on 9 November 2026 |
|---|---|---|
| [AXIS Companion Classic support page (downloads and documents)](https://www.axis.com/products/axis-companion-classic/support) | [copy from 08/02/2026](https://web.archive.org/web/20260208050244/https://www.axis.com/products/axis-companion-classic/support) |  |
| [Windows app 3.80.1 installer (`AXISCompanionSetup.exe`)](https://www.axis.com/ftp/pub_soft/cam_srv/cam_companion/latest/AXISCompanionSetup.exe) | [copy from 16/01/2026](https://web.archive.org/web/20260116090039/https://www.axis.com/ftp/pub_soft/cam_srv/cam_companion/latest/AXISCompanionSetup.exe) | `55D881BD634CE7FDCE7648897986940000880DA7D9AB45BE9E06485C1467F744` |
| [Windows app release notes (`relnote.txt`)](https://www.axis.com/ftp/pub_soft/cam_srv/cam_companion/latest/relnote.txt) | [copy from 08/05/2026](https://web.archive.org/web/20260508142511/https://www.axis.com/ftp/pub_soft/cam_srv/cam_companion/latest/relnote.txt) | `6FF2764324C6D0854CF95AB2368ABD8ADD12B28575CE1A671A2B575EDE52B29E` |
| [Android app: AXIS Companion Classic (Google Play)](https://play.google.com/store/apps/details?id=com.axis.acc) | [copy from 13/03/2026](https://web.archive.org/web/20260313054854/https://play.google.com/store/apps/details?id=com.axis.acc) |  |
| [Android app: all versions (APKPure)](https://apkpure.com/axis-companion-classic/com.axis.acc/versions) | [search](https://web.archive.org/web/*/https://apkpure.com/axis-companion-classic/com.axis.acc/versions) |  |

### Manuals and guides
| Document | Wayback Machine | SHA-256 of the copy I downloaded on 9 November 2026 |
|---|---|---|
| [User manual](https://www.axis.com/dam/public/eb/d4/58/axis-companion-classic-user-manual-en-en-US-358443.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031241/https://www.axis.com/dam/public/eb/d4/58/axis-companion-classic-user-manual-en-en-US-358443.pdf) | `CE8EEED4E79967EC8EC254BD6686262A2D58A617EDAA5F785DD45048F83F7D58` |
| [Datasheet](https://www.axis.com/dam/public/55/e0/f6/datasheet-axis-companion-classic-en-US-375129.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031243/https://www.axis.com/dam/public/55/e0/f6/datasheet-axis-companion-classic-en-US-375129.pdf) | `5CA4E0041C2E60B6EDBC2CEDD42973FD85E065E257A051872F18B54BBA334355` |
| [Datasheet (older edition)](https://www.axis.com/dam/public/0a/5a/d5/datasheet-axis-companion-classic-en-US-361007.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031242/https://www.axis.com/dam/public/0a/5a/d5/datasheet-axis-companion-classic-en-US-361007.pdf) | `E5691457F4046ADE231E5831AFB227628142014631F1993C21760A0E5A843C27` |
| [NAS best practices](https://www.axis.com/dam/public/8a/72/3c/axis-camera-companion--nas-best-practices-en-US-57549.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031241/https://www.axis.com/dam/public/8a/72/3c/axis-camera-companion--nas-best-practices-en-US-57549.pdf) | `8E95645E3A0F0F2F05EAE4B5670FB0290F9BCB43D77C9679EADE1AFC34803F37` |
| [QNAP autoconfiguration](https://www.axis.com/dam/public/dc/0f/97/axis-camera-companion--qnap-autoconfiguration-en-US-59273.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031245/https://www.axis.com/dam/public/dc/0f/97/axis-camera-companion--qnap-autoconfiguration-en-US-59273.pdf) | `3A8AF9458309B9F50A652C72D9A5BA5AE3948C4D10AE87003591B9537547FE7C` |
| [Synology setup guide](https://www.axis.com/dam/public/c4/6f/21/axis-camera-companion--synology-setup-guide-en-US-57555.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031238/https://www.axis.com/dam/public/c4/6f/21/axis-camera-companion--synology-setup-guide-en-US-57555.pdf) | `80C4EBB53DD32EF4A246829744A61970163CCB686EE240ED299B9E8EC5D314E8` |

### Notices and statements
| Document | Wayback Machine | SHA-256 of the copy I downloaded on 9 November 2026 |
|---|---|---|
| [Product discontinuation: AXIS Companion Classic (rev 2)](https://www.axis.com/dam/public/28/23/51/product-discontinuation-axis-companion-classic_rev2pdf-en-US-460527.pdf) | [copy from 15/01/2026](https://web.archive.org/web/20260115074747/https://www.axis.com/dam/public/28/23/51/product-discontinuation-axis-companion-classic_rev2pdf-en-US-460527.pdf) | `89F7E358B2F27A3BD7111F2904B82ED84A5056A581D75E1504AA07473959B5A5` |
| [Discontinuation statement: AXIS Secure Remote Access for Companion Classic](https://www.axis.com/dam/public/41/42/5d/product-discontinuation-sra-axis-companion-classic-en-US-385806.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031242/https://www.axis.com/dam/public/41/42/5d/product-discontinuation-sra-axis-companion-classic-en-US-385806.pdf) | `211C067C74E338BC13E6333D9993999C3BCBF5942B6FD2C3F40D0BE0203C2B84` |
| [Disclaimer: AXIS S3008 and AXIS Companion Classic](https://www.axis.com/dam/public/6d/c0/21/disclaimer--axis-s3008-and-axis-companion-classic-en-US-403725.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031245/https://www.axis.com/dam/public/6d/c0/21/disclaimer--axis-s3008-and-axis-companion-classic-en-US-403725.pdf) | `47C7C4F9D9308A21CEFA44D4F5719FCFB4B722EFE1AE205D34B1B2BCD31485EA` |
| [Migration from AXIS Companion Classic to AXIS Companion version 4](https://www.axis.com/dam/public/bd/e2/00/migration-from-axis-companion-classic-to-axis-companion-version-4-en-US-404554.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031238/https://www.axis.com/dam/public/bd/e2/00/migration-from-axis-companion-classic-to-axis-companion-version-4-en-US-404554.pdf) | `83093E1B7ACA6F2A2BB1050808F7937518DFB4DF2B845B4C6FAE0F4A73DE9187` |
| [AXIS software licence agreement](https://www.axis.com/dam/public/1a/6d/54/axis-software-license-agreement-en-US-91132.pdf) | [copy from 16/05/2025](https://web.archive.org/web/20250516031238/https://www.axis.com/dam/public/1a/6d/54/axis-software-license-agreement-en-US-91132.pdf) | `65CFBB535BB9D0DBFA8757262BD928C6ABDEC80E66E0CB42B4335225D2DB2065` |
| [Mobile app software licence agreement](https://www.axis.com/dam/public/48/e4/f0/mobile-app:-axis-software-agreement-license-en-US-110377.pdf) | [copy from 15/05/2025](https://web.archive.org/web/20250515183015/https://www.axis.com/dam/public/48/e4/f0/mobile-app:-axis-software-agreement-license-en-US-110377.pdf) | `CF3AE7F416B55907F4461D6A1A51274713750C6E923448B061D0C54793303EBC` |
| [Axis FAQ: Secure Remote Access discontinued for Companion Classic](https://faq.axis.com/s/article/vms-axis-secure-remote-access-service-discontinued?language=en_US) | [copy from 16/07/2026](https://web.archive.org/web/20260716234229/https://faq.axis.com/s/article/vms-axis-secure-remote-access-service-discontinued?language=en_US) |  |
| [Axis FAQ116603: Secure Remote Access](https://www.axis.com/support/faq/FAQ116603) | [search](https://web.archive.org/web/*/https://www.axis.com/support/faq/FAQ116603) |  |

### AXIS Camera Station Edge (version 4)
| Document | Wayback Machine | SHA-256 of the copy I downloaded on 9 November 2026 |
|---|---|---|
| [Product page](https://www.axis.com/products/axis-camera-station-edge) | [copy from 18/05/2026](https://web.archive.org/web/20260518032127/https://www.axis.com/products/axis-camera-station-edge) |  |
| [User manual, including requirements for upgrading from Classic](https://help.axis.com/en-us/axis-camera-station-edge) | [copy from 15/07/2026](https://web.archive.org/web/20260715042947/https://help.axis.com/en-us/axis-camera-station-edge) |  |
| [User manual PDF (September 2026)](https://help.axis.com/download/um_camera_station_edge_t10074276_2609.pdf) | [search](https://web.archive.org/web/*/https://help.axis.com/download/um_camera_station_edge_t10074276_2609.pdf) | `1D671BFBDECD6CA941362D1474F651AABB11029882E9F9B0A160F1D1ED187523` |
| [Former AXIS Companion product page ("upgraded to AXIS Camera Station Edge")](https://www.axis.com/products/axis-companion) | [copy from 11/09/2026](https://web.archive.org/web/20260911100728/https://www.axis.com/products/axis-companion) |  |

### Other
| Document | Wayback Machine | SHA-256 of the copy I downloaded on 9 November 2026 |
|---|---|---|
| [NetcamCenter: Remote access AXIS Camera Companion Classic](https://netcamcenter.com/en/remote-access-companion-classic-versie-3-2) | [copy from 08/02/2026](https://web.archive.org/web/20260208160940/https://netcamcenter.com/en/remote-access-companion-classic-versie-3-2) |  |

## FAQ
**My cameras disappeared from the AXIS Companion Classic Android app. Can I get them back?**
Yes. Clearing the app's storage or reinstalling it deletes them from the phone, and Axis's online service can't restore them any more. Load them again from a `.accs` file as described above.

**The app says "Can't create site". What can I do?**
The app can't set up new sites any more. Loading a `.accs` file is the only way to add one.

**Can I keep recording to my NAS now Axis's online service has closed?**
Yes. Recording to the NAS is set up on each camera, so the cameras carry on by themselves. Only the app's online login stopped working. Loading the file gets live video on the phone working again. AXIS Camera Station Edge can't record to a NAS.

**Do I need an Axis account or an internet connection?**
No. The app connects straight to the cameras on your home network.

**Can I watch my cameras away from home?**
Yes, through a VPN such as Tailscale. See [Viewing your cameras away from home](#viewing-your-cameras-away-from-home).

**Does this work on an iPhone?**
I haven't tested it. This guide only covers Android.

**What is the site password?**
It's the password of the `ACCAdmin` user that AXIS Companion Classic added to each camera. It isn't in the `.accs` file. The app asks for it the first time you open the site. See [The site password](#the-site-password).

**Does the same file work in the Windows app?**
It should. The Windows app has Import site and Export site options that use the same `.accs` file. See [Windows app](#windows-app).

## Disclaimer
This isn't connected to or approved by Axis Communications. AXIS, AXIS Companion and AXIS Camera Station are trademarks of Axis AB. Use this at your own risk. It only uses features that are already in the app.

## Licence
[MIT](LICENSE). You're free to use, change and share it, including this guide.
