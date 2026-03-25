from build_release_artifacts import RUNTIME_ROOT, build_release_artifacts


if __name__ == "__main__":
    build_release_artifacts(include_runtime=True, include_claude=False)
    print(f"Generated npx runtime package at {RUNTIME_ROOT}")

