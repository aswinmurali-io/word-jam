import os
import shutil
import kivy

blacklist = [
    r"api-ms-win-core-console-l1-1-0.dll",
    r"api-ms-win-core-datetime-l1-1-0.dll",
    r"api-ms-win-core-debug-l1-1-0.dll",
    r"api-ms-win-core-errorhandling-l1-1-0.dll",
    r"api-ms-win-core-file-l1-1-0.dll",
    r"api-ms-win-core-file-l1-2-0.dll",
    r"api-ms-win-core-file-l2-1-0.dll",
    r"api-ms-win-core-handle-l1-1-0.dll",
    r"api-ms-win-core-heap-l1-1-0.dll",
    r"api-ms-win-core-interlocked-l1-1-0.dll",
    r"api-ms-win-core-libraryloader-l1-1-0.dll",
    r"api-ms-win-core-localization-l1-2-0.dll",
    r"api-ms-win-core-memory-l1-1-0.dll",
    r"api-ms-win-core-namedpipe-l1-1-0.dll",
    r"api-ms-win-core-processenvironment-l1-1-0.dll",
    r"api-ms-win-core-processthreads-l1-1-0.dll",
    r"api-ms-win-core-processthreads-l1-1-1.dll",
    r"api-ms-win-core-profile-l1-1-0.dll",
    r"api-ms-win-core-rtlsupport-l1-1-0.dll",
    r"api-ms-win-core-string-l1-1-0.dll",
    r"api-ms-win-core-synch-l1-1-0.dll",
    r"api-ms-win-core-synch-l1-2-0.dll",
    r"api-ms-win-core-sysinfo-l1-1-0.dll",
    r"api-ms-win-core-timezone-l1-1-0.dll",
    r"api-ms-win-core-util-l1-1-0.dll",
    r"api-ms-win-crt-conio-l1-1-0.dll",
    r"api-ms-win-crt-convert-l1-1-0.dll",
    r"api-ms-win-crt-environment-l1-1-0.dll",
    r"api-ms-win-crt-filesystem-l1-1-0.dll",
    r"api-ms-win-crt-heap-l1-1-0.dll",
    r"api-ms-win-crt-locale-l1-1-0.dll",
    r"api-ms-win-crt-math-l1-1-0.dll",
    r"api-ms-win-crt-process-l1-1-0.dll",
    r"api-ms-win-crt-runtime-l1-1-0.dll",
    r"api-ms-win-crt-stdio-l1-1-0.dll",
    r"api-ms-win-crt-string-l1-1-0.dll",
    r"api-ms-win-crt-time-l1-1-0.dll",
    r"api-ms-win-crt-utility-l1-1-0.dll",
    r"comctl32.dll",
    r"libcrypto-1_1.dll",
    r"libfreetype-6.dll",
    r"libjpeg-8.dll",
    r"libmpg123-0.dll",
    r"libogg-0.dll",
    r"libpng16-16.dll",
    # r"libpng16.dll",
    r"libssl-1_1.dll",
    r"libtiff-5.dll",
    r"libvorbis-0.dll",
    r"libvorbisfile-3.dll",
    r"libwebp-5.dll",
    r"optimise_list.py",
    r"pyexpat.pyd",
    r"python37.dll",
    r"pythoncom37.dll",
    r"pywintypes37.dll",
    r"sdl.dll",
    r"sdl2_mixer.dll",
    r"sdl_image.dll",
    r"sdl_mixer.dll",
    r"sdl_ttf.dll",
    r"select.pyd",
    r"tcl86t.dll",
    r"tk86t.dll",
    r"ucrtbase.dll",
    r"unicodedata.pyd",
    r"vcruntime140.dll",
    r"win32api.pyd",
    r"win32file.pyd",
    r"zlib1.dll",
    r"_asyncio.pyd",
    r"_bz2.pyd",
    r"_decimal.pyd",
    r"_elementtree.pyd",
    r"_hashlib.pyd",
    r"_lzma.pyd",
    r"_msi.pyd",
    r"_multiprocessing.pyd",
    r"_overlapped.pyd",
    r"_socket.pyd",
    r"_ssl.pyd",
    r"_tkinter.pyd",
    r"_win32sysloader.pyd",
    r"kivy\core\audio\audio_sdl2.pyd",
    r"kivy\core\clipboard\_clipboard_sdl2.pyd",
    r"kivy\data\settings_kivy.json",
    r"kivy\data\fonts\DejaVuSans.ttf",
    r"kivy\data\images\background.jpg",
    r"kivy\data\images\cursor.png",
    r"kivy\data\images\defaultshape.png",
    r"kivy\data\images\image-loading.gif",
    r"kivy\data\images\testpattern.png",
    r"kivy\data\keyboards\azerty.json",
    r"kivy\data\keyboards\de.json",
    r"kivy\data\keyboards\de_CH.json",
    r"kivy\data\keyboards\en_US.json",
    r"kivy\data\keyboards\fr_CH.json",
    r"kivy\data\keyboards\qwerty.json",
    r"kivy\data\keyboards\qwertz.json",
    r"kivy\data\logo\kivy-icon-128.png",
    r"kivy\data\logo\kivy-icon-16.png",
    r"kivy\data\logo\kivy-icon-24.png",
    r"kivy\data\logo\kivy-icon-256.png",
    r"kivy\data\logo\kivy-icon-32.png",
    r"kivy\data\logo\kivy-icon-48.png",
    r"kivy\data\logo\kivy-icon-512.png",
    r"kivy\data\logo\kivy-icon-64.png",
    r"kivy\graphics\svg.pyd",
    r"kivy\lib\gstplayer\_gstplayer.pyd",
    r"PIL\_imaging.pyd",
    r"pygame\base.pyd",
    r"pygame\bufferproxy.pyd",
    r"pygame\cdrom.pyd",
    r"pygame\color.pyd",
    r"pygame\constants.pyd",
    r"pygame\display.pyd",
    r"pygame\draw.pyd",
    r"pygame\event.pyd",
    r"pygame\fastevent.pyd",
    r"pygame\font.pyd",
    r"pygame\image.pyd",
    r"pygame\imageext.pyd",
    r"pygame\joystick.pyd",
    r"pygame\key.pyd",
    r"pygame\mask.pyd",
    r"pygame\math.pyd",
    r"pygame\mixer.pyd",
    r"pygame\mixer_music.pyd",
    r"pygame\mouse.pyd",
    r"pygame\overlay.pyd",
    r"pygame\pixelarray.pyd",
    r"pygame\pixelcopy.pyd",
    r"pygame\rect.pyd",
    r"pygame\rwobject.pyd",
    r"pygame\scrap.pyd",
    r"pygame\surface.pyd",
    r"pygame\surflock.pyd",
    r"pygame\time.pyd",
    r"pygame\transform.pyd",
    r"pygame\_freetype.pyd",
    r"res\icon.ico",
    r"res\icon.png",
    r"res\presplash.png",
    r"src\common.py",
    r"src\config.py",
    r"src\grid.py",
    r"src\monitor.py",
    r"src\save.py",
    r"src\__init__.py",
    r"src\__main__.py",
    r"win32com\shell\shell.pyd",
]

copy_dir = [
    'src', 'res', 'lvl'
]

rm_dir = [
    'PIL', 'pygame', 'win32com'
]

shutil.copytree(kivy.__path__[0] + '/data/', 'main.dist/kivy/data')

for dir in copy_dir:
    try:
        shutil.copytree(dir, "main.dist/" + dir)
    except:
        print('Ignore ' + dir)

for file in blacklist:
    try:
        os.remove("main.dist/" + file)
    except:
        print('Ignore ' + file)

for dir in rm_dir:
    try:
        os.rmdir(dir)
    except:
        pass
