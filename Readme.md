// --- BASE URL ---
// Émulateur Android : http://10.0.2.2:8000
// iOS / Web / Real Device : http://127.0.0.1:8000 (ou ton IP locale)

// --- AUTHENTIFICATION (PUBLIC) ---
POST /api/auth/register
POST /api/token/pair   //pour le login
POST /api/token/refresh
POST /api/auth/forgot-password
POST /api/auth/reset-password

// --- GESTION PROFIL (PRIVATE - Nécessite Header Authorization: Bearer <token>) ---
GET    /api/auth/me
PATCH  /api/auth/me/update
POST   /api/auth/become-seller
POST   /api/auth/logout
DELETE /api/auth/me/delete