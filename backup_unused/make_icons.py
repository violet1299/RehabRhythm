import os
import asyncio
from PIL import Image, ImageFilter
from playwright.async_api import async_playwright


SVG_DIR = "assets/icons/svg"
OUT_DIR = "assets/icons/png"

ICON_MAP = {
    "play": "train",
    "chart-no-axes-column": "history",
    "settings": "settings",
    "music": "song",
    "activity": "difficulty",
    "heart-pulse": "heart",
    "target": "target",
    "info" :"about"
    
}

COLORS = {
    "train": "#57c785",
    "history": "#4da6ff",
    "settings": "#9b7dff",
    "song": "#f2c14e",
    "difficulty": "#ff4dd3",
    "heart": "#e76f51",
    "target":"#e7e43e",
    "about":"#db2967"
    
}


def add_glow(path, color_hex):
    img = Image.open(path).convert("RGBA")
    alpha = img.getchannel("A")

    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:7], 16)

    glow = Image.new("RGBA", img.size, (r, g, b, 120))
    glow.putalpha(alpha.filter(ImageFilter.GaussianBlur(8)))

    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.alpha_composite(glow)
    result.alpha_composite(img)
    result.save(path)


async def convert_icon(page, svg_name, out_name):
    svg_path = os.path.join(SVG_DIR, f"{svg_name}.svg")
    out_path = os.path.join(OUT_DIR, f"{out_name}.png")

    if not os.path.exists(svg_path):
        print("缺少 SVG:", svg_path)
        return

    with open(svg_path, "r", encoding="utf-8") as f:
        svg = f.read()

    color = COLORS[out_name]

    svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    svg = svg.replace('width="24"', 'width="128"')
    svg = svg.replace('height="24"', 'height="128"')
    svg = svg.replace('stroke-width="2"', 'stroke-width="3"')

    html = f"""
    <html>
    <body style="margin:0;background:transparent;width:128px;height:128px;
                 display:flex;align-items:center;justify-content:center;">
        {svg}
    </body>
    </html>
    """

    await page.set_content(html)
    await page.screenshot(path=out_path, omit_background=True)
    add_glow(out_path, color)

    print("生成:", out_path)


async def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 128, "height": 128}, device_scale_factor=2)

        for svg_name, out_name in ICON_MAP.items():
            await convert_icon(page, svg_name, out_name)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())