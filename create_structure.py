from pathlib import Path

BASE_DIR = Path(".")

STRUCTURE = [
    "data/raw",
    "data/interim",
    "data/processed",
    "data/labels",

    "src",
    "src/config",
    "src/preprocessing",
    "src/datasets",
    "src/models",
    "src/training",
    "src/inference",
    "src/monitoring",
    "src/governance",
    "src/utils",

    "scripts",
    "tests",
    "artifacts/models",
    "artifacts/metrics",
    "artifacts/explanations",
]

FILES = [
    "README.md",
    "pyproject.toml",

    "src/config/base.yaml",
    "src/config/training.yaml",
    "src/config/inference.yaml",
    "src/config/routing.yaml",

    "src/preprocessing/email_cleaner.py",
    "src/preprocessing/normalizer.py",
    "src/preprocessing/tokenizer.py",

    "src/datasets/email_dataset.py",
    "src/datasets/label_schema.py",

    "src/models/classifier.py",
    "src/models/calibration.py",
    "src/models/explainability.py",

    "src/training/train.py",
    "src/training/evaluate.py",
    "src/training/retrain.py",

    "src/inference/predict.py",
    "src/inference/router.py",
    "src/inference/postprocess.py",

    "src/monitoring/drift.py",
    "src/monitoring/metrics.py",
    "src/monitoring/alerts.py",

    "src/governance/model_card.py",
    "src/governance/audit_log.py",
    "src/governance/approval.py",

    "src/utils/logging.py",
    "src/utils/io.py",

    "scripts/bootstrap_labels.py",
    "scripts/run_training.sh",
    "scripts/deploy_model.sh",

    "tests/test_preprocessing.py",
    "tests/test_inference.py",
    "tests/test_routing.py",
]

GITIGNORE_CONTENT = """
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so
*.egg-info/
.eggs/

# Virtual environments
.venv/
venv/
env/

# IDEs / Editors
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Data & artifacts
data/raw/
data/interim/
data/processed/
artifacts/
models/

# ML / DL
checkpoints/
wandb/
mlruns/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/
"""

def main():
    # Create directories
    for folder in STRUCTURE:
        path = BASE_DIR / folder
        path.mkdir(parents=True, exist_ok=True)

        # Add __init__.py to Python packages under src
        if path.parts and path.parts[0] == "src":
            init_file = path / "__init__.py"
            init_file.touch(exist_ok=True)

    # Create files
    for file in FILES:
        path = BASE_DIR / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    # Create .gitignore
    gitignore_path = BASE_DIR / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(GITIGNORE_CONTENT.strip())

    print("✅ Project structure created successfully")
    print("✅ __init__.py files added")
    print("✅ .gitignore created")

if __name__ == "__main__":
    main()