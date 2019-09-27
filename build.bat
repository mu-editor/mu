
【カバレッジの個別チェックコマンド例】
pytest tests\interface\test_panes.py



python -m pip install --upgrade pip
python -m pip install -e .
python run.py

python -m pip install pynsist
python -m pip install pytest

make check
make win64
make win32

dist/mu-editor_64bit.exeにdev/sign.batを実行

##################################################
# for Mac

# Makefileのcheckを下記にする
#check: clean

uname -a
sw_vers
sudo bash package/install_osx.sh
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

sudo pip install .[dev]
pip freeze

sudo make clean

# Makefileのcheckの処理を修正する
sudo make macos
mkdir dist
zip -r -X dist/mu-editor.zip macOS/mu-editor.app
du -sk dist/

codesign -s "ARTEC CO.,LTD." -f mu-editor.app

