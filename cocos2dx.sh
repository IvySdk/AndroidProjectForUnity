#!/bin/bash

copy_so_files(){
    for FILE in $1/*; do
        if [ -d "$FILE" ]; then
            mkdir "app/libs/$FILE"
        elif [ -f "$FILE" ]; then
            if [ $(basename "$FILE") == "libmmkv.so" ]
                echo "ignore $FILE"
            else 
                cp FILE "app/libs/$FILE"
            fi
        fi
    done
}


echo "start setup cocos2dx pack mode"

if [ -f $1 ]; then
    echo "apk file $1 exist"
else 
    echo "apk file $1 doesn\'t exist\n"
    echo "any key to exit...\n"
    read -n 1
    exit 0
fi

echo "start delete existing files"
rm -r "app/libs/"
rm -r "app/src/main/"
rm -r "app/assets/"
echo "delete existing files succeed"

echo "start init pack"
cp -r "cocos2dx_res/libs/" "app/"
cp -r "cocos2dx_res/main/" "app/src/"
echo "init pack succeed"

echo "start parse apk file $1"
rm -r "cocos2dx_tmp"
mkdir "cocos2dx_tmp"
unzip $1 -d "cocos2dx_tmp"
cp -r "cocos2dx_tmp/app/assets/" "app/"

if [ -d "cocos2dx_tmp/lib" ]; then
    copy_so_files "cocos2dx_tmp/lib"
else 
    echo "dir lib doesn\'t exist in apk file $1, check for libs"
    if [ -d "cocos2dx_tmp/libs" ]; then
        copy_so_files "cocos2dx_tmp/libs"
    else 
        rm -r "cocos2dx_tmp"
        echo "had not find so files"
        echo "any key to exit...\n"
        read -n 1
        exit 0
    fi
fi
rm -r "cocos2dx_tmp"
echo "parse apk file $1 succeed"