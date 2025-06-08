#!/bin/sh

# Bundling script
echo "✨ Starting pyinstaller command"

# python3 -m PyInstaller TheSimDiary.spec -y;
if ! python3 -m PyInstaller TheSimDiary.spec -y; then 
	echo "❌ Something went wrong creating executable with pyinstaller. Aborting"
	exit 1
fi

echo "✅ Done bundling the application using pyinstaller."
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
echo "🗑️ Removing existing .dmg files"
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/TheSimDiary.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/TheSimDiary.dmg" && rm "dist/TheSimDiary.dmg"


if [ ! -f "./src/TheSimDiaryLogo.icns" ]; then 
	echo "❌ Missing TheSimDiaryLogo.icns file. Aborting"
	exit 1
fi

echo "✨ Creating the dmg"
if ! create-dmg \
  --volname "TheSimDiary" \
  --volicon "src/TheSimDiaryLogo.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "TheSimDiary.app" 175 120 \
  --hide-extension "TheSimDiary.app" \
  --app-drop-link 425 120 \
  "dist/dmg/TheSimDiary.dmg" \
  "dist/dmg/"; then 
	echo "❌ Something went wrong while running create-dmg. See above error. Aborting"
	exit 1
fi 


echo "✅ Create dmg successfully. See dist/dmg."

echo "🧹 Cleaning up files"

rm -r dist/dmg/TheSimDiary.app
rm -f dist/*.dmg
