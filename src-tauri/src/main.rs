#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use std::thread;
use std::path::PathBuf;

fn main() {
  // Spawn Python backend in a background thread when the app starts.
  thread::spawn(|| {
    // Determine the project root directory (parent of src-tauri).
    // If running from the executable, go up from the binary path to find the project root.
    let project_root = std::env::current_exe()
      .ok()
      .and_then(|exe| {
        // exe is typically at target/debug/face-recog-gallery.exe or similar
        // We need to go up several directories to reach the project root
        let mut path = exe;
        // Go up until we find a directory with 'backend' and '.venv' folders
        for _ in 0..10 {
          path = path.parent()?.to_path_buf();
          if path.join("backend").exists() && path.join(".venv").exists() {
            return Some(path);
          }
        }
        None
      })
      .unwrap_or_else(|| PathBuf::from("."));

    // Construct the path to the venv Python executable
    #[cfg(target_os = "windows")]
    let python_exe = project_root.join(".venv\\Scripts\\python.exe");
    #[cfg(not(target_os = "windows"))]
    let python_exe = project_root.join(".venv/bin/python");

    // Spawn the backend process
    let _ = Command::new(&python_exe)
      .args(&["-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"])
      .current_dir(&project_root)
      .spawn();
  });

  tauri::Builder::default()
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
