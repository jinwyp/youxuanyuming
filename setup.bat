@echo off
IF NOT EXIST venv (
    python -m venv venv
) ELSE (
    echo venv folder already exists, skipping creation...
)
call .\venv\Scripts\activate.bat

timeout /t 2 /nobreak 

python -m pip install --upgrade pip

@REM python -m pip install paddlepaddle-gpu==2.6.0.post120 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html

@REM python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

@REM pip install torch==2.3.0+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
@REM pip install torchaudio==2.3.0+cu118 --extra-index-url https://download.pytorch.org/whl/cu118
@REM pip install -r requirements.txt


pip install requests
pip install beautifulsoup4

