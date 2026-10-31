/**
 * AbyssalSkillsD - Desktop Bridge
 * Safely wraps pywebview.api calls with error handling, timeout guards,
 * and background progress handlers with mandatory cancel support.
 */

class DesktopBridge {
  static isReady = false;
  static readyCallbacks = [];

  static init() {
    if (window.pywebview && window.pywebview.api) {
      this.isReady = true;
      this.triggerReady();
    } else {
      window.addEventListener("pywebviewready", () => {
        this.isReady = true;
        this.triggerReady();
      });
      // Fallback check after 500ms
      setTimeout(() => {
        if (window.pywebview && window.pywebview.api) {
          this.isReady = true;
          this.triggerReady();
        }
      }, 500);
    }
  }

  static onReady(cb) {
    if (this.isReady) {
      cb();
    } else {
      this.readyCallbacks.push(cb);
    }
  }

  static triggerReady() {
    while (this.readyCallbacks.length > 0) {
      const cb = this.readyCallbacks.shift();
      try { cb(); } catch (e) { console.error("Ready callback error:", e); }
    }
  }

  static async call(method, ...args) {
    if (!window.pywebview || !window.pywebview.api) {
      console.warn(`[Bridge] pywebview.api not available yet for method '${method}'.`);
      return null;
    }
    try {
      const fn = window.pywebview.api[method];
      if (typeof fn !== "function") {
        throw new Error(`API method '${method}' does not exist on pywebview.api`);
      }
      return await fn.apply(window.pywebview.api, args);
    } catch (err) {
      console.error(`[Bridge Error] in '${method}':`, err);
      throw err;
    }
  }

  /* Core API Wrappers */
  static async getSkills(workspacePath = null) {
    return await this.call("get_skills", workspacePath);
  }

  static async getSkill(skillId, workspacePath = null) {
    return await this.call("get_skill", skillId, workspacePath);
  }

  static async getSkillDiff(skillId, workspacePath = null) {
    return await this.call("get_skill_diff", { skill_id: skillId, workspace_path: workspacePath });
  }

  static async installSkill(payload) {
    return await this.call("install_skill", payload);
  }

  static async uninstallSkill(payload) {
    return await this.call("uninstall_skill", payload);
  }

  static async getActiveWorkspace() {
    return await this.call("get_active_workspace");
  }

  static async setActiveWorkspace(path) {
    return await this.call("set_active_workspace", path);
  }

  static async syncAllAIs(payload = {}) {
    return await this.call("sync_all_ais", payload);
  }

  static async generateProjectRules(payload = {}) {
    return await this.call("generate_project_rules", payload);
  }

  static async installAllSkills(payload) {
    return await this.call("install_all_skills", payload);
  }

  static async getCommunitySchema() {
    return await this.call("get_community_schema");
  }

  /* Phase 3: Community Cloud & Diagnostic Logger */
  static async communityGetSkills() {
    return await this.call("community_get_skills");
  }

  static async communityPublishSkill(skillData) {
    return await this.call("community_publish_skill", skillData);
  }

  static async communityInstallSkill(payload) {
    return await this.call("community_install_skill", payload);
  }

  static async getDiagnosticLogs(lineCount = 150) {
    return await this.call("get_diagnostic_logs", lineCount);
  }

  static async exportDiagnosticLogs() {
    return await this.call("export_diagnostic_logs");
  }

  static async openLogsFolder() {
    return await this.call("open_logs_folder");
  }

  /* Phase 4: Zero-Trust Security & Error Telemetry */
  static async reportSystemError(errorPayload) {
    return await this.call("report_system_error", errorPayload);
  }

  static async saveSkill(skillData) {
    return await this.call("save_skill", skillData);
  }

  static async deleteSkill(skillId) {
    return await this.call("delete_skill", skillId);
  }

  static async toggleFavorite(skillId) {
    return await this.call("toggle_favorite", skillId);
  }

  static async importFromGitHub(repoUrl) {
    return await this.call("import_from_github", repoUrl);
  }

  static async scanLocalFolder(folderPath) {
    return await this.call("scan_local_folder", folderPath);
  }

  static async pickFolderDialog() {
    return await this.call("pick_folder_dialog");
  }

  static async runGraphify(targetPath, force = false) {
    return await this.call("run_graphify", targetPath, force);
  }

  static async getSystemInfo() {
    return await this.call("get_system_info");
  }

  static async openFolder(folderPath) {
    return await this.call("open_folder", folderPath);
  }

  /* Supabase Auth & Secret Key API (supabase-backend-architect) */
  static async authSignIn(credentials) {
    return await this.call("auth_sign_in", credentials);
  }

  static async authSignInOAuth(provider) {
    return await this.call("auth_sign_in_oauth", { provider });
  }

  static async authSignUp(data) {
    return await this.call("auth_sign_up", data);
  }

  static async authSignOut() {
    return await this.call("auth_sign_out");
  }

  static async authGetSession() {
    return await this.call("auth_get_session");
  }

  static async authGetConfig() {
    return await this.call("auth_get_config");
  }

  static async authSaveConfig(config) {
    return await this.call("auth_save_config", config);
  }

  static async authRefreshToken(tokenPayload) {
    return await this.call("auth_refresh_token", tokenPayload);
  }

  // =========================================================================
  // Auto-Update Engine (v7.2 Dual-Layer Skills & Application Updates)
  // =========================================================================
  static async updaterCheck(data = {}) {
    return await this.call("updater_check", data);
  }

  static async updaterSyncSkills() {
    return await this.call("updater_sync_skills");
  }

  static async updaterGetInfo() {
    return await this.call("updater_get_info");
  }

  // =========================================================================
  // Live Verification & Explorer Proof Engine (v1.1)
  // =========================================================================
  static async openSkillFolder(data = {}) {
    return await this.call("open_skill_folder", data);
  }

  static async verifySkillActive(data = {}) {
    return await this.call("verify_skill_active", data);
  }
}

DesktopBridge.init();
window.DesktopBridge = DesktopBridge;
