from git_changelog import build, versioning  # noqa

# Create a changelog object to determine versions
changes = build.Changelog(
    repository=".",
    convention="angular",
    provider="gitlab",
    parse_trailers=True,
    sections=("build", "deps", "feat", "fix", "refactor"),
    versioning="semver",
    bump="auto",
    zerover=False,
)

# Get our next version
next_version = changes.versions_list[0].planned_tag

if next_version is None:
    # If we don't have one, start at 0.1.0
    print("0.1.0")  # noqa T201
else:
    # Otherwise, get just the version string to pass to Hatch
    print(versioning.version_prefix(next_version)[0])  # noqa T201
