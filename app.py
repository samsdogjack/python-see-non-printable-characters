from flask import Flask, request, render_template_string
import html

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>View non-printable unicode characters</title>
<style type="text/css">
body {
    font-family: Helvetica, Arial, sans-serif;
    background-color: #EEEEEE;
}
div.main {
    background-color: white;
    border-radius: 10px;
    border: 2px solid #666666;
    box-shadow: 5px 5px 5px #999999;
    padding: 2.4em 3em;
    margin: 0 auto;
    max-width: 1000px;
}
div.output {
    margin: 3em 0;
    border: 1px solid #666666;
    padding: 0.4em 0.2em;
    font-family: Courier New, Courier, monospaced;
    cursor: default;
}
div.output span.symbol {
    color: white;
    background-color: #999999;
    padding: 0 2px;
    margin: 0 2px;
}
div.output span.hex {
    color: black;
    background-color: #9999FF;
    padding: 0 2px;
    margin: 0 2px;
}
span.S2Tooltip.anchor {
      white-space: nowrap;
}
span.S2Tooltip.container {
    position: absolute; z-index: 999;
      left: -99999px; top: -99999px;
}
span.S2Tooltip.anchor:hover {
    background-color: #FF9999;
}
span.S2Tooltip.anchor:hover + span.S2Tooltip.container {
      left: auto; top: auto;
}
span.S2Tooltip.tiptext {
      position: absolute;
      left: -2em; top: 1.5em; 
    padding: 0.5em 0.8em 0.7em 0.8em;
    color: black; background-color: #DDDDFF; border: 1px solid #9999FF;
    font-weight: normal; text-align: left; 
    display: block;
      text-indent: 0;
}
</style>
</head>
<body>
<div class="main">
    <h1>View non-printable unicode characters</h1>
    <p>Online tool to display non-printable characters that may be hidden in copy&amp;pasted strings.</p>
    <form action="" method="POST" accept-charset="UTF-8">
        <div style="margin-top: 3em;">
            Please paste the string here:
        </div>
        <div>
            <textarea name="s" rows="8" cols="40" style="width: 100%; box-sizing: border-box;" dir="auto">{{ s|e }}</textarea>
        </div>
        <div>
            <button type="submit">Show me the characters</button>
        </div>
    </form>
    {{ output|safe }}
    <div style="margin: -2.5em 0 4em 0;">{{ char_count }} characters, {{ byte_count }} bytes</div>
    <h2>Helpful Sites for Details on UTF Characters</h2>
    <ul>
        <li><a href="https://www.branah.com/unicode-converter" target="_blank">Branah.com Unicode Converter</a></li>
        <li><a href="http://www.fileformat.info/info/unicode/char/search.htm" target="_blank">FileFormat.Info</a></li>
        <li><a href="http://utf8-chartable.de/unicode-utf8-table.pl" target="_blank">utf8-chartable.de</a></li>
    </ul>
    <h2>Privacy Note</h2>
    <p>This web page (tool) does not store any information about you (no cookies, no IP logging) and it does not store any of the
        text that is written or pasted into the box above.</p>
    <h2>Source Code</h2>
    <p>As this tools has received some attention on <a href="https://www.soscisurvey.de/tools/view-chars.php">soscisurvey.de</a>,
        we chose to make the source code available on <a href="https://github.com/BurninLeo/see-non-printable-characters">GitHub</a>.</p>
</div>
</body>
</html>
"""

def html_char(c):
    codepoint = ord(c)
    if c == '\r':
        symbol = '<span class="symbol S2Tooltip anchor">CR</span>'
        desc = f"{codepoint}<br>0x{codepoint:02X}"
        hexval = f"{codepoint:02X}"
    elif c == '\n':
        symbol = '<span class="symbol S2Tooltip anchor">LF</span>'
        desc = f"{codepoint}<br>0x{codepoint:02X}"
        hexval = f"{codepoint:02X}"
    elif c == '\t':
        symbol = '<span class="symbol S2Tooltip anchor">⟶</span>&#8203;'
        desc = f"{codepoint}<br>0x{codepoint:02X}"
        hexval = f"{codepoint:02X}"
    elif c == ' ':
        symbol = '<span class="white S2Tooltip anchor">·</span>&#8203;'
        desc = f"{codepoint}<br>0x{codepoint:02X}"
        hexval = f"{codepoint:02X}"
    else:
        import unicodedata
        try:
            name = unicodedata.name(c)
        except ValueError:
            name = "UNKNOWN"
        if c.isprintable() and not c.isspace():
            symbol = f'<span class="S2Tooltip anchor">{html.escape(c)}</span>'
        else:
            symbol = f'<span class="hex S2Tooltip anchor">U+{codepoint:04X}</span>'
        desc = f"&amp;#{codepoint};<br>\\u{codepoint:04X}<br>{name}"
        hexval = f"U+{codepoint:04X}"
    return (
        symbol +
        f'<span class="S2Tooltip container">' +
        f'<span class="S2Tooltip tiptext rounded shadow">{desc}</span>' +
        '</span>'
    )

def text2html(s):
    html_out = '<div class="output" dir="auto">\n'
    nlc = 0
    for c in s:
        if c == '\r':
            if nlc == 0:
                nlc = 1
                html_out += html_char(c)
            elif nlc == 1:
                html_out += '<br>\n' + html_char(c)
                nlc = 1
            elif nlc == 2:
                html_out += html_char(c) + '<br>\n'
                nlc = 0
        elif c == '\n':
            sym = html_char(c)
            if nlc == 0:
                nlc = 2
                html_out += sym
            elif nlc == 2:
                html_out += '<br>\n' + sym
                nlc = 2
            elif nlc == 1:
                html_out += sym + '<br>\n'
                nlc = 0
        else:
            html_out += html_char(c)
    html_out += '</div>\n'
    return html_out

@app.route("/", methods=["GET", "POST"])
def index():
    default = "See\u00A0what's hidden in your string\u2026\tor be\\u200Bhind\uFEFF"
    s = request.form.get("s", default)
    output = text2html(s)
    char_count = len(s)
    byte_count = len(s.encode("utf-8"))
    return render_template_string(
        HTML_TEMPLATE,
        s=s,
        output=output,
        char_count=char_count,
        byte_count=byte_count
    )

if __name__ == "__main__":
    app.run(debug=True)