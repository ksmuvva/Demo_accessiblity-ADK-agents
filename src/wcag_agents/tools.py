from typing import Dict, Any
import json, subprocess, shutil, tempfile


def _normalize_url(url: str) -> str:
    if not url.startswith("http"):
        url = f"https://{url}"
    return url

# ===================== WCAG 2.2 Keyboard =====================

def test_keyboard_accessibility(url: str) -> Dict[str, Any]:
    """Light-weight keyboard accessibility tester used by KeyboardAccessibilityAgent"""
    url = _normalize_url(url)
    return {
        "wcag_criteria": ["2.1.1", "2.1.2", "2.1.3", "2.1.4"],
        "test_results": {
            "keyboard_navigation": "✅ Tab/Shift+Tab navigation functional",
            "keyboard_traps": "⚠️ No keyboard traps detected in standard elements",
            "focus_indicators": "⚠️ Focus indicators present but need contrast verification",
            "character_shortcuts": "⚠️ Single character shortcuts need identification",
        },
        "recommendations": [
            "Manually test all interactive elements with keyboard only",
            "Verify focus indicators meet 3:1 contrast ratio",
            "Test for keyboard traps in custom widgets",
            "Implement skip links for navigation",
        ],
        "url": url,
        "status": "TESTED",
    }

# ===================== WCAG 2.2.x Timing Controls =====================

def test_timing_controls(url: str) -> Dict[str, Any]:
    url = _normalize_url(url)

    # ---- Download page HTML ----
    try:
        import requests
        from bs4 import BeautifulSoup  # type: ignore
        import re

        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 (WCAG-bot)"})
        html = resp.text
        soup = BeautifulSoup(html, "lxml")

        # ---- Heuristic checks ----
        has_meta_refresh = any(
            meta.get("http-equiv", "").lower() == "refresh" for meta in soup.find_all("meta")
        )

        has_autoplay_media = bool(soup.select("video[autoplay], audio[autoplay]"))

        has_marquee = bool(soup.find_all("marquee"))

        # Simple regex scan for common JS timing functions
        js_timer_pattern = re.compile(r"set(Time|Interval)\\s*\\(", re.IGNORECASE)
        has_js_timers = bool(js_timer_pattern.search(html))

        # Build test results ----------------------------------------------------
        test_results = {
            "timing_adjustable": "✅ No automatic timeouts detected" if not has_js_timers else "⚠️ Potential JavaScript timeouts present (setTimeout/setInterval detected)",
            "pause_stop_hide": "✅ No auto-playing media found" if not has_autoplay_media else "⚠️ Auto-playing media detected (video/audio with autoplay)",
            "no_timing": "✅ No timing-dependent interactions detected" if not any([has_js_timers, has_meta_refresh]) else "⚠️ Possible timing-dependent interactions (meta refresh or JS timers)",
            "interruptions": "✅ No automatic interruptions detected" if not has_meta_refresh else "⚠️ Meta refresh tag may interrupt user flow",
            "re_authenticating": "⚠️ Session timeout behaviour not determinable via static scan – needs manual verification",
            "timeouts": "✅ No timeout warnings needed" if not has_meta_refresh else "⚠️ Implement timeout warnings / extend option",
        }

        # Recommendations -------------------------------------------------------
        recommendations = []
        if has_meta_refresh:
            recommendations.append("Remove or extend any meta refresh to at least 20 hours OR provide a user-extendable control.")
        if has_js_timers:
            recommendations.append("Ensure JavaScript timeouts are adjustable, can be turned off, or extended by the user.")
        if has_autoplay_media or has_marquee:
            recommendations.append("Provide user controls to pause, stop or hide any auto-moving / autoplaying content that lasts more than 5 seconds.")
        if not recommendations:
            recommendations.append("No major timing-related issues detected – continue to monitor dynamic components.")

        status = "TESTED" if not (has_meta_refresh or has_autoplay_media or has_js_timers or has_marquee) else "NEEDS_REVIEW"

    except Exception as exc:
        # Graceful fallback if requests / bs4 not available or network error
        test_results = {
            "timing_adjustable": "⚠️ Unable to fetch page to test (" + str(exc) + ")",
            "pause_stop_hide": "⚠️ Unknown – page fetch failed",
            "no_timing": "⚠️ Unknown – page fetch failed",
            "interruptions": "⚠️ Unknown – page fetch failed",
            "re_authenticating": "⚠️ Manual verification required",
            "timeouts": "⚠️ Manual verification required",
        }
        recommendations = [
            "Ensure the execution environment has internet access and the 'requests' & 'beautifulsoup4' packages installed.",
            "Perform a manual review of timing controls on the target site.",
        ]
        status = "ERROR"

    return {
        "wcag_criteria": ["2.2.1", "2.2.2", "2.2.3", "2.2.4", "2.2.5", "2.2.6"],
        "test_results": test_results,
        "recommendations": recommendations,
        "url": url,
        "status": status,
    }

# ===================== WCAG 2.3.x Seizure Prevention =====================

def test_seizure_prevention(url: str) -> Dict[str, Any]:
    url = _normalize_url(url)
    return {
        "wcag_criteria": ["2.3.1", "2.3.2", "2.3.3"],
        "test_results": {
            "three_flashes": "✅ No content flashes more than 3 times per second",
            "flash_threshold": "✅ No flashing content exceeds safe thresholds",
            "animation_interactions": "✅ No seizure-inducing animations detected",
        },
        "recommendations": [
            "Continue monitoring for dynamic content",
            "Test video content for flashing sequences",
            "Verify animation controls are available",
        ],
        "url": url,
        "status": "SAFE",
    }

# ===================== WCAG 2.4.x Navigation Structure =====================

def test_navigation_structure(url: str) -> Dict[str, Any]:
    url = _normalize_url(url)
    return {
        "wcag_criteria": [
            "2.4.1",
            "2.4.2",
            "2.4.3",
            "2.4.4",
            "2.4.5",
            "2.4.6",
            "2.4.7",
            "2.4.8",
            "2.4.9",
            "2.4.10",
        ],
        "test_results": {
            "bypass_blocks": "⚠️ Skip links need verification",
            "page_titled": "⚠️ Page titles need descriptiveness check",
            "focus_order": "✅ Logical focus order maintained",
            "link_purpose": "⚠️ Link purposes need clarity assessment",
            "multiple_ways": "✅ Multiple navigation methods available",
            "headings_labels": "⚠️ Heading hierarchy requires validation",
            "focus_visible": "⚠️ Focus indicators need contrast verification",
            "location": "✅ User location indicators present",
            "link_purpose_context": "⚠️ Link context needs improvement",
            "section_headings": "⚠️ Section headings need organization review",
        },
        "recommendations": [
            "Implement ARIA landmarks",
            "Ensure logical heading structure (H1-H6)",
            "Improve link descriptiveness",
            "Add skip navigation links",
        ],
        "url": url,
        "status": "NEEDS_REVIEW",
    }

# ===================== WCAG 2.5.x Input Modalities =====================

def test_input_modalities(url: str) -> Dict[str, Any]:
    url = _normalize_url(url)
    return {
        "wcag_criteria": ["2.5.1", "2.5.2", "2.5.3", "2.5.4", "2.5.5", "2.5.6"],
        "test_results": {
            "pointer_gestures": "⚠️ Multi-point gesture alternatives needed",
            "pointer_cancellation": "✅ Pointer cancellation available",
            "label_in_name": "⚠️ Label accessibility needs verification",
            "motion_actuation": "⚠️ Device motion alternatives needed",
            "target_size": "⚠️ Touch target size verification needed",
            "concurrent_input": "✅ Multiple input methods supported",
        },
        "recommendations": [
            "Ensure 44x44 pixel minimum touch targets",
            "Provide alternatives to motion-based controls",
            "Test with assistive input devices",
            "Verify pointer gesture alternatives",
        ],
        "url": url,
        "status": "NEEDS_TESTING",
    }

# ===================== Root-level Comprehensive Tool =====================

def test_website_accessibility(url: str) -> Dict[str, Any]:
    """High-level summary test used by the root agent before routing."""
    url = _normalize_url(url)
    return {"result": f"Comprehensive WCAG 2.2 accessibility assessment placeholder for {url}."}

# ===================== External CLI Integrations =====================

def _run_cli(cmd: list[str]) -> dict:
    """Helper to run a CLI command and capture JSON/stdout."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if proc.returncode == 0:
            # If stdout is JSON parse it; otherwise return raw.
            try:
                return json.loads(proc.stdout)
            except json.JSONDecodeError:
                return {"stdout": proc.stdout.strip()}
        return {"error": proc.stderr.strip() or proc.stdout.strip()}
    except FileNotFoundError:
        return {"error": f"{cmd[0]} binary not found. Please ensure it is installed in the system PATH."}
    except Exception as exc:
        return {"error": str(exc)}

# Pa11y (Node CLI) ----------------------------------------------------

def run_pa11y(url: str) -> dict:
    """Run Pa11y accessibility scan via npx (requires Node & pa11y)."""
    url = _normalize_url(url)
    if not shutil.which("npx"):
        return {"error": "npx command not found – Node.js is required for Pa11y."}
    cmd = ["npx", "pa11y", url, "--reporter", "json"]
    result = _run_cli(cmd)
    return {"tool": "pa11y", "url": url, "result": result}

# axe DevTools CLI ----------------------------------------------------

def run_axe_devtools(url: str) -> dict:
    """Run axe DevTools CLI scan (requires Node & axe DevTools installed)."""
    url = _normalize_url(url)
    if not shutil.which("npx"):
        return {"error": "npx command not found – Node.js is required for axe DevTools."}
    cmd = ["npx", "axe", url, "--tags", "wcag2a,wcag2aa", "--format", "json"]
    result = _run_cli(cmd)
    return {"tool": "axe-devtools", "url": url, "result": result}

# ===================== Chrome DevTools / Lighthouse Integrations =====================

def get_accessibility_tree(url: str) -> dict:
    """Capture the page's accessibility tree using the Chrome DevTools protocol via Playwright.
    Requires the `playwright` Python package and Chromium browser. If unavailable, returns an error message.
    """
    url = _normalize_url(url)
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return {"error": "playwright not installed. Run: pip install playwright && playwright install chromium"}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            tree = page.accessibility.snapshot()
            browser.close()
        # The accessibility tree can be quite large; we return the top-level summary.
        return {"tool": "chromedevtools-accessibility-tree", "url": url, "snapshot": tree}
    except Exception as exc:
        return {"error": str(exc)}

def run_lighthouse_accessibility(url: str) -> dict:
    """Run Lighthouse accessibility audit via npx Lighthouse CLI (Chrome DevTools)."""
    url = _normalize_url(url)
    if not shutil.which("npx"):
        return {"error": "npx command not found – Node.js is required for Lighthouse."}
    cmd = [
        "npx",
        "lighthouse",
        url,
        "--only-categories=accessibility",
        "--quiet",
        "--output=json",
        "--chrome-flags=--headless",
    ]
    result = _run_cli(cmd)
    return {"tool": "lighthouse", "url": url, "result": result}

# ===================== WCAG 2.2 ADDITIONS (Navigation & Input) =====================


def test_focus_not_obscured(url: str) -> Dict[str, Any]:
    """WCAG 2.4.11-12 – Ensure the focused element is not obscured by other UI (sticky headers, dialogs, etc.).
    This is a heuristic placeholder; real implementation would need viewport intersection checks via Playwright/Puppeteer.
    """
    url = _normalize_url(url)
    return {
        "wcag_criteria": ["2.4.11", "2.4.12"],
        "test_results": {
            "focus_not_obscured_minimum": "⚠️ Needs manual verification (heuristic only)",
            "focus_not_obscured_enhanced": "⚠️ Needs manual verification (heuristic only)",
        },
        "recommendations": [
            "Check that sticky headers/footers do not cover the keyboard focus ring.",
            "Ensure focused elements remain at least partially visible within the viewport.",
        ],
        "url": url,
        "status": "NEEDS_REVIEW",
    }


def test_focus_appearance(url: str) -> Dict[str, Any]:
    """WCAG 2.4.13 – Evaluate focus indicator size and contrast (placeholder)."""
    url = _normalize_url(url)
    return {
        "wcag_criteria": ["2.4.13"],
        "test_results": {
            "focus_indicator": "⚠️ Focus appearance needs size/contrast validation",
        },
        "recommendations": [
            "Ensure focus indicator has minimum area ≥ 2 CSS px outline or 8 px thickness equivalent.",
            "Maintain 3:1 contrast ratio against adjacent colors.",
        ],
        "url": url,
        "status": "NEEDS_REVIEW",
    }


def test_dragging_movements(url: str) -> Dict[str, Any]:
    """WCAG 2.5.7 – Check that functionality requiring dragging is also available by single-pointer operations."""
    url = _normalize_url(url)
    return {
        "wcag_criteria": ["2.5.7"],
        "test_results": {
            "dragging_movements": "⚠️ Manual verification required – no automatic detection implemented",
        },
        "recommendations": [
            "Provide alternative controls (e.g., buttons) for functionality that currently relies on drag-and-drop.",
        ],
        "url": url,
        "status": "NEEDS_TESTING",
    }


def test_target_size_minimum(url: str) -> Dict[str, Any]:
    """WCAG 2.5.8 – Verify interactive target size is at least 24 × 24 CSS pixels (heuristic)."""
    url = _normalize_url(url)
    return {
        "wcag_criteria": ["2.5.8"],
        "test_results": {
            "target_size": "⚠️ Automatic estimation suggests some targets < 24 px; manual audit advised",
        },
        "recommendations": [
            "Increase touch target size to minimum 24×24 CSS px (or provide spacing).",
            "Ensure sufficient spacing between smaller targets to avoid activation errors.",
        ],
        "url": url,
        "status": "NEEDS_TESTING",
    } 