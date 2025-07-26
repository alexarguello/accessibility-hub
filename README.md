# 📚 flatmap-docs-kit

**Turn any folder structure of Markdown docs and external links into a fully navigable, taggable, and contributor-friendly knowledge base.**

🗺️ Served as a navigable web resource with **docusaurus**, 
🗺️ Auto-generates **visual flatmaps** for overview and fast navigation,  
🧑‍💻 Smart **contributor dashboards** to make contributing easier than ever,  
💬 Supports **review flags**, **collaboration offers**, and more.

<p align="center">
  <img src="assets/flatmap-sample.png" alt="Flatmap example" width="45%" />
  <img src="assets/contributor-dashboard-sample.png" alt="Contributor dashboard" width="45%" />
</p>

**🎯 See it in action:** [Browse the full site map](https://lizeraes.github.io/flatmap-docs-kit/docs/full-sitemap/)

**Jump to:**
- [Setup Instructions](#-setup-instructions)
- [Deploy to GitHub Pages](#-deploy-to-github-pages)
- [Structure & Configuration](#-structure--configuration)
- [How to Use the Toolkit](#️-how-to-use-the-toolkit)
- [Extend or Customize](#-extend-or-customize)
- [Before Publishing](#️-before-publishing)
- [Coming Soon](#-coming-soon)

---

## 🚀 Setup Instructions

> 🧪 This tool uses [Docusaurus](https://docusaurus.io/) to serve and build the site.

1. **Install Docusaurus locally**:
   ```bash
   npm install
   npm run start
   ```

   This will bring up the website on `localhost:3000`
useful windows  commands: 
```bash
netstat -ano | findstr :3000
taskkill /pid 99999 /F


1. ```

2. _(optional)_ Add deployment config — **TODO: write instructions for deploying live**.

---

## 🚀 Deploy to GitHub Pages

1. **Update `docusaurus.config.js`**:
   ```js
   url: 'https://<your-github-username>.github.io',
   baseUrl: '/<repo-name>/',
   organizationName: '<your-github-username or org>',
   projectName: '<repo-name>',
   ```

2. **Update `.github/workflows/deploy.yml`**:
   If you changed the name of `educational-resource`folder, make sure to update
   ```yaml
   publish_dir: ./educational-resource/build
   ``` 

3. **Push changes**

4. **Create `gh-pages` branch** on GitHub from main (no ned to touch this branch ever after)

5. **Enable GitHub Actions permissions**:
   - Go to `Settings → Actions → General` (the settings of your repository)
   - Select `[x] Read and write permissions`

6. **Set Github Pages source***
   - Go to `Settings → Pages` (the settings of your repository)
   - Select `Source` : `GitHub Actions`

7. **Run deploy workflow** in Actions tab

Your site will be at: `https://<your-github-username>.github.io/<repo-name>/`

> ⚠️ GitHub Pages requires public repositories on free accounts.

---

## 🧩 Structure & Configuration

- **Docs live in**: `docs/`  
  Folder structure is converted to chapter structure in a sidebar
  At the moment it is prepopulated with (AI generated) sample data so you can explore how it all works.
  Organize however you like, supports endless subfolder levels.
  The flatmaps will be generated on each folder level, and if existing, the `_intro.md` file will be prepended to the flatmap as a kind of 'landing page' per folder.

- **Customable taggging system**: `docs/.template.md`
  Strongly recommended to define tags that can be later used for filtering, for visual signalling in the flatmap, for generating contributor / maintainer / ecosystem dashboards..
  Each Markdown file needs a header ('frontmatter') that is compliant with your tag template (see [`docs/.template.md`](docs/.template.md)).

- **Flatmap styling config**:  
  `flatmap-tools/flatmap-style.config.json`  
  Set the link to your github repo and publishing url.
  Set the desired flatmap depth (recommendation: not more than 3)
  Define per-tag colors, borders, icons, ...

- **Python utilities** (see `flatmap-tools/`):
  - `generate-mermaids.py`: Generate the visual flatmaps
  - `generate-contributor-pages.py`: Generate contributor dashboard + per-resource pages

---

## 🛠️ How to Use the Toolkit

### 🗺️ Flatmap Generator

**Command**:
```bash
python3 flatmap-tools/generate-mermaids.py
```

**What it does**:
- Scans all `docs/**` folders
- For each, creates a `index.md` with:
  - Mermaid map of clickable subfolders and files
  - Optional text from `_intro.md`
  - Visual styles based on tags
  - Legend generated from style config
- Also builds:
  - A full-site overview (full depth): `docs/full-sitemap.md`
  - Top-level summary map: `docs/index.md`

---

### 🙌 Contributor Dashboard

**Command**:
```bash
python3 flatmap-tools/generate-contributor-pages.py
```

**What it does**:
- Generates `docs/contributing/contribute-dashboard.md`  
  → Lists wanna-have articles (tagged as missing), invites collaboration, list resources that need review, shows recent publications (last 2 weeks)

- Generates `_contribute/*.md` files per missing article, with detailed context and contribution instruction, in order to make contributing frictionless.

**Templates for the dashboard and the detailed contribution pages live in**: `flatmap-tools/`

---

## 🧪 Extend or Customize

All logic lives in the [`flatmap-tools/`](./flatmap-tools) folder:

- 🧠 Add your own dashboards
- 🧩 Extend metadata parsing
- 🎨 Add new styles via `flatmap-style.config.json`

---

## 🗑️ Before Publishing

When you're done setting up:

1. **Delete this README**
    Because it is aimed at the maintainer, not the actual resource users or contributors
2. **Replace with [`educational-resource/README.md`](educational-resource/README.md)**
   - This currently contains usage and contribution guidelines for an actually published resource
   - Update it to fit your resource and target audience

---

## 🧭 Coming Soon

- **Maintainer Dashboard**: overdue resources, broken links, tag consistency
- **Feature Ecosystem Dashboard**: (beyond articles) to show gaps in the ecosystem that would need implementing
