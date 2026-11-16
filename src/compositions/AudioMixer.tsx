import React from "react";
import { Audio, staticFile } from "remotion";

interface AudioMixerProps {
  voiceoverSrc?: string;
  backgroundMusicSrc?: string;
  musicDucking?: number;
}

export const AudioMixer: React.FC<AudioMixerProps> = ({
  voiceoverSrc,
  backgroundMusicSrc,
  musicDucking = 0.18,
}) => {
  return (
    <>
      {/* Primary Voiceover Track */}
      {voiceoverSrc && (
        <Audio
          src={
            voiceoverSrc.startsWith("http")
              ? voiceoverSrc
              : staticFile(voiceoverSrc)
          }
          volume={1.0}
        />
      )}

      {/* Ambient Score Bed (Ducked during narration) */}
      {backgroundMusicSrc && (
        <Audio
          src={
            backgroundMusicSrc.startsWith("http")
              ? backgroundMusicSrc
              : staticFile(backgroundMusicSrc)
          }
          volume={musicDucking}
        />
      )}
    </>
  );
};
