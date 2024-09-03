---
tags:
  - tools
layout: null
slug: dedup-spaces
---

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>
        {% if page.id == "home" %}
            {{ site.title }}
        {% else %}
            {{ page.title }} — {{ site.title }}
        {% endif %}
    </title>

    <link rel="canonical" href="{{ page.canonical_url | default: site.url | append: page.url }}">
    <link rel="alternate" type="application/rss+xml" title="{{ site.title }}" href="{{ site.baseurl }}/rss.xml">

    {% if page.tags %}
        <meta itemprop="keywords" content="{{ page.tags | join: ',' }}">
        {% for tag in page.tags %}
            <meta property="article:tag" content="{{ tag }}">
        {% endfor %}
    {% endif %}

    <link href="{{ '/style.css' | relative_url }}" rel="stylesheet">
    <link href="{{ '/pagefind/pagefind-ui.css' | relative_url }}" rel="stylesheet">
    <script src="{{ '/pagefind/pagefind-ui.js' | relative_url }}"></script>
    <script type="module">
        import PagefindHighlight from '{{ "/pagefind/pagefind-highlight.js" | relative_url }}';
        new PagefindHighlight({ highlightParam: "highlight" });
    </script>
    <script src="{{ '/assets/js/search.js' | relative_url }}" defer></script>
    <script src="{{ '/assets/js/prism.js' | relative_url }}" defer></script>
</head>

<body>
    <a class="search-input-block" id="search"></a>

    <header>
        <nav aria-label="Main navigation">
            <div class="header-container">
                <a class="internal-link" href="/">
                    <img src="{{ '/assets/Sudden_Death_Rune.gif' | relative_url }}" alt="Sudden Death Rune" class="favicon">
                </a>
                <a href="https://ib.bsb.br/archive">
                    <img src="{{ '/favicon.ico' | relative_url }}" alt="Archive Icon" class="favicon">
                </a>
                <a href="https://ib.bsb.br/tags">
                    <img src="{{ '/assets/Label.gif' | relative_url }}" alt="Tags Icon" class="favicon">
                </a>
                <a href="https://ib.bsb.br/events">
                    <img src="{{ '/assets/Paralyse_Rune.gif' | relative_url }}" alt="Events Icon" class="favicon">
                </a>
            </div>
        </nav>
    </header>
    <div class="editor-container">
        <div class="editor-ui">
            <textarea id="input-data" placeholder="Paste your text here..."></textarea>
        </div>
        <div>
            <button class="convert-btn" id="remove-duplicate-spaces" onclick="remove_duplicate_spaces()">Remove Duplicate Spaces</button>
            <button class="convert-btn" id="copy-btn" onclick="copyTextToClipboard()">Copy</button>
        </div>
        <div class="editor-ui">
            <textarea id="result" placeholder="Result will show here..." readonly></textarea>
        </div>
    </div>
    <script type="text/javascript">
        function remove_duplicate_spaces() {
            var input_data = document.getElementById("input-data");
            var result = document.getElementById("result");
            result.value = input_data.value.replace(/\s+/g,' ');
        }
    </script>
    <script>
        function fallbackCopyTextToClipboard(text) {
            var textArea = document.createElement("textarea");
            textArea.value = text;

            // Avoid scrolling to bottom
            textArea.style.top = "0";
            textArea.style.left = "0";
            textArea.style.position = "fixed";

            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                var successful = document.execCommand('copy');
                var msg = successful ? 'successful' : 'unsuccessful';
                console.log('Fallback: Copying text command was ' + msg);
            } catch (err) {
                console.error('Fallback: Oops, unable to copy', err);
            }

            document.body.removeChild(textArea);
        }

        function copyTextToClipboard() {
    
            let text = document.getElementById('result').value
        
            if (!navigator.clipboard) {
                fallbackCopyTextToClipboard(text);
                return;
            }
            navigator.clipboard.writeText(text).then(function () {
                console.log('Async: Copying to clipboard was successful!');
            }, function (err) {
                console.error('Async: Could not copy text: ', err);
            });
        }
    </script>
</body>
