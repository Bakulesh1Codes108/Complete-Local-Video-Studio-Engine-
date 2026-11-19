import React from "react";
import { Sequence, AbsoluteFill, staticFile, Img } from "remotion";
import { TimelineData, SceneData } from "../types/timeline";
import { KenBurns } from "./KenBurns";
import { VerticalV3Subtitle } from "./VerticalV3Subtitle";
import { VerticalV3ProgressBar } from "./VerticalV3ProgressBar";
import { AudioMixer } from "./AudioMixer";
import { CinematicGrade } from "./CinematicGrade";
import { HiggsfieldCamera } from "./HiggsfieldCamera";
import { ThreeJsScene } from "./ThreeJsScene";

interface VerticalCompositionProps {
  timeline: TimelineData;
}

export const VerticalComposition: React.FC<VerticalCompositionProps> = ({
  timeline,
}) => {
  const scenes = timeline?.scenes || [];

  if (scenes.length === 0) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: "#080c14",
          color: "#ffffff",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontFamily: "system-ui, sans-serif",
          textAlign: "center",
          padding: "40px",
        }}
      >
        <div>
          <h2 style={{ fontSize: "48px", marginBottom: "16px" }}>
            📱 Antigravity Vertical V3
          </h2>
          <p style={{ opacity: 0.6, fontSize: "24px" }}>
            Awaiting 9:16 scenes in timeline.json...
          </p>
        </div>
      </AbsoluteFill>
    );
  }

  let accumulatedFrames = 0;

  return (
    <CinematicGrade
      preset={timeline.defaultColorGrade || "teal-and-orange"}
      letterbox={false} // Never letterbox vertical reels
      filmGrainOpacity={0.05}
    >
      <AbsoluteFill style={{ backgroundColor: "#000000" }}>
        {/* 1. Global Retention Hook Progress Bar across the 9:16 Canvas */}
        <VerticalV3ProgressBar color="#FFEE00" height={10} />

        {/* 2. Scene Sequences */}
        {scenes.map((scene: SceneData, index: number) => {
          const fromFrame = accumulatedFrames;
          const duration = Math.max(1, scene.durationInFrames || 90);
          accumulatedFrames += duration;

          // OpenCut J-Cut: Audio leads visual transition by up to 10 frames
          const jCutOffset =
            scene.jCutFrames && index > 0 ? Math.min(scene.jCutFrames, 10) : 0;
          const audioFromFrame = Math.max(0, fromFrame - jCutOffset);

          const isThreeJs =
            scene.engine === "threejs" || Boolean(scene.threeJsScene);
          const imageSrc = scene.visual
            ? scene.visual.startsWith("http")
              ? scene.visual
              : staticFile(scene.visual)
            : null;

          return (
            <React.Fragment key={scene.id || index}>
              {/* Visual Sequence wrapped in Open Higgsfield Camera Rig */}
              <Sequence from={fromFrame} durationInFrames={duration}>
                {/* Smart Blur-Pad Background for Landscape Assets */}
                {imageSrc && !isThreeJs && (
                  <AbsoluteFill style={{ overflow: "hidden", zIndex: 1 }}>
                    <Img
                      src={imageSrc}
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        filter: "blur(32px) brightness(0.55) saturate(1.4)",
                        transform: "scale(1.2)",
                      }}
                    />
                  </AbsoluteFill>
                )}

                {/* Foreground Primary Visual with Higgsfield 3D Rig */}
                <div style={{ position: "relative", width: "100%", height: "100%", zIndex: 2 }}>
                  <HiggsfieldCamera
                    durationInFrames={duration}
                    motion={scene.higgsfieldMotion || "whip_pan"}
                    intensity={1.1}
                  >
                    {isThreeJs ? (
                      <ThreeJsScene
                        sceneType={scene.threeJsScene || "3d_rotating_globe"}
                        title={scene.subtitle || "3D Visual"}
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
                </div>

                {/* Vertical V3 Kinetic Word-by-Word Subtitle (Platform Safe Zone) */}
                <VerticalV3Subtitle
                  text={scene.subtitle}
                  durationInFrames={duration}
                  highlightColor="#FFEE00"
                />
              </Sequence>

              {/* Audio Sequence with J-Cut Lead */}
              <Sequence
                from={audioFromFrame}
                durationInFrames={duration + jCutOffset}
              >
                <AudioMixer
                  voiceoverSrc={scene.voiceover}
                  backgroundMusicSrc={timeline.backgroundMusic}
                  musicDucking={scene.musicDucking ?? 0.22}
                />
              </Sequence>
            </React.Fragment>
          );
        })}
      </AbsoluteFill>
    </CinematicGrade>
  );
};
