import { HiggsfieldMotionType } from "../compositions/HiggsfieldCamera";
import { ThreeJsSceneType } from "../compositions/ThreeJsScene";

export type ColorGradePreset =
  | "teal-and-orange"
  | "moody-documentary"
  | "kodak-portra"
  | "noir-monochrome"
  | "clean";

export type SceneRenderEngine =
  | "remotion"
  | "threejs"
  | "manim"
  | "blender"
  | "gsap";

export interface SceneData {
  id: string;
  durationInFrames: number;
  engine?: SceneRenderEngine;
  voiceover?: string;
  visual?: string;
  subtitle?: string;
  motion?: "zoom-in" | "zoom-out" | "pan-left" | "pan-right" | "static";
  higgsfieldMotion?: HiggsfieldMotionType;
  threeJsScene?: ThreeJsSceneType;
  colorGrade?: ColorGradePreset;
  jCutFrames?: number; // Frames audio leads visual cut (OpenCut / Film technique)
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
