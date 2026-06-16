import os
import urllib.parse
import flet as ft

IMAGE_FIT_CONTAIN = "contain"
IMAGE_FIT_COVER   = "cover"

# ── Identity ──────────────────────────────────────────────────────────────────
PROFILE_NAME     = "Shivute Johannes S"
PROFILE_ROLE     = "Metallurgical Engineer"
PROFILE_EMAIL    = "shivutejohannes100@gmail.com"
PROFILE_IMAGE    = "profile_pic.jpeg"
PROFILE_GITHUB   = "https://github.com/"
PROFILE_LINKEDIN = ""

# ── Forge Palette ─────────────────────────────────────────────────────────────
BG        = "#07090B"
PANEL     = "#0F1923"
PANEL_2   = "#152030"
INK       = "#EDF2F7"
STEEL     = "#A8BCCB"
MUTED     = "#5A7A8E"
AMBER     = "#E8921A"
ARC       = "#2ACDAA"
GOLD      = "#C8A84B"
LINE      = "#1E3045"

_base_dir   = os.path.dirname(os.path.abspath(__file__))
_assets_dir = os.path.join(_base_dir, "assets")


def main(page: ft.Page):
    page.title = f"{PROFILE_NAME} | Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=AMBER, font_family="Inter")
    page.bgcolor = BG
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window.min_width = 1100
    page.window.min_height = 750
    page.window.width  = 1280
    page.window.height = 820

    active_key = "home"

    # ── Asset helpers ─────────────────────────────────────────────────────────
    import base64 as _base64

    def asset_url(filename):
        """Return a base64 data URI for any file in assets/."""
        if not filename:
            return ""
        path = os.path.join(_assets_dir, filename)
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as f:
            raw = f.read()
        if raw.startswith(b"\x89PNG\r\n\x1a\n"):
            mime = "image/png"
        elif raw.startswith(b"\xff\xd8\xff"):
            mime = "image/jpeg"
        elif raw.startswith(b"GIF87a") or raw.startswith(b"GIF89a"):
            mime = "image/gif"
        elif raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
            mime = "image/webp"
        elif raw.startswith(b"%PDF"):
            mime = "application/pdf"
        else:
            ext = os.path.splitext(filename)[1].lower().lstrip(".")
            mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                    "gif": "image/gif", "webp": "image/webp", "pdf": "application/pdf"}.get(ext, "application/octet-stream")
        data = _base64.b64encode(raw).decode()
        return f"data:{mime};base64,{data}"

    def asset_b64(filename):
        """Return a base64 data URI string for ft.Image(src=...)."""
        if not filename:
            return ""
        path = os.path.join(_assets_dir, filename)
        if not os.path.exists(path):
            return ""
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")
        with open(path, "rb") as f:
            raw = f.read()
        data = _base64.b64encode(raw).decode()
        return f"data:{mime};base64,{data}"

    def find_asset(*candidates):
        """Return the first candidate filename that exists in assets/, else ''."""
        for name in candidates:
            if os.path.exists(os.path.join(_assets_dir, name)):
                return name
        return ""

    # Profile image as base64 data URI
    PROFILE_SRC = asset_url(PROFILE_IMAGE)

    # GitHub evidence — auto-find any image with "github" in the filename
    def find_github_image():
        if not os.path.isdir(_assets_dir):
            return ""
        for f in os.listdir(_assets_dir):
            if "github" in f.lower() and f.lower().endswith((".jpeg", ".jpg", ".png", ".webp")):
                return f
        return ""

    GITHUB_EVIDENCE_FILE = find_github_image()

    # Reflection video — auto-find any video with "reflection" in the filename
    def find_reflection_video():
        if not os.path.isdir(_assets_dir):
            return ""
        for f in os.listdir(_assets_dir):
            if "reflection" in f.lower() and f.lower().endswith((".mp4", ".webm", ".mov")):
                return f
        return ""

    REFLECTION_VIDEO_FILE = find_reflection_video()
    REFLECTION_VIDEO_SRC  = ("/" + urllib.parse.quote(REFLECTION_VIDEO_FILE)) if REFLECTION_VIDEO_FILE else ""
    # NOTE: ft.Video / ft.VideoMedia require the `flet-video` package.
    # Install with:  pip install flet-video --break-system-packages
    # If not installed, the player below will raise an AttributeError —
    # see fallback handling in the blog page section.
    HAS_VIDEO_WIDGET = hasattr(ft, "Video") and hasattr(ft, "VideoMedia")

    # ── DEBUG: print to terminal so you can see exactly what was found ────────
    print(f"\n[DEBUG] assets dir : {_assets_dir}")
    print(f"[DEBUG] files found: {os.listdir(_assets_dir) if os.path.isdir(_assets_dir) else 'DIR NOT FOUND'}")
    print(f"[DEBUG] evidence   : '{GITHUB_EVIDENCE_FILE}'\n")

    # Pre-encode the evidence image as base64 so it always works in web mode
    GITHUB_EVIDENCE_SRC = asset_b64(GITHUB_EVIDENCE_FILE)

    def open_url(url: str):
        async def _launch():
            try:
                await page.launch_url(url)
            except Exception as ex:
                snack(f"Could not open link: {ex}")
        page.run_task(_launch)

    def snack(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg, color=INK), bgcolor=PANEL_2, open=True)
        page.update()

    def card(content, width=None, accent=AMBER):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(width=4, bgcolor=accent, border_radius=ft.BorderRadius(4, 0, 0, 4)),
                    ft.Container(content=content, expand=True, padding=ft.Padding(22, 22, 22, 22)),
                ],
                spacing=0,
            ),
            width=width,
            border_radius=8,
            bgcolor=PANEL,
            border=ft.Border(
                top   =ft.BorderSide(1, LINE),
                right =ft.BorderSide(1, LINE),
                bottom=ft.BorderSide(1, LINE),
            ),
        )

    def heading(title: str, subtitle: str):
        return ft.Column(
            [
                ft.Text(
                    title.upper(),
                    size=50,
                    weight=ft.FontWeight.W_900,
                    color=INK,
                    text_align=ft.TextAlign.CENTER,
                    style=ft.TextStyle(letter_spacing=6),
                ),
                ft.Row(
                    [
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                        ft.Container(width=12, height=12, bgcolor=AMBER, border_radius=6),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=8,
                ),
                ft.Text(subtitle, size=16, color=MUTED, text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(italic=True)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        )

    def tag(label: str, color: str = AMBER):
        return ft.Container(
            padding=ft.Padding(12, 6, 12, 6),
            border_radius=4,
            bgcolor=ft.Colors.with_opacity(0.12, color),
            border=ft.Border(
                left  =ft.BorderSide(1, ft.Colors.with_opacity(0.5, color)),
                top   =ft.BorderSide(1, ft.Colors.with_opacity(0.5, color)),
                right =ft.BorderSide(1, ft.Colors.with_opacity(0.5, color)),
                bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.5, color)),
            ),
            content=ft.Text(label, size=12, color=color, weight=ft.FontWeight.W_700,
                            style=ft.TextStyle(letter_spacing=1)),
        )

    def shell(content):
        return ft.Container(
            expand=True,
            padding=ft.Padding(48, 52, 48, 52),
            content=ft.Column(
                [content],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            ),
        )

    def open_project(name: str):
        snack(f"Opening: {name}")

    def contact_submit(_):
        if not name_field.value or not email_field.value or not message_field.value:
            snack("Please complete all fields before sending.")
            return
        snack(f"Message received — thank you, {name_field.value}.")
        name_field.value = email_field.value = message_field.value = ""
        page.update()

    # ── Data ──────────────────────────────────────────────────────────────────
    skills = [
        ("Python",           "Automating calculations, parsing materials data, and building interactive engineering tools.",  ft.Icons.TERMINAL,        ARC),
        ("Flet",             "Crafting clean, cross-platform desktop UIs entirely in Python — no web stack required.",        ft.Icons.WEB_ASSET,        AMBER),
        ("MATLAB",           "Simulations, cooling curve plots, matrix operations, and engineering-grade computation.",       ft.Icons.AUTO_GRAPH,       GOLD),
        ("HTML / CSS",       "Responsive front-end layouts with deliberate visual hierarchy and clean presentation.",         ft.Icons.DESIGN_SERVICES,  ARC),
        ("Materials Science","Phase diagrams, solidification theory, heat treatment, corrosion mechanisms, and alloy design.",ft.Icons.SCIENCE,          AMBER),
        ("GitHub",           "Version-controlled projects, commit discipline, branching strategies, and published code.",     ft.Icons.CODE,             ARC),
    ]

    projects = [
        ("Alloy Property Dashboard", "An interactive comparison tool for density, hardness, tensile strength, and heat-treatment schedules across engineering alloys.", ft.Icons.DASHBOARD,  AMBER),
        ("Cooling Curve Plotter",    "Plots temperature-time curves from raw thermocouple data and automatically marks phase transformation events.",                    ft.Icons.SHOW_CHART, ARC),
        ("Corrosion Logbook",        "A structured field-and-lab logging tool for sample IDs, environments, corrosion rates, and photographic observations.",           ft.Icons.FACT_CHECK, GOLD),
    ]

    certificates = [
        ("MATLAB Onramp",                       "Core MATLAB syntax, scripts, and engineering workflows.",              "MATLAB Onramp certificate.pdf"),
        ("Simulink Onramp",                     "Model-based design fundamentals using Simulink block diagrams.",       "Simulink Onramp certificate.pdf"),
        ("Machine Learning Onramp",             "Supervised learning concepts applied within MATLAB.",                  "Machine Learning Onramp certificate.pdf"),
        ("Deep Learning Onramp",                "Neural network architecture and training pipelines in MATLAB.",        "Deep Learning Onramp certificate.pdf"),
        ("Explore Data with MATLAB Plots",      "Data visualisation techniques and publication-quality plots.",         "Explore Data with MATLAB Plots certificate.pdf"),
        ("Make and Manipulate Matrices",        "Matrix construction, indexing, and transformation operations.",        "Make and Manipulate Matrices certificate.pdf"),
        ("Calculations with Vectors & Matrices","Vectorised arithmetic and linear algebra for engineering problems.",   "Calculations with Vectors and Matrices certificate.pdf"),
        ("MATLAB Fundamentals",                 "Comprehensive review of MATLAB programming fundamentals and best practices.", "MATLAB Fundamentals certificate.pdf"),
    ]

    preview_count_text = ft.Text("", size=12, color=MUTED, weight=ft.FontWeight.W_700)
    preview_title_text = ft.Text("", size=28, weight=ft.FontWeight.W_900, color=INK)
    preview_desc_text = ft.Text("", size=15, color=STEEL)
    preview_file_text = ft.Text("", size=13, color=AMBER, weight=ft.FontWeight.W_700)
    preview_note_text = ft.Text("", size=13, color=MUTED)
    preview_tags_row = ft.Row([], spacing=8, wrap=True)
    preview_image = ft.Image(src="", fit=IMAGE_FIT_CONTAIN, border_radius=10)
    certificate_preview_cache = {}

    try:
        import fitz
    except Exception:
        fitz = None

    def certificate_preview_src(filename: str) -> str:
        cached = certificate_preview_cache.get(filename)
        if cached:
            return cached
        if fitz is None:
            return ""

        path = os.path.join(_assets_dir, filename)
        if not os.path.exists(path):
            return ""

        try:
            document = fitz.open(path)
            page = document.load_page(0)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(1.75, 1.75), alpha=False)
            image_data = _base64.b64encode(pixmap.tobytes("png")).decode()
            data_uri = f"data:image/png;base64,{image_data}"
            certificate_preview_cache[filename] = data_uri
            document.close()
            return data_uri
        except Exception as ex:
            print(f"[DEBUG] certificate preview failed for {filename}: {ex}")
            return ""

    def select_certificate(index: int):
        title, desc, file_name = certificates[index]
        preview_count_text.value = f"CERTIFICATE {index + 1:02d} / {len(certificates):02d}"
        preview_title_text.value = title
        preview_desc_text.value = desc
        preview_file_text.value = file_name
        preview_note_text.value = (
            "This certificate stays inside the portfolio so visitors can browse your work without opening a browser tab."
        )
        preview_tags_row.controls = [tag("Verified", ARC), tag("PDF", AMBER), tag("Local asset", GOLD)]
        preview_image.src = certificate_preview_src(file_name)
        preview_image.fit = IMAGE_FIT_CONTAIN
        page.update()

    select_certificate(0)

    # ── GitHub Evidence data ──────────────────────────────────────────────────
    commit_history = [
        ("feat: add alloy density comparison module", "alloy-dashboard", "main", "2026-04-02"),
        ("fix: correct phase-transition temperature lookup", "cooling-curve-plotter", "main", "2026-04-09"),
        ("docs: expand Fe-C phase diagram notes", "engineering-notes", "main", "2026-04-15"),
        ("feat: add corrosion rate calculator to logbook", "corrosion-logbook", "develop", "2026-04-22"),
        ("refactor: clean up Flet navigation structure", "metallurgy-portfolio", "main", "2026-05-03"),
    ]

    pull_requests = [
        ("Add heat-treatment schedule selector", "alloy-dashboard", "Merged", ARC,
         "Proposed and implemented a UI component allowing users to select heat-treatment schedules and view resulting hardness predictions."),
        ("Improve CSV parsing for thermocouple exports", "cooling-curve-plotter", "Merged", ARC,
         "Reviewed teammate's CSV import code, suggested error-handling improvements for malformed timestamps, then merged after revisions."),
        ("Add SQLite persistence for corrosion samples", "corrosion-logbook", "In Review", AMBER,
         "Implemented a lightweight SQLite layer so corrosion sample records persist between sessions; awaiting final review."),
    ]

    impact_summary_text = (
        "My core contribution to the group project focused on the Metallurgical module — specifically "
        "the alloy property comparison engine and the cooling curve analysis pipeline. I authored the "
        "data-handling logic that maps raw thermocouple readings to phase transformation events, which "
        "the team's main application now uses to flag potential quality issues during alloy solidification. "
        "I also reviewed and merged contributions from teammates working on the corrosion logging module, "
        "helping standardise our database schema across the Metallurgy, Mining, and Civil sub-teams."
    )

    github_repos = [
        ("metallurgy-portfolio",   "The complete source code for this Flet portfolio application, including all pages, design system, and assets.", ["Python", "Flet", "UI"],              ft.Icons.WEB_ASSET,  AMBER, f"{PROFILE_GITHUB}metallurgy-portfolio"),
        ("alloy-dashboard",        "Interactive desktop tool for comparing mechanical properties, density, and heat-treatment data across alloy families.", ["Python", "Materials Data", "Pandas"], ft.Icons.DASHBOARD,  ARC,   f"{PROFILE_GITHUB}alloy-dashboard"),
        ("cooling-curve-plotter",  "Reads thermocouple CSV exports, plots temperature-time curves, and marks phase transformation temperatures.", ["Python", "MATLAB", "Matplotlib"],       ft.Icons.SHOW_CHART, GOLD,  f"{PROFILE_GITHUB}cooling-curve-plotter"),
        ("corrosion-logbook",      "Lab logging tool for recording corrosion sample data, environments, weight-loss measurements, and observations.", ["Python", "SQLite", "Flet"],         ft.Icons.FACT_CHECK, AMBER, f"{PROFILE_GITHUB}corrosion-logbook"),
        ("matlab-scripts",         "Collection of MATLAB scripts covering matrix operations, data visualisation, machine learning exercises, and Simulink models.", ["MATLAB", "Simulink", "ML"], ft.Icons.AUTO_GRAPH, ARC,   f"{PROFILE_GITHUB}matlab-scripts"),
        ("engineering-notes",      "Structured study notes on phase diagrams, Fe-C system, solidification theory, and corrosion mechanisms — in Markdown.", ["Markdown", "Metallurgy", "Docs"], ft.Icons.MENU_BOOK,  GOLD,  f"{PROFILE_GITHUB}engineering-notes"),
    ]

    timeline = [
        ("Week 1", "Architected the Flet application structure, defined the visual design system, and established component patterns.", "Complete"),
        ("Week 2", "Set up Git version control with structured branching, semantic commits, and a clean project history.",              "Complete"),
        ("Week 3", "Researched and authored all metallurgy content: phase diagrams, material properties, and engineering notes.",       "Complete"),
        ("Week 4", "Built data modules for alloy parameters, cost tables, property comparisons, and calculation pipelines.",           "Complete"),
        ("Week 5", "Implemented robust error handling, input validation, and user-facing feedback across all interactive pages.",       "Complete"),
        ("Week 6", "Conducted final code review, prepared deployment documentation, and verified cross-platform compatibility.",        "Complete"),
    ]

    # ══════════════════════════════════════════════════════════════════════════
    # HOME PAGE
    # ══════════════════════════════════════════════════════════════════════════
    home_page = ft.Container(
        expand=True,
        padding=ft.Padding(48, 52, 48, 52),
        content=ft.Column(
            [
                # HERO
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(width=40, height=2, bgcolor=AMBER),
                                ft.Text("PORTFOLIO · 2026", size=12, color=AMBER, weight=ft.FontWeight.W_800,
                                        style=ft.TextStyle(letter_spacing=4)),
                                ft.Container(width=40, height=2, bgcolor=AMBER),
                            ],
                            spacing=12,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Text(
                            PROFILE_NAME.upper(),
                            size=64,
                            weight=ft.FontWeight.W_900,
                            color=INK,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(letter_spacing=8),
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    padding=ft.Padding(20, 10, 20, 10),
                                    border_radius=4,
                                    bgcolor=ft.Colors.with_opacity(0.15, AMBER),
                                    border=ft.Border(
                                        left  =ft.BorderSide(3, AMBER),
                                        top   =ft.BorderSide(1, ft.Colors.with_opacity(0.3, AMBER)),
                                        right =ft.BorderSide(1, ft.Colors.with_opacity(0.3, AMBER)),
                                        bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.3, AMBER)),
                                    ),
                                    content=ft.Text(
                                        PROFILE_ROLE.upper(),
                                        size=18,
                                        color=AMBER,
                                        weight=ft.FontWeight.W_800,
                                        style=ft.TextStyle(letter_spacing=4),
                                    ),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Text(
                            "Where the science of metals meets the precision of software engineering.",
                            size=18,
                            color=STEEL,
                            text_align=ft.TextAlign.CENTER,
                            style=ft.TextStyle(italic=True),
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    padding=ft.Padding(28, 14, 28, 14),
                                    border_radius=6,
                                    bgcolor=AMBER,
                                    content=ft.Row(
                                        [ft.Icon(ft.Icons.WORK_OUTLINE, color=BG, size=18),
                                         ft.Text("View Projects", size=15, color=BG, weight=ft.FontWeight.W_800)],
                                        spacing=8, tight=True,
                                    ),
                                    on_click=lambda _: show_page("projects"),
                                ),
                                ft.Container(
                                    padding=ft.Padding(28, 14, 28, 14),
                                    border_radius=6,
                                    border=ft.Border(
                                        left  =ft.BorderSide(1, AMBER),
                                        top   =ft.BorderSide(1, AMBER),
                                        right =ft.BorderSide(1, AMBER),
                                        bottom=ft.BorderSide(1, AMBER),
                                    ),
                                    content=ft.Row(
                                        [ft.Icon(ft.Icons.EMAIL_OUTLINED, color=AMBER, size=18),
                                         ft.Text("Get in Touch", size=15, color=AMBER, weight=ft.FontWeight.W_700)],
                                        spacing=8, tight=True,
                                    ),
                                    on_click=lambda _: show_page("contact"),
                                ),
                            ],
                            spacing=16,
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True,
                        ),
                    ],
                    spacing=22,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),

                ft.Container(
                    margin=ft.Margin(0, 44, 0, 44),
                    height=1,
                    gradient=ft.LinearGradient(
                        colors=[BG, AMBER, ARC, BG],
                        begin=ft.Alignment(-1, 0),
                        end=ft.Alignment(1, 0),
                    ),
                ),

                # ABOUT + PROFILE
                ft.ResponsiveRow(
                    [
                        # Profile card
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=card(
                                ft.Column(
                                    [
                                        ft.Container(
                                            width=180,
                                            height=180,
                                            border_radius=90,
                                            bgcolor=PANEL_2,
                                            border=ft.Border(
                                                left  =ft.BorderSide(3, AMBER),
                                                top   =ft.BorderSide(3, AMBER),
                                                right =ft.BorderSide(3, AMBER),
                                                bottom=ft.BorderSide(3, AMBER),
                                            ),
                                            content=ft.Image(
                                                src=PROFILE_SRC,
                                                width=180,
                                                height=180,
                                                fit="cover",
                                                border_radius=90,
                                            ),
                                        ),
                                        ft.Text(PROFILE_NAME, size=18, color=INK,
                                                weight=ft.FontWeight.W_800, text_align=ft.TextAlign.CENTER),
                                        ft.Text("B.Eng. Metallurgy · UNAM", size=13, color=AMBER,
                                                weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER),
                                        ft.Container(height=1, bgcolor=LINE),
                                        ft.Row([ft.Icon(ft.Icons.EMAIL_OUTLINED, color=MUTED, size=15),
                                                ft.Text(PROFILE_EMAIL, size=12, color=MUTED)], spacing=6),
                                        ft.Row(
                                            [
                                                ft.Container(
                                                    padding=ft.Padding(12, 8, 12, 8), border_radius=5,
                                                    bgcolor=ft.Colors.with_opacity(0.12, ARC),
                                                    border=ft.Border(left=ft.BorderSide(1, ft.Colors.with_opacity(0.4, ARC)), top=ft.BorderSide(1, ft.Colors.with_opacity(0.4, ARC)), right=ft.BorderSide(1, ft.Colors.with_opacity(0.4, ARC)), bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.4, ARC))),
                                                    content=ft.Row([ft.Icon(ft.Icons.CODE, color=ARC, size=15), ft.Text("GitHub", size=12, color=ARC, weight=ft.FontWeight.W_700)], spacing=6, tight=True),
                                                    on_click=lambda _: open_url(PROFILE_GITHUB),
                                                ),
                                                ft.Container(
                                                    padding=ft.Padding(12, 8, 12, 8), border_radius=5,
                                                    bgcolor=ft.Colors.with_opacity(0.12, AMBER),
                                                    border=ft.Border(left=ft.BorderSide(1, ft.Colors.with_opacity(0.4, AMBER)), top=ft.BorderSide(1, ft.Colors.with_opacity(0.4, AMBER)), right=ft.BorderSide(1, ft.Colors.with_opacity(0.4, AMBER)), bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.4, AMBER))),
                                                    content=ft.Row([ft.Icon(ft.Icons.PEOPLE_OUTLINE, color=AMBER, size=15), ft.Text("LinkedIn", size=12, color=AMBER, weight=ft.FontWeight.W_700)], spacing=6, tight=True),
                                                    on_click=lambda _: open_url(PROFILE_LINKEDIN),
                                                ),
                                            ],
                                            spacing=10,
                                        ),
                                    ],
                                    spacing=14,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ),

                        # Bio cards
                        ft.Container(
                            col={"sm": 12, "md": 8},
                            content=ft.Column(
                                [
                                    card(
                                        ft.Column(
                                            [
                                                ft.Row(
                                                    [ft.Container(width=3, height=24, bgcolor=ARC, border_radius=2),
                                                     ft.Text("WHO I AM", size=12, color=ARC, weight=ft.FontWeight.W_800,
                                                             style=ft.TextStyle(letter_spacing=3))],
                                                    spacing=10,
                                                ),
                                                ft.Text(
                                                    "I am a Metallurgical Engineering student at the University of Namibia with a dual obsession: "
                                                    "understanding how materials behave under stress, heat, and corrosion — and building the software tools "
                                                    "that make those insights accessible and actionable. I do not simply study metals; I engineer solutions around them.",
                                                    size=16, color=STEEL,
                                                ),
                                                ft.Text(
                                                    "This portfolio is evidence of both disciplines working in concert — clean, purposeful code in service of serious engineering.",
                                                    size=14, color=MUTED, style=ft.TextStyle(italic=True),
                                                ),
                                            ],
                                            spacing=14,
                                        ),
                                        accent=ARC,
                                    ),
                                    ft.Container(height=14),
                                    card(
                                        ft.Column(
                                            [
                                                ft.Row(
                                                    [ft.Container(width=3, height=24, bgcolor=AMBER, border_radius=2),
                                                     ft.Text("CURRENT FOCUS", size=12, color=AMBER, weight=ft.FontWeight.W_800,
                                                             style=ft.TextStyle(letter_spacing=3))],
                                                    spacing=10,
                                                ),
                                                ft.Text(
                                                    "Developing a suite of Python-based engineering tools designed specifically for metallurgical practice — "
                                                    "from interactive alloy comparison dashboards that map mechanical properties across entire material families, "
                                                    "to automated cooling curve analysers that identify phase transformation events directly from thermocouple data. "
                                                    "Every tool is built to the same standard I apply in the laboratory: precise, reproducible, and built to last.",
                                                    size=16, color=STEEL,
                                                ),
                                                ft.Row(
                                                    [tag("Python"), tag("Flet UI"), tag("MATLAB"),
                                                     tag("Materials Data", ARC), tag("Open Source", ARC)],
                                                    spacing=8, wrap=True,
                                                ),
                                            ],
                                            spacing=14,
                                        ),
                                        accent=AMBER,
                                    ),
                                ],
                                spacing=0,
                            ),
                        ),
                    ],
                    spacing=20,
                    run_spacing=20,
                ),

                # STATS ROW
                ft.Container(
                    margin=ft.Margin(0, 36, 0, 0),
                    content=ft.ResponsiveRow(
                        [
                            ft.Container(col={"sm": 6, "md": 3}, content=card(ft.Column([ft.Text("8", size=46, weight=ft.FontWeight.W_900, color=AMBER), ft.Text("MATLAB Certificates", size=13, color=MUTED, weight=ft.FontWeight.W_600)], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER), accent=AMBER)),
                            ft.Container(col={"sm": 6, "md": 3}, content=card(ft.Column([ft.Text("3", size=46, weight=ft.FontWeight.W_900, color=ARC),   ft.Text("Engineering Projects", size=13, color=MUTED, weight=ft.FontWeight.W_600)], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER), accent=ARC)),
                            ft.Container(col={"sm": 6, "md": 3}, content=card(ft.Column([ft.Text("6", size=46, weight=ft.FontWeight.W_900, color=AMBER), ft.Text("Skills Developed",    size=13, color=MUTED, weight=ft.FontWeight.W_600)], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER), accent=AMBER)),
                            ft.Container(col={"sm": 6, "md": 3}, content=card(ft.Column([ft.Text("1", size=46, weight=ft.FontWeight.W_900, color=ARC),   ft.Text("University — UNAM",   size=13, color=MUTED, weight=ft.FontWeight.W_600)], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER), accent=ARC)),
                        ],
                        spacing=16, run_spacing=16,
                    ),
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SKILLS PAGE
    # ══════════════════════════════════════════════════════════════════════════
    skills_page = shell(
        ft.Column(
            [
                heading("Skills", "The technical toolkit behind the engineering work."),
                ft.Container(height=28),
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            col={"sm": 12, "md": 6, "lg": 4},
                            content=card(
                                ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Container(width=50, height=50, border_radius=10,
                                                    bgcolor=ft.Colors.with_opacity(0.15, color),
                                                    alignment=ft.Alignment(0, 0),
                                                    content=ft.Icon(icon, color=color, size=26)),
                                                ft.Text(title, size=20, weight=ft.FontWeight.W_800, color=INK, expand=True),
                                            ],
                                            spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        ft.Text(desc, size=14, color=MUTED),
                                    ],
                                    spacing=12,
                                ),
                                accent=color,
                            ),
                        )
                        for title, desc, icon, color in skills
                    ],
                    spacing=16, run_spacing=16,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # PROJECTS PAGE
    # ══════════════════════════════════════════════════════════════════════════
    projects_page = shell(
        ft.Column(
            [
                heading("Projects", "Engineering concepts translated into working software."),
                ft.Container(height=28),
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            col={"sm": 12, "md": 4},
                            content=card(
                                ft.Column(
                                    [
                                        ft.Container(width=60, height=60, border_radius=12,
                                            bgcolor=ft.Colors.with_opacity(0.12, color),
                                            alignment=ft.Alignment(0, 0),
                                            content=ft.Icon(icon, color=color, size=32)),
                                        ft.Text(title, size=20, weight=ft.FontWeight.W_800, color=INK),
                                        ft.Text(desc, size=14, color=MUTED),
                                        ft.Container(
                                            padding=ft.Padding(16, 10, 16, 10), border_radius=5,
                                            bgcolor=ft.Colors.with_opacity(0.12, color),
                                            border=ft.Border(left=ft.BorderSide(1, ft.Colors.with_opacity(0.5, color)), top=ft.BorderSide(1, ft.Colors.with_opacity(0.5, color)), right=ft.BorderSide(1, ft.Colors.with_opacity(0.5, color)), bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.5, color))),
                                            content=ft.Row([ft.Icon(ft.Icons.OPEN_IN_FULL, color=color, size=15), ft.Text("View Concept", size=13, color=color, weight=ft.FontWeight.W_700)], spacing=8, tight=True),
                                            on_click=lambda _, p=title: open_project(p),
                                        ),
                                    ],
                                    spacing=14,
                                ),
                                accent=color,
                            ),
                        )
                        for title, desc, icon, color in projects
                    ],
                    spacing=16, run_spacing=16,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # MATLAB PAGE
    # ══════════════════════════════════════════════════════════════════════════
    matlab_page = shell(
        ft.Column(
            [
                heading("Certificate Portfolio", "Verified computational skills presented as an in-app viewer."),
                ft.Container(height=28),
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            col={"sm": 12, "md": 5},
                            content=card(
                                ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Container(width=3, height=20, bgcolor=GOLD, border_radius=2),
                                                ft.Text("CERTIFICATE LIBRARY", size=12, color=GOLD, weight=ft.FontWeight.W_800,
                                                        style=ft.TextStyle(letter_spacing=3)),
                                            ],
                                            spacing=10,
                                        ),
                                        ft.Container(
                                            padding=ft.Padding(16, 14, 16, 14),
                                            border_radius=6,
                                            bgcolor=ft.Colors.with_opacity(0.08, GOLD),
                                            border=ft.Border(
                                                left=ft.BorderSide(1, ft.Colors.with_opacity(0.4, GOLD)),
                                                top=ft.BorderSide(1, ft.Colors.with_opacity(0.4, GOLD)),
                                                right=ft.BorderSide(1, ft.Colors.with_opacity(0.4, GOLD)),
                                                bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.4, GOLD)),
                                            ),
                                            content=ft.Column(
                                                [
                                                    ft.Text("Choose a certificate to preview.", size=16, color=INK, weight=ft.FontWeight.W_800),
                                                    ft.Text(
                                                        "Each item stays inside the portfolio so visitors can browse your certifications without opening a browser window.",
                                                        size=13, color=MUTED,
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                        ),
                                        ft.Column(
                                            [
                                                ft.Container(
                                                    padding=ft.Padding(14, 14, 14, 14),
                                                    border_radius=6,
                                                    bgcolor=ft.Colors.with_opacity(0.06, PANEL_2),
                                                    border=ft.Border(
                                                        left=ft.BorderSide(1, LINE),
                                                        top=ft.BorderSide(1, LINE),
                                                        right=ft.BorderSide(1, LINE),
                                                        bottom=ft.BorderSide(1, LINE),
                                                    ),
                                                    content=ft.Column(
                                                        [
                                                            ft.Text(title, size=16, color=INK, weight=ft.FontWeight.W_800),
                                                            ft.Text(desc, size=13, color=MUTED),
                                                            ft.Container(
                                                                padding=ft.Padding(12, 8, 12, 8),
                                                                border_radius=5,
                                                                bgcolor=ft.Colors.with_opacity(0.12, GOLD),
                                                                content=ft.Row(
                                                                    [
                                                                        ft.Icon(ft.Icons.OPEN_IN_NEW, color=GOLD, size=15),
                                                                        ft.Text("Preview in portfolio", size=12, color=GOLD, weight=ft.FontWeight.W_700),
                                                                    ],
                                                                    spacing=6,
                                                                    tight=True,
                                                                ),
                                                                on_click=lambda _, i=i: select_certificate(i),
                                                            ),
                                                        ],
                                                        spacing=10,
                                                    ),
                                                    on_click=lambda _, i=i: select_certificate(i),
                                                )
                                                for i, (title, desc, file_name) in enumerate(certificates)
                                            ],
                                            spacing=12,
                                        ),
                                    ],
                                    spacing=14,
                                ),
                                accent=GOLD,
                            ),
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 7},
                            content=card(
                                ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Container(width=3, height=20, bgcolor=ARC, border_radius=2),
                                                ft.Text("PORTFOLIO VIEWER", size=12, color=ARC, weight=ft.FontWeight.W_800,
                                                        style=ft.TextStyle(letter_spacing=3)),
                                                ft.Container(expand=True, height=1, bgcolor=LINE),
                                            ],
                                            spacing=12,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        ft.Container(
                                            padding=ft.Padding(18, 18, 18, 18),
                                            border_radius=8,
                                            bgcolor=ft.Colors.with_opacity(0.06, PANEL_2),
                                            border=ft.Border(
                                                left=ft.BorderSide(1, LINE),
                                                top=ft.BorderSide(1, LINE),
                                                right=ft.BorderSide(1, LINE),
                                                bottom=ft.BorderSide(1, LINE),
                                            ),
                                            content=ft.Column(
                                                [
                                                    preview_count_text,
                                                    preview_title_text,
                                                    ft.Container(height=4),
                                                    preview_tags_row,
                                                    preview_desc_text,
                                                    ft.Container(height=8),
                                                    ft.Container(
                                                        height=420,
                                                        padding=ft.Padding(12, 12, 12, 12),
                                                        border_radius=10,
                                                        bgcolor=ft.Colors.with_opacity(0.05, BG),
                                                        border=ft.Border(
                                                            left=ft.BorderSide(1, LINE),
                                                            top=ft.BorderSide(1, LINE),
                                                            right=ft.BorderSide(1, LINE),
                                                            bottom=ft.BorderSide(1, LINE),
                                                        ),
                                                        content=ft.Stack(
                                                            [
                                                                ft.Container(
                                                                    alignment=ft.Alignment(0, 0),
                                                                    content=preview_image,
                                                                ),
                                                                ft.Container(
                                                                    alignment=ft.Alignment(1, 1),
                                                                    padding=ft.Padding(12, 12, 12, 12),
                                                                    content=ft.Container(
                                                                        padding=ft.Padding(10, 6, 10, 6),
                                                                        border_radius=4,
                                                                        bgcolor=ft.Colors.with_opacity(0.78, BG),
                                                                        content=ft.Text(
                                                                            "Rendered from the local PDF file",
                                                                            size=11,
                                                                            color=MUTED,
                                                                        ),
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ),
                                                    ft.Container(
                                                        padding=ft.Padding(16, 16, 16, 16),
                                                        border_radius=10,
                                                        bgcolor=ft.Colors.with_opacity(0.12, AMBER),
                                                        border=ft.Border(
                                                            left=ft.BorderSide(2, AMBER),
                                                            top=ft.BorderSide(1, ft.Colors.with_opacity(0.35, AMBER)),
                                                            right=ft.BorderSide(1, ft.Colors.with_opacity(0.35, AMBER)),
                                                            bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.35, AMBER)),
                                                        ),
                                                        content=ft.Column(
                                                            [
                                                                ft.Row(
                                                                    [
                                                                        ft.Icon(ft.Icons.MENU_BOOK, color=AMBER, size=18),
                                                                        ft.Text("Certificate file", size=13, color=AMBER, weight=ft.FontWeight.W_800),
                                                                    ],
                                                                    spacing=8,
                                                                ),
                                                                preview_file_text,
                                                                preview_note_text,
                                                            ],
                                                            spacing=8,
                                                        ),
                                                    ),
                                                ],
                                                spacing=12,
                                            ),
                                        ),
                                    ],
                                    spacing=14,
                                ),
                                accent=ARC,
                            ),
                        ),
                    ],
                    spacing=16,
                    run_spacing=16,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # GITHUB PAGE
    # ══════════════════════════════════════════════════════════════════════════
    github_page = shell(
        ft.Column(
            [
                heading("GitHub", "Open-source code, engineering notebooks, and project repositories."),
                ft.Container(height=28),

                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=GOLD, border_radius=2),
                        ft.Text("CERTIFICATE PORTFOLIO", size=12, color=GOLD, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),
                card(
                    ft.Column(
                        [
                            ft.Text("Browse certificates inside the portfolio.", size=18, color=INK, weight=ft.FontWeight.W_800),
                            ft.Text(
                                "This keeps the certificates on-page, with no browser redirects or external PDF popups.",
                                size=13, color=MUTED,
                            ),
                            ft.Container(
                                padding=ft.Padding(14, 10, 14, 10),
                                border_radius=5,
                                bgcolor=ft.Colors.with_opacity(0.12, GOLD),
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.OPEN_IN_NEW, color=GOLD, size=15),
                                        ft.Text("Open Certificate Viewer", size=12, color=GOLD, weight=ft.FontWeight.W_800),
                                    ],
                                    spacing=8,
                                    tight=True,
                                ),
                                on_click=lambda _: show_page("matlab"),
                            ),
                        ],
                        spacing=12,
                    ),
                    accent=GOLD,
                ),

                ft.Container(height=28),

                # ── Activity Evidence section label ────────────────────────
                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=ARC, border_radius=2),
                        ft.Text("ACTIVITY EVIDENCE", size=12, color=ARC, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),

                # ── GitHub evidence image ───────────────────────────────────
                card(
                    ft.Image(
                        src=GITHUB_EVIDENCE_SRC,
                        fit=IMAGE_FIT_CONTAIN,
                        border_radius=6,
                    ),
                    accent=ARC,
                ) if GITHUB_EVIDENCE_SRC else card(
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED_OUTLINED, color=MUTED, size=18),
                            ft.Text(
                                "No GitHub activity image found in assets/ (filename containing 'github')",
                                size=13, color=MUTED,
                            ),
                        ],
                        spacing=8,
                    ),
                    accent=ARC,
                ),

                ft.Container(height=28),

                # ── Commit History label ───────────────────────────────────
                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=ARC, border_radius=2),
                        ft.Text("COMMIT HISTORY", size=12, color=ARC, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),
                card(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.COMMIT, color=ARC, size=18),
                                    ft.Column(
                                        [
                                            ft.Text(msg, size=14, color=INK, weight=ft.FontWeight.W_700),
                                            ft.Row(
                                                [
                                                    tag(repo, ARC),
                                                    tag(branch, STEEL),
                                                    ft.Text(date, size=12, color=MUTED),
                                                ],
                                                spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                        ],
                                        spacing=6, expand=True,
                                    ),
                                ],
                                spacing=12, vertical_alignment=ft.CrossAxisAlignment.START,
                            )
                            for msg, repo, branch, date in commit_history
                        ],
                        spacing=18,
                    ),
                    accent=ARC,
                ),
                ft.Container(height=28),

                # ── Pull Request Logs label ────────────────────────────────
                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=AMBER, border_radius=2),
                        ft.Text("PULL REQUEST LOGS", size=12, color=AMBER, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),
                ft.Column(
                    [
                        card(
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(title, size=15, weight=ft.FontWeight.W_800, color=INK, expand=True),
                                            tag(status, scolor),
                                        ],
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    ft.Row([tag(repo, STEEL)], spacing=6),
                                    ft.Text(desc, size=13, color=MUTED),
                                ],
                                spacing=10,
                            ),
                            accent=scolor,
                        )
                        for title, repo, status, scolor, desc in pull_requests
                    ],
                    spacing=14,
                ),
                ft.Container(height=28),

                # ── Impact Summary label ───────────────────────────────────
                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=GOLD, border_radius=2),
                        ft.Text("IMPACT SUMMARY", size=12, color=GOLD, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),
                card(
                    ft.Text(impact_summary_text, size=15, color=STEEL),
                    accent=GOLD,
                ),

                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=AMBER, border_radius=2),
                        ft.Text("REPOSITORIES", size=12, color=AMBER, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                        ft.Text(f"{len(github_repos)} public repos", size=12, color=MUTED),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),

                ft.ResponsiveRow(
                    [
                        ft.Container(
                            col={"sm": 12, "md": 6, "lg": 4},
                            content=card(
                                ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Container(width=38, height=38, border_radius=8,
                                                    bgcolor=ft.Colors.with_opacity(0.14, rc),
                                                    alignment=ft.Alignment(0, 0),
                                                    content=ft.Icon(ri, color=rc, size=20)),
                                                ft.Text(rn, size=15, weight=ft.FontWeight.W_800, color=rc, expand=True),
                                            ],
                                            spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        ft.Text(rd, size=13, color=MUTED),
                                        ft.Row([tag(t, STEEL) for t in rt], spacing=6, wrap=True),
                                        ft.Container(
                                            padding=ft.Padding(14, 8, 14, 8), border_radius=5,
                                            border=ft.Border(left=ft.BorderSide(1, ft.Colors.with_opacity(0.5, rc)), top=ft.BorderSide(1, ft.Colors.with_opacity(0.5, rc)), right=ft.BorderSide(1, ft.Colors.with_opacity(0.5, rc)), bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.5, rc))),
                                            bgcolor=ft.Colors.with_opacity(0.08, rc),
                                            content=ft.Row([ft.Icon(ft.Icons.OPEN_IN_NEW, color=rc, size=14), ft.Text("Open Repository", size=12, color=rc, weight=ft.FontWeight.W_700)], spacing=6, tight=True),
                                            on_click=lambda _, u=ru: open_url(u),
                                        ),
                                    ],
                                    spacing=12,
                                ),
                                accent=rc,
                            ),
                        )
                        for rn, rd, rt, ri, rc, ru in github_repos
                    ],
                    spacing=16, run_spacing=16,
                ),
                ft.Container(height=24),
                card(
                    ft.Row(
                        [
                            ft.Column([ft.Text(str(len(github_repos)), size=36, weight=ft.FontWeight.W_900, color=AMBER), ft.Text("Repositories", size=12, color=MUTED, weight=ft.FontWeight.W_600)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Container(width=1, height=50, bgcolor=LINE),
                            ft.Column([ft.Text("Python", size=36, weight=ft.FontWeight.W_900, color=ARC),  ft.Text("Primary Language", size=12, color=MUTED, weight=ft.FontWeight.W_600)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Container(width=1, height=50, bgcolor=LINE),
                            ft.Column([ft.Text("MIT",    size=36, weight=ft.FontWeight.W_900, color=GOLD), ft.Text("Licence",          size=12, color=MUTED, weight=ft.FontWeight.W_600)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            ft.Container(width=1, height=50, bgcolor=LINE),
                            ft.Column([ft.Text("2026",   size=36, weight=ft.FontWeight.W_900, color=AMBER),ft.Text("Active Since",     size=12, color=MUTED, weight=ft.FontWeight.W_600)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True,
                    ),
                    accent=ARC,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SCHOOL PAGE
    # ══════════════════════════════════════════════════════════════════════════
    school_page = shell(
        ft.Column(
            [
                heading("Education", "The institution forging the engineer."),
                ft.Container(height=28),
                card(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(width=88, height=88, border_radius=12,
                                        bgcolor=ft.Colors.WHITE, alignment=ft.Alignment(0, 0),
                                        content=ft.Image(src="unam logo.jpeg", width=78, height=78, fit=IMAGE_FIT_CONTAIN)),
                                    ft.Column(
                                        [
                                            ft.Text("University of Namibia", size=28, weight=ft.FontWeight.W_900, color=INK),
                                            ft.Text("Jose Eduardo dos Santos Engineering Campus", size=16, color=AMBER, weight=ft.FontWeight.W_600),
                                            ft.Text("Bachelor of Engineering (Honours) — Metallurgy", size=14, color=MUTED),
                                        ],
                                        spacing=6, expand=True,
                                    ),
                                ],
                                spacing=24, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Container(height=1, bgcolor=LINE),
                            ft.ResponsiveRow(
                                [
                                    ft.Container(col={"sm": 12, "md": 4}, content=ft.Container(padding=16, border_radius=8, bgcolor=ft.Colors.with_opacity(0.10, AMBER), content=ft.Column([ft.Icon(ft.Icons.LOCATION_ON, color=AMBER, size=26), ft.Text("Location", size=12, color=MUTED), ft.Text("Ongwediva, Oshana Region\nNamibia", size=15, color=INK, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6))),
                                    ft.Container(col={"sm": 12, "md": 4}, content=ft.Container(padding=16, border_radius=8, bgcolor=ft.Colors.with_opacity(0.10, ARC),   content=ft.Column([ft.Icon(ft.Icons.SCIENCE,     color=ARC,   size=26), ft.Text("Faculty",  size=12, color=MUTED), ft.Text("Faculty of Engineering\n& IT",           size=15, color=INK, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6))),
                                    ft.Container(col={"sm": 12, "md": 4}, content=ft.Container(padding=16, border_radius=8, bgcolor=ft.Colors.with_opacity(0.10, ARC),   content=ft.Column([ft.Icon(ft.Icons.VERIFIED,    color=ARC,   size=26), ft.Text("Status",   size=12, color=MUTED), ft.Text("Currently Enrolled\nFull-Time",          size=15, color=INK, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6))),
                                ],
                                spacing=14, run_spacing=14,
                            ),
                        ],
                        spacing=22,
                    ),
                    width=1020,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TIMELINE PAGE
    # ══════════════════════════════════════════════════════════════════════════
    timeline_page = shell(
        ft.Column(
            [
                heading("Timeline", "Six weeks — from architecture to deployment."),
                ft.Container(height=28),
                card(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(width=88, padding=ft.Padding(0, 14, 0, 14),
                                        bgcolor=ft.Colors.with_opacity(0.15, AMBER), border_radius=6,
                                        alignment=ft.Alignment(0, 0),
                                        content=ft.Text(week, size=16, color=AMBER, weight=ft.FontWeight.W_900)),
                                    ft.Container(width=3, height=48, bgcolor=ft.Colors.with_opacity(0.25, AMBER)),
                                    ft.Column(
                                        [
                                            ft.Text(subtitle, size=15, color=STEEL, weight=ft.FontWeight.W_600),
                                            ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ARC, size=14),
                                                    ft.Text(status, size=12, color=ARC, weight=ft.FontWeight.W_700)], spacing=6),
                                        ],
                                        spacing=5, expand=True,
                                    ),
                                ],
                                spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            )
                            for week, subtitle, status in timeline
                        ],
                        spacing=14,
                    ),
                    width=1100,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TECHNICAL BLOG PAGE
    # ══════════════════════════════════════════════════════════════════════════
    blog_posts = [
        (
            "Confidence in Concepts: Total Cost Modelling",
            ft.Icons.CALCULATE,
            AMBER,
            "When estimating the cost of a batch of raw materials for an alloy formulation, every "
            "component contributes proportionally to its quantity and unit price, with fixed "
            "overheads added on top. Expressed formally, the total cost for n materials is:",
            "Total Cost = \u03A3 (i=1 to n) [ Q\u1d62 \u00D7 P\u1d62 ]  +  Overheads",
            "In the alloy dashboard module, this maps directly to a loop over each material's "
            "quantity (Qi) and unit price (Pi), summed and combined with a fixed overhead constant. "
            "Implementing it this way keeps the calculation auditable — each line item can be traced "
            "back to a single multiplication, which matters when an engineer needs to justify a "
            "costing decision to a client.",
        ),
        (
            "Confidence in Concepts: Cooling Curve Analysis",
            ft.Icons.SHOW_CHART,
            ARC,
            "Phase transformations during solidification appear as inflection points or plateaus "
            "in a temperature-time curve, because latent heat release temporarily slows the cooling "
            "rate. The cooling rate at any point can be approximated as the derivative of temperature "
            "with respect to time:",
            "Cooling Rate = dT / dt",
            "The cooling-curve plotter detects these plateaus by computing a discrete approximation "
            "of dT/dt across the dataset and flagging windows where the rate drops sharply below the "
            "surrounding average. This lets the tool automatically mark candidate phase-transformation "
            "temperatures for an engineer to review, rather than requiring manual inspection of every "
            "curve.",
        ),
        (
            "Confidence in Concepts: Corrosion Rate Estimation",
            ft.Icons.FACT_CHECK,
            GOLD,
            "Corrosion rate from weight-loss data depends on the mass lost, the exposed surface "
            "area, the material density, and the exposure time. A common form used in the "
            "corrosion logbook is:",
            "Corrosion Rate = (K \u00D7 W) / (A \u00D7 T \u00D7 D)",
            "Here K is a unit-conversion constant, W is mass loss, A is exposed area, T is exposure "
            "time, and D is material density. The logbook stores W, A, T, and D for each sample and "
            "computes the rate automatically, which removes a common source of manual arithmetic "
            "error in lab record-keeping.",
        ),
    ]

    def blog_post_card(title, icon, color, intro, formula, body):
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(width=46, height=46, border_radius=10,
                                bgcolor=ft.Colors.with_opacity(0.15, color),
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(icon, color=color, size=24)),
                            ft.Text(title, size=18, weight=ft.FontWeight.W_800, color=INK, expand=True),
                        ],
                        spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Text(intro, size=14, color=STEEL),
                    ft.Container(
                        padding=ft.Padding(18, 14, 18, 14),
                        border_radius=6,
                        bgcolor=ft.Colors.with_opacity(0.10, color),
                        border=ft.Border(left=ft.BorderSide(3, color), top=ft.BorderSide(1, ft.Colors.with_opacity(0.3, color)), right=ft.BorderSide(1, ft.Colors.with_opacity(0.3, color)), bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.3, color))),
                        content=ft.Text(formula, size=16, color=color, weight=ft.FontWeight.W_700,
                                         style=ft.TextStyle(italic=True, letter_spacing=1)),
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Text(body, size=14, color=MUTED),
                ],
                spacing=14,
            ),
            accent=color,
        )

    blog_page = shell(
        ft.Column(
            [
                heading("Technical Blog", "Confidence in Concepts — written explanations and a project reflection."),
                ft.Container(height=28),

                # ── Confidence in Concepts label ───────────────────────────
                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=AMBER, border_radius=2),
                        ft.Text("CONFIDENCE IN CONCEPTS", size=12, color=AMBER, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),
                ft.Column(
                    [blog_post_card(*post) for post in blog_posts],
                    spacing=18,
                ),
                ft.Container(height=28),

                # ── Reflection Video label ─────────────────────────────────
                ft.Row(
                    [
                        ft.Container(width=3, height=20, bgcolor=ARC, border_radius=2),
                        ft.Text("SEMESTER PROJECT REFLECTION", size=12, color=ARC, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=3)),
                        ft.Container(expand=True, height=1, bgcolor=LINE),
                    ],
                    spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=14),
                card(
                    ft.Column(
                        [
                            ft.Text(
                                "A short video (max 1:30) detailing my individual contributions to the "
                                "group project this semester.",
                                size=14, color=MUTED, style=ft.TextStyle(italic=True),
                            ),
                            ft.Container(
                                height=400,
                                border_radius=8,
                                bgcolor=PANEL_2,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Video(
                                    playlist=[ft.VideoMedia(REFLECTION_VIDEO_SRC)],
                                    autoplay=False,
                                    show_controls=True,
                                    aspect_ratio=16 / 9,
                                    fill_color=PANEL_2,
                                ) if (REFLECTION_VIDEO_SRC and HAS_VIDEO_WIDGET) else ft.Column(
                                    [
                                        ft.Icon(ft.Icons.VIDEOCAM_OUTLINED, color=MUTED, size=40),
                                        ft.Text(
                                            "No reflection video found in assets/ "
                                            "(filename containing 'reflection', e.g. reflection.mp4)"
                                            if not REFLECTION_VIDEO_SRC else
                                            "Video found, but the 'flet-video' package is not installed.\n"
                                            "Run: pip install flet-video",
                                            size=13, color=MUTED, text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                    spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ],
                        spacing=14,
                    ),
                    accent=ARC,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # CONTACT PAGE
    # ══════════════════════════════════════════════════════════════════════════
    def _tf(label, multiline=False, min_lines=1, max_lines=1):
        return ft.TextField(
            label=label, text_size=15, multiline=multiline,
            min_lines=min_lines, max_lines=max_lines,
            border_radius=6, border_color=LINE,
            focused_border_color=AMBER, cursor_color=AMBER,
            label_style=ft.TextStyle(color=MUTED, size=13),
            text_style=ft.TextStyle(color=INK),
        )

    name_field    = _tf("Your Name")
    email_field   = _tf("Your Email")
    message_field = _tf("Your Message", multiline=True, min_lines=5, max_lines=10)

    contact_page = shell(
        ft.Column(
            [
                heading("Contact", "Open to collaboration, research partnerships, and opportunities."),
                ft.Container(height=28),
                card(
                    ft.Column(
                        [
                            ft.Text("Whether you have a project idea, a research question, or just want to connect — reach out. I respond to every serious enquiry.",
                                    size=15, color=MUTED, style=ft.TextStyle(italic=True)),
                            ft.Container(height=1, bgcolor=LINE),
                            name_field,
                            email_field,
                            message_field,
                            ft.Row(
                                [
                                    ft.Container(
                                        padding=ft.Padding(28, 13, 28, 13), border_radius=6, bgcolor=AMBER,
                                        content=ft.Row([ft.Icon(ft.Icons.SEND, color=BG, size=17), ft.Text("Send Message", size=14, color=BG, weight=ft.FontWeight.W_800)], spacing=8, tight=True),
                                        on_click=contact_submit,
                                    ),
                                    ft.Container(
                                        padding=ft.Padding(22, 13, 22, 13), border_radius=6,
                                        border=ft.Border(left=ft.BorderSide(1, LINE), top=ft.BorderSide(1, LINE), right=ft.BorderSide(1, LINE), bottom=ft.BorderSide(1, LINE)),
                                        content=ft.Row([ft.Icon(ft.Icons.HOME_OUTLINED, color=MUTED, size=17), ft.Text("Back Home", size=14, color=MUTED)], spacing=8, tight=True),
                                        on_click=lambda _: show_page("home"),
                                    ),
                                ],
                                spacing=12, wrap=True,
                            ),
                        ],
                        spacing=16,
                    ),
                    width=940,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # ══════════════════════════════════════════════════════════════════════════
    # NAVIGATION
    # ══════════════════════════════════════════════════════════════════════════
    pages = {
        "home":     home_page,
        "skills":   skills_page,
        "projects": projects_page,
        "matlab":   matlab_page,
        "github":   github_page,
        "school":   school_page,
        "timeline": timeline_page,
        "blog":     blog_page,
        "contact":  contact_page,
    }

    page_host   = ft.Column([], expand=True)
    nav_buttons = {}

    def nav_style(is_active: bool):
        return ft.ButtonStyle(
            color=AMBER if is_active else STEEL,
            bgcolor=ft.Colors.with_opacity(0.12, AMBER) if is_active else ft.Colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(radius=5),
            text_style=ft.TextStyle(size=12, weight=ft.FontWeight.W_700, letter_spacing=1),
            padding=ft.Padding(14, 10, 14, 10),
        )

    def set_nav_styles():
        for key, btn in nav_buttons.items():
            btn.style = nav_style(key == active_key)

    def show_page(key: str):
        nonlocal active_key
        active_key = key
        page_host.controls.clear()
        page_host.controls.append(pages[key])
        set_nav_styles()
        page.update()

    def make_nav(label: str, key: str, icon: str):
        btn = ft.TextButton(
            label.upper(), icon=icon,
            style=nav_style(key == active_key),
            on_click=lambda _, k=key: show_page(k),
        )
        nav_buttons[key] = btn
        return btn

    nav_items = [
        ("Home",     "home",     ft.Icons.HOME_OUTLINED),
        ("Skills",   "skills",   ft.Icons.BUILD_OUTLINED),
        ("Projects", "projects", ft.Icons.WORK_OUTLINE),
        ("Certificates", "matlab", ft.Icons.DESCRIPTION_OUTLINED),
        ("GitHub",   "github",   ft.Icons.CODE),
        ("School",   "school",   ft.Icons.SCHOOL_OUTLINED),
        ("Timeline", "timeline", ft.Icons.TIMELINE),
        ("Blog",     "blog",     ft.Icons.ARTICLE_OUTLINED),
        ("Contact",  "contact",  ft.Icons.EMAIL_OUTLINED),
    ]

    desktop_nav = ft.Row([make_nav(label, key, icon) for label, key, icon in nav_items], spacing=2, wrap=True)
    mobile_nav  = ft.PopupMenuButton(
        icon=ft.Icons.MENU, icon_color=AMBER, tooltip="Navigation",
        items=[
            ft.PopupMenuItem(
                content=ft.Row([ft.Icon(icon, size=16, color=AMBER), ft.Text(label, color=INK, weight=ft.FontWeight.W_600)], spacing=10, tight=True),
                on_click=lambda _, k=key: show_page(k),
            )
            for label, key, icon in nav_items
        ],
    )

    def update_nav_visibility(_=None):
        w = page.width or 1200
        desktop_nav.visible = w >= 1000
        mobile_nav.visible  = w < 1000
        page.update()

    page.on_resize = update_nav_visibility

    page.appbar = ft.AppBar(
        toolbar_height=64,
        title=ft.Row(
            [
                ft.Container(width=36, height=36, border_radius=6, bgcolor=AMBER,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Image(src="unam_logo.png", width=26, height=26, fit=IMAGE_FIT_CONTAIN)),
                ft.Column(
                    [
                        ft.Text(PROFILE_NAME, size=15, color=INK, weight=ft.FontWeight.W_800,
                                style=ft.TextStyle(letter_spacing=1)),
                        ft.Text("Metallurgy · Software", size=10, color=AMBER, weight=ft.FontWeight.W_700,
                                style=ft.TextStyle(letter_spacing=2)),
                    ],
                    spacing=1,
                ),
            ],
            spacing=12, tight=True,
        ),
        bgcolor=PANEL,
        actions=[desktop_nav, mobile_nav],
    )

    page.add(
        ft.Container(
            height=3,
            gradient=ft.LinearGradient(colors=[AMBER, GOLD, ARC, AMBER], begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0)),
        ),
        page_host,
        ft.Container(
            padding=ft.Padding(48, 18, 48, 18),
            bgcolor=PANEL,
            border=ft.Border(top=ft.BorderSide(1, LINE)),
            content=ft.Row(
                [
                    ft.Text("© 2026  Shivute Johannes S  ·  Metallurgical Engineering Portfolio  ·  Built with Flet", color=MUTED, size=12),
                    ft.Row(
                        [
                            ft.Container(padding=ft.Padding(10, 6, 10, 6), border_radius=4, content=ft.Text("GitHub",   size=12, color=MUTED), on_click=lambda _: open_url(PROFILE_GITHUB)),
                            ft.Container(padding=ft.Padding(10, 6, 10, 6), border_radius=4, content=ft.Text("LinkedIn", size=12, color=MUTED), on_click=lambda _: open_url(PROFILE_LINKEDIN)),
                        ],
                        spacing=4,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True,
            ),
        ),
    )

    show_page("home")
    update_nav_visibility()


if __name__ == "__main__":
    print(f"Launching: {__file__}")
    ft.app(                          # ← FIXED: was ft.run — ft.app is correct
        target=main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER,
        port=8550,
    )