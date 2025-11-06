"""
Generate PDF from Markdown using markdown2pdf or pypandoc
Simple conversion maintaining Markdown styling
"""

import subprocess
import sys
from pathlib import Path

def generate_pdf_with_pandoc(md_file, output_pdf):
    """Use pandoc to convert Markdown to PDF"""
    try:
        # Check if pandoc is installed
        subprocess.run(['pandoc', '--version'], 
                      capture_output=True, check=True)
        
        # Convert with pandoc
        cmd = [
            'pandoc',
            md_file,
            '-o', output_pdf,
            '--pdf-engine=xelatex',
            '-V', 'geometry:margin=2cm',
            '-V', 'fontsize=11pt',
            '-V', 'colorlinks=true',
            '--highlight-style=tango',
            '--toc',
            '--toc-depth=3'
        ]
        
        subprocess.run(cmd, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def generate_pdf_with_markdown_pdf(md_file, output_pdf):
    """Use markdown-pdf npm package"""
    try:
        cmd = ['markdown-pdf', md_file, '-o', output_pdf]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def generate_html_for_pdf(md_file, output_html):
    """Generate styled HTML that can be printed to PDF"""
    import markdown
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'toc', 'tables']
    )
    
    # Create styled HTML
    styled_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Task 1 - AI-Powered Analysis</title>
    <style>
        @page {{ size: A4; margin: 2cm; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            font-size: 11pt;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            page-break-before: auto;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 25px;
            page-break-after: avoid;
        }}
        h3 {{
            color: #2c3e50;
            margin-top: 20px;
            page-break-after: avoid;
        }}
        code {{
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            color: #c7254e;
        }}
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            page-break-inside: avoid;
        }}
        pre code {{
            background: transparent;
            border: none;
            padding: 0;
            color: #333;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            page-break-inside: avoid;
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 10px;
            text-align: left;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        blockquote {{
            border-left: 4px solid #3498db;
            background-color: #f0f7fb;
            padding: 15px 20px;
            margin: 15px 0;
            page-break-inside: avoid;
        }}
        ul, ol {{ margin: 10px 0; padding-left: 30px; }}
        li {{ margin: 5px 0; }}
        strong {{ color: #2c3e50; }}
        @media print {{
            body {{ font-size: 10pt; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    {html_content}
    <div class="no-print" style="position: fixed; bottom: 20px; right: 20px; background: #3498db; color: white; padding: 10px 20px; border-radius: 5px; font-size: 14px;">
        Press Ctrl+P (Cmd+P on Mac) to save as PDF
    </div>
</body>
</html>"""
    
    # Save HTML
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(styled_html)
    
    return output_html

def main():
    md_file = "FINAL_TASK1_RESPONSE.md"
    output_pdf = "FINAL_TASK1_RESPONSE.pdf"
    output_html = "FINAL_TASK1_RESPONSE_PRINTABLE.html"
    
    print("="*70)
    print("MARKDOWN TO PDF CONVERTER")
    print("="*70)
    print(f"\nInput:  {md_file}")
    print(f"Output: {output_pdf}")
    print()
    
    # Try different methods
    success = False
    
    # Method 1: Try pandoc
    print("Method 1: Trying pandoc...")
    if generate_pdf_with_pandoc(md_file, output_pdf):
        print("✓ PDF generated successfully using pandoc!")
        success = True
    else:
        print("✗ Pandoc not available or failed")
    
    # Method 2: Generate printable HTML
    if not success:
        print("\nMethod 2: Generating printable HTML...")
        try:
            html_file = generate_html_for_pdf(md_file, output_html)
            print(f"✓ HTML generated: {html_file}")
            print("\nTo create PDF:")
            print(f"  1. Open {html_file} in your browser")
            print("  2. Press Cmd+P (Mac) or Ctrl+P (Windows)")
            print("  3. Select 'Save as PDF'")
            print(f"  4. Save as {output_pdf}")
            print("\nAlternatively, run:")
            print(f"  open {html_file}")
            
            # Try to open in browser
            import webbrowser
            file_path = Path(html_file).absolute()
            webbrowser.open(f'file://{file_path}')
            print(f"\n✓ Opened in browser automatically")
            success = True
        except Exception as e:
            print(f"✗ Failed: {e}")
    
    # Method 3: Instructions
    if not success:
        print("\n" + "="*70)
        print("ALTERNATIVE METHODS TO CREATE PDF:")
        print("="*70)
        print("\n1. Install pandoc (recommended):")
        print("   brew install pandoc")
        print("   brew install basictex")
        print("   Then run this script again")
        print("\n2. Use online converter:")
        print("   Upload FINAL_TASK1_RESPONSE.md to:")
        print("   - https://www.markdowntopdf.com/")
        print("   - https://md2pdf.netlify.app/")
        print("\n3. Use VS Code extension:")
        print("   - Install 'Markdown PDF' extension")
        print("   - Right-click on .md file → 'Markdown PDF: Export (pdf)'")
        print("\n4. Manual method:")
        print(f"   - Open {output_html} in browser")
        print("   - Print to PDF (Cmd+P)")
    
    print("\n" + "="*70)
    if success:
        print("✅ CONVERSION COMPLETE!")
    else:
        print("⚠️  MANUAL STEP REQUIRED")
    print("="*70)

if __name__ == "__main__":
    main()
