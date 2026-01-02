# How to Add GitHub Workflows

The workflows are ready locally but need to be added via GitHub web interface due to token permissions.

## Option 1: Create Token with Workflow Scope (Recommended)

1. Go to: https://github.com/settings/tokens/new
2. Name: `Health-Monitor-Workflows`
3. Select scopes:
   - ✅ `repo` (Full control)
   - ✅ `workflow` (Update GitHub Action workflows)
4. Generate and copy token
5. Run:
```bash
git push origin main
# Use token as password
```

## Option 2: Add Workflows via GitHub Web Interface

1. Go to: https://github.com/bhaskarm-dotcom/Health-Monitor
2. Click "Add file" > "Create new file"
3. For each workflow file:

### File 1: `.github/workflows/build.yml`
- Path: `.github/workflows/build.yml`
- Copy content from local file

### File 2: `.github/workflows/ci.yml`
- Path: `.github/workflows/ci.yml`
- Copy content from local file

### File 3: `.github/workflows/demo.yml`
- Path: `.github/workflows/demo.yml`
- Copy content from local file

### File 4: `.github/workflows/pages.yml`
- Path: `.github/workflows/pages.yml`
- Copy content from local file

## Quick Copy Commands

To view workflow file contents:
```bash
cat .github/workflows/build.yml
cat .github/workflows/ci.yml
cat .github/workflows/demo.yml
cat .github/workflows/pages.yml
```

