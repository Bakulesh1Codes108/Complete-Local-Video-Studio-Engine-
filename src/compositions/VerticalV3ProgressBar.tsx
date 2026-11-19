import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

interface VerticalV3ProgressBarProps {
  color?: string;
  height?: number;
}

export const VerticalV3ProgressBar: React.FC<VerticalV3ProgressBarProps> = ({
  color = "#FFD700", // Vibrant Gold / Hormozi Yellow
  height = 8,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames], [0, 100], {
    extrapolateRight: "clamp",
    extrapolateLeft: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        height,
        backgroundColor: "rgba(0, 0, 0, 0.4)",
        zIndex: 100,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          width: `${progress}%`,
          height: "100%",
          background: `linear-gradient(90deg, ${color}, #FF4500)`,
          boxShadow: `0 0 12px ${color}`,
          borderRadius: "0 4px 4px 0",
          transition: "width 0.05s linear",
        }}
      />
    </div>
  );
};
