# Pushing this workspace to GitHub

The workspace is fully prepped and committed locally. To publish it as `srqt2/STUPIDMEI` (public), you need to run ONE of the two flows below. I could not finish this step automatically because creating a remote GitHub repo requires authenticating an HTTP session that the sandbox correctly refused to do on your behalf.

---

## Flow A (one-time setup, use `gh` CLI) — recommended

If `gh` is installed (a `winget install GitHub.cli` was kicked off in the background):

```powershell
cd "C:\Users\janua\Downloads\Equity Projects\ERFS"
gh auth login --web    # opens a browser, one-time
gh repo create STUPIDMEI --public --source=. --remote=origin --push
```

That single `gh repo create` line creates the GitHub repo, sets the remote, and pushes the existing commit. About 20 seconds total.

## Flow B (no `gh`, manual repo create) — fallback

1. Open https://github.com/new in your browser.
2. Repository name: `ERFS`. Visibility: **Public**. Do NOT add a README, gitignore, or license (the local repo already has them; tick nothing).
3. Click "Create repository". GitHub will show you the URL. Then:

```powershell
cd "C:\Users\janua\Downloads\Equity Projects\ERFS"
git remote add origin https://github.com/srqt2/STUPIDMEI.git
git push -u origin main
```

The push will use your existing git credentials (your stored PAT from IntelliDesk pushes works here too, same GitHub account).

---

## What's in the commit waiting to push

```
.claude/agents/
  alpha.md       3.0K
  charlie.md     3.2K
  delta.md       2.4K
  kilo.md        3.4K
.claude/settings.json    SessionStart hook (Node-based, cross-platform)
.claude/skills/.gitkeep  mount point for cloned finance-skills
.gitignore               excludes .claude/skills/finance-skills
README.md                full usage doc
```

The SessionStart hook has been tested locally: it clones `himself65/finance-skills` cleanly into `.claude/skills/finance-skills` in about 2 seconds.

## After it's pushed

Tell your friend to open https://github.com/srqt2/STUPIDMEI in their Claude web environment. The SessionStart hook fires on their first message, clones the skills, and they can run research immediately. Their output should be PDF/DOCX via the `anthropic-skills:pdf` and `anthropic-skills:docx` skills — they hand the file back to you, you decide whether to merge into IntelliDesk.
