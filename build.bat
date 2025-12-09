@echo off
echo Building PlantUML Wrapper...
.venv\Scripts\pyinstaller --noconfirm --onefile --windowed ^
    --name "PlantUMLGenerator" ^
    --add-data "plantuml-1.2025.10.jar;." ^
    --collect-all customtkinter ^
    main.py
echo Build Complete. Check dist/ folder.
pause
