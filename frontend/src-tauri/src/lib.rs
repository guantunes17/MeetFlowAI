use tauri::Manager;
use tauri_plugin_shell::ShellExt;

struct BackendProcess(std::sync::Mutex<tauri_plugin_shell::process::CommandChild>);

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            let app_data_dir = app
                .path()
                .app_local_data_dir()
                .expect("failed to resolve app local data directory");
            std::fs::create_dir_all(&app_data_dir).expect("failed to create app local data directory");

            let db_path = app_data_dir.join("meetflow.db");
            let app_secret_path = app_data_dir.join("app_secret.txt");

            let sidecar = app
                .shell()
                .sidecar("meetflow-backend")
                .expect("meetflow-backend binary not found in bundle");
            let (_rx, child) = sidecar
                .env("MEETFLOW_DB_PATH", db_path.to_string_lossy().to_string())
                .env("MEETFLOW_APP_SECRET_PATH", app_secret_path.to_string_lossy().to_string())
                .spawn()
                .expect("failed to spawn meetflow-backend");
            app.manage(BackendProcess(std::sync::Mutex::new(child)));
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
