python -m pip install --upgrade pip
python -m pip install -e .
python run.py

#python -m pip install pynsist
python -m pip install pytest

dist/mu-editor_64bit.exeÇ…dev/sign.batÇé¿çs


# for Mac
uname -a
then sw_vers
bash package/install_osx.sh
pyenv install 3.6.5
pyenv versions
pyenv global 3.6.5
eval "$(pyenv init -)"
pip install --upgrade pip setuptools

echo $PATH
python --version
python -c "import struct; print(struct.calcsize('P') * 8)"
python -c "import sys; print(sys.executable)"
python -m pip --version
pip --version

pip install .[dev]
pip freeze

make clean

make macos
mkdir dist
zip -r -X dist/mu-editor.zip macOS/mu-editor.app
du -sk dist/

codesign -s "ARTEC CO.,LTD." -f mu-editor.app

