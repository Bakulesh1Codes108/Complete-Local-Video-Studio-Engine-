import React from "react";
import { interpolate, useCurrentFrame, AbsoluteFill } from "remotion";

export type HiggsfieldMotionType =
  | "orbit_360"
  | "fpv_drone_dive"
  | "vertigo_dolly_zoom"
  | "crane_up_reveal"
  | "bullet_time_freeze"
  | "whip_pan"
  | "handheld_subtle"
  | "none";

interface HiggsfieldCameraProps {
  children: React.ReactNode;
  durationInFrames: number;
  motion?: HiggsfieldMotionType;
  intensity?: number; // 0.5 to 2.0 (default 1.0)
}

export const HiggsfieldCamera: React.FC<HiggsfieldCameraProps> = ({
  children,
  durationInFrames,
  motion = "orbit_360",
  intensity = 1.0,
}) => {
  const frame = useCurrentFrame();

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;
  let rotateZ = 0;
  let rotateX = 0;
  let rotateY = 0;
  let perspective = 1200;

  switch (motion) {
    case "orbit_360": {
      // 3D elliptical rotation simulating an orbital camera rig
      scale = interpolate(frame, [0, durationInFrames / 2, durationInFrames], [1.08, 1.15, 1.08], {
        extrapolateRight: "clamp",
      });
      translateX = interpolate(frame, [0, durationInFrames], [-25 * intensity, 25 * intensity], {
        extrapolateRight: "clamp",
      });
      rotateY = interpolate(frame, [0, durationInFrames], [-8 * intensity, 8 * intensity], {
        extrapolateRight: "clamp",
      });
      rotateZ = interpolate(frame, [0, durationInFrames / 2, durationInFrames], [-1.2 * intensity, 1.2 * intensity, -1.2 * intensity]);
      break;
    }
    case "fpv_drone_dive": {
      // Rapid forward dive with banking roll
      scale = interpolate(frame, [0, durationInFrames], [1.0, 1.35 * intensity], {
        extrapolateRight: "clamp",
      });
      translateY = interpolate(frame, [0, durationInFrames], [-30 * intensity, 40 * intensity], {
        extrapolateRight: "clamp",
      });
      rotateZ = interpolate(frame, [0, durationInFrames * 0.4, durationInFrames], [0, -4 * intensity, 3 * intensity], {
        extrapolateRight: "clamp",
      });
      rotateX = interpolate(frame, [0, durationInFrames], [6 * intensity, -4 * intensity]);
      break;
    }
    case "vertigo_dolly_zoom": {
      // Hitchcock Vertigo effect: scaling up while reversing perspective warp
      scale = interpolate(frame, [0, durationInFrames], [1.0, 1.3 * intensity], {
        extrapolateRight: "clamp",
      });
      perspective = interpolate(frame, [0, durationInFrames], [600, 1800], {
        extrapolateRight: "clamp",
      });
      translateY = interpolate(frame, [0, durationInFrames], [0, -18 * intensity]);
      break;
    }
    case "crane_up_reveal": {
      // Low angle rising smoothly into a wide panoramic reveal
      scale = interpolate(frame, [0, durationInFrames], [1.18, 1.05], {
        extrapolateRight: "clamp",
      });
      translateY = interpolate(frame, [0, durationInFrames], [50 * intensity, -20 * intensity], {
        extrapolateRight: "clamp",
      });
      rotateX = interpolate(frame, [0, durationInFrames], [-10 * intensity, 2 * intensity]);
      break;
    }
    case "bullet_time_freeze": {
      // Slow-motion sweep around subject
      scale = 1.15;
      translateX = interpolate(frame, [0, durationInFrames], [-40 * intensity, 40 * intensity], {
        extrapolateRight: "clamp",
      });
      rotateY = interpolate(frame, [0, durationInFrames], [-14 * intensity, 14 * intensity], {
        extrapolateRight: "clamp",
      });
      rotateZ = interpolate(frame, [0, durationInFrames], [-2 * intensity, 2 * intensity]);
      break;
    }
    case "whip_pan": {
      // High-velocity snap pan with ease-in-out
      scale = 1.12;
      translateX = interpolate(
        frame,
        [0, durationInFrames * 0.2, durationInFrames * 0.8, durationInFrames],
        [60 * intensity, 10 * intensity, -10 * intensity, -60 * intensity],
        { extrapolateRight: "clamp" }
      );
      rotateZ = interpolate(frame, [0, durationInFrames], [2 * intensity, -2 * intensity]);
      break;
    }
    case "handheld_subtle": {
      // Organic natural documentary camera breathing
      const t = frame / 15;
      scale = 1.06;
      translateX = Math.sin(t) * 4 * intensity;
      translateY = Math.cos(t * 0.8) * 3 * intensity;
      rotateZ = Math.sin(t * 0.5) * 0.8 * intensity;
      break;
    }
    case "none":
    default:
      break;
  }

  return (
    <AbsoluteFill
      style={{
        overflow: "hidden",
        backgroundColor: "#000",
        perspective: `${perspective}px`,
      }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${scale}) translate3d(${translateX}px, ${translateY}px, 0px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) rotateZ(${rotateZ}deg)`,
          transformOrigin: "center center",
          willChange: "transform",
        }}
      >
        {children}
      </div>
    </AbsoluteFill>
  );
};
