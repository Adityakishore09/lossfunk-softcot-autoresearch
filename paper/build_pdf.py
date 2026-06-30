from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image as RLImage,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
OUT = ROOT / "main.pdf"
FIG_DIR.mkdir(exist_ok=True)


def font(size=16, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_bar_chart(path, title, labels, series, colors_hex, y_min=0.0, y_max=1.0, ylabel="Accuracy"):
    width, height = 1300, 760
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    f_title = font(34, True)
    f_axis = font(22)
    f_small = font(19)
    left, right, top, bottom = 120, 60, 110, 130
    plot_w, plot_h = width - left - right, height - top - bottom
    d.text((width / 2, 35), title, fill=(20, 20, 20), font=f_title, anchor="ma")
    for i in range(6):
        val = y_min + (y_max - y_min) * i / 5
        y = top + plot_h - (val - y_min) / (y_max - y_min) * plot_h
        d.line((left, y, width - right, y), fill=(225, 225, 225), width=1)
        d.text((left - 12, y), f"{val:.1f}", fill=(70, 70, 70), font=f_small, anchor="ra")
    d.line((left, top, left, top + plot_h), fill=(40, 40, 40), width=2)
    d.line((left, top + plot_h, width - right, top + plot_h), fill=(40, 40, 40), width=2)
    d.text((60, top + plot_h / 2), ylabel, fill=(60, 60, 60), font=f_axis, anchor="mm")
    groups = len(labels)
    n_series = len(series)
    group_w = plot_w / groups
    bar_w = min(70, group_w / (n_series + 1.5))
    for gi, label in enumerate(labels):
        cx = left + group_w * (gi + 0.5)
        d.text((cx, top + plot_h + 28), label, fill=(35, 35, 35), font=f_axis, anchor="ma")
        for si, (name, vals) in enumerate(series.items()):
            val = vals[gi]
            x0 = cx - (n_series * bar_w) / 2 + si * bar_w
            x1 = x0 + bar_w * 0.82
            y = top + plot_h - (val - y_min) / (y_max - y_min) * plot_h
            d.rectangle((x0, y, x1, top + plot_h), fill=colors_hex[si])
            d.text(((x0 + x1) / 2, y - 8), f"{val:.3f}", fill=(40, 40, 40), font=f_small, anchor="mb")
    legend_x = left + 20
    legend_y = height - 55
    for si, name in enumerate(series.keys()):
        d.rectangle((legend_x, legend_y - 12, legend_x + 22, legend_y + 10), fill=colors_hex[si])
        d.text((legend_x + 32, legend_y), name, fill=(40, 40, 40), font=f_small, anchor="lm")
        legend_x += 260
    img.save(path)


def draw_delta_chart(path):
    width, height = 1300, 620
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    f_title = font(34, True)
    f_axis = font(22)
    f_small = font(19)
    title = "Learned SoftCoT minus no-SoftCoT baseline"
    d.text((width / 2, 35), title, fill=(20, 20, 20), font=f_title, anchor="ma")
    labels = ["GSM8K", "ASDiv-Aug", "StrategyQA", "ASDiv full", "StrategyQA full"]
    vals = [-0.0433, -0.0117, 0.1150, -0.0135, 0.1063]
    left, right, top, bottom = 180, 70, 110, 90
    plot_w, plot_h = width - left - right, height - top - bottom
    x0 = left + plot_w / 2
    scale = plot_w / 2 / 0.15
    for tick in [-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15]:
        x = x0 + tick * scale
        d.line((x, top, x, top + plot_h), fill=(230, 230, 230), width=1)
        d.text((x, top + plot_h + 20), f"{tick:+.2f}", fill=(70, 70, 70), font=f_small, anchor="ma")
    d.line((x0, top, x0, top + plot_h), fill=(40, 40, 40), width=3)
    row_h = plot_h / len(labels)
    for i, (lab, val) in enumerate(zip(labels, vals)):
        y = top + row_h * (i + 0.5)
        d.text((left - 15, y), lab, fill=(35, 35, 35), font=f_axis, anchor="rm")
        x_end = x0 + val * scale
        fill = (42, 130, 218) if val >= 0 else (208, 82, 82)
        d.rectangle((min(x0, x_end), y - 20, max(x0, x_end), y + 20), fill=fill)
        d.text((x_end + (8 if val >= 0 else -8), y), f"{val:+.4f}", fill=(30, 30, 30), font=f_small, anchor="lm" if val >= 0 else "rm")
    img.save(path)


draw_bar_chart(
    FIG_DIR / "core_accuracy.png",
    "Core fixed-split accuracy by condition",
    ["GSM8K", "ASDiv-Aug", "StrategyQA"],
    {
        "Learned": [0.8250, 0.8567, 0.6517],
        "Zero control": [0.7950, 0.7950, 0.5867],
        "Baseline": [0.8683, 0.8683, 0.5367],
    },
    [(44, 123, 182), (255, 187, 120), (127, 127, 127)],
)
draw_delta_chart(FIG_DIR / "learned_minus_baseline.png")


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, fontSize=18, leading=22, spaceAfter=12))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10, leading=13, textColor=colors.HexColor("#444444"), spaceAfter=12))
styles.add(ParagraphStyle(name="Body", parent=styles["Normal"], fontSize=9.4, leading=12, spaceAfter=6))
styles.add(ParagraphStyle(name="Small", parent=styles["Normal"], fontSize=8, leading=10, spaceAfter=4))
styles.add(ParagraphStyle(name="Heading1x", parent=styles["Heading1"], fontSize=13, leading=16, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="Heading2x", parent=styles["Heading2"], fontSize=11, leading=14, spaceBefore=8, spaceAfter=4))


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def H(text):
    return Paragraph(text, styles["Heading1x"])


def H2(text):
    return Paragraph(text, styles["Heading2x"])


def bullets(items):
    return ListFlowable([ListItem(P(x), leftIndent=10) for x in items], bulletType="bullet", start="circle", leftIndent=18)


def table(data, widths=None, small=True):
    tbl = Table(data, colWidths=widths, repeatRows=1)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.6 if small else 8.6),
                ("LEADING", (0, 0), (-1, -1), 9.2 if small else 10.5),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bbbbbb")),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return tbl


story = []
story.append(P("A Timeboxed Transfer Audit of GSM8K-Trained SoftCoT", "TitleCenter"))
story.append(P("Aditya Kishore - Lossfunk Autoresearch Sprint - AI-authored first draft", "Subtitle"))
story.append(H("Abstract"))
story.append(P("Soft chain-of-thought methods invite an attractive interpretation: if learned continuous thought tokens improve benchmark accuracy, perhaps they encode reusable latent reasoning. This first-draft autoresearch artifact tests a narrow version of that interpretation. We trained only the SoftCoT projection component on GSM8K and evaluated the resulting source-trained setup on GSM8K, ASDiv-Aug, and StrategyQA, with no target-task tuning. Across three seeds and fixed 200-example splits, learned SoftCoT improved over a zero soft-thought control on all three datasets, but did not improve over the no-SoftCoT baseline on GSM8K or ASDiv-Aug. The clearest learned-over-baseline gain instead appeared on StrategyQA: +11.5 points on the fixed subset and +10.6 points in a full-dev extension. The original related-transfer hypothesis was not supported."))
story.append(H("1. Introduction"))
story.append(P("SoftCoT proposes to replace part of explicit chain-of-thought decoding with instance-specific soft thought tokens produced by a small assistant model and projected into a larger frozen model's representation space. The submitted proposal asked whether these soft thought tokens should be interpreted as reusable latent reasoning states or as task-specific continuous prompts."))
story.append(P("The sprint tested one diagnostic: transfer. If GSM8K-trained soft thoughts encode reusable arithmetic reasoning, their learned projection should help ASDiv-Aug, a related arithmetic target, more than StrategyQA, a boolean commonsense target. The observed pattern was the reverse of the intended support: the learned projection beat a zero control but did not beat baseline on ASDiv-Aug, while it consistently beat baseline on StrategyQA."))
story.append(bullets([
    "A scoped source-only SoftCoT transfer audit using Qwen2.5 models.",
    "Three-seed fixed-split comparisons on GSM8K, ASDiv-Aug, and StrategyQA.",
    "Controls for learned SoftCoT, zero soft-thought vectors, and no-SoftCoT baseline.",
    "A full-target learned-versus-baseline extension for StrategyQA dev and ASDiv-Aug test.",
    "Visible preservation of failures, caveats, costs, and human interventions.",
]))
story.append(H("2. Experimental design"))
story.append(P("The experiment used Qwen2.5-7B-Instruct as the frozen base model and Qwen2.5-1.5B-Instruct as the fixed assistant model. Only the projection module was trained; logs report 5,508,608 trainable parameters out of 9,164,839,424 total parameters. The source task was GSM8K. The related target was ASDiv-Aug. The unrelated target was StrategyQA."))
story.append(P("Each core seed evaluated learned SoftCoT, a zero soft-thought control, and a no-SoftCoT baseline on deterministic 200-example fixed splits. Target labels were not used for tuning, prompt selection, or checkpoint selection. The full-target extension reused existing checkpoints and evaluated learned SoftCoT versus baseline on full StrategyQA dev (229 examples per seed) and ASDiv-Aug test (1,038 examples per seed)."))
story.append(H("3. Results"))
story.append(P("Table 1 gives the core fixed-split means. Learned SoftCoT beat zero controls on all tasks, but it did not beat the no-SoftCoT baseline on GSM8K or ASDiv-Aug. It did beat baseline on StrategyQA."))
story.append(table([
    ["Task", "Learned", "Zero control", "Baseline"],
    ["GSM8K", "0.8250", "0.7950", "0.8683"],
    ["ASDiv-Aug", "0.8567", "0.7950", "0.8683"],
    ["StrategyQA", "0.6517", "0.5867", "0.5367"],
], [1.55 * inch, 1.05 * inch, 1.25 * inch, 1.25 * inch]))
story.append(Spacer(1, 8))
story.append(RLImage(str(FIG_DIR / "core_accuracy.png"), width=5.7 * inch, height=3.35 * inch))
story.append(P("The learned-minus-baseline target deltas were -0.0117 on ASDiv-Aug and +0.1150 on StrategyQA. The pre-registered related-minus-unrelated contrast was therefore about -0.1267, not positive."))
story.append(table([
    ["Task", "Seed 41", "Seed 42", "Seed 43"],
    ["GSM8K", "-0.020", "-0.110", "0.000"],
    ["ASDiv-Aug", "-0.030", "-0.050", "+0.045"],
    ["StrategyQA", "+0.105", "+0.090", "+0.150"],
], [1.55 * inch, 1.05 * inch, 1.05 * inch, 1.05 * inch]))
story.append(Spacer(1, 8))
story.append(RLImage(str(FIG_DIR / "learned_minus_baseline.png"), width=5.7 * inch, height=2.72 * inch))
story.append(H2("Item-level agreement"))
story.append(P("Across 600 paired examples per task, learned SoftCoT had 117 StrategyQA items correct that baseline missed, while baseline had 48 items correct that learned SoftCoT missed. On ASDiv-Aug the corresponding counts were 23 versus 30, and on GSM8K they were 36 versus 62."))
story.append(table([
    ["Task", "Paired N", "Learned-only correct", "Baseline-only correct"],
    ["GSM8K", "600", "36", "62"],
    ["ASDiv-Aug", "600", "23", "30"],
    ["StrategyQA", "600", "117", "48"],
], [1.45 * inch, 0.85 * inch, 1.65 * inch, 1.65 * inch]))
story.append(H2("Full-target extension"))
story.append(table([
    ["Task", "N/seed", "Learned", "Baseline", "Delta"],
    ["StrategyQA dev", "229", "0.6405", "0.5342", "+0.1063"],
    ["ASDiv-Aug test", "1,038", "0.8642", "0.8776", "-0.0135"],
], [1.55 * inch, 0.75 * inch, 0.95 * inch, 0.95 * inch, 0.9 * inch]))
story.append(H("4. Discussion"))
story.append(P("The original proposal expected GSM8K-trained soft thoughts to transfer preferentially to another arithmetic dataset. This sprint found the opposite descriptive pattern. The learned projection contains signal relative to a zero-vector intervention, but that signal did not reliably beat direct prompting on the arithmetic source or related target. The robust gain appeared on StrategyQA, the nominally unrelated target."))
story.append(P("This does not prove that SoftCoT is only a hidden prompt. It does weaken the simple reusable-arithmetic-reasoning interpretation. The next proposal should study when soft thought vectors behave as reusable latent reasoning objects versus task- or format-specific continuous prompts. Router, Verifier, and Memory should become follow-up mechanisms, not assumptions."))
story.append(H("5. Reviewer-pass caveats"))
story.append(P("A skeptical reviewer pass before drafting rejected broad transfer claims, confirmation of the related-transfer distinction, statistical significance beyond a small three-seed run, latency claims, and full faithful reproduction claims. Caveats include seed 43's lower-memory protocol, shared GPU contention, simple StrategyQA parsing, fixed-subset limitations, missing full-target zero controls, and Qwen-specific implementation changes."))
story.append(H("6. Reproducibility"))
story.append(P("The canonical artifact root is all-spikes/gsm8k-asdiv-strategyqa-transfer/. The frozen core archive is lossfunk_results_seed41_42_43.tar.gz with SHA-256 0e331230d33b09da8d87ab0000f17d1861a5ea8ced308c90bc573590b89afd8b. The full-target extension archive is lossfunk_full_target_extension_seed41_42_43.tar.gz with SHA-256 7d8ddf85d2dda16bdecc4465860c39c821a9878f9816f170e78ba9bae9c5cfad."))
story.append(P("Main commands: bash scripts/run_seed.sh 41 1; bash scripts/run_seed.sh 42 1; MIN_GPU_FREE_MIB_OVERRIDE=30000 bash scripts/run_seed.sh 43 1; then TASKS=\"strategyqa asdiv-aug\" CONDITIONS=\"learned baseline\" bash scripts/run_full_target_evals.sh for seeds 41, 42, and 43."))
story.append(H("7. Conclusion"))
story.append(P("The seven-day audit corrected the proposal. GSM8K-trained SoftCoT did not show the expected related arithmetic transfer advantage. It contained signal relative to a zero-vector control, but the clearest learned-over-baseline gain appeared on StrategyQA rather than ASDiv-Aug."))
story.append(PageBreak())
story.append(H("Appendix A. Prompt and session summary"))
story.append(P("The full prompt/session record is preserved in logs/human-intervention.md and logs/prompt-session.md. Key human interventions: selected exploration option 1; provided server access; installed the ephemeral public SSH key; asked for exact commands and live status; authorized contended GPU execution and a 30 GiB lower-memory override for seed 43; reported completion snippets; requested full-target and item-level diagnostics; requested this paper draft."))
story.append(H("Appendix B. Material failures preserved"))
story.append(bullets([
    "Seed 41 first run failed at Trainer checkpoint serialization due to Qwen tied weights.",
    "A resume crashed when the evaluator used Instance.get on FastNLP Instance rows.",
    "StrategyQA JSONL fixed splits initially failed under a JSON loader.",
    "Summary regeneration initially refused to overwrite existing outputs.",
    "Several SSH attempts failed due to sandbox or VPN reachability.",
    "No local TeX compiler was available; this PDF was generated with the bundled PDF runtime, while main.tex remains the canonical source.",
]))
story.append(H("Appendix C. AI involvement and responsibility"))
story.append(P("Hypothesis development: mostly AI assisted by human, medium iteration. Experimental design: mostly AI assisted by human, medium iteration. Analysis: AI-generated, medium iteration. Writing: AI-generated, low iteration. AI systems used: Codex for research orchestration and writing; Qwen2.5 models for SoftCoT training/evaluation. No paid external LLM API calls generated scientific results."))
story.append(P("Code, raw results, commands, costs, failures, and dataset provenance are included in the selected spike. Known external spend is US$0.00 because the GPU was user-provided shared lab hardware with no billing receipt. Statistical uncertainty remains limited; no robust significance claim is made."))
story.append(H("References"))
refs = [
    "Xu, Yige, Xu Guo, Zhiwei Zeng, and Chunyan Miao. SoftCoT: Soft Chain-of-Thought for Efficient Reasoning with LLMs. arXiv:2502.12134, 2025.",
    "Qwen Team. Qwen2.5 Technical Report. arXiv:2412.15115, 2025.",
    "Cobbe et al. Training Verifiers to Solve Math Word Problems. arXiv:2110.14168, 2021.",
    "Geva et al. Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies. arXiv:2101.02235, 2021.",
    "Wei et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. arXiv:2201.11903, 2022.",
    "Lester, Al-Rfou, and Constant. The Power of Scale for Parameter-Efficient Prompt Tuning. arXiv:2104.08691, 2021.",
    "Vu et al. SPoT: Better Frozen Model Adaptation through Soft Prompt Transfer. arXiv:2110.07904, 2022.",
    "xuyige. ASDiv-Aug Dataset Card and Test Split. Hugging Face dataset, 2026.",
]
story.append(bullets(refs))


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(letter[0] / 2, 0.45 * inch, f"AI-authored first draft - page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT),
    pagesize=letter,
    rightMargin=0.75 * inch,
    leftMargin=0.75 * inch,
    topMargin=0.72 * inch,
    bottomMargin=0.72 * inch,
)
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(OUT)
