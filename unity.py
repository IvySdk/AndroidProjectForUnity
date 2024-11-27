import sys
import os
import shutil
import zipfile


class UnityPack:

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
            if os.path.exists("libs/"):
                shutil.rmtree("libs/")
            if os.path.exists("src/"):
                shutil.rmtree("src/")
            print("delete existing files succeed\n")
            return True
        except OSError as e:
            print(f"delete existing files err:{e}\n")
        return False

    @staticmethod
    def copyRes() -> bool:
        try:
            print("start copy mode files\n")
            shutil.copytree("unity_res/src/", "src/", dirs_exist_ok=True)
            if os.path.exists("proguard-unity.txt"):
                os.remove("proguard-unity.txt")
            shutil.copy("unity_res/proguard-unity.txt", "proguard-unity.txt")
            if os.path.exists("unity_res/libs/unity-classes.jar"):
                shutil.copytree("unity_res/libs/", "libs", dirs_exist_ok=True)
                print("unity-classes.jar found")
            else:
                print("The required unity-classes.jar was not found!!!")
                return False          
            print("copy mode files succeed\n")
            return True
        except OSError as e:
            print(f"copy mode files err:{e}\n")
        return False

    @staticmethod
    def copy_so_files(src) -> bool:
        print(f"start copy so files from {src}\n")
        shutil.copytree(src, "src/main/jniLibs", dirs_exist_ok=True)
        for root, dirs, files in os.walk("src/main/jniLibs"):
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
                shutil.copytree("tmp/assets/", "src/main/assets/", dirs_exist_ok=True)
            else:
                print("doesn't find assets folder!!!\n")
                return False
            if os.path.exists("tmp/libs"):
                return UnityPack.copy_so_files("tmp/libs/")
            elif os.path.exists("tmp/lib"):
                return UnityPack.copy_so_files("tmp/lib/")
            else: 
                print("doesn't find any so files!!! check it\n")
                return False
        except OSError as e:
            print(f"unzip apk file ${apkFile} err:{e}\n")
        finally:
            shutil.rmtree("tmp")
            pass
        return False

    @staticmethod
    def pack(apkFile):
        status = UnityPack.is_apk_file(apkFile)
        if not status:
            return
        status = UnityPack.delExistFiles()
        if not status:
            return
        status = UnityPack.copyRes()
        if not status:
            return
        status = UnityPack.unzipApkFile(apkFile)
        if not status:
            return
        print("project files ready!!!")
        pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        apkFile = sys.argv[1]
        print(f"apk file: ${apkFile}\n")
        UnityPack.pack(apkFile)
    else:
        print("apk file not specified\n")
    pass