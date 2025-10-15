#!/usr/bin/env python3
"""
Build release artifact for Reframe SWIFT CBPR+ Package
Minifies all JSON files and creates a zip archive with only necessary files
"""

import json
import os
import shutil
import zipfile
from pathlib import Path

# Configuration
PACKAGE_VERSION = "v2.0.0"
RELEASE_DIR = "release"
PACKAGE_NAME = f"reframe-swift-cbpr-{PACKAGE_VERSION}"
ZIP_NAME = f"{PACKAGE_NAME}.zip"

# Directories to include in release
INCLUDE_DIRS = [
    "transform",
    "validate",
    "generate",
    "scenarios"
]

# Individual files to include
INCLUDE_FILES = [
    "reframe-package.json",
    "README.md",
    "LICENSE"
]

# Files to exclude (patterns)
EXCLUDE_PATTERNS = [
    ".DS_Store",
    "__pycache__",
    "*.pyc",
    ".git",
    ".gitignore"
]

def minify_json(json_path):
    """Read JSON file and return minified version"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Minify: no whitespace, compact separators
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    except Exception as e:
        print(f"Error minifying {json_path}: {e}")
        return None

def should_exclude(path, exclude_patterns):
    """Check if path should be excluded"""
    path_str = str(path)
    for pattern in exclude_patterns:
        if pattern.startswith('*.'):
            if path_str.endswith(pattern[1:]):
                return True
        elif pattern in path_str:
            return True
    return False

def build_release():
    """Build the release package"""

    # Get source directory (script location)
    source_dir = Path(__file__).parent

    # Create release directory
    release_path = source_dir / RELEASE_DIR
    package_path = release_path / PACKAGE_NAME

    # Clean up existing release directory
    if release_path.exists():
        shutil.rmtree(release_path)

    package_path.mkdir(parents=True, exist_ok=True)

    print(f"Building release package: {PACKAGE_NAME}")
    print("=" * 60)

    # Track statistics
    stats = {
        'json_files': 0,
        'json_bytes_before': 0,
        'json_bytes_after': 0,
        'other_files': 0,
        'total_files': 0
    }

    # Copy and minify JSON files from included directories
    for dir_name in INCLUDE_DIRS:
        src_dir = source_dir / dir_name
        if not src_dir.exists():
            print(f"Warning: Directory {dir_name} not found, skipping...")
            continue

        print(f"\nProcessing directory: {dir_name}/")

        # Walk through directory
        for root, dirs, files in os.walk(src_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d, EXCLUDE_PATTERNS)]

            for file in files:
                src_file = Path(root) / file

                # Skip excluded files
                if should_exclude(src_file, EXCLUDE_PATTERNS):
                    continue

                # Calculate relative path
                rel_path = src_file.relative_to(source_dir)
                dest_file = package_path / rel_path

                # Create destination directory
                dest_file.parent.mkdir(parents=True, exist_ok=True)

                # Process JSON files
                if file.endswith('.json'):
                    original_size = src_file.stat().st_size
                    minified_content = minify_json(src_file)

                    if minified_content:
                        dest_file.write_text(minified_content, encoding='utf-8')
                        minified_size = dest_file.stat().st_size

                        stats['json_files'] += 1
                        stats['json_bytes_before'] += original_size
                        stats['json_bytes_after'] += minified_size

                        reduction = ((original_size - minified_size) / original_size * 100) if original_size > 0 else 0
                        print(f"  ✓ {rel_path} ({original_size:,} → {minified_size:,} bytes, {reduction:.1f}% reduction)")
                    else:
                        # Fallback: copy original if minification fails
                        shutil.copy2(src_file, dest_file)
                        print(f"  ⚠ {rel_path} (copied without minification)")
                        stats['other_files'] += 1
                else:
                    # Copy non-JSON files as-is
                    shutil.copy2(src_file, dest_file)
                    stats['other_files'] += 1

                stats['total_files'] += 1

    # Copy individual files
    print(f"\nCopying additional files:")
    for file_name in INCLUDE_FILES:
        src_file = source_dir / file_name
        if src_file.exists():
            dest_file = package_path / file_name
            shutil.copy2(src_file, dest_file)
            stats['other_files'] += 1
            stats['total_files'] += 1
            print(f"  ✓ {file_name}")
        else:
            print(f"  ⚠ {file_name} not found, skipping...")

    # Create zip archive
    print(f"\nCreating zip archive: {ZIP_NAME}")
    zip_path = release_path / ZIP_NAME

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_path):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_path.parent)
                zipf.write(file_path, arcname)

    zip_size = zip_path.stat().st_size

    # Print statistics
    print("\n" + "=" * 60)
    print("RELEASE BUILD COMPLETE")
    print("=" * 60)
    print(f"Package version:        {PACKAGE_VERSION}")
    print(f"Total files:            {stats['total_files']}")
    print(f"JSON files minified:    {stats['json_files']}")
    print(f"Other files:            {stats['other_files']}")
    print(f"\nJSON size reduction:")
    print(f"  Before:               {stats['json_bytes_before']:,} bytes")
    print(f"  After:                {stats['json_bytes_after']:,} bytes")
    if stats['json_bytes_before'] > 0:
        total_reduction = ((stats['json_bytes_before'] - stats['json_bytes_after']) / stats['json_bytes_before'] * 100)
        print(f"  Total reduction:      {total_reduction:.1f}%")
    print(f"\nFinal archive:")
    print(f"  Location:             {zip_path}")
    print(f"  Size:                 {zip_size:,} bytes ({zip_size / 1024 / 1024:.2f} MB)")
    print("=" * 60)

if __name__ == "__main__":
    build_release()
