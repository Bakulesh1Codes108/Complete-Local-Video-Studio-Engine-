import React from "react";
import { Sequence, AbsoluteFill } from "remotion";
import { TimelineData, SceneData } from "../types/timeline";
import { KenBurns } from "./KenBurns";
import { KineticSubtitle } from "./KineticSubtitle";
import { AudioMixer } from "./AudioMixer";

interface DocumentaryCompositionProps {
  timeline: TimelineData;
}

export const DocumentaryComposition: React.FC<DocumentaryCompositionProps> = ({
  timeline,
}) => {
  let accumulatedFrames = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {timeline.scenes.map((scene: SceneData, index: number) => {
        const fromFrame = accumulatedFrames;
        accumulatedFrames += scene.durationInFrames;

        return (
          <Sequence
            key={scene.id || index}
            from={fromFrame}
            durationInFrames={scene.durationInFrames}
          >
            {/* 1. Visual Keyframe with Cinematic Ken Burns Camera Motion */}
            <KenBurns
              src={scene.visual}
              durationInFrames={scene.durationInFrames}
              motion={scene.motion || "zoom-in"}
            />

            {/* 2. Synchronized Animated Subtitles */}
            <KineticSubtitle text={scene.subtitle} />

            {/* 3. Audio & Voiceover Layer */}
            <AudioMixer
              voiceoverSrc={scene.voiceover}
              backgroundMusicSrc={timeline.backgroundMusic}
              musicDucking={scene.musicDucking ?? 0.18}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
