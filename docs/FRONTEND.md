# Frontend

Next.js dashboard using Supabase Google OAuth.

Initial authorized account: rabbaniindia2000@gmail.com

Setup:
1. Enable Google in Supabase Authentication Providers.
2. Configure Google OAuth credentials using the callback URL Supabase displays.
3. Add your frontend URL to Supabase Authentication URL Configuration.
4. Copy frontend/.env.example to frontend/.env.local and fill the public Supabase URL and publishable key.
5. cd frontend && npm install && npm run dev

The email allowlist is an MVP installation guard. Production authorization should move to database-backed roles rather than source-code email checks.
