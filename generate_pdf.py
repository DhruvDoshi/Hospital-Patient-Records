"""
Generate PDF from Markdown with styling
Converts FINAL_TASK1_RESPONSE.md to a professional PDF
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def generate_pdf_from_markdown(md_file, output_pdf):
    """Convert Markdown file to styled PDF"""
    
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML with extensions
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'extra',  # Tables, fenced code blocks, etc.
            'codehilite',  # Code syntax highlighting
            'toc',  # Table of contents
            'nl2br',  # New line to break
        ]
    )
    
    # Create styled HTML document
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @bottom-center {{
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10pt;
                    color: #666;
                }}
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 20px;
                font-size: 11pt;
            }}
            
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-top: 30px;
                margin-bottom: 20px;
                font-size: 28pt;
                page-break-before: auto;
            }}
            
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 8px;
                margin-top: 25px;
                margin-bottom: 15px;
                font-size: 20pt;
                page-break-after: avoid;
            }}
            
            h3 {{
                color: #2c3e50;
                margin-top: 20px;
                margin-bottom: 10px;
                font-size: 16pt;
                page-break-after: avoid;
            }}
            
            h4 {{
                color: #555;
                margin-top: 15px;
                margin-bottom: 8px;
                font-size: 13pt;
            }}
            
            p {{
                margin: 10px 0;
                text-align: justify;
            }}
            
            ul, ol {{
                margin: 10px 0;
                padding-left: 30px;
            }}
            
            li {{
                margin: 5px 0;
            }}
            
            code {{
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 2px 6px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 10pt;
                color: #c7254e;
            }}
            
            pre {{
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                overflow-x: auto;
                margin: 15px 0;
                page-break-inside: avoid;
            }}
            
            pre code {{
                background-color: transparent;
                border: none;
                padding: 0;
                color: #333;
                font-size: 9pt;
                line-height: 1.4;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                font-size: 10pt;
                page-break-inside: avoid;
            }}
            
            th {{
                background-color: #3498db;
                color: white;
                padding: 10px;
                text-align: left;
                font-weight: bold;
            }}
            
            td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            blockquote {{
                border-left: 4px solid #3498db;
                background-color: #f0f7fb;
                padding: 15px 20px;
                margin: 15px 0;
                font-style: italic;
                page-break-inside: avoid;
            }}
            
            hr {{
                border: none;
                border-top: 2px solid #ddd;
                margin: 20px 0;
            }}
            
            strong {{
                color: #2c3e50;
                font-weight: bold;
            }}
            
            em {{
                color: #555;
            }}
            
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            
            /* Emoji and special characters */
            .emoji {{
                font-size: 14pt;
            }}
            
            /* Status indicators */
            [title*="✅"], [title*="✓"] {{
                color: #27ae60;
            }}
            
            [title*="❌"], [title*="✗"] {{
                color: #e74c3c;
            }}
            
            [title*="⏳"], [title*="🔲"] {{
                color: #f39c12;
            }}
            
            /* Print optimization */
            @media print {{
                body {{
                    font-size: 10pt;
                }}
                h1 {{
                    font-size: 24pt;
                }}
                h2 {{
                    font-size: 18pt;
                }}
                h3 {{
                    font-size: 14pt;
                }}
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Generate PDF
    HTML(string=styled_html).write_pdf(
        output_pdf,
        stylesheets=[CSS(string='@page { size: A4; margin: 2cm; }')]
    )
    
    print(f"✓ PDF generated successfully: {output_pdf}")
    print(f"  File size: {Path(output_pdf).stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    md_file = "FINAL_TASK1_RESPONSE.md"
    output_pdf = "FINAL_TASK1_RESPONSE.pdf"
    
    print("Converting Markdown to PDF...")
    print(f"Input: {md_file}")
    print(f"Output: {output_pdf}")
    print()
    
    try:
        generate_pdf_from_markdown(md_file, output_pdf)
        print("\n✅ PDF generation complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTrying alternative method...")
        
        # Fallback: Simple conversion
        import subprocess
        try:
            # Try using pandoc if available
            subprocess.run([
                'pandoc', md_file,
                '-o', output_pdf,
                '--pdf-engine=xelatex',
                '-V', 'geometry:margin=2cm'
            ], check=True)
            print("✓ PDF generated using pandoc")
        except:
            print("Please install required packages:")
            print("  pip install markdown weasyprint")
            print("  or")
            print("  brew install pandoc")
