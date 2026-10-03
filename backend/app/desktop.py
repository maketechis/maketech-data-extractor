import os,subprocess,sys
from pathlib import Path
def backend_command(port=8000):return [sys.executable,"-m","uvicorn","app.main:app","--host","127.0.0.1","--port",str(port)]
def migrate():
    root=Path(__file__).resolve().parents[1];subprocess.run([sys.executable,"-m","alembic","upgrade","head"],cwd=root,check=True)
def serve():
    migrate();os.execv(sys.executable,backend_command())
if __name__=="__main__":serve()
