<div align="center">

<img src="docs/cover.png" alt="ZikkO VPN Configs" width="100%">

**1,500 configurations · Refreshed every two hours**

[Get a subscription](#subscriptions) &nbsp; / &nbsp; [Download a client](#clients) &nbsp; / &nbsp; [Connect your device](#setup)

</div>

## Subscriptions

**Full Feed** gives you the entire collection. Copy this URL into your VPN client's subscription field:

```text
https://raw.githubusercontent.com/Z-ikko/ZikkO-Vpn-configs/main/sub/all.txt
```

For a smaller download, choose one **300-profile pack**. New configurations appear at the top of Pack 01. Each pack has a permanent address and refreshes as new profiles arrive.

| Subscription | Profiles | Direct URL |
| :--- | :--- | :--- |
| **Full Feed** | All 1,500 | [Full subscription](https://raw.githubusercontent.com/Z-ikko/ZikkO-Vpn-configs/main/sub/all.txt) |
| **Pack 01** | 1–300 | [Pack 01 subscription](https://raw.githubusercontent.com/Z-ikko/ZikkO-Vpn-configs/main/sub/1.txt) |
| **Pack 02** | 301–600 | [Pack 02 subscription](https://raw.githubusercontent.com/Z-ikko/ZikkO-Vpn-configs/main/sub/2.txt) |
| **Pack 03** | 601–900 | [Pack 03 subscription](https://raw.githubusercontent.com/Z-ikko/ZikkO-Vpn-configs/main/sub/3.txt) |
| **Pack 04** | 901–1200 | [Pack 04 subscription](https://raw.githubusercontent.com/Z-ikko/ZikkO-Vpn-configs/main/sub/4.txt) |
| **Pack 05** | 1201–1500 | [Pack 05 subscription](https://raw.githubusercontent.com/Z-ikko/ZikkO-Vpn-configs/main/sub/5.txt) |

On a phone, press and hold a subscription link and choose **Copy Link**. On a computer, right-click and choose **Copy link address**.

## Clients

| Client | Windows | Android | iPhone & iPad |
| :--- | :--- | :--- | :--- |
| **Hiddify** | [GitHub](https://github.com/hiddify/hiddify-app/releases/latest) | [GitHub](https://github.com/hiddify/hiddify-app/releases/latest) | [App Store](https://apps.apple.com/app/id6596777532) |
| **Karing** | [GitHub](https://github.com/KaringX/karing/releases/latest) | [GitHub](https://github.com/KaringX/karing/releases/latest) | [App Store](https://apps.apple.com/app/id6472431552) |
| **Happ** | [GitHub](https://github.com/Happ-proxy/happ-desktop/releases/latest) | [GitHub](https://github.com/Happ-proxy/happ-android/releases/latest) | [App Store](https://apps.apple.com/app/id6504287215) |
| **v2rayN** | [GitHub](https://github.com/2dust/v2rayN/releases/latest) | — | — |
| **v2rayNG** | — | [GitHub](https://github.com/2dust/v2rayNG/releases/latest) | — |
| **Throne** | [GitHub](https://github.com/throneproj/Throne/releases/latest) | — | — |
| **V2Box** | — | [Google Play](https://play.google.com/store/apps/details?id=dev.hexasoftware.v2box) | [App Store](https://apps.apple.com/app/id6446814690) |
| **Streisand** | — | — | [App Store](https://apps.apple.com/app/id6450534064) |
| **Shadowrocket** | — | — | [App Store](https://apps.apple.com/app/id932747118) (paid) |

GitHub links open the latest release. Choose the Windows package for your PC or the Android APK for your phone.

## Setup

Copy the **Full Feed** URL or a single pack above. Expand the instructions for your app.

<details>
<summary><strong>Windows · v2rayN</strong></summary>

1. Open **Subscription group → Subscription group settings** and add a group.
2. Enter `ZikkO` under **Remarks**, paste the URL into the address field, and save.
3. In **Subscription group**, update the subscription. Select a server from the new group and set it as active.
4. To route supported Windows apps through it, select **Set system proxy** in v2rayN.

</details>

<details>
<summary><strong>Android · v2rayNG</strong></summary>

1. Open the subscription groups screen and tap **+**.
2. Name the group `ZikkO`, paste the URL, and save with the checkmark.
3. Return to the server list, select the group, and use **Update subscription** in the menu.
4. Select a server, tap the connect button, and approve the Android VPN request.

</details>

<details>
<summary><strong>iPhone / iPad · Streisand</strong></summary>

1. Copy the subscription URL, open Streisand, and tap **+ → Import from Clipboard**.
2. Allow pasting if iOS asks. The subscription will appear in the profiles list.
3. Open the subscription, refresh its profiles, and select a server.
4. Tap the power button and allow iOS to add the VPN configuration when prompted.

</details>

<details>
<summary><strong>Android or iPhone / iPad · V2Box</strong></summary>

1. Open **Configs**, tap **+**, and choose **Add Subscription**.
2. Enter `ZikkO` as the name, paste the URL, and save.
3. Open the subscription and select a server. If the list is empty, refresh the subscription.
4. Go to **Home** and use the connect control. Approve the VPN permission on your device.

</details>

<details>
<summary><strong>Hiddify · Windows, Android & iOS</strong></summary>

1. Copy a ZikkO subscription URL. In Hiddify, open the profile picker, select **New profile**, then import from the clipboard.
2. Select the imported profile and press the power button. Use the profile’s update control to fetch new entries.

</details>

<details>
<summary><strong>Karing · Windows, Android & iOS</strong></summary>

1. Open **Add Profile**, choose the subscription-link option and paste the ZikkO URL. Save the profile.
2. Select the profile in **My Profiles**, choose a server and connect. Refresh the saved profile for updates.

</details>

<details>
<summary><strong>Happ · Windows, Android & iOS</strong></summary>

1. Copy the ZikkO URL. In Happ, select **+** and import from the clipboard.
2. Expand the new subscription, select a server and connect. Use the subscription’s refresh control to update the list.

</details>

<details>
<summary><strong>Throne · Windows</strong></summary>

1. Open the group manager, create a subscription group and enter the ZikkO URL as its subscription address.
2. Save and update the group, then select a server and start it. Enable the system proxy if you want Windows apps that use it to follow this connection.

</details>

<details>
<summary><strong>Shadowrocket · iPhone & iPad</strong></summary>

1. Tap **+**, set **Type** to **Subscribe**, paste the ZikkO URL and save.
2. Open the subscription on the Home screen, select a server and enable the connection. Allow the VPN configuration when iOS asks.

</details>

Refresh the saved subscription in your client to pick up new entries. Individual connections can vary by network. [View the update history](https://github.com/Z-ikko/ZikkO-Vpn-configs/actions/workflows/update.yml).

