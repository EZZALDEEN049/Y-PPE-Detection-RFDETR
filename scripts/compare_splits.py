import argparse
import hashlib
from pathlib import Path
from typing import Dict, Iterable, Set

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
SPLIT_ALIASES = {
    "train": ("train",),
    "valid": ("valid", "val", "validation"),
    "test": ("test",),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def locate_split(dataset_root: Path, aliases: Iterable[str]) -> Path:
    aliases_lower = {alias.lower() for alias in aliases}
    candidates = []
    for path in dataset_root.rglob("*"):
        if path.is_dir() and path.name.lower() in aliases_lower:
            candidates.append(path)

    if not candidates:
        raise FileNotFoundError(
            f"Could not locate split {sorted(aliases_lower)} under {dataset_root}"
        )

    # Prefer the shallowest matching directory, e.g. dataset/train rather than nested paths.
    return min(candidates, key=lambda p: len(p.relative_to(dataset_root).parts))


def collect_hashes(dataset_root: Path) -> Dict[str, Set[str]]:
    result: Dict[str, Set[str]] = {}
    for canonical, aliases in SPLIT_ALIASES.items():
        split_root = locate_split(dataset_root, aliases)
        files = list(image_files(split_root))
        result[canonical] = {sha256_file(path) for path in files}
        print(
            f"{dataset_root.name}: {canonical}: "
            f"{len(files)} image files, {len(result[canonical])} unique hashes"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare train/valid/test image membership between two exported datasets."
    )
    parser.add_argument("dataset_a", type=Path, help="Path to the first exported dataset")
    parser.add_argument("dataset_b", type=Path, help="Path to the second exported dataset")
    args = parser.parse_args()

    if not args.dataset_a.exists() or not args.dataset_b.exists():
        raise SystemExit("Both dataset paths must exist.")

    hashes_a = collect_hashes(args.dataset_a)
    hashes_b = collect_hashes(args.dataset_b)

    print("\n=== Split identity report ===")
    all_identical = True

    for split in ("train", "valid", "test"):
        a = hashes_a[split]
        b = hashes_b[split]
        only_a = a - b
        only_b = b - a
        intersection = a & b
        identical = a == b
        all_identical &= identical

        print(f"\n{split.upper()}")
        print(f"  Dataset A unique images: {len(a)}")
        print(f"  Dataset B unique images: {len(b)}")
        print(f"  Shared images:           {len(intersection)}")
        print(f"  Only in Dataset A:       {len(only_a)}")
        print(f"  Only in Dataset B:       {len(only_b)}")
        print(f"  Identical membership:    {'YES' if identical else 'NO'}")

    print("\n=== Overall conclusion ===")
    if all_identical:
        print("PASS: train/valid/test image membership is identical by SHA-256.")
    else:
        print(
            "NOT CONTROLLED: at least one split differs. Re-evaluate both models on "
            "one common held-out test set before making a strict architecture comparison."
        )


if __name__ == "__main__":
    main()
