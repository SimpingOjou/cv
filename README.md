# Simone Lin — Academic CV Website

A minimalist, editorial academic website built with [Astro](https://astro.build/) and structured for easy content updating.

🔗 **Live Website**: [**https://simpingojou.github.io/cv/**](https://simpingojou.github.io/cv/)

---

## ⚡ Instant Local Preview (`preview.html`)

You can preview your website offline at any time without needing Node.js or any local dev server:

1. **Open in browser**: Simply double-click [`preview.html`](preview.html) (or right click ➔ *Open With* ➔ your favorite browser).
2. **Recompiling the preview after editing `src/data/cv.json`**:
   Whenever you edit your CV data in [`src/data/cv.json`](src/data/cv.json) or styles in [`src/styles/global.css`](src/styles/global.css), regenerate the preview with a single command:
   ```bash
   python3 build_preview.py
   ```
   This will immediately rebuild [`preview.html`](preview.html) with all your latest changes, PIs/supervisors boxes, and publications formatting.

---

## 🛠️ Project Structure

```
.
├── .github/workflows/deploy.yml # Automated GitHub Pages CI/CD workflow
├── astro.config.mjs             # Astro configuration (base: '/cv')
├── build_preview.py             # Script to regenerate preview.html
├── package.json                 # Node dependencies & build scripts
├── preview.html                 # Standalone compiled version (instant offline preview)
├── public/
│   └── favicon.svg              # Custom "SL." SVG icon
└── src/
    ├── data/
    │   └── cv.json              # 👈 All CV content is configured here
    ├── layouts/
    │   └── BaseLayout.astro     # Core HTML shell & SEO tags
    ├── pages/
    │   └── index.astro          # Astro main page template
    └── styles/
        └── global.css           # Editorial typography & dark minimalist styles
```

---

## ✏️ How to Update Your Content

You don't need to touch complex HTML or CSS to update publications or experience. Simply edit **[`src/data/cv.json`](src/data/cv.json)**:
- **`research`**: Research lede, supervisor, affiliations.
- **`publications`**: Published papers, conference abstracts, and works in preparation. *(Authors matching "Lin" will be automatically highlighted, while others like "Linz" remain unhighlighted)*.
- **`experience`**: Research positions and assistantships. Include `PI: <Name>` to automatically generate a highlighted PI badge box.
- **`education`**: Ph.D., M.Sc., B.Sc. degrees and thesis topics. Include `Supervisor: <Name>` or `Supervisors: <Names>` to automatically generate a supervisor badge box.
- **`projects`**: Technical and biomedical engineering projects with badges.
- **`skills`**: Categorized technical stacks (PyTorch, MATLAB, COMSOL, etc.).
- **`teaching` & `leadership`**: Courses taught and student lab leadership.
- **`references`**: PIs, titles, affiliations, and contact emails.

---

## 🌐 Deploying to GitHub Pages

The repository is configured to deploy automatically via GitHub Actions:

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Update CV"
   git push origin main
   ```
2. In your GitHub repository at **[github.com/SimpingOjou/cv](https://github.com/SimpingOjou/cv)**:
   - Navigate to **Settings** ➔ **Pages**.
   - Under **Build and deployment > Source**, ensure **GitHub Actions** is selected.
3. Your live site will automatically update at:
   👉 **[https://simpingojou.github.io/cv/](https://simpingojou.github.io/cv/)**

---

## 💻 Optional: Running Locally with Node.js & Astro

If you install Node.js and prefer running Astro's live-reload development server locally:

1. **Install Node.js** (via Homebrew on macOS):
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
   Open `http://localhost:4321/cv/` in your browser.
