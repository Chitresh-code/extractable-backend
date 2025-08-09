from pathlib import Path
from django.conf import settings
from django.http import HttpResponse
import markdown

def home(request):
    readme_path = Path(settings.BASE_DIR) / "docs" / "README.md"
    this_file = Path(__file__).resolve()
    if not readme_path.exists():
        return HttpResponse(f"<h1>README.md not found at {readme_path} from {this_file}</h1>")

    text = readme_path.read_text(encoding="utf-8")
    html = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "toc", "codehilite"],
        output_format="html5"
    )

    return HttpResponse(f"""
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1"/>
            <title>📄 ExtracTable Docs</title>
            <style>
              :root {{
                --bg-color: #ffffff;
                --text-color: #333333;
                --pre-bg: #f6f8fa;
                --border-color: #ddd;
                --button-bg: #f0f0f0;
                --button-hover: #e0e0e0;
              }}
              
              [data-theme="dark"] {{
                --bg-color: #1a1a1a;
                --text-color: #e0e0e0;
                --pre-bg: #2d2d2d;
                --border-color: #444;
                --button-bg: #333;
                --button-hover: #444;
              }}
              
              body {{ 
                max-width: 900px; 
                margin: 2rem auto; 
                font-family: sans-serif; 
                line-height: 1.6; 
                background-color: var(--bg-color);
                color: var(--text-color);
                transition: background-color 0.3s ease, color 0.3s ease;
                padding: 0 1rem;
              }}
              
              .theme-toggle {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--button-bg);
                border: 1px solid var(--border-color);
                border-radius: 6px;
                padding: 8px 12px;
                cursor: pointer;
                font-size: 14px;
                color: var(--text-color);
                transition: background-color 0.3s ease;
                z-index: 1000;
              }}
              
              .theme-toggle:hover {{
                background: var(--button-hover);
              }}
              
              pre {{ 
                background: var(--pre-bg); 
                padding: 10px; 
                border-radius: 6px; 
                overflow-x: auto;
                border: 1px solid var(--border-color);
              }}
              
              code {{ 
                font-family: monospace; 
                background: var(--pre-bg);
                padding: 2px 4px;
                border-radius: 3px;
              }}
              
              table {{ 
                border-collapse: collapse; 
                width: 100%;
              }}
              
              th, td {{ 
                border: 1px solid var(--border-color); 
                padding: .5rem; 
              }}
              
              th {{
                background: var(--pre-bg);
              }}
              
              a {{
                color: var(--text-color);
                opacity: 0.8;
              }}
              
              a:hover {{
                opacity: 1;
              }}
              
              blockquote {{
                border-left: 4px solid var(--border-color);
                margin: 0;
                padding-left: 1rem;
                background: var(--pre-bg);
                padding: 1rem;
                border-radius: 0 6px 6px 0;
              }}
            </style>
          </head>
          <body>
            <button class="theme-toggle" onclick="toggleTheme()">
              <span id="theme-icon">🌙</span> <span id="theme-text">Dark Mode</span>
            </button>
            {html}
            
            <script>
              function toggleTheme() {{
                const body = document.body;
                const themeIcon = document.getElementById('theme-icon');
                const themeText = document.getElementById('theme-text');
                
                if (body.getAttribute('data-theme') === 'dark') {{
                  body.removeAttribute('data-theme');
                  themeIcon.textContent = '🌙';
                  themeText.textContent = 'Dark Mode';
                  localStorage.setItem('theme', 'light');
                }} else {{
                  body.setAttribute('data-theme', 'dark');
                  themeIcon.textContent = '☀️';
                  themeText.textContent = 'Light Mode';
                  localStorage.setItem('theme', 'dark');
                }}
              }}
              
              // Load saved theme or default to light mode
              const savedTheme = localStorage.getItem('theme');
              if (savedTheme === 'dark') {{
                document.body.setAttribute('data-theme', 'dark');
                document.getElementById('theme-icon').textContent = '☀️';
                document.getElementById('theme-text').textContent = 'Light Mode';
              }}
            </script>
          </body>
        </html>
    """)