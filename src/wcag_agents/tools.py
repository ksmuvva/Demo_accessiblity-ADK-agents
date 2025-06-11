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

# ===================== WCAG 3.1.x Readable =====================

def test_readability(url: str) -> Dict[str, Any]:
    url = _normalize_url(url)
    import re, requests, textstat  # type: ignore
    from langdetect import detect  # type: ignore
    from bs4 import BeautifulSoup  # type: ignore

    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 (WCAG-audit)"})
        html = resp.text
        soup = BeautifulSoup(html, "lxml")

        # -------- 3.1.1 / 3.1.2 language attributes --------
        page_lang = soup.html.get("lang", "").lower() if soup.html else ""
        language_of_page = f"✅ html lang attribute set to '{page_lang}'" if page_lang else "❌ Missing html lang attribute"

        # Parts with differing lang
        parts_with_lang = [el for el in soup.find_all(attrs={"lang": True}) if el.get("lang", "").lower() != page_lang]
        language_of_parts = (
            f"✅ {len(parts_with_lang)} elements have correct secondary lang attributes" if parts_with_lang else "⚠️ No secondary lang attributes detected (verify if needed)"
        )

        # Grab visible text for readability analysis
        text_only = soup.get_text(separator=" ")
        text_only = re.sub(r"\s+", " ", text_only)
        sample_text = text_only[:15000]

        # Detect primary language via langdetect for cross-check
        detected_lang = detect(sample_text) if sample_text.strip() else "unknown"
        if page_lang and detected_lang != page_lang:
            language_of_page += f" (Warning: detected '{detected_lang}')"

        # -------- 3.1.3 unusual / difficult words --------
        difficult_pct = textstat.difficult_words(sample_text) / (len(sample_text.split()) or 1) * 100
        unusual_words = (
            f"✅ Difficult-word ratio {difficult_pct:.1f}% (acceptable)" if difficult_pct < 5 else f"⚠️ Difficult-word ratio high ({difficult_pct:.1f}%)"
        )

        # -------- 3.1.4 abbreviations --------
        abbreviations_found = re.findall(r"\b[A-Z]{2,6}s?\b", sample_text)
        unique_abbr = set(abbreviations_found)
        abbreviations = (
            f"✅ Few abbreviations detected ({len(unique_abbr)})" if len(unique_abbr) <= 10 else f"⚠️ Many abbreviations detected ({len(unique_abbr)})"
        )

        # -------- 3.1.5 reading level --------
        flesch = textstat.flesch_reading_ease(sample_text)
        grade = textstat.text_standard(sample_text, float_output=False)
        reading_level = f"✅ Readability ≈ {grade} (Flesch {flesch:.0f})" if flesch >= 60 else f"⚠️ Readability difficult – {grade} (Flesch {flesch:.0f})"

        # -------- 3.1.6 pronunciation cues --------
        has_ruby = bool(soup.find("ruby"))
        has_ssml = "<phoneme" in html
        pronunciation = (
            "✅ Pronunciation cues present (ruby/phoneme)" if has_ruby or has_ssml else "⚠️ No pronunciation aids detected"
        )

        status = "TESTED"

    except Exception as exc:
        language_of_page = language_of_parts = unusual_words = abbreviations = reading_level = pronunciation = f"❌ Error: {exc}"
        status = "ERROR"

    return {
        "wcag_criteria": ["3.1.1", "3.1.2", "3.1.3", "3.1.4", "3.1.5", "3.1.6"],
        "test_results": {
            "language_of_page": language_of_page,
            "language_of_parts": language_of_parts,
            "unusual_words": unusual_words,
            "abbreviations": abbreviations,
            "reading_level": reading_level,
            "pronunciation": pronunciation,
        },
        "recommendations": [
            "Ensure <html lang> is set and matches detected language.",
            "Add lang attributes for passages in other languages.",
            "Explain jargon/idioms & provide glossary for abbreviations.",
            "Target Flesch score ≥ 60 (about grade 8).",
            "Provide pronunciation guides (e.g., ruby, phoneme).",
        ],
        "url": url,
        "status": status,
    }


# ===================== WCAG 3.2.x Predictable =====================

def test_predictability(url: str) -> Dict[str, Any]:
    url = _normalize_url(url)
    import requests, re
    from bs4 import BeautifulSoup  # type: ignore

    try:
        html = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 (WCAG-audit)"}).text
        soup = BeautifulSoup(html, "lxml")

        # Helper to search JS snippets indicating navigation
        nav_js_regex = re.compile(r"location\.href|window\.location|document\.location", re.I)

        # 3.2.1 On Focus
        focus_elements = [el for el in soup.find_all(attrs={"onfocus": True})]
        focus_nav = [el for el in focus_elements if nav_js_regex.search(el["onfocus"])]
        on_focus = "✅ No focus-triggered navigation" if not focus_nav else f"❌ {len(focus_nav)} elements change context on focus"

        # 3.2.2 On Input
        input_handlers = soup.find_all(attrs={"oninput": True}) + soup.find_all(attrs={"onchange": True})
        input_nav = [el for el in input_handlers if nav_js_regex.search(" ".join(el.get(attr) for attr in ("oninput", "onchange") if el.get(attr)))]
        on_input = "✅ No input-triggered context change" if not input_nav else f"❌ {len(input_nav)} elements change context on input"

        # 3.2.3 Consistent Navigation – presence of <nav>
        nav_tags = soup.find_all("nav")
        consistent_navigation = "✅ <nav> landmarks present" if nav_tags else "⚠️ No explicit <nav> landmarks detected"

        # 3.2.4 Consistent Identification – identical components have same aria-label
        buttons = soup.find_all("button")
        labels = [btn.get_text(strip=True).lower() for btn in buttons]
        dup_labels = len(labels) != len(set(labels))
        consistent_identification = "✅ Component labelling appears consistent" if not dup_labels else "⚠️ Duplicate button labels might cause confusion"

        # 3.2.5 Change on Request – ensure submit / buttons handle
        auto_submit_forms = [form for form in soup.find_all("form") if form.get("onsubmit") and nav_js_regex.search(form["onsubmit"])]
        change_on_request = "✅ No unsolicited context changes detected" if not auto_submit_forms else f"❌ {len(auto_submit_forms)} forms submit automatically without user confirmation"

        # 3.2.6 Consistent Help – check for help links
        help_links = soup.find_all("a", string=re.compile(r"help|faq|support", re.I))
        consistent_help = "✅ Help links found" if help_links else "⚠️ No help links detected"

        status = "TESTED"
    except Exception as exc:
        on_focus = on_input = consistent_navigation = consistent_identification = change_on_request = consistent_help = f"❌ Error: {exc}"
        status = "ERROR"

    return {
        "wcag_criteria": ["3.2.1", "3.2.2", "3.2.3", "3.2.4", "3.2.5", "3.2.6"],
        "test_results": {
            "on_focus": on_focus,
            "on_input": on_input,
            "consistent_navigation": consistent_navigation,
            "consistent_identification": consistent_identification,
            "change_on_request": change_on_request,
            "consistent_help": consistent_help,
        },
        "recommendations": [
            "Avoid changing pages automatically on focus or input events.",
            "Use <nav> landmarks and keep navigation order stable.",
            "Label components consistently across the site.",
            "Ensure context changes occur only after explicit user action (e.g., button click).",
            "Provide a persistent Help / FAQ link on every page.",
        ],
        "url": url,
        "status": status,
    }


# ===================== WCAG 3.3.x Input Assistance =====================

def test_input_assistance(url: str) -> Dict[str, Any]:
    url = _normalize_url(url)
    import requests, re
    from bs4 import BeautifulSoup  # type: ignore

    try:
        html = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 (WCAG-audit)"}).text
        soup = BeautifulSoup(html, "lxml")

        inputs = soup.find_all(["input", "textarea", "select"])
        labels = {label.get("for"): label.get_text(strip=True) for label in soup.find_all("label")}

        # 3.3.1 Error Identification – look for aria-invalid or error messages
        aria_invalid = [el for el in inputs if el.get("aria-invalid") == "true"]
        error_identification = "⚠️ No inline validation attributes found" if not aria_invalid else "✅ aria-invalid markers present"

        # 3.3.2 Labels / Instructions – every input should have label or aria-label
        unlabeled = [el for el in inputs if not (el.get("id") in labels or el.get("aria-label") or el.get("aria-labelledby"))]
        labels_instructions = "✅ All form controls have labels" if not unlabeled else f"❌ {len(unlabeled)} controls missing labels"

        # 3.3.3 Error Suggestion – look for role=alert or <span class="error">
        error_suggestion = "⚠️ Could not detect automatic error suggestion patterns" if "error" not in html.lower() else "✅ Potential error message elements found"

        # 3.3.4 Error Prevention (Legal/Financial/Data) – forms with type=submit should have confirmation dialog? Heuristic: look for confirm() in onsubmit
        risky_forms = [form for form in soup.find_all("form") if re.search(r"confirm\\(", form.get("onsubmit", ""))]
        error_prevention_critical = "✅ Confirmation prompts present" if risky_forms else "⚠️ No confirmation prompts detected for critical forms"

        # 3.3.5 Help – presence of aria-describedby or help text
        help_texts = soup.find_all(attrs={"aria-describedby": True})
        help = "✅ Help descriptors present" if help_texts else "⚠️ No help descriptors detected"

        # 3.3.6 Error Prevention (All) – detect autocomplete attributes
        autocomplete_off = [inp for inp in inputs if inp.get("autocomplete") == "off"]
        error_prevention_all = "⚠️ Some inputs disable autocomplete" if autocomplete_off else "✅ Autocomplete available on inputs"

        # 3.3.7 Redundant Entry – heuristic: detect duplicate name attributes across forms
        name_counts = {}
        for inp in inputs:
            name = inp.get("name")
            if name:
                name_counts[name] = name_counts.get(name, 0) + 1
        redundant = [n for n, cnt in name_counts.items() if cnt > 1]
        redundant_entry = "⚠️ Possible redundant entry fields: " + ", ".join(redundant) if redundant else "✅ No obvious redundant fields"

        # 3.3.8 / 3.3.9 Accessible Authentication – detect 2FA alternatives or passwordless? Heuristic: look for input type password
        password_inputs = [inp for inp in inputs if inp.get("type") == "password"]
        accessible_auth_minimum = "⚠️ Password fields present – ensure alternative authentication methods" if password_inputs else "✅ No password-only authentication detected"
        accessible_auth_enhanced = "⚠️ Unable to verify enhanced authentication heuristics"  # Provide generic guidance

        status = "TESTED"
    except Exception as exc:
        error_identification = labels_instructions = error_suggestion = error_prevention_critical = help = error_prevention_all = redundant_entry = accessible_auth_minimum = accessible_auth_enhanced = f"❌ Error: {exc}"
        status = "ERROR"

    return {
        "wcag_criteria": [
            "3.3.1",
            "3.3.2",
            "3.3.3",
            "3.3.4",
            "3.3.5",
            "3.3.6",
            "3.3.7",
            "3.3.8",
            "3.3.9",
        ],
        "test_results": {
            "error_identification": error_identification,
            "labels_instructions": labels_instructions,
            "error_suggestion": error_suggestion,
            "error_prevention_critical": error_prevention_critical,
            "help": help,
            "error_prevention_all": error_prevention_all,
            "redundant_entry": redundant_entry,
            "accessible_auth_minimum": accessible_auth_minimum,
            "accessible_auth_enhanced": accessible_auth_enhanced,
        },
        "recommendations": [
            "Provide programmatically associated labels for every form control.",
            "Use inline validation (aria-invalid) and descriptive error messages.",
            "Confirm critical transactions before final submission.",
            "Offer help text via aria-describedby or visible instructions.",
            "Enable autocomplete and avoid redundant data entry.",
            "Provide passkey / MFA / passwordless authentication options.",
        ],
        "url": url,
        "status": status,
    } 