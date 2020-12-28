from pycaw.pycaw import AudioUtilities
import pythoncom

CHANGE_AMOUNT = 0.05


def get_applications():
    pythoncom.CoInitialize()
    applications = []
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process:
            process = {
                'name': session.Process.name(),
                'volume': volume.GetMasterVolume()
            }
            applications.append(process)
    return applications


def increment_application_volume(process_name):
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        interface = session.SimpleAudioVolume
        if session.Process and session.Process.name() == process_name:
            volume = interface.GetMasterVolume()
            volume = min(1.0, volume + CHANGE_AMOUNT)
            interface.SetMasterVolume(volume, None)
            return volume
    return "Did not find the application"


def decrement_application_volume(process_name):
    pythoncom.CoInitialize()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        interface = session.SimpleAudioVolume
        if session.Process and session.Process.name() == process_name:
            volume = interface.GetMasterVolume()
            volume = max(0.0, volume - CHANGE_AMOUNT)
            interface.SetMasterVolume(volume, None)
            return volume
    return "Did not find the application"
