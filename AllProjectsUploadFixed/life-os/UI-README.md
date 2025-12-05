Life OS — UI run instructions (quick)

1) Next.js web UI
cd frontend-next
npm install
npm run dev
Open http://localhost:3000

2) Electron
cd desktop-electron
npm install
npm start
(Note: Next dev should be running or Electron will open fallback)

3) Tauri (frontend only)
Open frontend-tauri/index.html in Tauri web build or point Tauri to this folder.

4) Mobile (Expo)
cd mobile-expo
expo start
Use Expo Go on device or simulator.

5) Studio (Notion-like)
cd studio-web
npm install
npm start
Open http://localhost:4000

General notes:
- All UIs expect backend at http://0.0.0.0:8000
- For Next dev, rewrites proxy to backend.
- For static UIs, run a static server from project root (python -m http.server or serve package)
