import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface KineticSubtitleProps {
  text?: string;
}

export const KineticSubtitle: React.FC<KineticSubtitleProps> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!text) return null;

  // Spring animation for smooth entry pop
  const entry = spring({
    frame,
    fps,
    config: {
      damping: 14,
      stiffness: 90,
    },
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 80,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 80px",
        pointerEvents: "none",
        zIndex: 50,
      }}
    >
      <div
        style={{
          background: "rgba(10, 15, 25, 0.72)",
          backdropFilter: "blur(8px)",
          borderRadius: "14px",
          padding: "16px 32px",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          boxShadow: "0 12px 32px rgba(0, 0, 0, 0.6)",
          transform: `scale(${0.92 + 0.08 * entry})`,
          opacity: entry,
          maxWidth: "85%",
          textAlign: "center",
        }}
      >
        <span
          style={{
            fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            fontSize: "36px",
            fontWeight: 700,
            color: "#FFFFFF",
            letterSpacing: "0.2px",
            lineHeight: 1.35,
            textShadow: "0 2px 8px rgba(0, 0, 0, 0.9)",
          }}
        >
          {text}
        </span>
      </div>
    </div>
  );
};
