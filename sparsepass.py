from pathlib import Path
import plistlib
from pymobiledevice3.cli.cli_common import Command
from pymobiledevice3.exceptions import NoDeviceConnectedError, PyMobileDevice3Exception
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3.services.installation_proxy import InstallationProxyService
from sparserestore import backup, perform_restore

screentime_plist = "ScreenTimeAgent.plist"
disabled_plist = "disabled.plist"
modifyplist = dict("com.apple.ScreenTimeAgent": True, "com.apple.homed": True, "com.apple.familycircled": True)

def main():
    print("ScreenTimePassX v1, by connor walsh (dumbButSkilledDev)")
    print("creating custom backup....")
    print("[custom backup] setting screenTimeAgent.plist to empty contents, and disabling all screen time services...")
    back = backup.Backup(
        files=[
            backup.Directory("", "RootDomain"),
            backup.Directory(
                "",
                "SysContainerDomain-../../../../../../../../var/backup/var/mobile/Library/Preferences",
                owner=33,
                group=33,
            ),
            backup.ConcreteFile(
                "",
                f"SysContainerDomain-../../../../../../../../var/backup/var/mobile/Library/Preferences/{screentime_plist}",
                owner=33,
                group=33,
                contents=b"",
                inode=0,
            ),
            backup.Directory(
                "",
                "SysContainerDomain-../../../../../../../../var/backup/var/db/com/apple.xpc.launchd/",
                owner=33,
                group=33,
            ),
            backup.ConcreteFile(
                "",
                f"SysContainerDomain-../../../../../../../../var/backup/var/mobile/Library/Preferences/{disabled_plist}",
                owner=33,
                group=33,
                contents=plistlib.dumps(modifyplist),
                inode=0,
            ),
        ]
    )

    print("I AM NOT RESPONSIABLE FOR ANY DAMGE TO YOUR DEVICE, THOUGH EXTREAMLY UNLIKELY. IF YOU ARE IN A BOOTLOOP, RESTORE WITH ITUNES, THOUGH THIS WILL PROBALLY NOT HAPPEN.")
    w = input("Plug your device in (make sure u have itunes on windows), disable find my on the device, and press enter to start, ctrl-c to cancel")
    print("Restoring....")

    try:
        perform_restore(back, reboot=False)
    except PyMobileDevice3Exception as e:
        if "Find My" in str(e):
            print("please disable find my, this tool will exit, then run it again with findmy disabled.")
            exit(1)
        elif "crash_on_purpose" not in str(e):
            raise e