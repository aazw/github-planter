import click
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page


def run(playwright: Playwright, url: str, output: str) -> None:
    browser: Browser = playwright.chromium.launch(headless=True)
    context: BrowserContext = browser.new_context(
        color_scheme="dark",
        device_scale_factor=2,
    )

    page: Page = context.new_page()
    page.goto(url)

    page.locator('div[data-graph-url="/users/aazw/contributions"]').screenshot(
        path=output
    )

    page.close()
    context.close()
    browser.close()


@click.command()
@click.option("--output", type=str, default="./contributions.png", help="")
@click.option("--url", type=str, default="https://github.com/aazw", help="")
def main(url: str, output: str) -> None:
    with sync_playwright() as playwright:
        run(playwright, url, output)


if __name__ == "__main__":
    main()
