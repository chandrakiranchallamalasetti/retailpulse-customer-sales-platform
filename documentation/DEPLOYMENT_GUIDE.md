# GitHub and Live Deployment Guide

## 1. Run locally

### Windows PowerShell
```powershell
cd retailpulse-customer-sales-platform
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_database.py
streamlit run app.py
```

### macOS/Linux
```bash
cd retailpulse-customer-sales-platform
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_database.py
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## 2. Add to GitHub with the command line
1. Create an empty GitHub repository named `retailpulse-customer-sales-platform`.
2. Do not initialize it with another README or license, because this folder already contains both.
3. In the project folder, run:

```bash
git init
git add .
git commit -m "Build RetailPulse customer sales analytics platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/retailpulse-customer-sales-platform.git
git push -u origin main
```

Alternative using GitHub CLI:
```bash
gh repo create retailpulse-customer-sales-platform --public --source=. --remote=origin --push
```

## 3. Deploy the Streamlit live demo
1. Sign in to Streamlit Community Cloud with GitHub.
2. Choose **Create app**.
3. Select your repository and the `main` branch.
4. Set the entrypoint to `app.py`.
5. Choose a subdomain and deploy.
6. Copy the resulting `https://...streamlit.app` URL.
7. Replace the placeholder live-demo URL in `README.md` and `docs/index.html`, then commit and push.

No secrets are required because the demo uses the included SQLite database.

## 4. Publish the project overview with GitHub Pages
1. Open the repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select branch `main` and folder `/docs`.
5. Save. The project site will be published from `docs/index.html`.
6. Copy the Pages URL and replace its placeholder in `README.md`.

## 5. Final portfolio cleanup
- Update `YOUR_USERNAME`, live-demo URL, and GitHub Pages URL.
- Add your name and exact modernization contributions without removing original team attribution.
- Add a dashboard screenshot under `docs/` and reference it in the README.
- Pin the repository on your GitHub profile.
- Add the live URL under the repository's **About** section.
