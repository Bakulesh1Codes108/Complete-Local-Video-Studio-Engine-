import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";

export class StudioSidebarProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = "antigravity.studio.preview";
  private _view?: vscode.WebviewView;

  constructor(private readonly _extensionUri: vscode.Uri) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ) {
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri],
    };

    webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

    // Handle messages from the Webview (Player controls, scene selection)
    webviewView.webview.onDidReceiveMessage(async (data) => {
      switch (data.type) {
        case "REFRESH_TIMELINE": {
          this.refreshTimeline();
          break;
        }
        case "TRIGGER_RENDER": {
          vscode.window.showInformationMessage("Rendering documentary MP4 via Remotion...");
          const terminal = vscode.window.createTerminal("Antigravity Video Render");
          terminal.show();
          terminal.sendText("npm run render");
          break;
        }
        case "TRIGGER_VOICEOVER": {
          vscode.window.showInformationMessage("Generating neural voiceover tracks...");
          const terminal = vscode.window.createTerminal("Antigravity Voiceover");
          terminal.show();
          terminal.sendText("npm run voiceover:generate");
          break;
        }
      }
    });

    // Auto-watch timeline.json for live reload
    this._watchTimelineFile();
  }

  public refreshTimeline() {
    if (!this._view) return;
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) return;

    const timelinePath = path.join(workspaceFolders[0].uri.fsPath, "timeline.json");
    if (fs.existsSync(timelinePath)) {
      try {
        const raw = fs.readFileSync(timelinePath, "utf-8");
        const timeline = JSON.parse(raw);
        this._view.webview.postMessage({
          type: "TIMELINE_LOADED",
          payload: timeline,
        });
      } catch (e) {
        console.error("Failed to parse timeline.json", e);
      }
    }
  }

  private _watchTimelineFile() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) return;

    const watcher = vscode.workspace.createFileSystemWatcher("**/timeline.json");
    watcher.onDidChange(() => this.refreshTimeline());
    watcher.onDidCreate(() => this.refreshTimeline());
  }

  private _getHtmlForWebview(webview: vscode.Webview): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Antigravity Video Studio</title>
  <style>
    body {
      font-family: var(--vscode-font-family, sans-serif);
      margin: 0;
      padding: 16px;
      color: var(--vscode-foreground);
      background-color: var(--vscode-editor-background);
    }
    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--vscode-widget-border, #333);
      padding-bottom: 12px;
      margin-bottom: 16px;
    }
    .btn {
      background: var(--vscode-button-background);
      color: var(--vscode-button-foreground);
      border: none;
      padding: 8px 14px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 600;
      margin-right: 8px;
    }
    .btn:hover {
      background: var(--vscode-button-hoverBackground);
    }
    .scene-card {
      background: var(--vscode-editorWidget-background, #1e1e1e);
      border: 1px solid var(--vscode-widget-border, #333);
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 12px;
    }
    .scene-title {
      font-weight: 700;
      color: var(--vscode-textLink-foreground, #3794ff);
      margin-bottom: 4px;
    }
    .badge {
      display: inline-block;
      font-size: 11px;
      padding: 2px 6px;
      background: #238636;
      color: white;
      border-radius: 10px;
      margin-left: 6px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h3 style="margin:0;">🎬 Antigravity Video Studio</h3>
    <div>
      <button class="btn" onclick="sendMsg('TRIGGER_VOICEOVER')">🎙️ Voiceover</button>
      <button class="btn" onclick="sendMsg('TRIGGER_RENDER')">🚀 Render MP4</button>
    </div>
  </div>

  <div id="timeline-container">
    <p style="color: var(--vscode-descriptionForeground);">Loading studio timeline from Graphify memory...</p>
  </div>

  <script>
    const vscode = acquireVsCodeApi();
    function sendMsg(type, payload = {}) {
      vscode.postMessage({ type, payload });
    }

    window.addEventListener('message', event => {
      const msg = event.data;
      if (msg.type === 'TIMELINE_LOADED') {
        renderTimeline(msg.payload);
      }
    });

    function renderTimeline(timeline) {
      const container = document.getElementById('timeline-container');
      if (!timeline || !timeline.scenes) {
        container.innerHTML = '<p>No scenes found in timeline.json</p>';
        return;
      }

      let html = '<h4>Project: ' + timeline.project + ' (' + timeline.scenes.length + ' Scenes)</h4>';
      timeline.scenes.forEach((sc, i) => {
        html += '<div class="scene-card">';
        html += '<div class="scene-title">Scene ' + (i+1) + ': ' + sc.id + ' <span class="badge">' + (sc.durationInFrames / 30).toFixed(1) + 's</span></div>';
        html += '<p style="margin: 6px 0; font-size: 13px;">' + (sc.subtitle || 'No narration') + '</p>';
        html += '<div style="font-size: 11px; opacity: 0.7;">Visual: ' + (sc.visual || 'Pending') + ' | Motion: ' + (sc.motion || 'zoom-in') + '</div>';
        html += '</div>';
      });
      container.innerHTML = html;
    }

    // Request initial timeline load
    sendMsg('REFRESH_TIMELINE');
  </script>
</body>
</html>`;
  }
}
