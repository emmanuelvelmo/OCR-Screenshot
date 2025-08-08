from cx_Freeze import setup, Executable

setup(name="OCR Screenshot", executables=[Executable("OCR Screenshot.py")], options={"build_exe": {"excludes": ["tkinter"]}})
