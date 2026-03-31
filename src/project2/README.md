# Project 2 - Text Visualization
## Attribution

This project uses content from a Wikipedia article in different languages:
- [Badminton (English)](https://en.wikipedia.org/wiki/Badminton)
- [Badminton (French)](https://fr.wikipedia.org/wiki/Badminton)

## Running the Interactive Wordcloud

1. Generate visualizations: `python main.py`
    - Creates PNGs and `wordcloud_data.json` in results/project2
2. Start a local server using one of these methods:
    - **VS Code Live Server (Recommended)**: Install the [Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer), right-click `index.html`, and select "Open with Live Server"
    - **Python HTTP Server**: Run `python -m http.server 8000` from `cs4990-group6/` root, then open http://localhost:8000/src/project2/index.html
    - Required because browsers block `fetch()` on `file://` URLs
3. The cloud reflects the latest run
