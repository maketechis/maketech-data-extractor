use std::process::{Child,Command};
use std::sync::Mutex;
use tauri::{Manager,RunEvent};
struct Backend(Mutex<Option<Child>>);
fn backend_path(app:&tauri::AppHandle)->std::path::PathBuf{
    let mut p=app.path().resource_dir().expect("resource dir");p.push("bin");p.push(if cfg!(windows){"maketech-backend.exe"}else{"maketech-backend"});p
}
#[cfg_attr(mobile,tauri::mobile_entry_point)]
pub fn run(){
    tauri::Builder::default().plugin(tauri_plugin_shell::init()).setup(|app|{
        let path=backend_path(&app.handle());let child=Command::new(path).env("ENVIRONMENT","desktop").spawn().expect("start local backend");
        app.manage(Backend(Mutex::new(Some(child))));Ok(())
    }).build(tauri::generate_context!()).expect("build app").run(|app,event|{
        if matches!(event,RunEvent::ExitRequested{..}|RunEvent::Exit){if let Some(state)=app.try_state::<Backend>(){if let Some(mut child)=state.0.lock().unwrap().take(){let _=child.kill();}}}
    });
}
