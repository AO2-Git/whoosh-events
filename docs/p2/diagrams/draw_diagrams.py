"""Diagram source for P2 sections 5.1 and 5.2 (Team 05, Whoosh Events).

Run:  python3 draw_diagrams.py   -> domain_model.png, sd_uc01.png, sd_uc02.png
The sequence diagrams are drawn straight from the scenario tables below, one row = one message,
so the message numbers always match the table step numbers.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "Arial"
INK = "#1f2937"
FILL = "#eef3fb"

# ---------------------------------------------------------------- 5.1 domain model
CLASSES = {
    # name: (x, y, attributes)
    "Organizer":    (0.0, 4.6, ["name"]),
    "SharedLink":   (5.2, 8.6, ["shared at"]),
    "Event":        (5.2, 5.4, ["title", "description", "date", "start time", "end time",
                                "location", "status", "last changed at"]),
    "Tag":          (10.6, 4.6, ["name"]),
    "SourceListing": (5.2, 0.5, ["original page address", "first seen at"]),
    "SourceSite":   (5.2, -2.6, ["name", "address", "last checked at", "last successful update at"]),
}
W = 3.4
LINE_H = 0.36


def box(ax, name, x, y, attrs):
    h = 0.55 + LINE_H * len(attrs) + 0.15
    ax.add_patch(plt.Rectangle((x, y - h), W, h, fc=FILL, ec=INK, lw=1.4))
    ax.text(x + W / 2, y - 0.3, name, ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
    ax.plot([x, x + W], [y - 0.55, y - 0.55], color=INK, lw=1.1)
    for i, a in enumerate(attrs):
        ax.text(x + 0.15, y - 0.55 - LINE_H * (i + 0.65), a, fontsize=11.5, va="center", color=INK)
    return (x, y - h, W, h)


def domain_model(path):
    fig, ax = plt.subplots(figsize=(10, 8.6))
    r = {n: box(ax, n, *v) for n, v in CLASSES.items()}

    def mid_left(n):  x, y, w, h = r[n]; return (x, y + h / 2)
    def mid_right(n): x, y, w, h = r[n]; return (x + w, y + h / 2)
    def top(n):       x, y, w, h = r[n]; return (x + w / 2, y + h)
    def bottom(n):    x, y, w, h = r[n]; return (x + w / 2, y)

    def assoc(p, q, m1, m2, label, off=(0, 0)):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=INK, lw=1.3)
        import math
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        if ny < 0 or (ny == 0 and nx < 0):
            nx, ny = -nx, -ny
        if abs(dy) > abs(dx):
            nx, ny = 1, 0
        for (pt, sgn, m) in ((p, 1, m1), (q, -1, m2)):
            ax.text(pt[0] + sgn * ux * 0.32 + nx * 0.28, pt[1] + sgn * uy * 0.32 + ny * 0.28, m,
                    fontsize=12.5, ha="center", va="center", color=INK)
        ax.text((p[0] + q[0]) / 2 - nx * 0.0 + off[0], (p[1] + q[1]) / 2 + off[1], label, fontsize=11.5,
                ha="center", va="center", style="italic", color="#374151",
                bbox=dict(fc="white", ec="none", pad=1.5))

    ev_y = r["Event"][1] + r["Event"][3] * 0.62
    assoc((r["Organizer"][0] + W, ev_y), (r["Event"][0], ev_y), "1", "0..*", "hosts", (0, -0.3))
    assoc((r["Event"][0] + W, ev_y), (r["Tag"][0], ev_y), "0..*", "0..*", "is labeled with", (0, -0.3))
    assoc(bottom("SharedLink"), top("Event"), "0..*", "1", "points to", (-0.8, 0))
    assoc(bottom("Event"), top("SourceListing"), "1", "1..2", "is listed as", (-0.9, 0))
    assoc(bottom("SourceListing"), top("SourceSite"), "0..*", "1", "is published by", (-1.1, 0))

    ax.set_xlim(-0.2, 14.2)
    ax.set_ylim(-5.6, 9.0)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=170, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


# ---------------------------------------------------------------- 5.2 sequence diagrams
def sequence(path, lifelines, rows, control, breaks_after=()):
    """rows: (number, sender, receiver, message, return_label or None).
    Actors are stick figures; the controller has an activation bar that ends after any row in
    breaks_after and restarts at the next message; every other object gets a short bar from the
    message it receives until it returns."""
    n = len(lifelines)
    gap = 3.7
    xs = {name: i * gap for i, name in enumerate(lifelines)}
    actors = {"Student", "Friend"}
    step = 0.85
    total = len(rows) * step + sum(step * 0.6 for r in rows if r[4]) + 1.2
    fig, ax = plt.subplots(figsize=(max(10, n * 2.6), 1.6 + total * 0.62))
    top_y = 0
    for name, x in xs.items():
        if name in actors:
            ax.add_patch(plt.Circle((x, top_y + 0.62), 0.14, fc="white", ec=INK, lw=1.4))
            ax.plot([x, x], [top_y + 0.48, top_y + 0.15], color=INK, lw=1.4)
            ax.plot([x - 0.22, x + 0.22], [top_y + 0.38, top_y + 0.38], color=INK, lw=1.4)
            ax.plot([x, x - 0.18], [top_y + 0.15, top_y - 0.1], color=INK, lw=1.4)
            ax.plot([x, x + 0.18], [top_y + 0.15, top_y - 0.1], color=INK, lw=1.4)
            ax.text(x, top_y - 0.28, name, ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
        else:
            ax.add_patch(plt.Rectangle((x - 1.2, top_y - 0.25), 2.4, 0.6, fc=FILL, ec=INK, lw=1.3))
            ax.text(x, top_y + 0.05, ":" + name, ha="center", va="center", fontsize=13, fontweight="bold", color=INK)
    end_y = -(total) - 0.3
    for x in xs.values():
        ax.plot([x, x], [top_y - 0.45, end_y], color="#9ca3af", lw=1, ls=(0, (4, 4)), zorder=0)

    def bar(x, y0, y1):
        ax.add_patch(plt.Rectangle((x - 0.09, y1), 0.18, y0 - y1, fc="white", ec=INK, lw=1.1, zorder=2))

    cx = xs[control]
    y = top_y - 0.9
    seg_start = y + 0.2
    open_at = {}
    for num, a, b, msg, ret in rows:
        if seg_start is None:
            seg_start = y + 0.2
        xa, xb = xs[a], xs[b]
        if a == b:
            if a != control and a not in open_at:
                open_at[a] = y + 0.15
            ax.annotate("", xy=(xa + 0.1, y - 0.35), xytext=(xa + 0.1, y),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2,
                                        connectionstyle="arc3,rad=-1.6"), zorder=3)
            ax.text(xa + 0.55, y - 0.12, f"{num}  {msg}", fontsize=12.5, va="center", color=INK)
            y -= step * 1.1
            if ret and a != control:
                ax.annotate("", xy=(cx + 0.09, y), xytext=(xa - 0.09, y),
                            arrowprops=dict(arrowstyle="->", color="#6b7280", lw=1.1, ls=(0, (4, 3))), zorder=3)
                ax.text((xa + cx) / 2, y + 0.12, ret, ha="center", fontsize=11.5, color="#4b5563", style="italic")
                bar(xa, open_at.pop(a), y - 0.05)
                y -= step * 0.6
        else:
            if a == control and b not in actors:
                open_at.setdefault(b, y + 0.05)
            s = 0.09 if xb > xa else -0.09
            ax.annotate("", xy=(xb - s, y), xytext=(xa + s if a == control else xa, y),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3), zorder=3)
            if xb > xa:
                ax.text(xa + 0.25, y + 0.13, f"{num}  {msg}", ha="left", fontsize=12.5, color=INK)
            else:
                ax.text(xa - 0.25, y + 0.13, f"{num}  {msg}", ha="right", fontsize=12.5, color=INK)
            y -= step
            if ret:
                ax.annotate("", xy=(xa + s, y), xytext=(xb - s, y),
                            arrowprops=dict(arrowstyle="->", color="#6b7280", lw=1.1, ls=(0, (4, 3))), zorder=3)
                ax.text((xa + xb) / 2, y + 0.12, ret, ha="center", fontsize=11.5, color="#4b5563", style="italic")
                if b in open_at:
                    bar(xb, open_at.pop(b), y - 0.05)
                y -= step * 0.6
        if num in breaks_after:
            bar(cx, seg_start, y + 0.45)
            seg_start = None
    if seg_start is not None:
        bar(cx, seg_start, y + 0.3)
    ax.set_xlim(-1.5, (n - 1) * gap + 1.5)
    ax.set_ylim(end_y - 0.2, top_y + 0.9)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=170, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


UC01 = [
    ("0a", "EventBrowser", "EventCatalog", "asks for the first 20 upcoming events, soonest first", "upcoming events"),
    ("0b", "EventBrowser", "EventCatalog", "asks for the tags in use", "tag list"),
    ("0c", "EventBrowser", "SourceSite", "asks when each site was last updated", "last update times"),
    ("0d", "EventBrowser", "Student", "shows events, tags and last-updated time", None),
    ("1", "Student", "EventBrowser", "chooses a tag", None),
    ("2a", "EventBrowser", "EventCatalog", "asks for upcoming events with that tag, soonest first", "matching events"),
    ("2b", "EventBrowser", "EventBrowser", "counts the matching events", None),
    ("2c", "EventBrowser", "Student", "shows the matching events and the count", None),
    ("3", "Student", "EventBrowser", "reaches the end of the events shown", None),
    ("4a", "EventBrowser", "EventCatalog", "asks for the next 20 matching events", "next events"),
    ("4b", "EventBrowser", "Student", "adds the next 20 matching events", None),
]

UC02 = [
    ("1", "Student", "EventBrowser", "asks to copy an event’s link", None),
    ("2a", "EventBrowser", "LinkRegistry", "asks for a link to the event", None),
    ("2b", "LinkRegistry", "LinkRegistry", "records the link with the time it was shared", "the link"),
    ("2c", "EventBrowser", "Student", "copies the link and says “Link copied”", None),
    ("3", "Friend", "EventBrowser", "opens the link", None),
    ("4a", "EventBrowser", "LinkRegistry", "asks which event the link points to and when it was shared", "event, shared at"),
    ("4b", "EventBrowser", "EventCatalog", "asks for the event’s current details and status", "details, status, last changed at"),
    ("4c", "EventBrowser", "EventBrowser", "checks the event is upcoming and unchanged since sharing", None),
    ("4d", "EventBrowser", "Friend", "shows the full details and the original-page link", None),
]

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    domain_model(os.path.join(here, "domain_model.png"))
    sequence(os.path.join(here, "sd_uc01.png"),
             ["Student", "EventBrowser", "EventCatalog", "SourceSite"], UC01, "EventBrowser")
    sequence(os.path.join(here, "sd_uc02.png"),
             ["Student", "Friend", "EventBrowser", "LinkRegistry", "EventCatalog"], UC02, "EventBrowser",
             breaks_after=("2c",))
    print("ok")


# ---------------------------------------------------------------- 3.4 use-case diagram
def stick(ax, x, y, name):
    ax.add_patch(plt.Circle((x, y + 0.75), 0.2, fc="white", ec=INK, lw=1.5))
    ax.plot([x, x], [y + 0.55, y - 0.05], color=INK, lw=1.5)
    ax.plot([x - 0.35, x + 0.35], [y + 0.35, y + 0.35], color=INK, lw=1.5)
    ax.plot([x, x - 0.3], [y - 0.05, y - 0.55], color=INK, lw=1.5)
    ax.plot([x, x + 0.3], [y - 0.05, y - 0.55], color=INK, lw=1.5)
    ax.text(x, y - 0.85, name, ha="center", va="top", fontsize=12, fontweight="bold", color=INK)


def use_case_diagram(path):
    from matplotlib.patches import Ellipse
    fig, ax = plt.subplots(figsize=(10, 6.4))
    ax.add_patch(plt.Rectangle((2.2, 0.0), 6.0, 7.6, fc="white", ec=INK, lw=1.5))
    ax.text(5.2, 7.25, "Whoosh Events", ha="center", fontsize=13, fontweight="bold", color=INK)
    ucs = [("UC-01 Find Events by Tag", 6.3), ("UC-02 Share an Event\nwith a Friend", 5.2),
           ("UC-03 View Event Details", 4.1), ("UC-04 Add an Event\nto My Calendar", 3.0),
           ("UC-05 Find Events by Organizer", 1.9), ("UC-06 Learn How to\nHost an Event", 0.8)]
    sx, fx = 0.9, 9.5
    stick(ax, sx, 3.8, "Student")
    stick(ax, fx, 5.0, "Friend")
    for name, y in ucs:
        ax.add_patch(Ellipse((5.2, y), 4.6, 0.85, fc=FILL, ec=INK, lw=1.3))
        ax.text(5.2, y, name, ha="center", va="center", fontsize=11, color=INK)
        ax.plot([sx + 0.4, 2.9], [3.9, y], color=INK, lw=1.1)
    ax.plot([7.5, fx - 0.4], [5.2, 5.1], color=INK, lw=1.1)
    ax.set_xlim(0, 10.4)
    ax.set_ylim(-0.3, 7.8)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=170, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


if __name__ == "__main__":
    import os
    use_case_diagram(os.path.join(os.path.dirname(os.path.abspath(__file__)), "use_case_diagram.png"))


# ---------------------------------------------------------------- 2.1 context diagram
def context_diagram(path):
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.add_patch(plt.Rectangle((3.6, 0.6), 3.4, 2.6, fc=FILL, ec=INK, lw=1.8))
    ax.text(5.3, 2.75, "Whoosh Events", ha="center", fontsize=13, fontweight="bold", color=INK)
    ax.text(5.3, 1.75, "event collector\n+\nwebsite", ha="center", va="center", fontsize=11, color=INK)
    stick(ax, 0.9, 2.5, "Student")
    stick(ax, 0.9, 0.0, "Friend")
    for (lbl, y) in (("UTD Calendar", 2.5), ("Nebula club calendar", 0.9)):
        ax.add_patch(plt.Rectangle((8.2, y - 0.4), 2.4, 0.8, fc="white", ec=INK, lw=1.3))
        ax.text(9.4, y + 0.08, lbl, ha="center", va="center", fontsize=11, color=INK)
        ax.text(9.4, y - 0.22, "«external system»", ha="center", va="center", fontsize=8.5, color="#4b5563")
        ax.annotate("", xy=(7.0, y), xytext=(8.2, y), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
        ax.text(7.6, y + 0.15, "event data", ha="center", fontsize=9.5, style="italic", color="#374151")
    for y, lbl in ((2.6, "browses, filters,\nshares events"), (0.3, "opens a shared link")):
        ax.annotate("", xy=(3.6, 1.9 if y > 1 else 1.0), xytext=(1.35, y),
                    arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.2))
        ax.text(2.45, (y + (1.9 if y > 1 else 1.0)) / 2 + 0.28, lbl, ha="center", fontsize=9.5, style="italic", color="#374151")
    ax.set_xlim(0, 10.8)
    ax.set_ylim(-1.3, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=170, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)


if __name__ == "__main__":
    import os
    context_diagram(os.path.join(os.path.dirname(os.path.abspath(__file__)), "context_diagram.png"))
