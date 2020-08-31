rmdir /s/q  %LOCALAPPDATA%\python\mu\mu_venv
del %LOCALAPPDATA%\python\mu\Logs\mu.log
del mu\wheels\*.whl
.venv\scripts\python -mmu
PAUSE