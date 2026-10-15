---
name: scientific-slides
description: Plan evidence-led scientific talks, conference presentations, journal clubs, and thesis defenses. Organize the research question, methods, results, limitations, citations, and rehearsal timing; use the host presentation tools to produce editable PPTX or Beamer. Ordinary business slides do not need this research-specific overlay.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
  runtime: Editable PPTX uses available host presentation tools or task-local PptxGenJS; python-pptx supports file validation. LibreOffice and Poppler or PyMuPDF can render previews. Paid OpenRouter generation is optional and not needed for native charts, text, tables, or supplied figures. Beamer is optional and requires TeX.
  version: "1.12"
  last-reviewed: "2026-10-01"
  skill-author: K-Dense Inc.
  openclaw:
    primaryEnv: OPENROUTER_API_KEY
    envVars:
    - name: OPENROUTER_API_KEY
      required: false
      description: OpenRouter API key for the skill's LLM-powered steps.
---

# Scientific Slides

## Codex route: research content, then editable slides

Use this skill for scientific storytelling and evidence review. When the host provides
a Presentations tool or skill, use it for deck composition, template fidelity, and
export. Otherwise use the PowerPoint guide's native PPTX route. Keep the user's
requested format, language, slide count, and template.

Start with the audience, duration, and source material already supplied. Map each
main finding to its data or paper, preserve units, sample sizes, uncertainty and
limitations, and select the figures that explain the result. Do not invent missing
research findings or citations. Label synthetic examples as synthetic.

Default to editable text, charts, and tables. Embed an existing scientific figure
unchanged when its raw data is unavailable; disclose which figures are raster
images. AI-generated visuals are optional conceptual illustrations, never a
required step or a substitute for measured results. Do not invoke paid image APIs
unless the user requests that route and the environment authorizes it.

`research-lookup`, `scientific-schematics`, and `markitdown` in upstream examples
are optional integrations. Use available source-reading and search tools instead.
Research only the missing context needed by the task. Source counts, slide counts,
and decorative-image rules in reference examples are heuristics, not quotas.

For editable PPTX, read `references/presentation_structure.md`,
`references/data_visualization_slides.md`, and the relevant parts of
`assets/powerpoint_design_guide.md`. Other references are conditional.
Render and inspect every slide. Validate slide count, Chinese text, native chart
data, figure labels, and editability separately from visual appearance. A parser
or a PDF preview cannot prove PowerPoint UI compatibility or accessibility.
Report any application-level checks that were not performed.

The image-generation and Beamer examples below are optional upstream workflows.
The Codex route above governs this adapted package when an example conflicts.

## Overview

Scientific presentations are a critical medium for communicating research, sharing findings, and engaging with academic and professional audiences. This skill provides comprehensive guidance for creating effective scientific presentations, from structure and content development to visual design and delivery preparation.

**Key Focus**: Oral presentations for conferences, seminars, defenses, and professional talks.

**CRITICAL DESIGN PHILOSOPHY**: Scientific presentations should be VISUALLY ENGAGING and RESEARCH-BACKED. Avoid dry, text-heavy slides at all costs. Great scientific presentations combine:
- **Compelling visuals**: High-quality figures, images, diagrams (not just bullet points)
- **Research context**: Proper citations from research-lookup establishing credibility
- **Minimal text**: Bullet points as prompts, YOU provide the explanation verbally
- **Professional design**: Modern color schemes, strong visual hierarchy, generous white space
- **Story-driven**: Clear narrative arc, not just data dumps

**Remember**: Boring presentations = forgotten science. Make your slides visually memorable while maintaining scientific rigor through proper citations.

## When to Use This Skill

This skill should be used when:
- Preparing conference presentations (5-20 minutes)
- Developing academic seminars (45-60 minutes)
- Creating thesis or dissertation defense presentations
- Designing grant pitch presentations
- Preparing journal club presentations
- Giving research talks at institutions or companies
- Teaching or tutorial presentations on scientific topics

## Slide Generation with Nano Banana 2

The bundled image helper uses `google/gemini-3.1-flash-image` (Nano Banana 2),
with `google/gemini-3.7-flash` for visual review. API contracts, setup, and limitations
are in [references/script_reference.md](references/script_reference.md). Generated
images are drafts: verify every claim, label, citation, and scientific relationship.

There are two workflows depending on output format:

### Image Workflow: PDF Slides

Generate conceptual or overview slides as complete images, then combine them into a PDF. Use editable PowerPoint or Beamer for quantitative results, exact equations, accessible text, or a user-supplied template.

**How it works:**
1. **Plan the deck**: Create a detailed plan for each slide (title, key points, visual elements)
2. **Generate slides**: Call Nano Banana 2 for each slide to create complete slide images
3. **Combine to PDF**: Assemble slide images into a single PDF presentation

**Step 1: Plan Each Slide**

Before generating, create a detailed plan for your presentation:

```markdown
# Presentation Plan: Introduction to Machine Learning

## Slide 1: Title Slide
- Title: "Machine Learning: From Theory to Practice"
- Subtitle: "AI Conference 2025"
- Speaker: Dr. Jane Smith, University of XYZ
- Visual: Modern abstract neural network background

## Slide 2: Introduction
- Title: "Why Machine Learning Matters"
- Key points: Industry adoption, breakthrough applications, future potential
- Visual: Icons showing different ML applications (healthcare, finance, robotics)

## Slide 3: Core Concepts
- Title: "The Three Types of Learning"
- Content: Supervised, Unsupervised, Reinforcement
- Visual: Three-part diagram showing each type with examples

... (continue for all slides)
```

**Step 2: Generate Each Slide**

Use the `generate_slide_image.py` script to create each slide.

**CRITICAL: Formatting Consistency Protocol**

To ensure unified formatting across all slides in a presentation:

1. **Define a Formatting Goal** at the start of your presentation and include it in EVERY prompt:
   - Color scheme (e.g., "dark blue background, white text, gold accents")
   - Typography style (e.g., "bold sans-serif titles, clean body text")
   - Visual style (e.g., "minimal, professional, corporate aesthetic")
   - Layout approach (e.g., "generous white space, left-aligned content")

2. **Always attach the previous slide** when generating subsequent slides using `--attach`:
   - This allows Nano Banana 2 to see and match the existing style
   - Creates visual continuity throughout the deck
   - Ensures consistent colors, fonts, and design language

3. **Use the supplied presenter name and affiliation**; omit them if unknown.

4. **Include citations directly in the prompt** for slides that reference research:
   - Add citations in the prompt text so they appear on the generated slide
   - Use format: "Include citation: (Author et al., Year)" or "Show reference: Author et al., Year"
   - For multiple citations, list them all in the prompt
   - Citations should appear in small text at the bottom of the slide or near relevant content

5. **Preserve scientific figures as original assets**:
   - Locate the user's figures and underlying data before composing results slides.
   - Embed the original chart unchanged in PowerPoint/Beamer, or regenerate it deterministically from the source data.
   - `--attach` guides the image model; it can redraw points, axes, labels, and logos. It does not paste the original pixels or guarantee quantitative fidelity.
   - Use attachments for style or conceptual layout drafts. For final results, add the original figure and verified text with a deterministic layout tool.

**Example with formatting consistency, citations, and figure attachments:**

```bash
# Title slide (first slide - establishes the style)
python scripts/generate_slide_image.py "Title slide for presentation: 'Machine Learning: From Theory to Practice'. Subtitle: '[Conference name and date]'. Speaker: '[Supplied presenter name]'. FORMATTING GOAL: Dark blue background (#1a237e), white text, gold accents (#ffc107), minimal design, sans-serif fonts, generous margins, no decorative elements." -o slides/01_title.png

# Content slide with citations (attach previous slide for consistency)
python scripts/generate_slide_image.py "Presentation slide titled 'Why Machine Learning Matters'. Three key points with simple icons: 1) Industry adoption, 2) Breakthrough applications, 3) Future potential. CITATIONS: Include at bottom in small text: (LeCun et al., 2015; Goodfellow et al., 2016). FORMATTING GOAL: Match attached slide style - dark blue background, white text, gold accents, minimal professional design, no visual clutter." -o slides/02_intro.png --attach slides/01_title.png

# Background slide with multiple citations
python scripts/generate_slide_image.py "Presentation slide titled 'Deep Learning Revolution'. Key milestones: ImageNet breakthrough (2012), transformer architecture (2017), GPT models (2018-present). CITATIONS: Show references at bottom: (Krizhevsky et al., 2012; Vaswani et al., 2017; Brown et al., 2020). FORMATTING GOAL: Match attached slide style exactly - same colors, fonts, minimal design." -o slides/03_background.png --attach slides/02_intro.png

# Results slides: insert figures/accuracy_chart.png as an original asset in
# PowerPoint or Beamer, then add verified findings and citations as text.
# The PowerPoint design guide below shows the explicit aspect-preserving geometry for this purpose.

# Conceptual methodology draft; provide the diagram file before running
python scripts/generate_slide_image.py "Presentation slide titled 'System Architecture'. Present the attached architecture diagram with brief explanatory bullet points: 1) Input processing, 2) Model inference, 3) Output generation. FORMATTING GOAL: Match attached slide style exactly." -o slides/04_architecture.png --attach slides/03_background.png --attach diagrams/system_architecture.png
```

**Before creating results slides:** find the original figure and source analysis, check labels,
units, sample sizes and uncertainty, then embed the figure without generative redrawing.
Numeric claims and placeholder references in these examples are illustrative, not evidence.

**Prompt Template:**

Include these elements in every prompt (customize as needed):
```
[Slide content description]
CITATIONS: Include at bottom: (Author1 et al., Year; Author2 et al., Year)
FORMATTING GOAL: [Background color], [text color], [accent color], minimal professional design, no decorative elements, consistent with attached slide style.
```

**Accessibility handoff:** Full-slide PNGs produce an image-only deck; their titles, equations, references, and data labels are not semantic text. Supply a transcript with slide numbers and descriptions of results figures. When the audience needs accessible slides, use the editable PowerPoint workflow with real title/text placeholders, reviewed alt text, and verified reading order; run PowerPoint's Accessibility Checker. Visual inspection alone cannot establish screen-reader usability. See [Microsoft's reading-order guidance](https://support.microsoft.com/en-us/powerpoint/make-slides-easier-to-read-by-using-the-reading-order-pane).

**Step 3: Combine to PDF**

```bash
# Combine all slides into a PDF presentation
python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
```

### PPT Workflow: PowerPoint with Generated Visuals

Create PowerPoint with native editable text, charts, and tables plus supplied figures. Optionally generate conceptual illustrations when that route is requested; the examples below illustrate that optional route.

**How it works:**
1. **Plan the deck**: Create content plan for each slide
2. **Generate visuals**: Use Nano Banana 2 with `--visual-only` flag to create images for slides
3. **Build PPTX**: Use PptxGenJS (or python-pptx for an existing template) to create slides with generated visuals and separate text

**Step 1: Generate Visuals for Each Slide**

```bash
# Generate a figure for the introduction slide
python scripts/generate_slide_image.py "Professional illustration showing machine learning applications: healthcare diagnosis, financial analysis, autonomous vehicles, and robotics. Modern flat design, colorful icons on white background." -o figures/ml_applications.png --visual-only

# Generate a diagram for the methods slide
python scripts/generate_slide_image.py "Neural network architecture diagram showing input layer, three hidden layers, and output layer. Clean, technical style with node connections. Blue and gray color scheme." -o figures/neural_network.png --visual-only

# Generate a conceptual graphic for results
python scripts/generate_slide_image.py "Before and after comparison showing improvement: left side shows cluttered data, right side shows organized insights. Arrow connecting them. Professional business style." -o figures/results_visual.png --visual-only
```

**Step 2: Build PowerPoint with PptxGenJS**

Use PptxGenJS to create slides that include:
- Generated images from step 1
- Title and body text added separately
- Professional layout and formatting

See `assets/powerpoint_design_guide.md` for the PptxGenJS and template workflows and the rendering check.

---

## Visual Enhancement with Scientific Schematics

In addition to slide generation, use the **scientific-schematics** skill for technical diagrams:

**When to use scientific-schematics instead:**
- Complex technical diagrams (circuit diagrams, chemical structures)
- Publication-quality figures for papers (higher quality threshold)
- Diagrams requiring scientific accuracy review

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png --doc-type presentation
```

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

---

## Core Capabilities

Presentation structure and organization, slide design principles, data visualization for
slides, talk-specific guidance, implementation options (Beamer / PowerPoint / generated
PDF), visual review and iteration, timing and pacing, and validation are all documented
in [references/slide_capabilities.md](references/slide_capabilities.md).

The staged development process — planning, design and creation, content development,
visual validation, practice and refinement, and final preparation — is in
[references/presentation_workflow.md](references/presentation_workflow.md).

Prompt-writing guidance for both full-slide and visual-only generation is in
[references/prompt_writing.md](references/prompt_writing.md). Every bundled script's
arguments and options are in
[references/script_reference.md](references/script_reference.md). The mistakes that most
often sink a talk are catalogued in
[references/common_pitfalls.md](references/common_pitfalls.md).

## Integration with Other Skills

**Research Lookup** (Critical for Scientific Presentations):
- **Background development**: Search literature to build introduction context
- **Citation gathering**: Find key papers to cite in your talk
- **Gap identification**: Identify what's unknown to motivate research
- **Prior work comparison**: Find papers to compare your results against
- **Supporting evidence**: Locate literature supporting your interpretations
- **Question preparation**: Find papers that might inform Q&A responses
- Verify the scientific context and citations using supplied sources and available research tools; research-lookup is optional.

**Scientific Writing**:
- Convert paper content to presentation format
- Extract key findings and simplify
- Use same figures (but redesigned for slides)
- Maintain consistent terminology

**MarkItDown**:
- Extract the text of an existing template or prior deck before reusing it (`markitdown template.pptx`)

**Data Visualization**:
- Create presentation-appropriate figures
- Simplify complex visualizations
- Ensure readability from distance
- Use progressive disclosure

## Reference Files

Comprehensive guides for specific aspects:

- **`references/presentation_structure.md`**: Detailed structure for all talk types, timing allocation, opening/closing strategies, transition techniques
- **`references/slide_design_principles.md`**: Typography, color theory, layout, accessibility, visual hierarchy, design workflow
- **`references/data_visualization_slides.md`**: Simplifying figures, chart types, progressive disclosure, common mistakes, recreation workflow
- **`references/talk_types_guide.md`**: Specific guidance for conferences, seminars, defenses, grants, journal clubs, with examples
- **`references/beamer_guide.md`**: Complete LaTeX Beamer documentation, themes, customization, advanced features, compilation
- **`references/visual_review_workflow.md`**: PDF to images conversion, systematic inspection, issue documentation, iterative improvement

- **`references/slide_capabilities.md`**: presentation structure, design principles, data visualization, talk types, implementation options, visual review, timing, validation
- **`references/presentation_workflow.md`**: the six development stages from planning to final preparation
- **`references/prompt_writing.md`**: full-slide and visual-only prompt patterns
- **`references/script_reference.md`**: arguments and options for every bundled script
- **`references/common_pitfalls.md`**: content, design, and timing mistakes to avoid

## Assets

### Templates

- **`assets/beamer_template_conference.tex`**: 15-minute conference talk template
- **`assets/beamer_template_seminar.tex`**: 45-minute academic seminar template
- **`assets/beamer_template_defense.tex`**: Dissertation defense template

### Guides

- **`assets/powerpoint_design_guide.md`**: Complete PowerPoint design and implementation guide
- **`assets/timing_guidelines.md`**: Comprehensive timing, pacing, and practice strategies

## Quick Start Guide

### For a 15-Minute Conference Talk

1. **Research & Plan** (45 minutes):
   - **Use research-lookup** to find 8-12 relevant papers for citations
   - Build reference list (background, comparison studies)
   - Outline content (intro → methods → 2-3 key results → conclusion)
   - **Create detailed plan for each slide** (title, key points, visual elements)
   - Target 15-18 slides

2. **Generate Conceptual Slides with Nano Banana 2** (1-2 hours):
   
   Use verified citations and supplied presenter details. The commands below are
   illustrative; use the native PowerPoint or Beamer workflow to add original
   quantitative figures and exact results text.
   
   ```bash
   # Title slide (establishes style - substitute the supplied presenter)
   python scripts/generate_slide_image.py "Title slide: 'Your Research Title'. Conference name, supplied presenter name. FORMATTING GOAL: [your color scheme], minimal professional design, no decorative elements, clean and corporate." -o slides/01_title.png
   
   # Introduction slide with citations (attach previous for consistency)
   python scripts/generate_slide_image.py "Slide titled 'Why This Matters'. Three key points with simple icons. CITATIONS: Include at bottom: (Smith et al., 2023; Jones et al., 2024). FORMATTING GOAL: Match attached slide style exactly." -o slides/02_intro.png --attach slides/01_title.png
   
   # Continue for each slide (always attach previous, include citations where relevant)
   python scripts/generate_slide_image.py "Slide titled 'Methods'. Key methodology points. CITATIONS: (Based on Chen et al., 2022). FORMATTING GOAL: Match attached slide style exactly." -o slides/03_methods.png --attach slides/02_intro.png
   
   # Combine to PDF
   python scripts/slides_to_pdf.py slides/*.png -o presentation.pdf
   ```

3. **Review & Iterate** (30 minutes):
   - Open the PDF and review each slide
   - Regenerate any slides that need improvement
   - Re-combine to PDF

4. **Practice** (2-3 hours):
   - Practice 3-5 times with timer
   - Aim for 13-14 minutes (leave buffer)
   - Record yourself, watch playback
   - **Prepare for questions** (use research-lookup to anticipate)

5. **Finalize** (30 minutes):
   - Generate backup/appendix slides if needed
   - Save multiple copies
   - Test on presentation computer

Total time: ~5-6 hours for quality AI-generated presentation

### Alternative: PowerPoint Workflow

If you need editable slides (e.g., for company templates):

1. **Plan slides** as above
2. **Use supplied figures or native charts**. If AI illustrations are explicitly requested, the optional visual-only command is:
   ```bash
   python scripts/generate_slide_image.py "diagram description" -o figures/fig1.png --visual-only
   ```
3. **Build PPTX** using host presentation tools or PptxGenJS with native objects and verified source figures
4. **Add text** separately as native, editable text boxes

See `assets/powerpoint_design_guide.md` for the complete PowerPoint workflow.

## Summary: Key Principles

1. **Evidence-first design**: Use a figure, chart, or diagram when it clarifies the research; a title or conclusion slide can use text alone.
2. **Research-backed**: Cite the sources supporting the actual claims; the required count depends on the talk.
3. **Modern Aesthetics**: Choose contemporary color palette matching topic, not default themes
4. **Minimal Text**: 3-4 bullets, 4-6 words each (24-28pt font), let visuals tell story
5. **Structure**: Follow story arc, spend 40-50% on results
6. **High Contrast**: 7:1 preferred for professional appearance
7. **Varied Layouts**: Mix full-figure, two-column, visual overlays (not all bullets)
8. **Timing**: Practice 3-5 times, ~1 slide per minute, never skip conclusions
9. **Validation**: Visual review workflow to catch overflow and overlap
10. **White Space**: 40-50% of slide empty for visual breathing room

**Remember**: 
- **Boring = Forgotten**: Dry, text-heavy slides fail to communicate your science
- **Visual + Research = Impact**: Combine compelling visuals with research-backed context
- **You are the presentation, slides are visual support**: They should enhance, not replace your talk

## Citing Scientific Agent Skills

This skill is part of Scientific Agent Skills by K-Dense. Preserve the bundled MIT
license and provenance when distributing this package. If the user requests software
attribution in a presentation or manuscript, verify the record below before including
it. Do not add a promotional citation to every deck automatically:

> Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent
> Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065.
> https://doi.org/10.48550/arXiv.2609.00065

Always cite the current version. The DOI and https://arxiv.org/abs/2609.00065 resolve to the
latest arXiv version, so never append a version suffix such as `v1`. When network access is
available, fetch https://arxiv.org/abs/2609.00065 (or
http://export.arxiv.org/api/query?id_list=2609.00065) before writing the reference and take
the author list, year, and version from that record. If the record lists a journal reference
or publisher DOI, cite the published version instead.
