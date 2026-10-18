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
        fig_html = ''
        if 'figure' in p and p['figure']:
            fig_data = p['figure']
            src = fig_data.get('src', '')
            caption = fig_data.get('caption', '')
            # For offline preview.html, embed as base64 so it works anywhere without a web server
            import os, base64
            img_path = os.path.join('public', src)
            if os.path.exists(img_path):
                with open(img_path, 'rb') as img_f:
                    b64_str = base64.b64encode(img_f.read()).decode('utf-8')
                    ext = src.split('.')[-1]
                    img_src = f'data:image/{ext};base64,{b64_str}'
            else:
                img_src = src
            caption_html = f'<p class="figure-caption u-mono">{caption}</p>' if caption else ''
            fig_html = f'''
            <div class="pub-figure" data-anima="fade-up">
              <img src="{img_src}" alt="{caption or p['title']}" loading="lazy" />
              {caption_html}
            </div>
            '''
        pubs_wip += f'''
        <article class="pub" data-anima="fade-up">
          <p class="year u-mono">{p["year"]}</p>
          <div class="main">
            <h3 class="title">{p["title"]}</h3>
            <p class="authors u-mono">{authors_html(p["authors"])}</p>
            <p class="venue">{p["venue"]}</p>
            {fig_html}
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
            <p class="meta u-mono">{e.get('institution', '')} · <span class="period">{e.get('period', '')}</span></p>
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
            <p class="meta u-mono">{ed.get('institution', '')} · <span class="period">{ed.get('period', '')}</span></p>
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
            <p class="meta u-mono">{pr.get('institution', '')} · <span class="period">{pr.get('year', '')}</span></p>
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
            <p class="meta u-mono">{t.get('venue', '')} · <span class="period">{t.get('year', '')}</span> ({t.get('duration', '')})</p>
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
            <p class="meta u-mono">{l.get('organization', '')} · <span class="period">{l.get('period', '')}</span></p>
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
            <p class="meta u-mono">{m.get('organizer', '')} · <span class="period">{m.get('year', '')}</span></p>
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

        <!-- Multi-Channel Biosignals Streaming Monitor (EEG + EMG + Kinematics + ECG) -->
        <div class="signals-monitor" aria-label="Simulated physiological signals over time">
          <div class="signals-header u-mono">
            <span class="signals-title">
              <span style="color: var(--dracula-pink);">◈</span> BIOSIGNAL TELEMETRY ACQUISITION
            </span>
            <span class="signals-status">
              <span class="status-dot"></span> LIVE · 1000 Hz
            </span>
          </div>

          <div class="signals-channels">
            <!-- Channel 1: EEG (Alpha/Theta rhythm) -->
            <div class="signal-row">
              <span class="signal-label sig-eeg u-mono">EEG (Cz)</span>
              <div class="signal-viewport">
                <div class="signal-stream sig-stream-eeg">
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M0 20 Q 15 8, 30 20 T 60 20 T 90 20 Q 105 5, 120 20 T 150 20 Q 165 32, 180 20 T 210 20 Q 225 10, 240 20 T 270 20 Q 285 30, 300 20 T 330 20 Q 345 6, 360 20 T 390 20 Q 405 32, 420 20 T 450 20 Q 465 12, 480 20 T 500 20" fill="none" stroke="var(--dracula-purple)" stroke-width="1.8" vector-effect="non-scaling-stroke"/>
                  </svg>
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M0 20 Q 15 8, 30 20 T 60 20 T 90 20 Q 105 5, 120 20 T 150 20 Q 165 32, 180 20 T 210 20 Q 225 10, 240 20 T 270 20 Q 285 30, 300 20 T 330 20 Q 345 6, 360 20 T 390 20 Q 405 32, 420 20 T 450 20 Q 465 12, 480 20 T 500 20" fill="none" stroke="var(--dracula-purple)" stroke-width="1.8" vector-effect="non-scaling-stroke"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Channel 2: EMG (Surface Muscle Burst) -->
            <div class="signal-row">
              <span class="signal-label sig-emg u-mono">EMG (TA)</span>
              <div class="signal-viewport">
                <div class="signal-stream sig-stream-emg">
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M 0 20 h 40 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 30 l 3 -5 l 3 6 l 3 -7 l 3 6 h 30 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 128 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 30 l 3 -5 l 3 6 l 3 -7 l 3 6 h 30 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 88" fill="none" stroke="var(--dracula-cyan)" stroke-width="1.4" vector-effect="non-scaling-stroke"/>
                  </svg>
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M 0 20 h 40 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 30 l 3 -5 l 3 6 l 3 -7 l 3 6 h 30 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 128 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 30 l 3 -5 l 3 6 l 3 -7 l 3 6 h 30 l 2 -12 l 3 16 l 2 -18 l 3 22 l 2 -15 l 3 12 l 2 -16 l 3 14 l 2 -10 l 3 7 h 88" fill="none" stroke="var(--dracula-cyan)" stroke-width="1.4" vector-effect="non-scaling-stroke"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Channel 3: Kinematics (Gait / Joint Angle) -->
            <div class="signal-row">
              <span class="signal-label sig-kin u-mono">KIN (Ankle)</span>
              <div class="signal-viewport">
                <div class="signal-stream sig-stream-kin">
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M0 26 C 30 26, 45 34, 75 32 C 105 30, 120 8, 150 8 C 175 8, 195 24, 220 26 C 240 28, 250 26, 250 26 C 280 26, 295 34, 325 32 C 355 30, 370 8, 400 8 C 425 8, 445 24, 470 26 C 490 28, 500 26, 500 26" fill="none" stroke="var(--dracula-green)" stroke-width="2" vector-effect="non-scaling-stroke"/>
                  </svg>
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M0 26 C 30 26, 45 34, 75 32 C 105 30, 120 8, 150 8 C 175 8, 195 24, 220 26 C 240 28, 250 26, 250 26 C 280 26, 295 34, 325 32 C 355 30, 370 8, 400 8 C 425 8, 445 24, 470 26 C 490 28, 500 26, 500 26" fill="none" stroke="var(--dracula-green)" stroke-width="2" vector-effect="non-scaling-stroke"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Channel 4: ECG (P-QRS-T complex) -->
            <div class="signal-row">
              <span class="signal-label sig-ecg u-mono">ECG (Lead II)</span>
              <div class="signal-viewport">
                <div class="signal-stream sig-stream-ecg">
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M 0 20 h 45 q 10 -5 20 0 h 25 l 4 3 l 6 -24 l 6 34 l 4 -13 h 25 q 15 -9 30 0 h 130 q 10 -5 20 0 h 25 l 4 3 l 6 -24 l 6 34 l 4 -13 h 25 q 15 -9 30 0 h 85" fill="none" stroke="var(--dracula-pink)" stroke-width="1.8" vector-effect="non-scaling-stroke"/>
                  </svg>
                  <svg viewBox="0 0 500 40" preserveAspectRatio="none">
                    <path d="M 0 20 h 45 q 10 -5 20 0 h 25 l 4 3 l 6 -24 l 6 34 l 4 -13 h 25 q 15 -9 30 0 h 130 q 10 -5 20 0 h 25 l 4 3 l 6 -24 l 6 34 l 4 -13 h 25 q 15 -9 30 0 h 85" fill="none" stroke="var(--dracula-pink)" stroke-width="1.8" vector-effect="non-scaling-stroke"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>
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
          <h3 class="group u-mono" data-anima="fade-in">{cv.get('publications_labels', {}).get('published', 'Published')}</h3>
          {pubs_published}

          <h3 class="group u-mono" data-anima="fade-in" style="margin-top: var(--space-6);">{cv.get('publications_labels', {}).get('in_progress', 'Conference Abstracts')}</h3>
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
