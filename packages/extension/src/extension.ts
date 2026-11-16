import * as vscode from "vscode";
import { StudioSidebarProvider } from "./SidebarProvider";

export function activate(context: vscode.ExtensionContext) {
  const sidebarProvider = new StudioSidebarProvider(context.extensionUri);

  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      StudioSidebarProvider.viewType,
      sidebarProvider
    )
  );

  // Command to refresh timeline from Graphify memory
  context.subscriptions.push(
    vscode.commands.registerCommand("antigravity.studio.syncMemory", () => {
      sidebarProvider.refreshTimeline();
      vscode.window.showInformationMessage("Synced Antigravity Video Studio with Graphify memory.");
    })
  );

  // Command to render final video
  context.subscriptions.push(
    vscode.commands.registerCommand("antigravity.studio.render", () => {
      const terminal = vscode.window.createTerminal("Remotion Render");
      terminal.show();
      terminal.sendText("npm run render");
    })
  );
}

export function deactivate() {}
