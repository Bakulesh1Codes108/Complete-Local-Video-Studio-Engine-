import React from "react";
import { Img, interpolate, useCurrentFrame, staticFile } from "remotion";

interface KenBurnsProps {
  src?: string;
  durationInFrames: number;
  motion?: "zoom-in" | "zoom-out" | "pan-left" | "pan-right" | "static";
}

export const KenBurns: React.FC<KenBurnsProps> = ({
  src,
  durationInFrames,
  motion = "zoom-in",
}) => {
  const frame = useCurrentFrame();

  if (!src) {
    return (
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "#0d1117",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          color: "#484f58",
          fontSize: 28,
          fontFamily: "Inter, sans-serif",
        }}
      >
        [Awaiting Visual Asset]
      </div>
    );
  }

  // Smooth interpolation calculations
  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;

  if (motion === "zoom-in") {
    scale = interpolate(frame, [0, durationInFrames], [1.0, 1.16], {
      extrapolateRight: "clamp",
    });
    translateY = interpolate(frame, [0, durationInFrames], [0, -20], {
      extrapolateRight: "clamp",
    });
  } else if (motion === "zoom-out") {
    scale = interpolate(frame, [0, durationInFrames], [1.16, 1.0], {
      extrapolateRight: "clamp",
    });
    translateY = interpolate(frame, [0, durationInFrames], [-20, 0], {
      extrapolateRight: "clamp",
    });
  } else if (motion === "pan-left") {
    scale = 1.1;
    translateX = interpolate(frame, [0, durationInFrames], [30, -30], {
      extrapolateRight: "clamp",
    });
  } else if (motion === "pan-right") {
    scale = 1.1;
    translateX = interpolate(frame, [0, durationInFrames], [-30, 30], {
      extrapolateRight: "clamp",
    });
  }

  // Resolves staticFile if path starts with assets or local file
  const imageSource = src.startsWith("http") ? src : staticFile(src);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        overflow: "hidden",
        backgroundColor: "#000",
        position: "relative",
      }}
    >
      <Img
        src={imageSource}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
          transition: "transform 0.05s linear",
        }}
      />
      {/* Subtle cinematic vignette overlay */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background:
            "radial-gradient(circle, rgba(0,0,0,0) 60%, rgba(0,0,0,0.55) 100%)",
          pointerEvents: "none",
        }}
      />
    </div>
  );
};
