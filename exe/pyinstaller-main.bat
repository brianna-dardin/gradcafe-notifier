::ico file downloaded from http://www.iconarchive.com/show/mono-business-2-icons-by-custom-icon-design/coffee-icon.html
pyinstaller --noconfirm --log-level=WARN ^
    --onefile --windowed ^
	--version-file="versioninfo.py" ^
	--icon=files\Coffee.ICO ^
	::key removed
	--key= ^
    gradcafe.py