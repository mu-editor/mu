REM %1 - PR number

git checkout master
git fetch upstream pull/%1/head:PR%1
git checkout PR%1
