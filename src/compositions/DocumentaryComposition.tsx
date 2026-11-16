import React from "react";
import { Sequence, AbsoluteFill } from "remotion";
import { TimelineData, SceneData } from "../types/timeline";
import { KenBurns } from "./KenBurns";
import { KineticSubtitle } from "./KineticSubtitle";
import { AudioMixer } from "./AudioMixer";
import { CinematicGrade } from "./CinematicGrade";

interface DocumentaryCompositionProps {
  timeline: TimelineData;
}

export const DocumentaryComposition: React.FC<DocumentaryCompositionProps> = ({
  timeline,
}) => {
  let accumulatedFrames = 0;

  return (
    <CinematicGrade
      preset={timeline.defaultColorGrade || "moody-documentary"}
      letterbox={timeline.letterbox ?? true}
      filmGrainOpacity={0.07}
    >
      <AbsoluteFill style={{ backgroundColor: "#000000" }}>
        {timeline.scenes.map((scene: SceneData, index: number) => {
          const fromFrame = accumulatedFrames;
          accumulatedFrames += scene.durationInFrames;

          // OpenCut / DaVinci J-Cut: Audio can start slightly before visual cut (e.g. 10-15 frames)
          const jCutOffset = scene.jCutFrames && index > 0 ? Math.min(scene.jCutFrames, 15) : 0;
          const audioFromFrame = Math.max(0, fromFrame - jCutOffset);

          return (
            <React.Fragment key={scene.id || index}>
              {/* Visual Sequence with Ken Burns Motion */}
              <Sequence
                from={fromFrame}
                durationInFrames={scene.durationInFrames}
              >
                <KenBurns
                  src={scene.visual}
                  durationInFrames={scene.durationInFrames}
                  motion={scene.motion || "zoom-in"}
                />

                {/* Synchronized Kinetic Subtitle */}
                <KineticSubtitle text={scene.subtitle} />
              </Sequence>

              {/* Audio Track with Optional J-Cut Audio Lead */}
              <Sequence
                from={audioFromFrame}
                durationInFrames={scene.durationInFrames + jCutOffset}
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
