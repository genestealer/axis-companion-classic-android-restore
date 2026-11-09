import re
import sys
import xml.etree.ElementTree as ET

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\ProgramData\Axis Communications\AXIS Companion\ApplicationSiteSettings.xml"
OUT = sys.argv[2] if len(sys.argv) > 2 else "site.accs"


def site_lines(group):
    lines = ["1.0"]
    # The local CameraList is what the desktop app shows; InternetSite > Cameras is the old cloud copy and can be stale.
    items = group.find("CameraList/List/Items")
    if items is None:
        return lines
    for cam in items:
        def g(tag):
            return cam.findtext(tag).strip()
        if ";" in g("Name"):
            raise SystemExit(f"Camera name contains ';': {g('Name')}")
        lines.append(f"{g('Address')}:{g('Port')};{g('VideoSourceIndex')};{g('SerialNumber')};{g('Name')}")
    return lines


groups = ET.parse(SRC).getroot().findall("group")
if not groups:
    raise SystemExit(f"No sites found in {SRC}")

for group in groups:
    name = group.get("name") or group.get("id")
    lines = site_lines(group)
    if len(lines) == 1:
        print(f"Skipping site '{name}': no cameras")
        continue
    out = OUT if len(groups) == 1 else re.sub(r'[\\/:*?"<>|]', "_", name) + ".accs"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"--- {out}: site '{name}', {len(lines) - 1} cameras")
    print("\n".join(lines))
