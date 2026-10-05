"""Logo -> vector path for the theme mark (the glyph inside every actor chip). PNG/JPG (any background) or SVG with <path d=...>.
Output file `mark.txt`: line 1 'W H', line 2 an SVG path (evenodd)."""
import re, sys


def from_svg(svg):
    t = open(svg).read(); vb = re.search(r'viewBox="([\d.\s-]+)"', t)
    ds = re.findall(r'\sd="([^"]+)"', t)
    if not ds: raise SystemExit('no <path d=...> found in SVG')
    x0, y0, w, h = (vb.group(1).split() if vb else ['0', '0', '100', '100']); return f'{w} {h}', ' '.join(ds)


def from_raster(png, size=200):
    import numpy as np
    from PIL import Image
    from skimage import measure
    im = Image.open(png).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    g = np.asarray(bg.convert('L').resize((size, size), Image.LANCZOS), dtype=float)
    if g.mean() < 128: g = 255 - g            # make the glyph dark on light
    mask = np.pad(g < 128, 1)
    d = []
    for c in measure.find_contours(mask.astype(float), .5):
        c = measure.approximate_polygon(c, .6)
        if len(c) < 4: continue
        d.append('M' + ' L'.join(f'{x - 1:.1f} {y - 1:.1f}' for y, x in c) + 'Z')
    return f'{size} {size}', ' '.join(d)


def make(src, out):
    wh, d = from_svg(src) if src.lower().endswith('.svg') else from_raster(src)
    open(out, 'w').write(wh + '\n' + d + '\n'); return out
