# Deploying WeldFatigue — Streamlit Community Cloud

Free deployment. No server to manage. Anyone with the link can access the app.

---

## Prerequisites

1. **GitHub account** — [github.com](https://github.com)
2. **Streamlit account** — [share.streamlit.io](https://share.streamlit.io) (sign in with GitHub)

---

## Step 1 — Push the project to GitHub

```bash
# From the project root (first time)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

If you already have a remote:

```bash
git add .
git commit -m "Add deployment config"
git push
```

---

## Step 2 — Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **"Create app"**
3. Select **"Deploy a public app from GitHub"** (or private if your repo is private)
4. Fill in the form:
   - **Repository**: `YOUR_USERNAME/YOUR_REPO_NAME`
   - **Branch**: `main`
   - **Main file path**: `app/main.py`
5. Click **"Deploy!"**

That's it. Streamlit will install all dependencies and launch the app.
It will give you a URL like: `https://your-app-name.streamlit.app`

---

## Notes

- **Sleep after inactivity**: the app sleeps if unused for a while — it wakes up in ~30 seconds when someone visits the link.
- **Private access**: you can restrict access to specific email addresses in the app settings on Streamlit Cloud (Settings → Sharing).
- **Updates**: every `git push` to `main` automatically redeploys the app.
