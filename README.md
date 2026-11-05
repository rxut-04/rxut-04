<!-- ============================================================ -->
<!--                      BANNER (LIGHT / DARK)                    -->
<!-- ============================================================ -->
<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,6,18&height=220&section=header&text=&fontSize=0&animation=fadeIn">
    <source media="(prefers-color-scheme: light)" srcset="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,12&height=220&section=header&text=&fontSize=0&animation=fadeIn">
    <img alt="Banner" src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,6,18&height=220&section=header&text=&fontSize=0&animation=fadeIn" width="100%">
  </picture>
</div>

<!-- ============================================================ -->
<!--                            TITLE                              -->
<!-- ============================================================ -->
<h1 align="center">Hey there, I'm [Om Raut] <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="32" alt="wave"></h1>

<!-- ============================================================ -->
<!--                        TYPING ANIMATION                       -->
<!-- ============================================================ -->
<div align="center">
  <a href="https://github.com/rxut-04">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=FF69B4&center=true&vCenter=true&width=650&lines=Final-Year+IT+Student;Full-Stack+%7C+Computer+Vision+%7C+Hardware;Building+things+that+actually+impress;Turning+ideas+into+shipped+projects" alt="Typing SVG" />
  </a>
</div>

<br>

<!-- ============================================================ -->
<!--                            BADGES                             -->
<!-- ============================================================ -->
<div align="center">
  <a href="https://github.com/rxut-04?tab=followers">
    <img src="https://img.shields.io/github/followers/rxut-04?style=for-the-badge&logo=github&logoColor=white&labelColor=1a1a1a&color=FF69B4" alt="Followers" />
  </a>
  <a href="https://github.com/rxut-04?tab=repositories">
    <img src="https://img.shields.io/github/stars/rxut-04?style=for-the-badge&logo=starship&logoColor=white&labelColor=1a1a1a&color=FF69B4" alt="Stars" />
  </a>
  <img src="https://komarev.com/ghpvc/?username=rxut-04&style=for-the-badge&label=PROFILE+VIEWS&labelColor=1a1a1a&color=FF69B4" alt="Profile Views" />
</div>

<br>

<!-- ============================================================ -->
<!--                           ABOUT ME                            -->
<!-- ============================================================ -->
<h2 align="center">✨ About Me</h2>

<table align="center" width="100%" border="0">
  <tr>
    <td width="65%" valign="middle">
      <p>👋 Hi! I'm <b>[Om Raut]</b>, a final-year <b>Information Technology</b> student who loves building ambitious projects.</p>
      <p>🔭 Currently working on <b>[Your Current Project]</b></p>
      <p>🌱 Currently learning <b>[Your Current Learning]</b></p>
      <p>⚡ I work across <b>full-stack web</b>, <b>computer vision</b>, <b>hardware</b>, and <b>mobile</b></p>
      <p>🤝 Open to collaborating on <b>[Your Interests]</b></p>
      <p>💬 Ask me about <b>[Your Topics]</b></p>
      <p>🎯 Fun fact: <b>[Your Fun Fact]</b></p>
    </td>
    <td width="35%" align="center" valign="middle">
      <img src="[YOUR_IMAGE_OR_GIF_URL]" alt="About me" width="100%" style="border-radius:16px;" />
    </td>
  </tr>
</table>

<br>

<!-- ============================================================ -->
<!--                           TECH STACK                          -->
<!-- ============================================================ -->
<h2 align="center">🛠️ Tech Stack</h2>

<div align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=html,css,js,ts,react,nodejs,express,java,python,flutter,dart,mongodb,mysql,git,github,linux,raspberrypi,opencv&perline=9" alt="Tech Stack" />
  </a>
</div>

<br>

<!-- ============================================================ -->
<!--                        GITHUB STATS                           -->
<!-- ============================================================ -->
<h2 align="center">📊 GitHub Stats</h2>

<div align="center">
  <img src="https://streak-stats.demolab.com?user=rxut-04&theme=transparent&hide_border=true&stroke=F8BBD0&ring=FF69B4&fire=EF93C4&currStreakNum=FF69B4&sideNums=FF69B4&currStreakLabel=EF93C4&sideLabels=F8BBD0&dates=F8BBD0&background=00000000" alt="GitHub Streak" width="85%" />
</div>

<br>

<div align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=rxut-04&bg_color=00000000&color=FF69B4&line=EF93C4&point=F8BBD0&area=true&area_color=F8BBD0&title_color=FF69B4&hide_border=true&radius=10" alt="Activity Graph" width="95%" />
</div>

<br>

<!-- ============================================================ -->
<!--                       CONTRIBUTION SNAKE                      -->
<!-- ============================================================ -->
<h2 align="center">🐍 Contribution Snake</h2>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rxut-04/rxut-04/output/github-snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rxut-04/rxut-04/output/github-snake.svg">
    <img alt="Contribution Snake" src="https://raw.githubusercontent.com/rxut-04/rxut-04/output/github-snake.svg" width="95%">
  </picture>
</div>

<!--
  GITHUB ACTION SETUP (Platane/snk)
  Create the file: .github/workflows/snake.yml

  name: Generate Snake
  on:
    schedule:
      - cron: "0 0 * * *"
    workflow_dispatch:
    push:
      branches: [main]
  permissions:
    contents: write
  jobs:
    generate:
      runs-on: ubuntu-latest
      steps:
        - uses: Platane/snk/svg-only@v3
          with:
            github_user_name: ${{ github.repository_owner }}
            outputs: |
              dist/github-snake.svg
              dist/github-snake-dark.svg?palette=github-dark
        - uses: crazy-max/ghaction-github-pages@v3.1.0
          with:
            target_branch: output
            build_dir: dist
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  Then: Actions tab → "Generate Snake" → Run workflow (first run only).
-->

<br>

<!-- ============================================================ -->
<!--                            CONNECT                            -->
<!-- ============================================================ -->
<h2 align="center">🤝 Let's Connect</h2>

<div align="center">
  <a href="https://linkedin.com/in/[LINKEDIN_USERNAME]">
    <img src="https://img.shields.io/badge/LinkedIn-FF69B4?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://x.com/[X_USERNAME]">
    <img src="https://img.shields.io/badge/X-FF69B4?style=for-the-badge&logo=x&logoColor=white" alt="X" />
  </a>
  <a href="https://instagram.com/[INSTAGRAM_USERNAME]">
    <img src="https://img.shields.io/badge/Instagram-FF69B4?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
  </a>
  <a href="https://tiktok.com/@[TIKTOK_USERNAME]">
    <img src="https://img.shields.io/badge/TikTok-FF69B4?style=for-the-badge&logo=tiktok&logoColor=white" alt="TikTok" />
  </a>
  <a href="https://youtube.com/@[YOUTUBE_HANDLE]">
    <img src="https://img.shields.io/badge/YouTube-FF69B4?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" />
  </a>
  <a href="mailto:[YOUR_EMAIL]">
    <img src="https://img.shields.io/badge/Email-FF69B4?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
</div>

<br>

<div align="center">
  <i>⭐ If you like what you see, drop a star on my repos! ⭐</i>
</div>

<!-- ============================================================ -->
<!--                        WAVING FOOTER                          -->
<!-- ============================================================ -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,2,12&height=140&section=footer&text=Thanks+for+stopping+by!&fontSize=24&fontColor=ffffff&animation=twinkling&fontAlignY=68" width="100%" alt="Footer" />
</div>
