from app.config import Settings
def test_desktop_environment_supported():assert Settings(environment="desktop").environment=="desktop"
