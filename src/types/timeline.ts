export type ColorGradePreset =
  | "teal-and-orange"
  | "moody-documentary"
  | "kodak-portra"
  | "noir-monochrome"
  | "clean";

export interface SceneData {
  id: string;
  durationInFrames: number;
  voiceover?: string;
  visual?: string;
  subtitle?: string;
  motion?: "zoom-in" | "zoom-out" | "pan-left" | "pan-right" | "static";
  colorGrade?: ColorGradePreset;
  jCutFrames?: number; // Frames audio leads the visual cut (OpenCut / Film technique)
  musicDucking?: number;
}

export interface TimelineData {
  project: string;
  fps: number;
  width: number;
  height: number;
  letterbox?: boolean; // 2.39:1 Anamorphic cinema bars
  defaultColorGrade?: ColorGradePreset;
  backgroundMusic?: string;
  scenes: SceneData[];
}
