echo "✨ Starting pyinstaller command"
pyinstaller index.py --onefile --windowed --add-data "src;src" --add-data "version.txt;." --add-data "data;data" --name TheSimDiary --icon "./src/TheSimDiaryLogo.ico"
echo "✅ Done bundling the application using pyinstaller."
echo "Windows compatible executable (.exe) created under ./dist/"