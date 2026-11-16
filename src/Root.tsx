import React from "react";
import { Composition } from "remotion";
import { DocumentaryComposition } from "./compositions/DocumentaryComposition";
import defaultTimeline from "../timeline.json";
import { TimelineData } from "./types/timeline";

export const RemotionRoot: React.FC = () => {
  const timeline = defaultTimeline as TimelineData;
  const totalFrames = timeline.scenes.reduce(
    (acc, s) => acc + (s.durationInFrames || 150),
    0
  );

  return (
    <>
      <Composition
        id="Documentary"
        component={DocumentaryComposition}
        durationInFrames={totalFrames || 300}
        fps={timeline.fps || 30}
        width={timeline.width || 1920}
        height={timeline.height || 1080}
        defaultProps={{
          timeline,
        }}
      />
    </>
  );
};
