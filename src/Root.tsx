import React from "react";
import { Composition } from "remotion";
import { DocumentaryComposition } from "./compositions/DocumentaryComposition";
import { VerticalComposition } from "./compositions/VerticalComposition";
import defaultTimeline from "../timeline.json";
import { TimelineData } from "./types/timeline";

export const RemotionRoot: React.FC = () => {
  const timeline = (defaultTimeline || {}) as TimelineData;
  const scenes = timeline.scenes || [];
  const totalFrames = scenes.reduce(
    (acc, s) => acc + (s.durationInFrames || 150),
    0
  );

  const duration = Math.max(30, totalFrames || 300);
  const fps = timeline.fps || 30;

  return (
    <>
      {/* 16:9 Cinematic Widescreen Composition */}
      <Composition
        id="Documentary"
        component={DocumentaryComposition}
        durationInFrames={duration}
        fps={fps}
        width={timeline.width || 1920}
        height={timeline.height || 1080}
        defaultProps={{
          timeline,
        }}
      />

      {/* 9:16 Vertical V3 Viral Reel / TikTok / Shorts Composition */}
      <Composition
        id="VerticalV3"
        component={VerticalComposition}
        durationInFrames={duration}
        fps={fps}
        width={1080}
        height={1920}
        defaultProps={{
          timeline,
        }}
      />
    </>
  );
};
