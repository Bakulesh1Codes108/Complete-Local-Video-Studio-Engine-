export interface SceneData {
  id: string;
  durationInFrames: number;
  voiceover?: string;
  visual?: string;
  subtitle?: string;
  motion?: "zoom-in" | "zoom-out" | "pan-left" | "pan-right" | "static";
  musicDucking?: number;
}

export interface TimelineData {
  project: string;
  fps: number;
  width: number;
  height: number;
  backgroundMusic?: string;
  scenes: SceneData[];
}
