import gradio as gr
import json
import os
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_custom_css():
    """Load custom CSS if available"""
    css_path = Path(__file__).parent / "static" / "style.css"
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def create_category_card(category):
    """Create HTML for a category card"""
    return f"""
    <div class="category-card">
        <div class="category-icon">{category['icon']}</div>
        <h3>{category['name']}</h3>
        <p>{category['description']}</p>
    </div>
    """

def create_model_card(item, item_type="model"):
    """Create HTML for a model or dataset card"""
    tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in item.get('tags', [])])

    links = []
    if item.get('repo'):
        links.append(f'<a href="https://huggingface.co/{item["repo"]}" target="_blank" class="card-link">🤗 View on HF</a>')
    if item.get('demo_url'):
        links.append(f'<a href="{item["demo_url"]}" target="_blank" class="card-link">🚀 Demo</a>')
    if item.get('paper_url'):
        links.append(f'<a href="{item["paper_url"]}" target="_blank" class="card-link">📄 Paper</a>')

    links_html = " ".join(links)

    size_info = f'<div class="card-size">{item["size"]}</div>' if item.get('size') else ''

    return f"""
    <div class="item-card">
        <h3>{item['name']}</h3>
        <p class="card-description">{item.get('description', '')}</p>
        {size_info}
        <div class="card-tags">{tags_html}</div>
        <div class="card-links">{links_html}</div>
    </div>
    """

def create_header(config):
    """Create site header"""
    site = config['site']
    social_links = []

    if site['social_links'].get('github'):
        social_links.append(f'<a href="{site["social_links"]["github"]}" target="_blank">GitHub</a>')
    if site['social_links'].get('twitter'):
        social_links.append(f'<a href="{site["social_links"]["twitter"]}" target="_blank">Twitter</a>')
    if site['social_links'].get('linkedin'):
        social_links.append(f'<a href="{site["social_links"]["linkedin"]}" target="_blank">LinkedIn</a>')

    social_html = " · ".join(social_links) if social_links else ""

    return f"""
    <div class="site-header">
        <h1>{site['title']}</h1>
        <p class="site-description">{site['description']}</p>
        <p class="site-author">by {site['author']}</p>
        <div class="social-links">{social_html}</div>
    </div>
    """

def create_category_section(config, category_id):
    """Create a section showing items from a specific category"""
    models = [m for m in config.get('models', []) if m.get('category') == category_id]
    datasets = [d for d in config.get('datasets', []) if d.get('category') == category_id]

    html = "<div class='items-grid'>"

    for model in models:
        html += create_model_card(model, "model")

    for dataset in datasets:
        html += create_model_card(dataset, "dataset")

    html += "</div>"

    if not models and not datasets:
        html = "<p class='no-items'>No items in this category yet.</p>"

    return html

def build_interface():
    """Build the Gradio interface"""
    config = load_config()
    custom_css = get_custom_css()

    with gr.Blocks(
        title=config['site']['title'],
        css=custom_css,
        theme=gr.themes.Soft(primary_hue="indigo")
    ) as demo:

        # Header
        gr.HTML(create_header(config))

        # Categories Overview
        gr.Markdown("## 📂 Categories", elem_classes="section-title")

        categories_html = "<div class='categories-grid'>"
        for category in config['categories']:
            categories_html += create_category_card(category)
        categories_html += "</div>"

        gr.HTML(categories_html)

        # Create tabs for each category
        with gr.Tabs():
            for category in config['categories']:
                with gr.Tab(f"{category['icon']} {category['name']}"):
                    gr.Markdown(f"### {category['description']}")
                    category_html = create_category_section(config, category['id'])
                    gr.HTML(category_html)

            # All items tab
            with gr.Tab("🌐 All Items"):
                gr.Markdown("### All Models and Datasets")
                all_html = "<div class='items-grid'>"

                for model in config.get('models', []):
                    all_html += create_model_card(model, "model")

                for dataset in config.get('datasets', []):
                    all_html += create_model_card(dataset, "dataset")

                all_html += "</div>"
                gr.HTML(all_html)

        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666; padding: 20px;">
            Built with <a href="https://github.com/marduk191/hf_site_builder" target="_blank">HF Site Builder</a> |
            Powered by <a href="https://gradio.app" target="_blank">Gradio</a> &
            <a href="https://huggingface.co/spaces" target="_blank">Hugging Face Spaces</a>
        </div>
        """)

    return demo

if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
