# Simone Lin — Academic CV Website

A minimalist, editorial academic website inspired by [pierregtch.github.io](https://pierregtch.github.io/). Built with [Astro](https://astro.build/) and structured for easy content updating.

## 🚀 Live Preview Right Now
A self-contained preview has already been compiled in this directory:
- Simply double click or open [`preview.html`](preview.html) in your browser!

---

## 🛠️ Project Structure

```
.
├── .github/workflows/deploy.yml # Automated GitHub Pages CI/CD workflow
├── astro.config.mjs             # Astro configuration
├── package.json                 # Node dependencies & build scripts
├── preview.html                 # Standalone compiled version (instant preview)
├── public/
│   └── favicon.svg              # Custom "SL." SVG icon
└── src/
    ├── data/
    │   └── cv.json              # 👈 ALL YOUR CV CONTENT IS CONFIGURED HERE!
    ├── layouts/
    │   └── BaseLayout.astro     # Core HTML shell & SEO tags
    ├── pages/
    │   └── index.astro          # Astro main page template
    └── styles/
        └── global.css           # Editorial typography & dark minimalist styles
```

---

## ✏️ How to Update Your Content

You don't need to touch complex HTML or CSS to add publications or experience. Simply edit **[`src/data/cv.json`](src/data/cv.json)**:
- **`research`**: Research lede, supervisor, affiliations.
- **`publications`**: Published papers, conference abstracts, and works in preparation.
- **`experience`**: Research positions and assistantships.
- **`education`**: Ph.D., M.Sc., B.Sc. degrees and thesis topics.
- **`projects`**: Technical and biomedical engineering projects with badges.
- **`skills`**: Categorized technical stacks (PyTorch, MATLAB, COMSOL, etc.).
- **`teaching` & `leadership`**: Courses taught and student lab leadership.
- **`references`**: PIs, titles, affiliations, and contact emails.

---

## 💻 Running Locally with Node.js & Astro

If you want to run Astro's live-reload development server locally:

1. **Install Node.js** (if not installed already):
   ```bash
   brew install node
   ```
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Start local dev server**:
   ```bash
   npm run dev
   ```
   Open `http://localhost:4321` in your browser.

---

## 🌐 Deploying for Free to GitHub Pages

This repository is already configured with an automated GitHub Action in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

1. Create a repository on GitHub (e.g. `CV` or `<username>.github.io`).
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial academic CV site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
3. On GitHub, go to **Settings > Pages**:
   - Under **Build and deployment > Source**, select **GitHub Actions**.
4. The deployment workflow will automatically run, build the Astro site, and publish your website!

