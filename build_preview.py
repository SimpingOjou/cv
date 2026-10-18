import json
import re

def build():
    cv = json.load(open('src/data/cv.json'))
    css = open('src/styles/global.css').read()

    def is_me(author):
        return bool(re.search(r'\bLin\b', author, re.IGNORECASE))

    def authors_html(authors):
        return ', '.join([f'<span class="me">{a}</span>' if is_me(a) else f'<span>{a}</span>' for a in authors])

    def format_details(text):
        if not text:
            return '', ''
        match = re.search(r'(.*?)(?:(?:\. |\s+|^)(PIs?|Supervisors?):\s*([^.]+?)(?:\.|$))', text, re.IGNORECASE)
        if match:
            body = match.group(1).strip()
            role = match.group(2)
            names = match.group(3).strip()
            return body, f'{role}: {names}'
        return text, ''

    pubs_published = ''
    for p in cv['publications'].get('published', []):
        doi_link = f'<ul class="links u-mono" style="margin-top:0.5rem;"><li><a href="{p["doi"]}" target="_blank" rel="noopener">DOI ↗</a></li></ul>' if 'doi' in p else ''
        pubs_published += f'''
        <article class="pub" data-anima="fade-up">
          <p class="year u-mono">{p["year"]}</p>
          <div class="main">
            <h3 class="title">{p["title"]}</h3>
            <p class="authors u-mono">{authors_html(p["authors"])}</p>
            <p class="venue">{p["venue"]}</p>
            {doi_link}
          </div>
        </article>
        '''

    pubs_wip = ''
    for p in cv['publications'].get('in_progress', []):
        pubs_wip += f'''
        <article class="pub" data-anima="fade-up">
          <p class="year u-mono">{p["year"]}</p>
          <div class="main">
            <h3 class="title">{p["title"]}</h3>
            <p class="authors u-mono">{authors_html(p["authors"])}</p>
            <p class="venue">{p["venue"]}</p>
          </div>
        </article>
        '''

    exp_html = ''
    for e in cv.get('experience', []):
        body, supervisor = format_details(e.get('details', ''))
        body_p = f'<p class="detail">{body}</p>' if body else ''
        sup_div = f'<div class="supervisor-badge u-mono"><span class="supervisor-icon">◈</span><span>{supervisor}</span></div>' if supervisor else ''
        exp_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{e["role"]}</h3>
            <p class="meta u-mono">{e.get('institution', '')} · {e.get('period', '')}</p>
          </div>
          {body_p}
          {sup_div}
        </article>
        '''

    edu_html = ''
    for ed in cv.get('education', []):
        body, supervisor = format_details(ed.get('details', ''))
        body_p = f'<p class="detail">{body}</p>' if body else ''
        sup_div = f'<div class="supervisor-badge u-mono"><span class="supervisor-icon">◈</span><span>{supervisor}</span></div>' if supervisor else ''
        edu_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{ed["degree"]}</h3>
            <p class="meta u-mono">{ed.get('institution', '')} · {ed.get('period', '')}</p>
          </div>
          {body_p}
          {sup_div}
        </article>
        '''

    proj_html = ''
    for pr in cv.get('projects', []):
        tags = ''.join([f'<span class="tag">{t}</span>' for t in pr.get('tags', [])])
        proj_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{pr["title"]}</h3>
            <p class="meta u-mono">{pr.get('institution', '')} · {pr.get('year', '')}</p>
          </div>
          <div class="tags">{tags}</div>
        </article>
        '''

    skills_html = ''
    for sk in cv.get('skills', []):
        tags = ''.join([f'<span class="tag">{item}</span>' for item in sk.get('items', [])])
        skills_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{sk["category"]}</h3>
          </div>
          <div class="tags">{tags}</div>
        </article>
        '''

    teach_html = ''
    for t in cv.get('teaching', []):
        teach_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{t["title"]}</h3>
            <p class="meta u-mono">{t.get('venue', '')} · {t.get('year', '')} ({t.get('duration', '')})</p>
          </div>
        </article>
        '''

    lead_html = ''
    for l in cv.get('leadership', []):
        det = f'<p class="detail">{l["details"]}</p>' if 'details' in l else ''
        lead_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{l["role"]}</h3>
            <p class="meta u-mono">{l.get('organization', '')} · {l.get('period', '')}</p>
          </div>
          {det}
        </article>
        '''

    meet_html = ''
    for m in cv.get('meetings', []):
        meet_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{m["title"]}</h3>
            <p class="meta u-mono">{m.get('organizer', '')} · {m.get('year', '')}</p>
          </div>
        </article>
        '''

    ref_html = ''
    for r in cv.get('references', []):
        ref_html += f'''
        <article class="entry" data-anima="fade-up">
          <div class="head">
            <h3 class="title">{r["name"]}</h3>
            <p class="meta u-mono">{r.get('title', '')}</p>
          </div>
          <p class="detail">{r.get('institution', '')}</p>
          <p class="detail u-mono" style="margin-top:0.25rem;">
            <a href="mailto:{r.get('email', '')}" style="color:var(--color-accent);">{r.get('email', '')}</a>
          </p>
        </article>
        '''

    facts_html = ''
    for f in cv['research'].get('facts', []):
        facts_html += f'''
        <div>
          <dt>{f["label"]}</dt>
          <dd>{f["value"]}</dd>
        </div>
        '''

    socials = cv.get('socials', {})
    social_links_html = ''
    if 'scholar' in socials and socials['scholar']:
        social_links_html += f'<li><a href="{socials["scholar"]}" target="_blank" rel="noopener">Scholar ↗</a></li>'
    if 'github' in socials and socials['github']:
        social_links_html += f'<li><a href="{socials["github"]}" target="_blank" rel="noopener">GitHub ↗</a></li>'
    if 'linkedin' in socials and socials['linkedin']:
        social_links_html += f'<li><a href="{socials["linkedin"]}" target="_blank" rel="noopener">LinkedIn ↗</a></li>'
    if 'orcid' in socials and socials['orcid']:
        social_links_html += f'<li><a href="{socials["orcid"]}" target="_blank" rel="noopener">ORCID ↗</a></li>'

    html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" type="image/svg+xml" href="favicon.svg" />
    <title>{cv.get('name', 'CV')} — {cv.get('role', '')}</title>
    <meta name="description" content="{cv.get('research', {}).get('statement', '')}" />
    <meta name="theme-color" content="#0b0b0d" />
    <style>
{css}
    </style>
  </head>
  <body>
    <div class="grain" aria-hidden="true"></div>
    
    <nav class="nav" aria-label="Primary">
      <div class="nav-inner u-container">
        <a class="brand" href="#top" aria-label="Back to top">
          {cv.get('initials', 'SL')}<span class="dot">.</span>
        </a>
        <ul class="links u-mono">
          <li><a href="#research">Research</a></li>
          <li><a href="#publications">Publications</a></li>
          <li><a href="#experience">Experience</a></li>
          <li><a href="#education">Education</a></li>
          <li><a href="#projects">Projects</a></li>
          <li><a href="#skills">Skills</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </div>
    </nav>

    <main id="main">
      <header id="top" class="hero u-container">
        <p class="eyebrow u-mono" data-anima="fade-in">{cv.get('eyebrow', '')}</p>
        <h1 class="name" data-anima="split-lines">{cv.get('name', '')}</h1>
        <div class="meta">
          <p class="role u-mono" data-anima="fade-up">{cv.get('role', '')}</p>
          <p class="tagline" data-anima="fade-up">{cv.get('tagline', '')}</p>
        </div>

        <div class="signal" aria-hidden="true">
          <svg class="signal-svg" viewBox="0 0 745 80" preserveAspectRatio="none" role="presentation">
            <path d="M0 40 h40 l10 -15 l8 30 l12 -45 l10 32 l12 -12 h70 l12 -28 l10 54 l10 -42 l12 20 h60 l15 -25 l10 46 l10 -38 l12 18 h70 l12 22 l10 -46 l10 40 l12 -18 h60 l14 -30 l10 58 l11 -46 l11 20 h60 l10 -18 l10 34 l12 -28 l10 14 h60" vector-effect="non-scaling-stroke"></path>
          </svg>
        </div>
      </header>

      <section id="research" class="section u-container" aria-labelledby="research-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">01</span>
          <h2 id="research-heading" class="section-title" data-anima="split-lines">Research</h2>
        </div>
        <div class="section-body">
          <p class="lede" data-anima="fade-up">{cv.get('research', {}).get('statement', '')}</p>
          <dl class="facts u-mono" data-anima="fade-up">
            {facts_html}
          </dl>
        </div>
      </section>

      <section id="publications" class="section u-container" aria-labelledby="publications-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">02</span>
          <h2 id="publications-heading" class="section-title" data-anima="split-lines">Publications</h2>
        </div>
        <div class="section-body">
          <h3 class="group u-mono" data-anima="fade-in">Peer-Reviewed & Conference Abstracts</h3>
          {pubs_published}

          <h3 class="group u-mono" data-anima="fade-in" style="margin-top: var(--space-6);">Work in Progress</h3>
          {pubs_wip}
        </div>
      </section>

      <section id="experience" class="section u-container" aria-labelledby="experience-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">03</span>
          <h2 id="experience-heading" class="section-title" data-anima="split-lines">Research Experience</h2>
        </div>
        <div class="section-body">
          {exp_html}
        </div>
      </section>

      <section id="education" class="section u-container" aria-labelledby="education-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">04</span>
          <h2 id="education-heading" class="section-title" data-anima="split-lines">Education</h2>
        </div>
        <div class="section-body">
          {edu_html}
        </div>
      </section>

      <section id="projects" class="section u-container" aria-labelledby="projects-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">05</span>
          <h2 id="projects-heading" class="section-title" data-anima="split-lines">Selected Projects</h2>
        </div>
        <div class="section-body">
          {proj_html}
        </div>
      </section>

      <section id="skills" class="section u-container" aria-labelledby="skills-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">06</span>
          <h2 id="skills-heading" class="section-title" data-anima="split-lines">Skills & Stack</h2>
        </div>
        <div class="section-body">
          {skills_html}
        </div>
      </section>

      <section id="teaching" class="section u-container" aria-labelledby="teaching-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">07</span>
          <h2 id="teaching-heading" class="section-title" data-anima="split-lines">Teaching & Outreach</h2>
        </div>
        <div class="section-body">
          <h3 class="group u-mono" data-anima="fade-in">Teaching</h3>
          {teach_html}

          <h3 class="group u-mono" data-anima="fade-in" style="margin-top: var(--space-6);">Community Leadership</h3>
          {lead_html}

          <h3 class="group u-mono" data-anima="fade-in" style="margin-top: var(--space-6);">Conferences & Meetings</h3>
          {meet_html}
        </div>
      </section>

      <section id="references" class="section u-container" aria-labelledby="references-heading">
        <div class="section-head">
          <span class="section-index u-mono" aria-hidden="true">08</span>
          <h2 id="references-heading" class="section-title" data-anima="split-lines">Academic References</h2>
        </div>
        <div class="section-body">
          {ref_html}
        </div>
      </section>
    </main>

    <footer id="contact" class="footer u-container">
      <div class="footer-top">
        <a class="mail" href="mailto:{cv.get('email', '')}" data-anima="fade-up">{cv.get('email', '')}</a>
        <ul class="links u-mono">
          {social_links_html}
        </ul>
      </div>
      <p class="colophon u-mono">© 2026 {cv.get('name', '')} · Built with Astro</p>
    </footer>

    <script>
      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            entry.target.classList.add('animated');
          }}
        }});
      }}, {{ threshold: 0.1 }});

      document.querySelectorAll('[data-anima]').forEach(el => observer.observe(el));
    </script>
  </body>
</html>
'''

    with open('preview.html', 'w') as f:
        f.write(html)
    print('preview.html successfully rebuilt!')

if __name__ == '__main__':
    build()
