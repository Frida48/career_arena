"""Həndəsə sualları üçün sadə SVG çertyojlar. Rənglər currentColor ilə verilir (açıq/qaranlıq rejim).

Nöqtələr riyazi koordinatlarda (y yuxarı) verilir, çertyoj W×H qutusuna avtomatik yerləşdirilir.
Çertyoj real koordinatlardan çəkilir, ona görə nisbətlər düzgündür.
"""
import math

W, H, PAD = 320, 220, 34


class Fig:
    def __init__(self):
        self.items = []  # (kind, data)
        self.pts = []

    # ---- elementlər ----
    def poly(self, pts, close=True):
        self.items.append(("poly", (list(pts), close)))
        self.pts += list(pts)
        return self

    def seg(self, a, b, dash=False):
        self.items.append(("seg", (a, b, dash)))
        self.pts += [a, b]
        return self

    def circle(self, c, r):
        self.items.append(("circle", (c, r)))
        self.pts += [(c[0] - r, c[1] - r), (c[0] + r, c[1] + r)]
        return self

    def dot(self, p):
        self.items.append(("dot", p))
        self.pts.append(p)
        return self

    def label(self, p, text, away=None, dist=13):
        """away — nöqtə; yazı ondan uzaq tərəfə qoyulur"""
        self.items.append(("label", (p, text, away, dist)))
        return self

    def side(self, a, b, text, inside=None):
        """AB tərəfinin ortasında yazı; inside — fiqurun daxili nöqtəsi (yazı əks tərəfə)"""
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        self.items.append(("label", (m, text, inside, 12)))
        return self

    def right(self, v, a, b, s=None):
        """v təpəsində düz bucaq işarəsi (va və vb istiqamətləri)"""
        self.items.append(("right", (v, a, b, s)))
        return self

    def arc(self, v, a, b, text=None):
        """v təpəsində a→b bucaq qövsü"""
        self.items.append(("arc", (v, a, b, text)))
        return self

    # ---- çevirmə ----
    def _tf(self):
        xs = [p[0] for p in self.pts]
        ys = [p[1] for p in self.pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        k = min((W - 2 * PAD) / max(x1 - x0, 1e-9), (H - 2 * PAD) / max(y1 - y0, 1e-9))
        ox = (W - k * (x1 - x0)) / 2
        oy = (H - k * (y1 - y0)) / 2

        def f(p):
            return (ox + (p[0] - x0) * k, H - (oy + (p[1] - y0) * k))
        return f, k

    def render(self):
        f, k = self._tf()
        n = lambda v: f"{v:.1f}"
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
               'fill="none" stroke="currentColor" stroke-width="1.6" font-family="sans-serif" font-size="14">']
        for kind, d in self.items:
            if kind == "poly":
                pts, close = d
                s = " ".join(f"{n(f(p)[0])},{n(f(p)[1])}" for p in pts)
                out.append(f'<{"polygon" if close else "polyline"} points="{s}"/>')
            elif kind == "seg":
                a, b, dash = d
                (x1, y1), (x2, y2) = f(a), f(b)
                extra = ' stroke-dasharray="5 4"' if dash else ""
                out.append(f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}"{extra}/>')
            elif kind == "circle":
                c, r = d
                x, y = f(c)
                out.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r * k)}"/>')
            elif kind == "dot":
                x, y = f(d)
                out.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="2.6" fill="currentColor"/>')
            elif kind == "right":
                v, a, b, s = d
                V, A, B = f(v), f(a), f(b)
                s = s or 10
                ua = _unit(V, A)
                ub = _unit(V, B)
                p1 = (V[0] + ua[0] * s, V[1] + ua[1] * s)
                p3 = (V[0] + ub[0] * s, V[1] + ub[1] * s)
                p2 = (p1[0] + ub[0] * s, p1[1] + ub[1] * s)
                out.append(f'<polyline points="{n(p1[0])},{n(p1[1])} {n(p2[0])},{n(p2[1])} {n(p3[0])},{n(p3[1])}" stroke-width="1.2"/>')
            elif kind == "arc":
                v, a, b, text = d
                V, A, B = f(v), f(a), f(b)
                rr = 18
                ua, ub = _unit(V, A), _unit(V, B)
                p1 = (V[0] + ua[0] * rr, V[1] + ua[1] * rr)
                p2 = (V[0] + ub[0] * rr, V[1] + ub[1] * rr)
                cross = ua[0] * ub[1] - ua[1] * ub[0]
                sweep = 1 if cross > 0 else 0
                out.append(f'<path d="M{n(p1[0])},{n(p1[1])} A{rr},{rr} 0 0 {sweep} {n(p2[0])},{n(p2[1])}" stroke-width="1.2"/>')
                if text:
                    bis = _unit((0, 0), (ua[0] + ub[0], ua[1] + ub[1]))
                    tx, ty = V[0] + bis[0] * (rr + 13), V[1] + bis[1] * (rr + 13) + 5
                    out.append(_text(tx, ty, text, 12))
            elif kind == "label":
                p, text, away, dist = d
                x, y = f(p)
                if away is not None:
                    ax, ay = f(away)
                    u = _unit((ax, ay), (x, y))
                    if u == (0.0, 0.0):
                        u = (0.0, -1.0)
                    x, y = x + u[0] * dist, y + u[1] * dist
                out.append(_text(x, y + 5, text, 14))
        out.append("</svg>")
        return "".join(out)


def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    return (dx / L, dy / L) if L else (0.0, 0.0)


def _text(x, y, s, size):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" fill="currentColor" stroke="none" '
            f'font-size="{size}">{s}</text>')


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def tri_from_sides(a, b, c):
    """BC=a, CA=b, AB=c. A=(0,0), B=(c,0), C yuxarıda. Qaytarır A, B, C."""
    x = (b * b + c * c - a * a) / (2 * c)
    y = math.sqrt(max(b * b - x * x, 0))
    return (0.0, 0.0), (float(c), 0.0), (x, y)


def labeled_polygon(names, pts, sides=None):
    """names: ['A','B','C'], sides: {(i,j): 'mətn'}"""
    fig = Fig().poly(pts)
    g = centroid(pts)
    for nm, p in zip(names, pts):
        fig.label(p, nm, away=g)
    for (i, j), t in (sides or {}).items():
        fig.side(pts[i], pts[j], t, inside=g)
    return fig
