import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface VerticalV3SubtitleProps {
  text?: string;
  durationInFrames: number;
  highlightColor?: string; // Default Hormozi Neon Yellow #FFEE00
}

export const VerticalV3Subtitle: React.FC<VerticalV3SubtitleProps> = ({
  text,
  durationInFrames,
  highlightColor = "#FFEE00",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!text) return null;

  // Split into words for kinetic active-word tracking
  const words = text.trim().split(/\s+/);
  if (words.length === 0) return null;

  // Calculate which word is currently spoken based on progress through the scene
  const framesPerWord = Math.max(1, durationInFrames / words.length);
  const activeWordIndex = Math.min(
    words.length - 1,
    Math.floor(frame / framesPerWord)
  );

  // Pop animation on active word change
  const wordRelativeFrame = frame % framesPerWord;
  const popSpring = spring({
    frame: wordRelativeFrame,
    fps,
    config: {
      damping: 12,
      stiffness: 140,
    },
  });

  return (
    <div
      style={{
        position: "absolute",
        // Platform Safe Zone: elevated clear of TikTok/Instagram bottom overlays
        bottom: "32%",
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 60px",
        pointerEvents: "none",
        zIndex: 90,
      }}
    >
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          gap: "14px 16px",
          maxWidth: "920px",
          textAlign: "center",
        }}
      >
        {words.map((word, idx) => {
          const isActive = idx === activeWordIndex;
          const scale = isActive ? 1.0 + 0.15 * popSpring : 1.0;

          return (
            <span
              key={`${word}-${idx}`}
              style={{
                fontFamily:
                  "Impact, 'Arial Black', -apple-system, system-ui, sans-serif",
                fontSize: "56px",
                fontWeight: 900,
                textTransform: "uppercase",
                letterSpacing: "1px",
                lineHeight: 1.1,
                display: "inline-block",
                transform: `scale(${scale})`,
                transition: "transform 0.05s ease-out",
                // Active Word: High-voltage highlight box
                backgroundColor: isActive ? highlightColor : "transparent",
                color: isActive ? "#000000" : "#FFFFFF",
                padding: isActive ? "4px 16px" : "2px 4px",
                borderRadius: isActive ? "8px" : "0px",
                boxShadow: isActive
                  ? `0 8px 24px ${highlightColor}88, 0 4px 12px rgba(0,0,0,0.8)`
                  : "none",
                WebkitTextStroke: isActive
                  ? "none"
                  : "4px rgba(0, 0, 0, 0.95)",
                textShadow: isActive
                  ? "none"
                  : "0 6px 18px rgba(0, 0, 0, 0.9)",
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
