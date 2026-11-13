import os
import re
import subprocess
import markdown

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

ACADEMIC_CSS = """
@page {
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
    @bottom-right {
        content: counter(page);
    }
}

@media print {
    body {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    h1, h2, h3, h4, h5 {
        page-break-after: avoid !important;
    }
    table, figure, pre, .mermaid, blockquote {
        page-break-inside: avoid !important;
    }
    .page-break {
        page-break-before: always;
    }
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1e293b;
    background-color: #ffffff;
    max-width: 100%;
    margin: 0;
    padding: 0;
}

/* Headings */
h1 {
    color: #0f172a;
    font-size: 18pt;
    font-weight: 700;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 12px;
}

h2 {
    color: #0369a1;
    font-size: 14pt;
    font-weight: 600;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 10px;
}

h3 {
    color: #0f172a;
    font-size: 12pt;
    font-weight: 600;
    margin-top: 16px;
    margin-bottom: 8px;
}

h4 {
    color: #334155;
    font-size: 11pt;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 6px;
}

p {
    margin-top: 0;
    margin-bottom: 10px;
    text-align: justify;
}

/* Links */
a {
    color: #0284c7;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 18px 0;
    font-size: 9.5pt;
}

th {
    background-color: #0f2b48;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #0f2b48;
}

td {
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
}

tr:nth-child(even) td {
    background-color: #f8fafc;
}

/* Code & Preformatted */
pre {
    background-color: #0f172a;
    color: #f1f5f9;
    padding: 12px 14px;
    border-radius: 6px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    overflow-x: auto;
    margin: 12px 0;
}

code {
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 9pt;
    background-color: #f1f5f9;
    color: #0369a1;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}

pre code {
    background-color: transparent;
    color: inherit;
    padding: 0;
    border: none;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid #0284c7;
    background-color: #f0f9ff;
    margin: 14px 0;
    padding: 10px 14px;
    border-radius: 0 6px 6px 0;
    color: #0c4a6e;
    font-size: 10pt;
}
blockquote p {
    margin: 0;
}

/* Horizontal Rule */
hr {
    border: none;
    border-top: 1px solid #cbd5e1;
    margin: 20px 0;
}

/* Mermaid Container */
.mermaid {
    text-align: center;
    background-color: #ffffff;
    margin: 16px 0;
    padding: 10px;
}

/* KaTeX equations */
.katex-display {
    margin: 12px 0 !important;
}

/* University Header Badge */
.uni-header {
    text-align: center;
    border-bottom: 2px solid #0f2b48;
    padding-bottom: 12px;
    margin-bottom: 18px;
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>

<!-- KaTeX CSS & JS for Math Rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>

<!-- Mermaid JS for Flowchart Rendering -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: false,
    theme: 'neutral',
    flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }}
  }});

  document.addEventListener("DOMContentLoaded", function() {{
    // Render Math
    if (typeof renderMathInElement !== 'undefined') {{
      renderMathInElement(document.body, {{
        delimiters: [
          {{left: "$$", right: "$$", display: true}},
          {{left: "$", right: "$", display: false}}
        ],
        throwOnError: false
      }});
    }}
    // Render Mermaid
    if (typeof mermaid !== 'undefined') {{
      mermaid.run();
    }}
  }});
</script>

<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""

def process_markdown_content(md_text: str) -> str:
    """Pre-process markdown to handle Mermaid blocks and other custom tags."""
    # Convert ```mermaid ... ``` code blocks to <pre class="mermaid">...</pre>
    def replace_mermaid(match):
        graph_def = match.group(1).strip()
        return f'<pre class="mermaid">\n{graph_def}\n</pre>'

    md_text = re.sub(r'```mermaid\s*\n(.*?)\n```', replace_mermaid, md_text, flags=re.DOTALL)
    return md_text

def convert_md_to_html(md_path: str, html_path: str, title: str):
    with open(md_path, 'r', encoding='utf-8') as f:
        raw_md = f.read()

    processed_md = process_markdown_content(raw_md)
    html_body = markdown.markdown(
        processed_md,
        extensions=['tables', 'fenced_code', 'sane_lists']
    )

    full_html = HTML_TEMPLATE.format(
        title=title,
        css=ACADEMIC_CSS,
        body=html_body
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Generated HTML: {html_path}")

def render_html_to_pdf(html_path: str, pdf_path: str):
    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(pdf_path)

    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--virtual-time-budget=6000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        abs_html
    ]

    print(f"Executing Edge headless to generate: {abs_pdf}...")
    subprocess.run(cmd, check=True)

    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        print(f"SUCCESS: {pdf_path} ({os.path.getsize(abs_pdf):,} bytes)")
    else:
        raise RuntimeError(f"Failed to generate {pdf_path}")

def main():
    workspace = os.path.dirname(os.path.abspath(__file__))

    # 1. Deliverable 1: Paper Approval Form
    approval_md = os.path.join(workspace, "PAPER_APPROVAL_FORM.md")
    approval_html = os.path.join(workspace, "PAPER_APPROVAL_FORM.html")
    approval_pdf = os.path.join(workspace, "PAPER_APPROVAL_FORM.pdf")

    print("\n--- Converting Deliverable 1: Paper Approval Form ---")
    convert_md_to_html(approval_md, approval_html, "FAST-NUCES Paper Approval Form")
    render_html_to_pdf(approval_html, approval_pdf)

    # 2. Deliverable 3: Project Report
    report_md = os.path.join(workspace, "PROJECT_REPORT.md")
    report_html = os.path.join(workspace, "PROJECT_REPORT.html")
    report_pdf = os.path.join(workspace, "PROJECT_REPORT.pdf")

    print("\n--- Converting Deliverable 3: Semester Project Report ---")
    convert_md_to_html(report_md, report_html, "CL3001 Machine Learning Lab Project Report")
    render_html_to_pdf(report_html, report_pdf)

    print("\nAll Markdown files successfully converted to high-quality PDF!")

if __name__ == "__main__":
    main()
