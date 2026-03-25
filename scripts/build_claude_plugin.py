from build_release_artifacts import CLAUDE_ROOT, build_release_artifacts


if __name__ == "__main__":
    build_release_artifacts(include_runtime=False, include_claude=True)
    print(f"Generated Claude plugin package at {CLAUDE_ROOT}")

