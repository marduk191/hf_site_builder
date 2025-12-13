#!/usr/bin/env python3
"""
HF Site Builder - CLI tool for managing your Hugging Face Space website
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, List

CONFIG_FILE = Path(__file__).parent / "config.json"

def load_config() -> Dict:
    """Load the configuration file"""
    if not CONFIG_FILE.exists():
        print(f"Error: {CONFIG_FILE} not found!")
        sys.exit(1)

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config: Dict):
    """Save the configuration file"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Configuration saved to {CONFIG_FILE}")

def update_site_info(args):
    """Update site information"""
    config = load_config()

    if args.title:
        config['site']['title'] = args.title
    if args.description:
        config['site']['description'] = args.description
    if args.author:
        config['site']['author'] = args.author
    if args.theme_color:
        config['site']['theme_color'] = args.theme_color

    save_config(config)
    print("✅ Site information updated!")

def add_category(args):
    """Add a new category"""
    config = load_config()

    new_category = {
        "id": args.id,
        "name": args.name,
        "icon": args.icon or "📁",
        "description": args.description or ""
    }

    config['categories'].append(new_category)
    save_config(config)
    print(f"✅ Category '{args.name}' added!")

def add_model(args):
    """Add a new model"""
    config = load_config()

    new_model = {
        "name": args.name,
        "repo": args.repo,
        "category": args.category,
        "description": args.description or "",
        "tags": args.tags.split(',') if args.tags else [],
        "demo_url": args.demo_url,
        "paper_url": args.paper_url
    }

    config['models'].append(new_model)
    save_config(config)
    print(f"✅ Model '{args.name}' added!")

def add_dataset(args):
    """Add a new dataset"""
    config = load_config()

    new_dataset = {
        "name": args.name,
        "repo": args.repo,
        "category": args.category,
        "description": args.description or "",
        "tags": args.tags.split(',') if args.tags else [],
        "size": args.size
    }

    config['datasets'].append(new_dataset)
    save_config(config)
    print(f"✅ Dataset '{args.name}' added!")

def list_items(args):
    """List all items in the config"""
    config = load_config()

    print("\n🏠 Site Information:")
    print(f"  Title: {config['site']['title']}")
    print(f"  Author: {config['site']['author']}")
    print(f"  Description: {config['site']['description']}")

    print("\n📂 Categories:")
    for cat in config['categories']:
        print(f"  {cat['icon']} {cat['name']} ({cat['id']})")

    print(f"\n🤖 Models ({len(config.get('models', []))}):")
    for model in config.get('models', []):
        print(f"  - {model['name']} [{model['category']}]")

    print(f"\n📊 Datasets ({len(config.get('datasets', []))}): ")
    for dataset in config.get('datasets', []):
        print(f"  - {dataset['name']} [{dataset['category']}]")

def remove_item(args):
    """Remove a model or dataset"""
    config = load_config()

    if args.type == "model":
        original_count = len(config.get('models', []))
        config['models'] = [m for m in config.get('models', []) if m['name'] != args.name]
        if len(config['models']) < original_count:
            save_config(config)
            print(f"✅ Model '{args.name}' removed!")
        else:
            print(f"❌ Model '{args.name}' not found!")

    elif args.type == "dataset":
        original_count = len(config.get('datasets', []))
        config['datasets'] = [d for d in config.get('datasets', []) if d['name'] != args.name]
        if len(config['datasets']) < original_count:
            save_config(config)
            print(f"✅ Dataset '{args.name}' removed!")
        else:
            print(f"❌ Dataset '{args.name}' not found!")

    elif args.type == "category":
        original_count = len(config['categories'])
        config['categories'] = [c for c in config['categories'] if c['id'] != args.name]
        if len(config['categories']) < original_count:
            save_config(config)
            print(f"✅ Category '{args.name}' removed!")
        else:
            print(f"❌ Category '{args.name}' not found!")

def validate_config(args):
    """Validate the configuration file"""
    try:
        config = load_config()

        errors = []

        # Check required fields
        if 'site' not in config:
            errors.append("Missing 'site' section")
        if 'categories' not in config:
            errors.append("Missing 'categories' section")

        # Check category IDs
        category_ids = [c['id'] for c in config.get('categories', [])]

        # Validate models
        for model in config.get('models', []):
            if model.get('category') not in category_ids:
                errors.append(f"Model '{model.get('name')}' has invalid category: {model.get('category')}")

        # Validate datasets
        for dataset in config.get('datasets', []):
            if dataset.get('category') not in category_ids:
                errors.append(f"Dataset '{dataset.get('name')}' has invalid category: {dataset.get('category')}")

        if errors:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print("✅ Configuration is valid!")

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="HF Site Builder - Manage your Hugging Face Space website",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Update site info
    site_parser = subparsers.add_parser('site', help='Update site information')
    site_parser.add_argument('--title', help='Site title')
    site_parser.add_argument('--description', help='Site description')
    site_parser.add_argument('--author', help='Author name')
    site_parser.add_argument('--theme-color', help='Theme color (hex)')
    site_parser.set_defaults(func=update_site_info)

    # Add category
    cat_parser = subparsers.add_parser('add-category', help='Add a new category')
    cat_parser.add_argument('id', help='Category ID (e.g., nlp)')
    cat_parser.add_argument('name', help='Category name')
    cat_parser.add_argument('--icon', help='Category icon (emoji)', default='📁')
    cat_parser.add_argument('--description', help='Category description')
    cat_parser.set_defaults(func=add_category)

    # Add model
    model_parser = subparsers.add_parser('add-model', help='Add a new model')
    model_parser.add_argument('name', help='Model name')
    model_parser.add_argument('repo', help='HuggingFace repo (username/repo-name)')
    model_parser.add_argument('category', help='Category ID')
    model_parser.add_argument('--description', help='Model description')
    model_parser.add_argument('--tags', help='Comma-separated tags')
    model_parser.add_argument('--demo-url', help='Demo URL')
    model_parser.add_argument('--paper-url', help='Paper URL')
    model_parser.set_defaults(func=add_model)

    # Add dataset
    dataset_parser = subparsers.add_parser('add-dataset', help='Add a new dataset')
    dataset_parser.add_argument('name', help='Dataset name')
    dataset_parser.add_argument('repo', help='HuggingFace repo (username/repo-name)')
    dataset_parser.add_argument('category', help='Category ID')
    dataset_parser.add_argument('--description', help='Dataset description')
    dataset_parser.add_argument('--tags', help='Comma-separated tags')
    dataset_parser.add_argument('--size', help='Dataset size (e.g., 100K samples)')
    dataset_parser.set_defaults(func=add_dataset)

    # List items
    list_parser = subparsers.add_parser('list', help='List all items')
    list_parser.set_defaults(func=list_items)

    # Remove item
    remove_parser = subparsers.add_parser('remove', help='Remove an item')
    remove_parser.add_argument('type', choices=['model', 'dataset', 'category'], help='Item type')
    remove_parser.add_argument('name', help='Item name or ID')
    remove_parser.set_defaults(func=remove_item)

    # Validate config
    validate_parser = subparsers.add_parser('validate', help='Validate configuration')
    validate_parser.set_defaults(func=validate_config)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == '__main__':
    main()
