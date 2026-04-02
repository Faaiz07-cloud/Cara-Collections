# Navigate to project folder
Set-Location -Path "C:\Users\faaiz\Cara Collections\Cara"

# Activate virtual environment
& "C:\Users\faaiz\Cara Collections\venv\Scripts\Activate.ps1"

# Start Django server in a new window
Start-Process python -ArgumentList "manage.py runserver 8888" -WindowStyle Hidden

# Open browser automatically
Start-Process "http://127.0.0.1:8888"