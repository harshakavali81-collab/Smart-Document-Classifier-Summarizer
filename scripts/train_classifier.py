"""Train and export demo classifier. Only load locally trusted joblib outputs."""
import argparse
from pathlib import Path
import joblib
from src.classification.model import load_examples, train

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="runtime/classifier.joblib")
    args = parser.parse_args()
    model = train(load_examples())
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    print(f"Trained synthetic model, exported to {path} (do not unpickle untrusted files).")

if __name__ == "__main__":
    main()
