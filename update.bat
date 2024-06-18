@ECHO OFF
if exist %UserProfile%\AppData\Local\Programs\Git\cmd\git.exe (
    git stash
    git pull --recurse-submodules
) else (
    ECHO "The folder must be cloned using Git.\nPlease install Git and clone the repository before using update."
)