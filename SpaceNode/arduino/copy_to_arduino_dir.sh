#/bin/sh
rm -rf ~/Dropbox/Arduino/libraries/SpaceNode/
cp -r SpaceNode ~/Dropbox/Arduino/libraries/SpaceNode
# Replace the timer directory
rm -rf ~/Dropbox/Arduino/libraries/TimeCheck/
cp -r SpaceNode/Required\ Libraries/TimeCheck ~/Dropbox/Arduino/libraries/TimeCheck
