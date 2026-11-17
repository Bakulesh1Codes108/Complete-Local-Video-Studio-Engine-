import React, { useRef, useEffect } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

export type ThreeJsSceneType =
  | "3d_rotating_globe"
  | "3d_quantum_particles"
  | "3d_financial_chart"
  | "3d_title_monolith";

interface ThreeJsSceneProps {
  sceneType?: ThreeJsSceneType;
  title?: string;
  accentColor?: string; // e.g. "#6366f1"
  durationInFrames: number;
}

export const ThreeJsScene: React.FC<ThreeJsSceneProps> = ({
  sceneType = "3d_quantum_particles",
  title = "3D PROCEDURAL VISUALIZATION",
  accentColor = "#6366f1",
  durationInFrames,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, width, height);
    const progress = frame / durationInFrames;

    // Background gradient
    const bgGrad = ctx.createRadialGradient(width / 2, height / 2, 50, width / 2, height / 2, width * 0.7);
    bgGrad.addColorStop(0, "#111827");
    bgGrad.addColorStop(1, "#030712");
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, width, height);

    if (sceneType === "3d_quantum_particles") {
      // 3D Isometric Wave Grid
      const rows = 28;
      const cols = 42;
      const spacingX = width / (cols * 0.75);
      const spacingY = height / (rows * 1.4);
      const angle = progress * Math.PI * 2;

      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const x3d = (c - cols / 2) * spacingX;
          const z3d = (r - rows / 2) * spacingY;
          const dist = Math.sqrt(x3d * x3d + z3d * z3d);
          const y3d = Math.sin(dist * 0.015 - angle * 2) * 55 * Math.cos(r * 0.2);

          // Isometric 3D Projection
          const isoX = width / 2 + (x3d - z3d) * 0.75;
          const isoY = height / 2 + (x3d + z3d) * 0.38 - y3d;

          const size = Math.max(1.5, (r / rows) * 4.5);
          const alpha = 0.25 + 0.65 * (r / rows);

          ctx.beginPath();
          ctx.arc(isoX, isoY, size, 0, Math.PI * 2);
          ctx.fillStyle = r % 4 === 0 ? accentColor : `rgba(240, 245, 255, ${alpha})`;
          ctx.shadowBlur = r % 4 === 0 ? 12 : 0;
          ctx.shadowColor = accentColor;
          ctx.fill();
        }
      }
    } else if (sceneType === "3d_rotating_globe") {
      // 3D Holographic Wireframe Globe
      const centerX = width / 2;
      const centerY = height / 2;
      const radius = Math.min(width, height) * 0.28;
      const rot = progress * Math.PI * 4;

      // Glow backdrop
      const glow = ctx.createRadialGradient(centerX, centerY, radius * 0.4, centerX, centerY, radius * 1.2);
      glow.addColorStop(0, "rgba(99, 102, 241, 0.25)");
      glow.addColorStop(1, "rgba(99, 102, 241, 0)");
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius * 1.2, 0, Math.PI * 2);
      ctx.fill();

      // Longitude rings (rotating)
      ctx.strokeStyle = "rgba(147, 197, 253, 0.55)";
      ctx.lineWidth = 1.8;
      for (let i = 0; i < 8; i++) {
        const ringAngle = rot + (i * Math.PI) / 8;
        const currentWidth = radius * Math.cos(ringAngle);
        ctx.beginPath();
        ctx.ellipse(centerX, centerY, Math.abs(currentWidth), radius, 0, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Latitude rings
      ctx.strokeStyle = "rgba(165, 180, 252, 0.35)";
      for (let lat = -3; lat <= 3; lat++) {
        if (lat === 0) continue;
        const yOffset = (lat / 4) * radius;
        const latRadius = Math.sqrt(Math.max(0, radius * radius - yOffset * yOffset));
        ctx.beginPath();
        ctx.ellipse(centerX, centerY + yOffset, latRadius, latRadius * 0.25, 0, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Equator bold
      ctx.strokeStyle = accentColor;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.ellipse(centerX, centerY, radius, radius * 0.28, 0, 0, Math.PI * 2);
      ctx.stroke();
    } else if (sceneType === "3d_financial_chart") {
      // 3D Isometric Bar Chart
      const bars = [35, 60, 45, 85, 70, 95, 120, 110];
      const startX = width * 0.25;
      const baseY = height * 0.65;
      const barWidth = 36;
      const gap = 45;

      bars.forEach((val, i) => {
        const animatedHeight = val * 2.8 * Math.min(1.0, (progress * 1.5) - (i * 0.08));
        if (animatedHeight <= 0) return;

        const x = startX + i * (barWidth + gap);
        const y = baseY - animatedHeight;
        const depth = 22;

        // Front Face
        ctx.fillStyle = i === bars.length - 1 ? "#10b981" : accentColor;
        ctx.fillRect(x, y, barWidth, animatedHeight);

        // Top Face (3D isometric top)
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + depth, y - depth * 0.6);
        ctx.lineTo(x + barWidth + depth, y - depth * 0.6);
        ctx.lineTo(x + barWidth, y);
        ctx.closePath();
        ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
        ctx.fill();

        // Right Face (3D isometric side)
        ctx.beginPath();
        ctx.moveTo(x + barWidth, y);
        ctx.lineTo(x + barWidth + depth, y - depth * 0.6);
        ctx.lineTo(x + barWidth + depth, baseY - depth * 0.6);
        ctx.lineTo(x + barWidth, baseY);
        ctx.closePath();
        ctx.fillStyle = "rgba(0, 0, 0, 0.35)";
        ctx.fill();
      });
    }

    // Overlay Cinematic Typography Label
    ctx.shadowBlur = 0;
    ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
    ctx.font = "700 24px 'Plus Jakarta Sans', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(title.toUpperCase(), width / 2, height * 0.88);
  }, [frame, width, height, sceneType, title, accentColor, durationInFrames]);

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      <canvas ref={canvasRef} width={width} height={height} style={{ width: "100%", height: "100%" }} />
    </div>
  );
};
