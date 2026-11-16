import React from "react";
import { AbsoluteFill } from "remotion";

export type ColorGradePreset =
  | "teal-and-orange"
  | "moody-documentary"
  | "kodak-portra"
  | "noir-monochrome"
  | "clean";

interface CinematicGradeProps {
  children: React.ReactNode;
  preset?: ColorGradePreset;
  letterbox?: boolean; // 2.39:1 Anamorphic cinema bars
  filmGrainOpacity?: number;
}

export const CinematicGrade: React.FC<CinematicGradeProps> = ({
  children,
  preset = "moody-documentary",
  letterbox = true,
  filmGrainOpacity = 0.08,
}) => {
  // Preset color filter matrix
  let filterStyle = "";
  switch (preset) {
    case "teal-and-orange":
      filterStyle = "contrast(1.18) saturate(1.15) brightness(0.96) hue-rotate(-5deg)";
      break;
    case "moody-documentary":
      filterStyle = "contrast(1.22) saturate(0.92) brightness(0.94) sepia(0.08)";
      break;
    case "kodak-portra":
      filterStyle = "contrast(1.08) saturate(1.05) brightness(1.02) sepia(0.12)";
      break;
    case "noir-monochrome":
      filterStyle = "grayscale(1.0) contrast(1.35) brightness(0.92)";
      break;
    case "clean":
    default:
      filterStyle = "none";
      break;
  }

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
      {/* 1. Graded Visual Content Layer */}
      <div
        style={{
          width: "100%",
          height: "100%",
          filter: filterStyle,
          position: "relative",
        }}
      >
        {children}
      </div>

      {/* 2. 35mm Organic Film Grain Overlay (Subtle Dynamic Texture) */}
      {filmGrainOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            pointerEvents: "none",
            opacity: filmGrainOpacity,
            mixBlendMode: "overlay",
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
          }}
        />
      )}

      {/* 3. Subtle Vignette (Darkened Edges to Focus the Viewer's Eye) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          pointerEvents: "none",
          background: "radial-gradient(circle at center, rgba(0,0,0,0) 65%, rgba(0,0,0,0.45) 100%)",
        }}
      />

      {/* 4. 2.39:1 Cinema Anamorphic Letterbox Bars (Top & Bottom) */}
      {letterbox && (
        <>
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              height: "7.5%",
              backgroundColor: "#000000",
              zIndex: 100,
              pointerEvents: "none",
            }}
          />
          <div
            style={{
              position: "absolute",
              bottom: 0,
              left: 0,
              right: 0,
              height: "7.5%",
              backgroundColor: "#000000",
              zIndex: 100,
              pointerEvents: "none",
            }}
          />
        </>
      )}
    </AbsoluteFill>
  );
};
