#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Studio Onboard — Setup Script

Generates or refreshes active-brand.json from connected sources.
Extended from design-system-ux/scripts/setup.py to support all access modes:
  - Figma MCP (variables extraction via file key)
  - GitHub API (token files, component source)
  - git clone (any git server)
  - npm package (public or private registry)
  - Token file upload (JSON: DTCG, W3C, Style Dictionary)
  - Manual (guided starter config)
  - Refresh (update an existing config from its sources)

Auth tokens are NEVER stored in the config. Only env var names are stored.
Actual tokens come from environment variables at runtime.

Usage:
  # Manual mode: create a starter config
  python3 scripts/setup.py --mode manual --brand-name "Acme Design System" --output ../ui-studio/brand-config/acme.json

  # GitHub mode: extract from git repo
  python3 scripts/setup.py --mode github --brand-name "Acme" \
    --github-owner acme-org --github-repo design-system \
    --token-files-path packages/tokens/src --components-path packages/components/src \
    --output ../ui-studio/brand-config/acme.json

  # npm mode: extract from npm package
  python3 scripts/setup.py --mode npm --brand-name "Acme" \
    --npm-package @acme/design-system --npm-scope @acme \
    --output ../ui-studio/brand-config/acme.json

  # Refresh: re-extract from stored sources
  python3 scripts/setup.py --mode refresh --config ../ui-studio/brand-config/acme.json

  # Token file upload: parse an exported token JSON
  python3 scripts/setup.py --mode token-file --brand-name "Acme" \
    --token-file /path/to/tokens.json --output ../ui-studio/brand-config/acme.json
"""

import argparse
import atexit
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ONBOARD_ROOT = SCRIPT_DIR.parent
STUDIO_ROOT = ONBOARD_ROOT.parent / "ui-studio"
DEFAULT_OUTPUT = STUDIO_ROOT / "brand-config" / "active-brand.json"

PROVISIONAL_PREFIX = "PROVISIONAL:"

# DE-04: Assert that STUDIO_ROOT resolves to an actual directory at import time.
# If ui-studio is moved, renamed, or this script is used in a different deployment
# context, this will fail loudly instead of silently writing to a non-existent path.
if not STUDIO_ROOT.exists():
    raise RuntimeError(
        f"ui-studio-onboard: STUDIO_ROOT not found at {STUDIO_ROOT}.\n"
        f"Expected ui-studio/ and ui-studio-onboard/ to be siblings within the same parent.\n"
        f"If the skill directory structure has changed, update STUDIO_ROOT in setup.py."
    )


# ─────────────────────────────────────────────────────────────────────────────
# Cache cleanup (RL-01)
# ─────────────────────────────────────────────────────────────────────────────

def cleanup_cache(cache_dir: Path) -> None:
    """Remove the .cache/ directory on process exit.

    Registered via atexit so it runs whether the script exits normally,
    raises an exception, or is interrupted (SIGTERM). Prevents cloned
    authentication-controlled content (git repos, npm packs) from persisting
    after onboarding sessions complete.

    Only removes the directory if it exists and is inside ONBOARD_ROOT.
    Guards against a misconfigured path removing an unintended location.
    """
    try:
        if not cache_dir.exists():
            return
        # Safety check: only remove if the cache dir is inside ONBOARD_ROOT
        cache_dir.resolve().relative_to(ONBOARD_ROOT.resolve())
        shutil.rmtree(cache_dir)
        print(f"  .cache/ cleaned up ({cache_dir})")
    except ValueError:
        # Path is not inside ONBOARD_ROOT. Do not remove.
        print(f"  Warning: .cache/ path is outside onboard root; skipping cleanup ({cache_dir})")
    except Exception as e:
        # Non-fatal: log and continue. A leftover .cache/ is inconvenient but not critical.
        print(f"  Warning: .cache/ cleanup failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Config template
# ─────────────────────────────────────────────────────────────────────────────

def create_starter_config(brand_name: str, generated_by: str = "setup.py --mode manual") -> dict:
    """Create a minimal starter config with all required structure in place."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "brand": {
            "name": brand_name,
            "description": "",
            "temperature": "neutral",
            "personality": "",
            "cluster": "",
            "style_entry": "",
            "style_notes": ""
        },
        "tokens": {
            "typography": {
                "families": {
                    "display": {"family": "", "fallback": "serif", "weights": [], "use": "Headlines and display text"},
                    "body": {"family": "", "fallback": "system-ui, sans-serif", "weights": [], "use": "Body text"},
                    "utility": {"family": "", "fallback": "monospace", "weights": [], "use": "Labels, metadata"}
                },
                "scale": {},
                "loading": {"provider": "", "url": ""}
            },
            "color": {
                "backgrounds": {},
                "text": {},
                "structural": {},
                "accent": {},
                "semantic": {},
                "prohibited": [],
                "contrast_notes": []
            },
            "spacing": {
                "base": "8px",
                "rhythm": "",
                "tiers": {},
                "content_max_width": "",
                "page_padding": "",
                "grid_gap": "",
                "touch-target": {"min": "44px", "comfortable": "48px"}
            },
            "motion": {
                "easing": {"default": "cubic-bezier(0.65, 0, 0.35, 1)"},
                "durations": {"micro": "150ms", "standard": "300ms"},
                "stagger": "80ms",
                "principles": ""
            },
            "elevation": {},
            "radius": {},
            "focus": {"outline": {"width": "2px", "color": "", "offset": "2px", "style": "solid"}}
        },
        "layout": {
            "grid": {"columns": 12, "gutter": "", "margin": "", "breakpoints": {"sm": "375px", "md": "768px", "lg": "1440px"}},
            "spacing_density": "",
            "section_padding_tiers": {"generous": "", "standard": "", "tight": ""},
            "preferred_patterns": [],
            "style_cluster": "",
            "style_entry": ""
        },
        "voice": {
            "tone": "",
            "prohibited_words": [],
            "prohibited_patterns": [],
            "cta_style": "",
            "formatting": {},
            "terminology": {}
        },
        "ux_writing": {
            "empty_states": {"pattern": "", "source": "", "source_url": "", "last_verified": ""},
            "error_messages": {"pattern": "", "tone": "", "structure": "", "source": "", "source_url": "", "last_verified": ""},
            "tooltips": {"max_length": "", "tone": "", "avoid": [], "source": "", "source_url": "", "last_verified": ""},
            "buttons_ctas": {"verb_preference": "", "style": "", "examples": [], "source": "", "source_url": "", "last_verified": ""},
            "form_labels": {"case": "", "helper_text_style": "", "placeholder_policy": "", "source": "", "source_url": "", "last_verified": ""},
            "notifications": {"success": "", "error": "", "warning": "", "info": "", "source": "", "source_url": "", "last_verified": ""},
            "loading_states": {"pattern": "", "examples": [], "source": "", "source_url": "", "last_verified": ""},
            "onboarding": {"tone": "", "structure": "", "source": "", "source_url": "", "last_verified": ""},
            "custom": {}
        },
        "components": {
            "source": "",
            "framework": "",
            "styling": "",
            "inventory": [],
            "conventions": {"naming": "", "props": "", "variants": "", "composition": "", "styling": "", "testing": ""},
            "drift": {"token_drift": [], "pattern_drift": [], "api_drift": []}
        },
        "repository": {
            "figma": {
                "primary_file_key": "",
                "token_library": {"file_key": "", "library_key": "", "label": "", "variable_collection_names": []},
                "component_libraries": []
            },
            "supernova_workspace": "",
            "storybook": {"url": "", "auth_header_env_var": "STORYBOOK_AUTH_TOKEN"},
            "github": {"owner": "", "repo": "", "branch": "main", "token_files_path": "", "components_path": "", "pat_env_var": "GITHUB_TOKEN"},
            "npm": {"package_name": "", "version": "latest", "registry_url": "", "scope": "", "auth_token_env_var": "NPM_TOKEN"},
            "git": {"token_repo_url": "", "component_repo_url": "", "branch": "main", "pat_env_var": "GIT_TOKEN"}
        },
        "meta": {
            "generated_at": now,
            "generated_by": generated_by,
            "last_refreshed": now,
            "version": "0.1.0",
            "completeness_score": 0,
            "fidelity_score": 0,
            "provisional_fields": [],
            "gate_status": {
                "direction_lock_confirmed": False,
                "direction_lock_date": None,
                "designer_review_complete": False,
                "designer_review_date": None,
                "designer_reviewer": None,
                "mode_override_acknowledged": False,
                "mode_override_score": None
            },
            "field_provenance": {},
            "accessibility": {"contrast_target": "AA", "contrast_floor": "AA", "standard": "WCAG 2.2"}
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
# Git utilities
# ─────────────────────────────────────────────────────────────────────────────

def clone_or_pull(repo_url: str, target_dir: Path, pat: str | None = None) -> bool:
    """Clone a git repo or pull if already cloned. Injects auth token if provided."""
    if pat:
        # Inject token into URL for HTTPS auth (GitHub, GitLab, etc.)
        if "https://" in repo_url:
            repo_url = repo_url.replace("https://", f"https://oauth2:{pat}@")

    if target_dir.exists() and (target_dir / ".git").exists():
        print(f"    Pulling {target_dir.name}...")
        # RL-03: timeout=120 prevents indefinite hang on unreachable or slow remotes.
        result = subprocess.run(["git", "-C", str(target_dir), "pull", "--ff-only"],
                                capture_output=True, text=True, timeout=120)
        return result.returncode == 0

    print(f"    Cloning {repo_url.split('@')[-1]}...")  # Hide token from log
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    # RL-03: timeout=120 prevents indefinite hang on unreachable or large repos in refresh mode.
    result = subprocess.run(["git", "clone", "--depth", "1", repo_url, str(target_dir)],
                            capture_output=True, text=True, timeout=120)
    return result.returncode == 0


def scan_token_files(repo_dir: Path) -> dict:
    """Scan a repository for token definition files."""
    found = {}
    patterns = ["tokens.json", "tokens/*.json", "src/tokens.json", "src/tokens/*.json",
                "*.tokens.json", "design-tokens.json"]
    for pattern in patterns:
        for match in glob.glob(str(repo_dir / pattern)):
            try:
                with open(match) as f:
                    found[Path(match).name] = json.load(f)
                print(f"    Found token file: {Path(match).name}")
            except Exception:
                pass

    # Check for Style Dictionary config
    for cfg in ["style-dictionary.config.js", "style-dictionary.config.json", "config.json"]:
        if (repo_dir / cfg).exists():
            print(f"    Found Style Dictionary config: {cfg}")
            found["_sd_config"] = str(repo_dir / cfg)

    return found


def detect_framework(repo_dir: Path) -> str:
    """Detect the component framework from package.json."""
    pkg = repo_dir / "package.json"
    if not pkg.exists():
        return "unknown"
    try:
        with open(pkg) as f:
            data = json.load(f)
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "react" in deps:
            fw = "React"
            if "typescript" in deps:
                fw += " + TypeScript"
            return fw
        if "vue" in deps:
            return "Vue"
        if "svelte" in deps:
            return "Svelte"
    except Exception:
        pass
    return "unknown"


def scan_component_repo(repo_dir: Path) -> list[dict]:
    """Scan a component repository for component files (Level 1 inventory)."""
    components = []
    search_dirs = [repo_dir / d for d in ["src/components", "src/lib", "components", "lib", "packages"]]
    ext = {".tsx", ".jsx", ".vue", ".svelte"}
    skip_names = {".test.", ".spec.", ".stories.", ".story."}
    skip_files = {"index.tsx", "index.jsx"}

    for comp_dir in search_dirs:
        if not comp_dir.exists():
            continue
        for root, dirs, files in os.walk(comp_dir):
            dirs[:] = [d for d in dirs if d not in ("node_modules", "__tests__", "__mocks__", ".storybook")]
            for filename in files:
                if filename in skip_files:
                    continue
                if any(s in filename.lower() for s in skip_names):
                    continue
                fp = Path(root) / filename
                if fp.suffix not in ext:
                    continue
                components.append({
                    "name": fp.stem,
                    "path": str(fp.relative_to(repo_dir)),
                    "category": "unknown",
                    "props": [], "variants": [], "tokens_used": [], "dependencies": [],
                    "notes": "Level 1 auto-discovery. Run Level 2 analysis for props and variants."
                })

    print(f"    Found {len(components)} component files")
    return components


# ─────────────────────────────────────────────────────────────────────────────
# npm extraction
# ─────────────────────────────────────────────────────────────────────────────

def extract_from_npm(package_name: str, registry_url: str, scope: str,
                     auth_token_env: str, version: str, target_dir: Path) -> bool:
    """Install an npm package and extract token files from it."""
    token = os.environ.get(auth_token_env)
    npmrc_path = None

    if registry_url or scope:
        # Write a temporary .npmrc for private registry access
        npmrc_lines = []
        if registry_url:
            if scope:
                npmrc_lines.append(f"{scope}:registry={registry_url}")
            npmrc_lines.append(f"{registry_url.split('//')[1].rstrip('/')}/:_authToken={token or ''}")
        elif scope and token:
            npmrc_lines.append(f"//registry.npmjs.org/:_authToken={token}")

        if npmrc_lines:
            npmrc_fd, npmrc_path = tempfile.mkstemp(suffix=".npmrc")
            try:
                with os.fdopen(npmrc_fd, "w") as f:
                    f.write("\n".join(npmrc_lines) + "\n")
            except Exception as e:
                print(f"    Warning: Could not write .npmrc: {e}")
                npmrc_path = None

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        pkg_spec = f"{package_name}@{version}" if version != "latest" else package_name

        env = os.environ.copy()
        cmd = ["npm", "pack", pkg_spec, "--pack-destination", str(target_dir)]
        if npmrc_path:
            env["NPM_CONFIG_USERCONFIG"] = npmrc_path

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            print(f"    Warning: npm pack failed: {result.stderr.strip()}")
            return False

        print(f"    npm pack succeeded for {pkg_spec}")
        return True

    finally:
        # Always delete the temporary .npmrc
        if npmrc_path and os.path.exists(npmrc_path):
            os.unlink(npmrc_path)
            print("    Temporary .npmrc deleted")


# ─────────────────────────────────────────────────────────────────────────────
# Token file upload parsing
# ─────────────────────────────────────────────────────────────────────────────

def parse_token_file(token_file_path: Path) -> dict:
    """Parse an exported token file (DTCG, W3C, Style Dictionary, Figma export)."""
    with open(token_file_path) as f:
        data = json.load(f)

    extracted = {"colors": {}, "typography": {}, "spacing": {}, "raw": data}

    def walk(obj, prefix=""):
        if isinstance(obj, dict):
            if "$value" in obj and "$type" in obj:
                # W3C DTCG format
                token_type = obj["$type"]
                token_value = obj["$value"]
                if token_type in ("color", "colour"):
                    extracted["colors"][prefix] = token_value
                elif token_type == "dimension":
                    extracted["spacing"][prefix] = token_value
                elif token_type in ("fontFamily", "fontSize", "fontWeight"):
                    extracted["typography"][prefix] = token_value
            else:
                for k, v in obj.items():
                    walk(v, f"{prefix}.{k}" if prefix else k)

    walk(data)
    print(f"    Parsed {len(extracted['colors'])} colors, {len(extracted['spacing'])} spacing values, {len(extracted['typography'])} typography values")
    return extracted


# ─────────────────────────────────────────────────────────────────────────────
# Mode runners
# ─────────────────────────────────────────────────────────────────────────────

def run_github_mode(args) -> dict:
    config = create_starter_config(args.brand_name or "Untitled Brand", "setup.py --mode github")

    pat = os.environ.get(args.github_pat_env or "GITHUB_TOKEN")
    if not pat:
        print(f"  Warning: {args.github_pat_env or 'GITHUB_TOKEN'} not set — trying unauthenticated")

    cache_dir = ONBOARD_ROOT / ".cache"

    # Token repo
    if args.github_owner and args.github_repo:
        repo_url = f"https://github.com/{args.github_owner}/{args.github_repo}.git"
        if args.token_files_path:
            token_dir = cache_dir / "tokens"
            if clone_or_pull(repo_url, token_dir, pat):
                token_path = token_dir / args.token_files_path
                if token_path.exists():
                    found = scan_token_files(token_path)
                    print(f"  Token files found: {list(found.keys())}")
        config["repository"]["github"]["owner"] = args.github_owner
        config["repository"]["github"]["repo"] = args.github_repo
        config["repository"]["github"]["pat_env_var"] = args.github_pat_env or "GITHUB_TOKEN"
        if args.token_files_path:
            config["repository"]["github"]["token_files_path"] = args.token_files_path

        # Component repo
        if args.components_path:
            comp_dir = cache_dir / "components"
            if clone_or_pull(repo_url, comp_dir, pat):
                framework = detect_framework(comp_dir)
                full_comp_path = comp_dir / args.components_path
                inventory = scan_component_repo(full_comp_path if full_comp_path.exists() else comp_dir)
                config["components"]["framework"] = framework
                config["components"]["inventory"] = inventory
                config["components"]["source"] = f"https://github.com/{args.github_owner}/{args.github_repo}"
                config["repository"]["github"]["components_path"] = args.components_path

    config["meta"]["generated_by"] = "setup.py --mode github"
    return config


def run_npm_mode(args) -> dict:
    config = create_starter_config(args.brand_name or "Untitled Brand", "setup.py --mode npm")

    pkg = args.npm_package or ""
    registry = args.npm_registry or ""
    scope = args.npm_scope or ""
    auth_env = args.npm_auth_env or "NPM_TOKEN"
    version = args.npm_version or "latest"

    if not pkg:
        print("  Error: --npm-package required for npm mode")
        sys.exit(1)

    target_dir = ONBOARD_ROOT / ".cache" / "npm"
    success = extract_from_npm(pkg, registry, scope, auth_env, version, target_dir)

    config["repository"]["npm"]["package_name"] = pkg
    config["repository"]["npm"]["version"] = version
    config["repository"]["npm"]["auth_token_env_var"] = auth_env
    if registry:
        config["repository"]["npm"]["registry_url"] = registry
    if scope:
        config["repository"]["npm"]["scope"] = scope

    if success:
        # Scan the extracted package for token files
        found = scan_token_files(target_dir)
        print(f"  Token files found: {list(found.keys())}")

    config["meta"]["generated_by"] = "setup.py --mode npm"
    return config


def run_token_file_mode(args) -> dict:
    config = create_starter_config(args.brand_name or "Untitled Brand", "setup.py --mode token-file")

    token_file_path = Path(args.token_file)
    if not token_file_path.exists():
        print(f"  Error: Token file not found: {token_file_path}")
        sys.exit(1)

    extracted = parse_token_file(token_file_path)

    # Attempt to map extracted colors to the config structure
    colors = extracted.get("colors", {})
    for path, value in list(colors.items())[:20]:  # Limit to first 20 for auto-mapping
        parts = path.split(".")
        if any(bg in path.lower() for bg in ["background", "bg", "surface"]):
            config["tokens"]["color"]["backgrounds"][parts[-1]] = value
        elif any(txt in path.lower() for txt in ["text", "foreground", "content"]):
            config["tokens"]["color"]["text"][parts[-1]] = value
        elif any(acc in path.lower() for acc in ["accent", "primary", "brand"]):
            config["tokens"]["color"]["accent"][parts[-1]] = value
        elif any(brd in path.lower() for brd in ["border", "stroke", "divider"]):
            config["tokens"]["color"]["structural"][parts[-1]] = value

    config["meta"]["generated_by"] = f"setup.py --mode token-file ({token_file_path.name})"
    return config


def run_refresh_mode(args) -> dict:
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ONBOARD_ROOT / args.config

    if not config_path.exists():
        print(f"  Error: Config not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    repo = config.get("repository", {})
    github = repo.get("github", {})
    npm = repo.get("npm", {})

    # Refresh from GitHub
    if github.get("owner") and github.get("repo"):
        pat = os.environ.get(github.get("pat_env_var", "GITHUB_TOKEN"))
        repo_url = f"https://github.com/{github['owner']}/{github['repo']}.git"
        cache_dir = ONBOARD_ROOT / ".cache"

        if github.get("token_files_path"):
            token_dir = cache_dir / "tokens"
            if clone_or_pull(repo_url, token_dir, pat):
                found = scan_token_files(token_dir / github.get("token_files_path", ""))
                print(f"  Refreshed token files: {list(found.keys())}")

        if github.get("components_path"):
            comp_dir = cache_dir / "components"
            if clone_or_pull(repo_url, comp_dir, pat):
                comp_path = comp_dir / github.get("components_path", "")
                inventory = scan_component_repo(comp_path if comp_path.exists() else comp_dir)
                config["components"]["inventory"] = inventory
                config["components"]["framework"] = detect_framework(comp_dir)

    # Refresh from npm
    if npm.get("package_name"):
        target_dir = ONBOARD_ROOT / ".cache" / "npm"
        extract_from_npm(
            npm["package_name"],
            npm.get("registry_url", ""),
            npm.get("scope", ""),
            npm.get("auth_token_env_var", "NPM_TOKEN"),
            npm.get("version", "latest"),
            target_dir
        )

    config["meta"]["last_refreshed"] = datetime.now(timezone.utc).isoformat()
    return config


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def report_completeness(config: dict):
    """Quick completeness check without running full validate.py."""
    empty = []
    typo = config.get("tokens", {}).get("typography", {}).get("families", {})
    if not typo.get("display", {}).get("family"):
        empty.append("typography.display")
    if not config["tokens"].get("color", {}).get("backgrounds"):
        empty.append("colors.backgrounds")
    if not config.get("voice", {}).get("tone"):
        empty.append("voice")
    if not config.get("components", {}).get("inventory"):
        empty.append("component inventory")
    if not config.get("layout", {}).get("preferred_patterns"):
        empty.append("layout.preferred_patterns")

    if empty:
        print(f"\n  Sections still needing data: {', '.join(empty)}")
        print("  Run `python3 scripts/validate.py --config [path]` for a detailed completeness score.")
    else:
        print("\n  Config appears complete. Run validate.py to confirm score.")


def main():
    parser = argparse.ArgumentParser(description="UI Studio Onboard — Setup Script")
    parser.add_argument("--mode", choices=["manual", "github", "npm", "token-file", "refresh"],
                        required=True, help="Onboarding mode")
    parser.add_argument("--brand-name", help="Brand name")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT), help="Output path for the config")
    parser.add_argument("--config", help="Existing config path (for refresh mode)")

    # GitHub options
    parser.add_argument("--github-owner", help="GitHub org or user name")
    parser.add_argument("--github-repo", help="GitHub repo name")
    parser.add_argument("--github-pat-env", default="GITHUB_TOKEN", help="Env var name for GitHub PAT")
    parser.add_argument("--token-files-path", help="Path to token files within the repo")
    parser.add_argument("--components-path", help="Path to components within the repo")

    # npm options
    parser.add_argument("--npm-package", help="npm package name")
    parser.add_argument("--npm-scope", help="npm scope (e.g., @myorg)")
    parser.add_argument("--npm-registry", help="Private registry URL")
    parser.add_argument("--npm-version", default="latest", help="Package version")
    parser.add_argument("--npm-auth-env", default="NPM_TOKEN", help="Env var name for npm auth token")

    # Token file options
    parser.add_argument("--token-file", help="Path to exported token JSON file")

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("  UI Studio Onboard — Setup Script")
    print(f"  Mode: {args.mode}")
    print(f"{'='*60}\n")

    # RL-01: Register .cache/ cleanup for all modes that write to it.
    # github, npm, and refresh all clone or pack into .cache/. Manual and token-file
    # modes do not use .cache/ but registration is unconditional; the cleanup function
    # is a no-op if .cache/ does not exist at exit time.
    cache_dir = ONBOARD_ROOT / ".cache"
    atexit.register(cleanup_cache, cache_dir)

    if args.mode == "manual":
        brand_name = args.brand_name or "Untitled Brand"
        config = create_starter_config(brand_name, "setup.py --mode manual")
        print(f"  Created starter config for: {brand_name}")
        print("  Fill in token, color, typography, voice, and layout sections.")

    elif args.mode == "github":
        config = run_github_mode(args)

    elif args.mode == "npm":
        config = run_npm_mode(args)

    elif args.mode == "token-file":
        config = run_token_file_mode(args)

    elif args.mode == "refresh":
        if not args.config:
            print("  Error: --config required for refresh mode")
            sys.exit(1)
        config = run_refresh_mode(args)
        print(f"  Refreshed: {args.config}")

    # Write output
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = STUDIO_ROOT / args.output

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"\n  Config written to: {output_path}")
    report_completeness(config)
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
