"""Main EXPLORE 2.0 application window.

Wizard-style workflow:

  Tab 1 — Project setup (name, path, videos, duration)
  Tab 2 — Object descriptions → scene parse → Grounding DINO detect → preview
  Tab 3 — Behavioral definition (CLIP text prompts)
  Tab 4 — Run + live log
"""

from __future__ import annotations

import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import numpy as np

from explore.config import (
    AnalysisConfig,
    BehaviorConfig,
    ExperimentConfig,
    ModelConfig,
    ObjectConfig,
    parse_scene_description,
    parse_scene_description_llm,
)

logger = logging.getLogger(__name__)

_DEFAULT_POS_PROMPTS = (
    "a mouse actively sniffing and investigating an object\n"
    "a rodent with nose close to an object, exploring it"
)
_DEFAULT_NEG_PROMPTS = (
    "a mouse walking past or ignoring objects\n"
    "a rodent resting or grooming away from objects"
)
_SCENE_PLACEHOLDER = (
    "Describe all objects in the arena — include role labels (familiar / novel) and "
    "positional cues when objects look similar.\n\n"
    "Examples:\n"
    "  familiar wooden cube top-right, novel plastic bottle bottom-left\n"
    "  1) a familiar wooden cube in the top-right corner  "
    "2) a novel plastic bottle in the bottom-left corner\n"
    "  familiar wooden cube top-right, familiar wooden cube bottom-left, "
    "novel green plastic object centre"
)


class ExploreApp:
    """Main EXPLORE 2.0 application."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("EXPLORE 2.0")
        root.minsize(700, 520)
        root.resizable(True, True)

        # Holds the most recent annotated detection frame (BGR ndarray or None)
        self._detection_preview: np.ndarray | None = None

        # Cached pipeline — models (CLIP + DINO) are expensive to load; reuse
        # across detect/run calls by updating .config instead of re-instantiating.
        self._pipeline: object | None = None  # ExplorationPipeline | None

        self._build_ui()

    # ------------------------------------------------------------------
    # Top-level UI
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        self._notebook = ttk.Notebook(self.root)
        self._notebook.pack(fill="both", expand=True, padx=10, pady=10)

        proj_tab = ttk.Frame(self._notebook, padding=12)
        self._notebook.add(proj_tab, text="1 · Project")
        self._build_project_tab(proj_tab)

        obj_tab = ttk.Frame(self._notebook, padding=12)
        self._notebook.add(obj_tab, text="2 · Objects")
        self._build_objects_tab(obj_tab)

        beh_tab = ttk.Frame(self._notebook, padding=12)
        self._notebook.add(beh_tab, text="3 · Behavior")
        self._build_behavior_tab(beh_tab)

        run_tab = ttk.Frame(self._notebook, padding=12)
        self._notebook.add(run_tab, text="4 · Run")
        self._build_run_tab(run_tab)

    # ------------------------------------------------------------------
    # Tab 1 — Project
    # ------------------------------------------------------------------

    def _build_project_tab(self, tab: ttk.Frame) -> None:
        tab.columnconfigure(1, weight=1)

        ttk.Label(tab, text="Project name:").grid(row=0, column=0, sticky="e", pady=4)
        self._proj_name = tk.StringVar()
        ttk.Entry(tab, textvariable=self._proj_name, width=30).grid(
            row=0, column=1, sticky="w", padx=8
        )

        ttk.Label(tab, text="Project folder:").grid(row=1, column=0, sticky="e", pady=4)
        self._proj_path = tk.StringVar()
        ttk.Entry(tab, textvariable=self._proj_path, width=44, state="readonly").grid(
            row=1, column=1, sticky="w", padx=8
        )
        ttk.Button(tab, text="Browse…", command=self._browse_project_path).grid(
            row=1, column=2, padx=4
        )

        ttk.Label(tab, text="Video files:").grid(row=2, column=0, sticky="ne", pady=4)
        frame = ttk.Frame(tab)
        frame.grid(row=2, column=1, sticky="w", padx=8)
        self._video_listbox = tk.Listbox(
            frame, height=5, width=50, selectmode="extended"
        )
        self._video_listbox.pack(side="left")
        sb = ttk.Scrollbar(frame, orient="vertical", command=self._video_listbox.yview)
        sb.pack(side="left", fill="y")
        self._video_listbox.configure(yscrollcommand=sb.set)
        btn_frame = ttk.Frame(tab)
        btn_frame.grid(row=2, column=2, sticky="n", padx=4)
        ttk.Button(btn_frame, text="Add…", command=self._add_videos).pack(pady=2)
        ttk.Button(btn_frame, text="Remove", command=self._remove_video).pack(pady=2)

        ttk.Label(tab, text="Video duration (min):").grid(
            row=3, column=0, sticky="e", pady=4
        )
        self._duration = tk.IntVar(value=5)
        ttk.Spinbox(tab, from_=1, to=120, textvariable=self._duration, width=6).grid(
            row=3, column=1, sticky="w", padx=8
        )

    def _browse_project_path(self) -> None:
        path = filedialog.askdirectory(title="Select project folder")
        if path:
            self._proj_path.set(path)

    def _add_videos(self) -> None:
        paths = filedialog.askopenfilenames(
            title="Select video files",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.MP4 *.AVI *.MOV"),
                ("All", "*.*"),
            ],
        )
        for p in paths:
            self._video_listbox.insert("end", p)

    def _remove_video(self) -> None:
        for idx in reversed(self._video_listbox.curselection()):
            self._video_listbox.delete(idx)

    # ------------------------------------------------------------------
    # Tab 2 — Objects
    # ------------------------------------------------------------------

    def _build_objects_tab(self, tab: ttk.Frame) -> None:
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

        # ---- Scene description input ----
        ttk.Label(
            tab,
            text=(
                "Describe the scene — include role labels (familiar / novel) and "
                "position for disambiguation."
            ),
            wraplength=600,
            justify="left",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

        self._scene_text = tk.Text(tab, height=4, wrap="word", fg="grey")
        self._scene_text.grid(row=1, column=0, sticky="ew", padx=(0, 6))
        self._scene_text.insert("1.0", _SCENE_PLACEHOLDER)
        self._scene_text.bind("<FocusIn>", self._scene_focus_in)
        self._scene_text.bind("<FocusOut>", self._scene_focus_out)
        self._scene_placeholder_active = True

        btn_col = ttk.Frame(tab)
        btn_col.grid(row=1, column=1, sticky="n")
        self._parse_btn = ttk.Button(
            btn_col, text="Parse scene →", command=self._parse_scene
        )
        self._parse_btn.pack(fill="x", pady=(0, 4))
        self._detect_btn = ttk.Button(
            btn_col, text="Detect objects ▸", command=self._detect_objects
        )
        self._detect_btn.pack(fill="x")
        self._detect_status_var = tk.StringVar(value="")
        ttk.Label(
            btn_col,
            textvariable=self._detect_status_var,
            wraplength=140,
            justify="left",
            foreground="gray",
        ).pack(fill="x", pady=(4, 0))

        # ---- Per-object rows (header) ----
        hdr = ttk.Frame(tab)
        hdr.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Label(hdr, text="Description  (for Grounding DINO)", width=42).pack(
            side="left", padx=4
        )
        ttk.Label(hdr, text="Name / role", width=16).pack(side="left", padx=4)

        # ---- Scrollable object rows ----
        canvas = tk.Canvas(tab, height=130)
        canvas.grid(row=3, column=0, columnspan=2, sticky="nsew")
        vsb = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        vsb.grid(row=3, column=2, sticky="ns")
        canvas.configure(yscrollcommand=vsb.set)

        self._obj_frame = ttk.Frame(canvas)
        self._obj_win = canvas.create_window(
            (0, 0), window=self._obj_frame, anchor="nw"
        )
        self._obj_frame.bind(
            "<Configure>",
            lambda _: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self._obj_win, width=e.width),
        )

        self._obj_rows: list[tuple[tk.StringVar, tk.StringVar]] = []
        self._add_object_row("small blue plastic bottle", "familiar")
        self._add_object_row("brown wooden cube", "novel")

        add_row = ttk.Frame(tab)
        add_row.grid(row=4, column=0, columnspan=2, sticky="w", pady=(4, 0))
        ttk.Button(
            add_row, text="+ Add object", command=lambda: self._add_object_row()
        ).pack(side="left")
        ttk.Button(add_row, text="Clear all", command=self._clear_object_rows).pack(
            side="left", padx=8
        )

        # ---- Detection preview thumbnail ----
        self._preview_label = ttk.Label(
            tab, text="Detection preview will appear here after detection."
        )
        self._preview_label.grid(row=5, column=0, columnspan=2, pady=(8, 0), sticky="w")

    def _scene_focus_in(self, _: tk.Event) -> None:  # type: ignore[type-arg]
        if self._scene_placeholder_active:
            self._scene_text.delete("1.0", "end")
            self._scene_text.configure(fg="black")
            self._scene_placeholder_active = False

    def _scene_focus_out(self, _: tk.Event) -> None:  # type: ignore[type-arg]
        if not self._scene_text.get("1.0", "end").strip():
            self._scene_text.insert("1.0", _SCENE_PLACEHOLDER)
            self._scene_text.configure(fg="grey")
            self._scene_placeholder_active = True

    def _get_scene_text(self) -> str:
        if self._scene_placeholder_active:
            return ""
        return self._scene_text.get("1.0", "end").strip()

    def _parse_scene(self) -> None:
        text = self._get_scene_text()
        if not text:
            messagebox.showinfo("Scene description", "Enter a scene description first.")
            return
        self._parse_btn.configure(state="disabled", text="Parsing…")
        self._detect_status_var.set("Loading parser model…\n(1 min on first use)")
        threading.Thread(target=self._parse_thread, args=(text,), daemon=True).start()

    def _parse_thread(self, text: str) -> None:
        try:
            objs = parse_scene_description_llm(text)
            logger.info("Scene parsed by local LLM.")
        except Exception as exc:
            logger.info("LLM parse failed (%s); falling back to regex.", exc)
            objs = parse_scene_description(text)

        if not objs:
            self.root.after(
                0,
                lambda: messagebox.showwarning(
                    "Parse error", "Could not extract any objects from the description."
                ),
            )
        else:
            self.root.after(0, lambda: self._apply_parse_results(objs))

        self.root.after(0, self._parse_done)

    def _parse_done(self) -> None:
        self._parse_btn.configure(state="normal", text="Parse scene →")
        self._detect_status_var.set("")

    def _apply_parse_results(self, objs: list) -> None:
        self._clear_object_rows()
        for o in objs:
            self._add_object_row(o.description, o.name)

    def _add_object_row(self, desc: str = "", name: str = "") -> None:
        row_idx = len(self._obj_rows)
        desc_var = tk.StringVar(value=desc)
        name_var = tk.StringVar(value=name)
        self._obj_rows.append((desc_var, name_var))

        row_frame = ttk.Frame(self._obj_frame)
        row_frame.pack(fill="x", pady=1)
        ttk.Label(row_frame, text=f"{row_idx + 1}.").pack(side="left", padx=(0, 4))
        ttk.Entry(row_frame, textvariable=desc_var, width=44).pack(side="left", padx=2)
        ttk.Entry(row_frame, textvariable=name_var, width=16).pack(side="left", padx=2)

    def _clear_object_rows(self) -> None:
        for widget in self._obj_frame.winfo_children():
            widget.destroy()
        self._obj_rows.clear()

    def _detect_objects(self) -> None:
        """Run Grounding DINO on the first video's reference frame."""
        videos = list(self._video_listbox.get(0, "end"))
        if not videos:
            messagebox.showwarning("No video", "Add at least one video first.")
            return
        try:
            cfg = self._build_config()
        except ValueError as exc:
            messagebox.showerror("Configuration error", str(exc))
            return

        self._detect_btn.configure(state="disabled", text="Detecting…")
        threading.Thread(target=self._detect_thread, args=(cfg,), daemon=True).start()

    def _detect_thread(self, cfg: ExperimentConfig) -> None:
        from explore.pipeline.prediction import ExplorationPipeline

        def status(msg: str) -> None:
            self.root.after(0, lambda: self._detect_status_var.set(msg))

        try:
            if self._pipeline is None:
                status("Loading models…\n(1–2 min on first run)")
                self._pipeline = ExplorationPipeline(cfg, headless=True)
            else:
                self._pipeline.config = cfg  # type: ignore[union-attr]

            status("Running Grounding DINO…")
            _, annotated = self._pipeline.detect_objects()  # type: ignore[union-attr]
            self.root.after(
                0, lambda: self._apply_detection_results(cfg.objects, annotated)
            )
        except Exception as exc:
            err = str(
                exc
            )  # capture now — Python 3 deletes `exc` after the except block
            logger.exception("Detection error")
            self.root.after(0, lambda: messagebox.showerror("Detection error", err))
        finally:
            self.root.after(0, self._detect_done)

    def _detect_done(self) -> None:
        """Reset detect button and status label after thread finishes."""
        self._detect_btn.configure(state="normal", text="Detect objects ▸")
        self._detect_status_var.set("")

    def _apply_detection_results(
        self,
        objects: list[ObjectConfig],
        annotated: np.ndarray | None,
    ) -> None:
        # Refresh name fields with auto-assigned names from detection
        for row_idx, obj in enumerate(objects):
            if row_idx < len(self._obj_rows):
                self._obj_rows[row_idx][1].set(obj.name)

        self._detection_preview = annotated
        if annotated is not None:
            self._show_preview_thumbnail(annotated)

    def _show_preview_thumbnail(self, bgr_frame: np.ndarray) -> None:
        try:
            import cv2
            from PIL import Image, ImageTk

            rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb)
            pil_img.thumbnail((560, 220), Image.LANCZOS)
            photo = ImageTk.PhotoImage(pil_img)

            self._preview_label.configure(image=photo, text="")
            self._preview_label.image = photo  # type: ignore[attr-defined]  # keep reference
        except Exception as exc:
            self._preview_label.configure(text=f"Preview unavailable: {exc}", image="")

    # ------------------------------------------------------------------
    # Tab 3 — Behavior
    # ------------------------------------------------------------------

    def _build_behavior_tab(self, tab: ttk.Frame) -> None:
        ttk.Label(
            tab,
            text=(
                "Describe what counts as 'exploration' in your experiment.\n"
                "These prompts become the behavioural definition in your Methods section."
            ),
            justify="left",
        ).pack(anchor="w", pady=(0, 8))

        ttk.Label(tab, text="Exploration prompts (one per line):").pack(anchor="w")
        self._pos_text = tk.Text(tab, height=5, wrap="word")
        self._pos_text.pack(fill="x", pady=(2, 8))
        self._pos_text.insert("1.0", _DEFAULT_POS_PROMPTS)

        ttk.Label(tab, text="Non-exploration prompts (one per line):").pack(anchor="w")
        self._neg_text = tk.Text(tab, height=4, wrap="word")
        self._neg_text.pack(fill="x", pady=(2, 8))
        self._neg_text.insert("1.0", _DEFAULT_NEG_PROMPTS)

        thr_frame = ttk.Frame(tab)
        thr_frame.pack(fill="x")
        ttk.Label(thr_frame, text="Confidence threshold:").pack(side="left")
        self._threshold = tk.DoubleVar(value=0.5)
        self._thr_label = ttk.Label(thr_frame, text="0.50")
        ttk.Scale(
            thr_frame,
            from_=0.1,
            to=0.9,
            variable=self._threshold,
            orient="horizontal",
            length=180,
            command=lambda v: self._thr_label.configure(text=f"{float(v):.2f}"),
        ).pack(side="left", padx=6)
        self._thr_label.pack(side="left")

    # ------------------------------------------------------------------
    # Tab 4 — Run
    # ------------------------------------------------------------------

    def _build_run_tab(self, tab: ttk.Frame) -> None:
        ttk.Button(tab, text="▶  Run Analysis", command=self._run).pack(pady=10)

        self._status_var = tk.StringVar(value="Ready.")
        ttk.Label(tab, textvariable=self._status_var, font=("", 10, "bold")).pack()

        self._log_text = tk.Text(tab, height=20, state="disabled", wrap="word")
        self._log_text.pack(fill="both", expand=True, pady=6)

    # ------------------------------------------------------------------
    # Config assembly
    # ------------------------------------------------------------------

    def _build_config(self) -> ExperimentConfig:
        name = self._proj_name.get().strip()
        path = self._proj_path.get().strip()
        videos = list(self._video_listbox.get(0, "end"))

        if not name:
            raise ValueError("Project name is required.")
        if not path:
            raise ValueError("Project folder is required.")
        if not videos:
            raise ValueError("At least one video must be selected.")

        objects: list[ObjectConfig] = []
        for desc_var, name_var in self._obj_rows:
            desc = desc_var.get().strip()
            obj_name = name_var.get().strip()
            if desc:
                objects.append(ObjectConfig(description=desc, name=obj_name))
        if not objects:
            raise ValueError("At least one object must be defined.")

        pos = [
            line.strip()
            for line in self._pos_text.get("1.0", "end").splitlines()
            if line.strip()
        ]
        neg = [
            line.strip()
            for line in self._neg_text.get("1.0", "end").splitlines()
            if line.strip()
        ]
        if not pos or not neg:
            raise ValueError(
                "Both exploration and non-exploration prompts are required."
            )

        # Auto-infer familiar/novel for DI/RI
        import re

        novel_names = [o.name for o in objects if re.match(r"^novel(_\d+)?$", o.name)]
        familiar_names = [
            o.name for o in objects if re.match(r"^familiar(_\d+)?$", o.name)
        ]
        familiar_obj = familiar_names[0] if len(familiar_names) == 1 else None
        novel_obj = novel_names[0] if len(novel_names) == 1 else None

        return ExperimentConfig(
            project_name=name,
            project_path=Path(path),
            video_paths=[Path(v) for v in videos],
            video_duration_minutes=self._duration.get(),
            objects=objects,
            behavior=BehaviorConfig(
                exploration_prompts=pos,
                no_exploration_prompts=neg,
                confidence_threshold=self._threshold.get(),
            ),
            model=ModelConfig(),
            analysis=AnalysisConfig(
                familiar_object=familiar_obj,
                novel_object=novel_obj,
                compute_di=bool(familiar_obj and novel_obj),
                compute_ri=bool(familiar_obj and novel_obj),
            ),
        )

    # ------------------------------------------------------------------
    # Run pipeline
    # ------------------------------------------------------------------

    def _run(self) -> None:
        try:
            cfg = self._build_config()
        except ValueError as exc:
            messagebox.showerror("Configuration error", str(exc))
            return

        self._log("Starting analysis …")
        threading.Thread(target=self._run_pipeline, args=(cfg,), daemon=True).start()

    def _run_pipeline(self, cfg: ExperimentConfig) -> None:
        from explore.pipeline.prediction import ExplorationPipeline

        try:
            if self._pipeline is None:
                self.root.after(
                    0, lambda: self._log("Loading models… (1–2 min on first run)")
                )
                self._pipeline = ExplorationPipeline(cfg, headless=False)
            else:
                self._pipeline.config = cfg  # type: ignore[union-attr]
                self._pipeline.headless = False  # type: ignore[union-attr]
            pipeline = self._pipeline

            missing = [
                o.name or o.description for o in cfg.objects if o.bounding_box is None
            ]
            if missing:
                raise ValueError(
                    "Object bounding boxes not set for: "
                    + ", ".join(f"'{m}'" for m in missing)
                    + ".\nRun 'Detect objects ▸' on the Objects tab first."
                )

            self.root.after(0, lambda: self._log("Running CLIP classification …"))
            results_df = pipeline.run()
            msg = f"Done!  {len(results_df)} rows written to results CSV."
            self.root.after(0, lambda m=msg: self._log(m))
        except Exception as exc:
            err = str(exc)
            self.root.after(0, lambda e=err: self._log(f"ERROR: {e}"))
            logger.exception("Pipeline error")

    def _log(self, msg: str) -> None:
        self._status_var.set(msg)
        self._log_text.configure(state="normal")
        self._log_text.insert("end", msg + "\n")
        self._log_text.see("end")
        self._log_text.configure(state="disabled")


def launch() -> None:
    """Entry point for the GUI application."""
    root = tk.Tk()
    ExploreApp(root)
    root.mainloop()
