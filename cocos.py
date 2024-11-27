import sys
import os
import shutil
import zipfile

class cocos2dxPack:
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def is_apk_file(apkFile) -> bool:
        if apkFile.lower().endswith(".apk"):
            if os.path.exists(apkFile):
                return True
            else:
                print("apk file not exists\n")
                return False
        else:
            print(f"not valid apk file:${apkFile}\n")
        return False

    @staticmethod
    def delExistFiles() -> bool:
        try:
            print("start delete existing files\n")
            if os.path.exists("app/libs/"):
                shutil.rmtree("app/libs/")
            if os.path.exists("app/src/main/"):
                shutil.rmtree("app/src/main/")
            if os.path.exists("app/assets/"):
                shutil.rmtree("app/assets/")
            print("delete existing files succeed\n")
            return True
        except OSError as e:
            print(f"delete existing files err:{e}\n")
        return False

    @staticmethod
    def copyRes() -> bool:
        try:
            print("start copy mode files\n")
            shutil.copytree("cocos2dx_res/libs/", "app/libs/", dirs_exist_ok=True)
            shutil.copytree("cocos2dx_res/main/", "app/src/main/", dirs_exist_ok=True)
            if os.path.exists("app/build.gradle"):
                os.remove("app/build.gradle")
            shutil.copy("cocos2dx_res/build.gradle", "app/build.gradle")
            print("copy mode files succeed\n")
            return True
        except OSError as e:
            print(f"copy mode files err:{e}\n")
        return False

    @staticmethod
    def copy_so_files(src) -> bool:
        print(f"start copy so files from {src}\n")
        shutil.copytree(src, "app/libs/", dirs_exist_ok=True)
        for root, dirs, files in os.walk("app/libs"):
            # for dir_name in dirs:
            #     os.mkdir(f"app/libs/${dir_name}")
            for file_name in files:
                if file_name == "libmmkv.so":
                    file_path = os.path.join(root, file_name)
                    os.remove(file_path)
        print(f"copy so files succeed\n")
        return True

    @staticmethod
    def unzipApkFile(apkFile) -> bool:
        try:
            print(f"start unzip apk file ${apkFile}\n")
            if os.path.exists("tmp"):
                shutil.rmtree("tmp")
            os.mkdir("tmp")
            with zipfile.ZipFile(apkFile, "r") as zip_ref:
                zip_ref.extractall("tmp")
            print(f"unzip apk file ${apkFile} succeed\n")
            if os.path.exists("tmp/assets/"):
                shutil.copytree("tmp/assets/", "app/assets/", dirs_exist_ok=True)
            else:
                print("doesn't find assets folder!!!\n")
                return False
            if os.path.exists("tmp/libs"):
                return cocos2dxPack.copy_so_files("tmp/libs/")
            elif os.path.exists("tmp/lib"):
                return cocos2dxPack.copy_so_files("tmp/lib/")
            else: 
                print("doesn't find any so files!!! check it\n")
                return False
        except OSError as e:
            print(f"unzip apk file ${apkFile} err:{e}\n")
        finally:
            shutil.rmtree("tmp")
        return False

    @staticmethod
    def pack(apkFile):
        status = cocos2dxPack.is_apk_file(apkFile)
        if not status:
            return
        status = cocos2dxPack.delExistFiles()
        if not status:
            return
        status = cocos2dxPack.copyRes()
        if not status:
            return
        status = cocos2dxPack.unzipApkFile(apkFile)
        if not status:
            return
        print("project files ready!!!")
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        apkFile = sys.argv[1]
        print(f"apk file: ${apkFile}\n")
        cocos2dxPack.pack(apkFile)
    else:
        print("apk file not specified\n")