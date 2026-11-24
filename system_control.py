import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Initialize laptop volume controller
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def change_brightness(action):
    current = sbc.get_brightness()[0]

    if action == "increase":
        new_value = min(current + 5, 100)
    else:
        new_value = max(current - 5, 0)

    sbc.set_brightness(new_value)
    print("Brightness:", new_value)


def change_volume(action):
    current = volume.GetMasterVolumeLevelScalar()

    if action == "increase":
        new_value = min(current + 0.05, 1.0)
    else:
        new_value = max(current - 0.05, 0.0)

    volume.SetMasterVolumeLevelScalar(new_value, None)
    print("Volume:", round(new_value * 100), "%")