# 🚀 HF Site Builder

A modern, customizable website builder for Hugging Face Spaces to showcase your AI models and datasets.

## ✨ Features

- 🎨 **Modern Design**: Beautiful, responsive UI with custom CSS styling
- 📂 **Custom Categories**: Organize your models and datasets into custom categories
- 🔗 **Direct Links**: Link to Hugging Face repos, demos, and papers
- 🏷️ **Tags & Metadata**: Add tags, descriptions, and metadata to your items
- 🛠️ **CLI Tool**: Easy-to-use command-line tool for managing your site
- 🌐 **Cross-Platform**: Built with Python and Gradio - works everywhere
- 📱 **Responsive**: Looks great on desktop, tablet, and mobile

## 🚀 Quick Start

### 1. Clone or Download

```bash
git clone https://github.com/marduk191/hf_site_builder.git
cd hf_site_builder
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your Site

Edit `config.json` to add your information:

```json
{
  "site": {
    "title": "My AI Model Hub",
    "description": "Explore my collection of AI models and datasets",
    "author": "Your Name"
  }
}
```

### 4. Run Locally

```bash
python app.py
```

Visit `http://localhost:7860` to see your site!

### 5. Deploy to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Choose **Gradio** as the SDK
3. Upload all files from this repository
4. Your site will be live at `https://huggingface.co/spaces/your-username/your-space`

## 📖 Configuration Guide

### Site Information

Update the `site` section in `config.json`:

```json
{
  "site": {
    "title": "My AI Model Hub",
    "description": "Explore my collection of AI models and datasets",
    "author": "Your Name",
    "theme_color": "#4F46E5",
    "social_links": {
      "github": "https://github.com/yourusername",
      "twitter": "https://twitter.com/yourusername",
      "linkedin": "https://linkedin.com/in/yourusername"
    }
  }
}
```

### Categories

Create custom categories to organize your items:

```json
{
  "categories": [
    {
      "id": "nlp",
      "name": "Natural Language Processing",
      "icon": "💬",
      "description": "Models for text understanding and generation"
    }
  ]
}
```

### Adding Models

```json
{
  "models": [
    {
      "name": "My Awesome Model",
      "repo": "username/model-name",
      "category": "nlp",
      "description": "A fine-tuned model for text classification",
      "tags": ["classification", "bert", "nlp"],
      "demo_url": "https://huggingface.co/spaces/username/demo",
      "paper_url": "https://arxiv.org/abs/..."
    }
  ]
}
```

### Adding Datasets

```json
{
  "datasets": [
    {
      "name": "My Dataset",
      "repo": "username/dataset-name",
      "category": "datasets",
      "description": "A curated dataset for specific tasks",
      "tags": ["text", "classification"],
      "size": "100K samples"
    }
  ]
}
```

## 🛠️ CLI Tool

The `builder.py` script helps you manage your site from the command line.

### Update Site Info

```bash
python builder.py site --title "My New Title" --author "Your Name"
```

### Add a Category

```bash
python builder.py add-category nlp "Natural Language Processing" --icon "💬" --description "Text models"
```

### Add a Model

```bash
python builder.py add-model "My Model" "username/model-name" nlp \
  --description "A great model" \
  --tags "bert,classification" \
  --demo-url "https://..."
```

### Add a Dataset

```bash
python builder.py add-dataset "My Dataset" "username/dataset-name" datasets \
  --description "A useful dataset" \
  --size "1M samples"
```

### List All Items

```bash
python builder.py list
```

### Remove an Item

```bash
python builder.py remove model "My Model"
python builder.py remove dataset "My Dataset"
python builder.py remove category nlp
```

### Validate Configuration

```bash
python builder.py validate
```

## 🎨 Customization

### Custom CSS

Edit `static/style.css` to customize the appearance:

```css
:root {
    --primary-color: #4F46E5;
    --secondary-color: #7C3AED;
    /* Add your custom colors */
}
```

### Custom Theme

You can modify the Gradio theme in `app.py`:

```python
gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo"))
```

Available themes: `Soft`, `Base`, `Monochrome`, `Glass`

## 📁 Project Structure

```
hf_site_builder/
├── app.py              # Main Gradio application
├── config.json         # Site configuration
├── builder.py          # CLI management tool
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css      # Custom CSS styling
└── README.md          # Documentation
```

## 🚀 Deployment

### Hugging Face Spaces

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose a name and select "Gradio" as SDK
4. Upload or push your files
5. Your site goes live automatically!

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Access at http://localhost:7860
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Credits

Built with:
- [Gradio](https://gradio.app) - For the web interface
- [Hugging Face Spaces](https://huggingface.co/spaces) - For hosting
- Modern CSS design principles

## 📧 Support

If you have questions or need help:
- Open an issue on GitHub
- Check the documentation
- Visit the Hugging Face community forums

---

Made with ❤️ for the AI community