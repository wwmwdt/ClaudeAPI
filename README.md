# Claude API Wrapper

A minimal FastAPI service that proxies requests to the Anthropic Claude API.
Built as a learning project to walk through Git, GitHub, and cloud deployment.

## Run locally

```bash
# Create a virtual environment (optional but tidy)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Start the server
uvicorn app:app --reload
```

The server runs at http://localhost:8000. FastAPI gives you interactive docs at http://localhost:8000/docs for free.

## Test it

```bash
# Health check
curl http://localhost:8000/health

# Ask Claude something
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of New Zealand?"}'
```

## Deploy to the cloud

### Option A: Render (easiest)

1. Push this repo to GitHub
2. Go to render.com, create a new Web Service, connect your GitHub repo
3. Set the environment variable `ANTHROPIC_API_KEY` in the Render dashboard
4. Render auto-detects the Procfile and deploys

### Option B: Railway

1. Push this repo to GitHub
2. Go to railway.app, create a new project from your GitHub repo
3. Set `ANTHROPIC_API_KEY` in Railway's Variables tab
4. Railway auto-deploys on push

Either way, you'll get a public URL like `https://your-app.up.railway.app/ask` that you can hit from anywhere.

## Git cheat sheet (for the CVS-familiar)

| What you want to do         | CVS                  | Git                          |
|-----------------------------|----------------------|------------------------------|
| Get the repo                | `cvs checkout`       | `git clone <url>`            |
| See what's changed          | `cvs status`         | `git status`                 |
| Stage changes for commit    | (automatic)          | `git add .`                  |
| Commit                      | `cvs commit`         | `git commit -m "message"`   |
| Send to server              | (automatic on commit)| `git push`                   |
| Get latest from server      | `cvs update`         | `git pull`                   |
| Create a branch             | `cvs tag -b`         | `git checkout -b branch-name`|
| See history                 | `cvs log`            | `git log --oneline`          |

The big difference: in Git, commit is local. Push sends it to GitHub. This two-step flow means you can commit freely without affecting anyone else.

## What's in each file

- **app.py** - The actual API. ~45 lines of Python.
- **requirements.txt** - Python dependencies.
- **Procfile** - Tells the cloud platform how to start the app.
- **.github/workflows/deploy.yml** - GitHub Actions CI/CD pipeline (optional, Render/Railway handle deploy without it).
- **.gitignore** - Keeps junk out of the repo.
