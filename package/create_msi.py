import os
import subprocess

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def BuildMsi(Name, BuildDir, WxsPath, WxsName):
    args = [os.path.join(THIS_DIR, "create_msi.bat"),
            Name,
            BuildDir,
            WxsPath,
            WxsName,
    ]
    p = subprocess.run(args)

if __name__ == "__main__":
    buildDir = os.path.join(THIS_DIR, "dist", "mu")
    wxsPath = os.path.join(THIS_DIR, "mu.wxs")
    wxsName = "mu"
    BuildMsi("Mu Editor", buildDir, wxsPath, wxsName)
