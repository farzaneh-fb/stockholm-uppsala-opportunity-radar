from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/index.html"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = Path(__file__).resolve().parent.parent / "data" / "test_output"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=CHROME)
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.goto(URL, wait_until="networkidle")
    page.evaluate("localStorage.setItem('opportunity-theme','dark')")
    page.reload(wait_until="networkidle")
    assert page.title() == "Farzaneh's Opportunity Radar"
    positions = page.evaluate("positions")
    expected_phd = sum(item["kind"] == "phd" for item in positions)
    expected_job = sum(item["kind"] == "job" for item in positions)
    expected_new = sum(item.get("new_date") == "2026-08-23" for item in positions)
    assert page.locator(".card").count() == expected_phd
    assert "developmental neuroscience" in page.locator("#results").inner_text()
    assert page.locator("#newCount").inner_text() == str(expected_new)
    assert page.locator("#phdCount").inner_text() == str(expected_phd)
    assert page.locator("#jobCount").inner_text() == str(expected_job)
    page.screenshot(path=OUT / "desktop_dark.png", full_page=True)

    page.get_by_role("tab", name="Job positions").click()
    assert page.locator(".card").count() == expected_job
    assert "Biomedical systems developer" in page.locator("#results").inner_text()
    assert "developmental neuroscience" not in page.locator("#results").inner_text()

    page.select_option("#statusFilter", "all")
    first_id = page.locator("[data-applied]").first.get_attribute("data-applied")
    page.locator("[data-applied]").first.check()
    assert page.locator(".card").count() == expected_job
    assert page.locator("[data-applied]").first.is_checked()
    page.select_option("#statusFilter", "unapplied")
    assert page.locator(".card").count() == 1
    page.select_option("#statusFilter", "applied")
    assert page.locator(".card").count() == 1
    assert page.locator("[data-applied]").first.is_checked()
    assert first_id in page.evaluate("localStorage.getItem('farzaneh-opportunity-applications-v1')")

    page.select_option("#statusFilter", "all")
    theme_before = page.locator("html").get_attribute("data-theme")
    page.click("#themeBtn")
    theme_after = page.locator("html").get_attribute("data-theme")
    assert theme_after in {"light", "dark"} and theme_after != theme_before
    page.evaluate("scrollTo(0, 0)")
    page.screenshot(path=OUT / f"desktop_{theme_after}_jobs.png", full_page=True)

    page.set_viewport_size({"width": 390, "height": 844})
    page.reload(wait_until="networkidle")
    # Reload restores the PhD tab and the default "Not applied" filter.
    assert page.locator(".card").count() == expected_phd
    assert page.locator("html").evaluate("e => e.scrollWidth <= e.clientWidth")
    page.screenshot(path=OUT / "mobile_light.png", full_page=True)

    assert not errors, errors
    browser.close()

print("report-e2e: PASS")
print(OUT / "desktop_dark.png")
print(OUT / f"desktop_{theme_after}_jobs.png")
print(OUT / "mobile_light.png")
