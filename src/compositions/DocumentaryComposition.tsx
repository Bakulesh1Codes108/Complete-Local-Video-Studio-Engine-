import React from "react";
import { Sequence, AbsoluteFill } from "remotion";
import { TimelineData, SceneData } from "../types/timeline";
import { KenBurns } from "./KenBurns";
import { KineticSubtitle } from "./KineticSubtitle";
import { AudioMixer } from "./AudioMixer";
import { CinematicGrade } from "./CinematicGrade";
import { HiggsfieldCamera } from "./HiggsfieldCamera";
import { ThreeJsScene } from "./ThreeJsScene";

interface DocumentaryCompositionProps {
  timeline: TimelineData;
}

export const DocumentaryComposition: React.FC<DocumentaryCompositionProps> = ({
  timeline,
}) => {
  const scenes = timeline?.scenes || [];

  if (scenes.length === 0) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: "#0a0f1d",
          color: "#ffffff",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        <div style={{ textAlign: "center" }}>
          <h2>🎬 Antigravity Video Studio</h2>
          <p style={{ opacity: 0.6 }}>Awaiting scenes in timeline.json...</p>
        </div>
      </AbsoluteFill>
    );
  }

  let accumulatedFrames = 0;

  return (
    <CinematicGrade
      preset={timeline.defaultColorGrade || "moody-documentary"}
      letterbox={timeline.letterbox ?? true}
      filmGrainOpacity={0.07}
    >
      <AbsoluteFill style={{ backgroundColor: "#000000" }}>
        {scenes.map((scene: SceneData, index: number) => {
          const fromFrame = accumulatedFrames;
          const duration = Math.max(1, scene.durationInFrames || 150);
          accumulatedFrames += duration;

          // OpenCut / DaVinci J-Cut: Audio leads visual cut by up to 15 frames
          const jCutOffset = scene.jCutFrames && index > 0 ? Math.min(scene.jCutFrames, 15) : 0;
          const audioFromFrame = Math.max(0, fromFrame - jCutOffset);

          // Decide visual element based on selected engine
          const isThreeJs = scene.engine === "threejs" || Boolean(scene.threeJsScene);

          return (
            <React.Fragment key={scene.id || index}>
              {/* Visual Sequence wrapped in Open Higgsfield Camera Rig */}
              <Sequence
                from={fromFrame}
                durationInFrames={duration}
              >
                <HiggsfieldCamera
                  durationInFrames={duration}
                  motion={scene.higgsfieldMotion || "orbit_360"}
                  intensity={1.0}
                >
                  {isThreeJs ? (
                    <ThreeJsScene
                      sceneType={scene.threeJsScene || "3d_quantum_particles"}
                      title={scene.subtitle || "3D Procedural Scene"}
                      durationInFrames={duration}
                    />
                  ) : (
                    <KenBurns
                      src={scene.visual}
                      durationInFrames={duration}
                      motion={scene.motion || "zoom-in"}
                    />
                  )}
                </HiggsfieldCamera>

                {/* Synchronized Kinetic Subtitle */}
                <KineticSubtitle text={scene.subtitle} />
              </Sequence>

              {/* Audio Track with J-Cut Audio Lead */}
              <Sequence
                from={audioFromFrame}
                durationInFrames={duration + jCutOffset}
              >
                <AudioMixer
                  voiceoverSrc={scene.voiceover}
                  backgroundMusicSrc={timeline.backgroundMusic}
                  musicDucking={scene.musicDucking ?? 0.18}
                />
              </Sequence>
            </React.Fragment>
          );
        })}
      </AbsoluteFill>
    </CinematicGrade>
  );
};
