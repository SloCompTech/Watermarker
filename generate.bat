pyinstaller watermarker.py ^
--onefile ^
--name watermarker ^
--add-data fonts;fonts ^
--add-data LICENSE.md;LICENSE.md ^
--add-data LICENSE.pillow.md;LICENSE.pillow.md ^
--add-data README.md;README.md ^
--log-level DEBUG ^
--icon img/logo.ico

:: TODO add icon with --icon <ico file>