import sys

def beep():
    try:
        if sys.platform.startswith('win'):
            import winsound
            frequency = 1000  # 1kHz
            duration = 300    # ms
            winsound.Beep(frequency, duration)
        else:
            # Beep on Linux/macOS
            print('\a', end='', flush=True)
    except Exception as e:
        # Optionally log or handle the error
        pass