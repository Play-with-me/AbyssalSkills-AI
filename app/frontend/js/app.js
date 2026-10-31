/**
 * AbyssalSkillsD - Main Application Controller
 * Handles Workbench states, Zero-Waterfall boot, Dual-Theme switcher,
 * Command Palette (Ctrl+K), Community Cloud Hub, and Optimistic UI.
 */

const App = {
  skills: [],
  filteredSkills: [],
  activeWorkspace: "library", // library, installed, guide, studio, community
  activeViewMode: "bento",    // bento, linear
  activeCategory: "all",
  activeSource: "all",        // all, skill_ai, addy_osmani
  searchQuery: "",
  selectedSkillId: null,
  activeDocId: "guide",
  isOnboardingCollapsed: (localStorage.getItem("abyssalskillsd-onboarding-collapsed") ?? localStorage.getItem("skillforge-onboarding-collapsed")) === "true",
  authSession: null,
  supabaseConfig: null,
  isUserMenuOpen: false,
  activeAuthTab: "signin",
  communitySchema: null,
  communitySkills: [],
  communitySubTab: "marketplace",
  communityFilterCat: "all",
  communitySearchQuery: "",
  isCommandPaletteOpen: false,
  commandPaletteIndex: 0,
  notifications: [],
  isNotificationTrayOpen: false,
  currentTheme: localStorage.getItem("abyssalskillsd-theme") || localStorage.getItem("skillforge-theme") || "dark",
  activeWorkspaceProject: localStorage.getItem("abyssalskillsd-workspace-project") || null,

  async init() {
    this.applyTheme(this.currentTheme);
    this.showIntro();
    this.bindEvents();
    this.showShimmer();

    DesktopBridge.onReady(async () => {
      await this.initWorkspaceProject();
      // Prioritize essential skills library first for immediate rendering
      await this.loadSkills();

      // Defer secondary background data loading to avoid CPU contention during intro animation
      setTimeout(async () => {
        await Promise.all([
          this.loadAuthSession(),
          this.updateSystemStatus()
        ]);
        const statusEl = document.getElementById("intro-status-text");
        if (statusEl && this.skills.length > 0) {
          statusEl.innerText = `${this.skills.length} Kỹ Năng Đã Sẵn Sàng Làm Việc`;
        }
        // Auto-check for updates silently in background
        setTimeout(() => this.checkAppUpdates(false), 4000);
      }, 1200);
    });
  },

  showIntro() {
    const mount = document.getElementById("intro-mount");
    if (!mount) return;

    if (this._introTimer) {
      clearTimeout(this._introTimer);
      this._introTimer = null;
    }
    if (this._introKeyHandler) {
      window.removeEventListener("keydown", this._introKeyHandler);
      this._introKeyHandler = null;
    }

    mount.innerHTML = UIComponents.renderIntroOverlay(this.skills.length || 36);

    const overlay = document.getElementById("intro-overlay");
    if (!overlay) return;

    let canInteract = false;
    let isExiting = false;

    // Grace period for shard assembly animation (400ms buffer)
    setTimeout(() => {
      canInteract = true;
    }, 400);

    const enter = () => {
      if (isExiting) return;
      isExiting = true;
      if (this._introTimer) {
        clearTimeout(this._introTimer);
        this._introTimer = null;
      }
      if (this._introKeyHandler) {
        window.removeEventListener("keydown", this._introKeyHandler);
        this._introKeyHandler = null;
      }
      // Ensure skills cards are rendered if user enters quickly
      if (this.filteredSkills.length === 0 && this.skills.length > 0) {
        this.applyFilters();
      }
      overlay.classList.add("zoom-through-out");
      setTimeout(() => {
        if (mount.contains(overlay)) {
          mount.innerHTML = "";
        }
      }, 550);
    };

    this.enterWorkbench = enter;

    this.replayIntro = () => {
      if (isExiting) return;
      this.showIntro();
    };

    // User must actively interact to enter workbench (No auto-dismiss)
    // Click prompt or anywhere on screen
    overlay.addEventListener("click", () => {
      if (canInteract) enter();
    });

    // Keyboard controls: Any key (Enter, Space, ESC, letter/number) enters workbench
    this._introKeyHandler = (e) => {
      if (!canInteract) return;
      if (['Shift', 'Control', 'Alt', 'Meta', 'CapsLock'].includes(e.key)) return;
      e.preventDefault();
      enter();
    };
    window.addEventListener("keydown", this._introKeyHandler);
  },

  applyTheme(theme) {
    this.currentTheme = theme;
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("abyssalskillsd-theme", theme);
    const themeBtn = document.getElementById("btn-toggle-theme");
    if (themeBtn) {
      themeBtn.innerHTML = theme === "dark" ? Icons.sun : Icons.moon;
      themeBtn.title = theme === "dark" ? "Chuyển sang giao diện Sáng (Daylight)" : "Chuyển sang giao diện Tối (Obsidian)";
    }
  },

  toggleTheme() {
    const nextTheme = this.currentTheme === "dark" ? "light" : "dark";
    this.applyTheme(nextTheme);
    this.showToast(`Đã chuyển sang giao diện ${nextTheme === 'dark' ? 'Tối (Obsidian)' : 'Sáng (Daylight)'}`, "info");
  },

  async loadSkills() {
    try {
      const data = await DesktopBridge.getSkills(this.activeWorkspaceProject);
      if (Array.isArray(data)) {
        this.skills = data;
        this.renderOrgBanner();
        this.updateBadges();

        // High-Performance Gate: If intro is active, defer heavy Bento DOM creation
        // so Edge WebView2 gives 100% GPU/CPU priority to smooth 60fps intro animation
        const isIntroActive = !!document.getElementById("intro-overlay");
        if (isIntroActive) {
          if ('requestIdleCallback' in window) {
            requestIdleCallback(() => this.applyFilters(), { timeout: 1000 });
          } else {
            setTimeout(() => this.applyFilters(), 500);
          }
        } else {
          this.applyFilters();
        }
      }
    } catch (err) {
      this.showToast("Không thể tải danh sách kỹ năng: " + err.message, "error");
    }
  },

  async initWorkspaceProject() {
    try {
      if (this.activeWorkspaceProject) {
        await DesktopBridge.setActiveWorkspace(this.activeWorkspaceProject);
      } else {
        const res = await DesktopBridge.getActiveWorkspace();
        if (res && res.workspace_path) {
          this.activeWorkspaceProject = res.workspace_path;
        }
      }
      this.updateWorkspaceBadge();
    } catch (e) {
      console.warn("initWorkspaceProject error:", e);
    }
  },

  updateWorkspaceBadge() {
    const badge = document.getElementById("workspace-current-badge");
    if (!badge) return;
    const pathStr = this.activeWorkspaceProject || "Chưa chọn thư mục";
    const parts = pathStr.split(/[\\/]/).filter(Boolean);
    const folderName = parts.length > 0 ? parts[parts.length - 1] : pathStr;
    badge.innerText = folderName;
    badge.title = pathStr;
  },

  async handleSelectWorkspaceProject() {
    try {
      const res = await DesktopBridge.pickFolderDialog();
      if (res && res.path) {
        this.activeWorkspaceProject = res.path;
        localStorage.setItem("abyssalskillsd-workspace-project", res.path);
        await DesktopBridge.setActiveWorkspace(res.path);
        this.updateWorkspaceBadge();
        this.showToast(`Đã chuyển dự án mục tiêu sang: ${res.path}`, "info");
        await this.loadSkills();
      }
    } catch (err) {
      this.showToast("Không thể chọn thư mục: " + (err.message || err), "error");
    }
  },

  openUninstallModal(skillId) {
    const skill = this.skills.find(s => s.id === skillId);
    if (!skill) return;
    const root = document.getElementById("modal-root");
    if (!root) return;

    root.innerHTML = UIComponents.renderUninstallConfirmModal(
      skill, 
      skill.installed_targets || [], 
      this.activeWorkspaceProject
    );

    document.getElementById("btn-confirm-uninstall-action")?.addEventListener("click", async () => {
      const checkedBoxes = Array.from(root.querySelectorAll(".uninstall-target-checkbox:checked"));
      const selectedTargets = checkedBoxes.map(cb => cb.value);
      if (selectedTargets.length === 0) {
        this.showToast("Vui lòng chọn ít nhất một nền tảng để gỡ bỏ.", "warning");
        return;
      }

      const confirmBtn = document.getElementById("btn-confirm-uninstall-action");
      if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = `<span>Đang gỡ bỏ...</span>`;
      }

      try {
        const res = await DesktopBridge.uninstallSkill({
          skill_id: skill.id,
          targets: selectedTargets,
          workspace_path: this.activeWorkspaceProject || null
        });

        if (res && res.success) {
          this.closeActiveModal();
          this.showToast(`✓ Đã gỡ bỏ kỹ năng "${skill.display_title || skill.name}" khỏi các nền tảng đã chọn!`, "success");
          await this.loadSkills();
          this.selectSkill(skill.id);
        } else {
          this.showToast(res ? res.message : "Gỡ bỏ thất bại.", "error");
          if (confirmBtn) {
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = `${Icons.trash} <span>Xác Nhận Gỡ Bỏ</span>`;
          }
        }
      } catch (err) {
        this.showToast("Lỗi khi gỡ bỏ: " + (err.message || err), "error");
        if (confirmBtn) {
          confirmBtn.disabled = false;
          confirmBtn.innerHTML = `${Icons.trash} <span>Xác Nhận Gỡ Bỏ</span>`;
        }
      }
    });
  },

  handleCustomizeInStudio(skillId) {
    const skill = this.skills.find(s => s.id === skillId);
    if (!skill) return;

    this.switchWorkspace("studio");

    setTimeout(() => {
      const titleInput = document.getElementById("studio-title");
      const idInput = document.getElementById("studio-id");
      const categorySelect = document.getElementById("studio-category");
      const descInput = document.getElementById("studio-desc");
      const contentInput = document.getElementById("studio-content");

      if (titleInput) titleInput.value = `${skill.display_title || skill.name} (Tùy Biến)`;
      if (idInput) {
        idInput.value = `${skill.id}-custom`;
        idInput.dataset.manual = "true";
      }
      if (categorySelect) categorySelect.value = skill.category || "architecture";
      if (descInput) descInput.value = skill.description || "";
      if (contentInput) {
        contentInput.value = skill.skill_content || "";
        contentInput.dispatchEvent(new Event("input"));
      }

      this.showToast(`✓ Đã nạp "${skill.display_title || skill.name}" vào Studio! Bạn có thể chỉnh sửa và lưu thành kỹ năng riêng.`, "success");
    }, 120);
  },

  openSyncAllModal() {
    const root = document.getElementById("modal-root");
    if (!root) return;

    root.innerHTML = UIComponents.renderSyncAllModal(
      this.skills.length || 36,
      ["antigravity", "claude", "copilot", "cursor", "windsurf", "workspace"],
      this.activeWorkspaceProject
    );

    document.getElementById("btn-confirm-sync-all-action")?.addEventListener("click", async () => {
      const checkboxes = Array.from(root.querySelectorAll(".sync-target-checkbox:checked"));
      const selectedTargets = checkboxes.map(cb => cb.value);
      if (selectedTargets.length === 0) {
        this.showToast("Vui lòng chọn ít nhất một môi trường AI để đồng bộ.", "warning");
        return;
      }

      const confirmBtn = document.getElementById("btn-confirm-sync-all-action");
      const progressBox = document.getElementById("sync-progress-box");
      const progressBar = document.getElementById("sync-progress-bar");
      const progressText = document.getElementById("sync-progress-text");

      if (confirmBtn) confirmBtn.disabled = true;
      if (progressBox) progressBox.style.display = "block";
      if (progressBar) progressBar.style.width = "40%";
      if (progressText) progressText.innerText = `Đang đồng bộ ${this.skills.length} kỹ năng vào ${selectedTargets.length} môi trường AI...`;

      try {
        const res = await DesktopBridge.syncAllAIs({
          targets: selectedTargets,
          workspace_path: this.activeWorkspaceProject || null
        });

        if (progressBar) progressBar.style.width = "100%";

        setTimeout(async () => {
          this.closeActiveModal();
          if (res && res.success) {
            this.showToast(`✓ ${res.message || "Đã đồng bộ toàn bộ kỹ năng thành công!"}`, "success");
            await this.loadSkills();
          } else {
            this.showToast(res ? res.message : "Đồng bộ thất bại.", "error");
          }
        }, 600);
      } catch (err) {
        this.closeActiveModal();
        this.showToast("Lỗi đồng bộ: " + (err.message || err), "error");
      }
    });
  },

  openGenerateRulesModal() {
    const root = document.getElementById("modal-root");
    if (!root) return;

    root.innerHTML = UIComponents.renderGenerateRulesModal(this.activeWorkspaceProject);

    document.getElementById("btn-confirm-generate-rules-action")?.addEventListener("click", async () => {
      const checkboxes = Array.from(root.querySelectorAll(".gen-rule-checkbox:checked"));
      const selectedRules = checkboxes.map(cb => cb.value);
      if (selectedRules.length === 0) {
        this.showToast("Vui lòng chọn ít nhất một loại tệp quy tắc.", "warning");
        return;
      }

      const confirmBtn = document.getElementById("btn-confirm-generate-rules-action");
      if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = `<span>Đang khởi tạo...</span>`;
      }

      try {
        const res = await DesktopBridge.generateProjectRules({
          workspace_path: this.activeWorkspaceProject || null,
          rule_types: selectedRules
        });

        this.closeActiveModal();
        if (res && res.success) {
          this.showToast(`✓ ${res.message || "Đã khởi tạo tệp quy tắc thành công!"}`, "success");
        } else {
          this.showToast(res ? res.message : "Khởi tạo thất bại.", "error");
        }
      } catch (err) {
        this.closeActiveModal();
        this.showToast("Lỗi khởi tạo quy tắc: " + (err.message || err), "error");
      }
    });
  },

  async loadCommunitySchema() {
    try {
      const res = await DesktopBridge.getCommunitySchema();
      if (res && res.success) {
        this.communitySchema = res;
      }
    } catch (e) {
      console.warn("Community schema load warning:", e);
    }
  },

  async updateSystemStatus() {
    try {
      const sys = await DesktopBridge.getSystemInfo();
      const txt = document.getElementById("footer-status-text");
      if (txt) {
        txt.innerHTML = `Đã đồng bộ ${this.skills.length} kỹ năng (7 Skill-AI • 29 Addy Osmani) • Sẵn sàng đa nền tảng`;
      }
    } catch (e) {}
  },

  updateBadges() {
    const totalEl = document.getElementById("badge-total-skills");
    const instEl = document.getElementById("badge-installed-skills");
    if (totalEl) totalEl.innerText = this.skills.length;
    if (instEl) {
      const installedCount = this.skills.filter(s => s.installed_targets && s.installed_targets.length > 0).length;
      instEl.innerText = installedCount;
    }

    const countAll = this.skills.length;
    const countSkillAi = this.skills.filter(s => (s.source_group || 'skill_ai') === 'skill_ai').length;
    const countAddy = this.skills.filter(s => s.source_group === 'addy_osmani').length;

    const elAll = document.getElementById("count-source-all");
    const elSkillAi = document.getElementById("count-source-skill-ai");
    const elAddy = document.getElementById("count-source-addy-osmani");

    if (elAll) elAll.innerText = countAll;
    if (elSkillAi) elSkillAi.innerText = countSkillAi;
    if (elAddy) elAddy.innerText = countAddy;
  },

  /* =========================================================================
     Supabase Auth & Session Management (supabase-backend-architect)
     ========================================================================= */
  async loadAuthSession() {
    try {
      const res = await DesktopBridge.authGetSession();
      if (res) {
        this.authSession = res;
        this.renderUserWidget();
      }
    } catch (e) {
      console.warn("Auth session load warning:", e);
    }
  },

  async loadSupabaseConfig() {
    try {
      const res = await DesktopBridge.authGetConfig();
      if (res) {
        this.supabaseConfig = res;
      }
    } catch (e) {
      console.warn("Supabase config load warning:", e);
    }
  },

  renderUserWidget() {
    const container = document.getElementById("user-account-widget");
    if (!container) return;
    container.innerHTML = UIComponents.renderUserWidget(this.authSession);

    document.getElementById("btn-trigger-login")?.addEventListener("click", () => {
      this.openAuthModal("signin");
    });

    document.getElementById("btn-user-profile-menu")?.addEventListener("click", (e) => {
      e.stopPropagation();
      this.toggleUserMenu();
    });
  },

  toggleUserMenu() {
    this.isUserMenuOpen = !this.isUserMenuOpen;
    const existing = document.getElementById("user-dropdown-panel");
    if (existing) {
      existing.remove();
      return;
    }

    if (this.isUserMenuOpen) {
      const widget = document.getElementById("user-account-widget");
      if (widget) {
        widget.insertAdjacentHTML("beforeend", UIComponents.renderUserDropdown(this.authSession));
        
        document.getElementById("btn-menu-open-profile")?.addEventListener("click", () => {
          this.closeUserMenu();
          this.switchWorkspace("profile");
        });

        document.getElementById("btn-menu-copy-token")?.addEventListener("click", () => {
          this.copyUserAccessToken();
          this.closeUserMenu();
        });

        document.getElementById("btn-menu-open-config")?.addEventListener("click", () => {
          this.closeUserMenu();
          this.openAuthModal("config");
        });

        document.getElementById("btn-menu-signout")?.addEventListener("click", () => {
          this.closeUserMenu();
          this.handleSignOut();
        });
      }
    }
  },

  closeUserMenu() {
    this.isUserMenuOpen = false;
    document.getElementById("user-dropdown-panel")?.remove();
  },

  async copyUserAccessToken() {
    const token = this.authSession?.access_token;
    if (!token) {
      this.showToast("Chưa có Access Token phiên.", "error");
      return;
    }
    try {
      await navigator.clipboard.writeText(token);
      this.showToast("✓ Đã sao chép Access Token (JWT) vào bộ nhớ tạm!", "success");
    } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = token;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      this.showToast("✓ Đã sao chép Access Token!", "success");
    }
  },

  openAuthModal(tab = "signin", errorMsg = "") {
    this.activeAuthTab = tab;
    const root = document.getElementById("modal-root");
    if (!root) return;
    root.innerHTML = UIComponents.renderAuthModal(this.activeAuthTab, this.supabaseConfig || {}, this.authSession || {}, errorMsg);
    this.bindAuthModalEvents();
  },

  switchAuthTab(tab, errorMsg = "") {
    this.activeAuthTab = tab;
    this.openAuthModal(tab, errorMsg);
  },

  bindAuthModalEvents() {
    const root = document.getElementById("modal-root");
    if (!root) return;

    // 1-Click Social Sign-In Events
    document.getElementById("btn-auth-google")?.addEventListener("click", async () => {
      await this.handleSocialLogin("google");
    });

    document.getElementById("btn-auth-github")?.addEventListener("click", async () => {
      await this.handleSocialLogin("github");
    });

    root.querySelectorAll(".auth-tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const tab = btn.getAttribute("data-authtab");
        this.switchAuthTab(tab);
      });
    });

    document.getElementById("btn-submit-signin")?.addEventListener("click", async () => {
      const email = document.getElementById("auth-signin-email")?.value.trim();
      const password = document.getElementById("auth-signin-password")?.value.trim();
      await this.handleSignIn(email, password);
    });

    document.getElementById("btn-submit-signup")?.addEventListener("click", async () => {
      const fullName = document.getElementById("auth-signup-name")?.value.trim();
      const email = document.getElementById("auth-signup-email")?.value.trim();
      const password = document.getElementById("auth-signup-password")?.value.trim();
      await this.handleSignUp(email, password, fullName);
    });

    document.getElementById("btn-save-supabase-config")?.addEventListener("click", async () => {
      const url = document.getElementById("cfg-supabase-url")?.value.trim();
      const anonKey = document.getElementById("cfg-anon-key")?.value.trim();
      const secretKey = document.getElementById("cfg-secret-key")?.value.trim();
      await this.handleSaveSupabaseConfig(url, anonKey, secretKey);
    });

    document.getElementById("btn-reset-supabase-config")?.addEventListener("click", async () => {
      await this.handleSaveSupabaseConfig("", "");
      this.showToast("Đã khôi phục cấu hình Supabase về mặc định.", "info");
    });

    document.getElementById("btn-modal-copy-token")?.addEventListener("click", () => {
      this.copyUserAccessToken();
    });
  },

  async handleSocialLogin(provider) {
    const btnId = provider === "google" ? "btn-auth-google" : "btn-auth-github";
    const btn = document.getElementById(btnId);
    const origHtml = btn ? btn.innerHTML : "";
    if (btn) {
      btn.disabled = true;
      btn.style.opacity = "0.7";
      btn.innerHTML = `<span style="display:inline-block; animation:spin 1s infinite linear;">↻</span><span>Đang mở trình duyệt ${provider === 'google' ? 'Google' : 'GitHub'}...</span>`;
    }

    try {
      const res = await DesktopBridge.authSignInOAuth(provider);
      if (res && res.success) {
        if (res.session) {
          // Instant demo/test session
          this.authSession = res.session;
          this.renderUserWidget();
          this.closeActiveModal();
          this.showToast(res.message, "success");
          return;
        }

        if (res.listening) {
          if (btn) {
            btn.innerHTML = `<span style="display:inline-block; animation:spin 1s infinite linear;">↻</span><span>Đang chờ đăng nhập trên trình duyệt...</span>`;
          }
          this.showToast(res.message, "info");

          // Start polling loop (every 1.5s, max 80 iterations = 120s)
          let attempts = 0;
          if (this._oauthPollInterval) clearInterval(this._oauthPollInterval);
          this._oauthPollInterval = setInterval(async () => {
            attempts++;
            if (attempts > 80) {
              clearInterval(this._oauthPollInterval);
              this._oauthPollInterval = null;
              if (btn) {
                btn.disabled = false;
                btn.style.opacity = "1";
                btn.innerHTML = origHtml;
              }
              this.showToast("Hết thời gian chờ xác thực OAuth. Vui lòng thử lại.", "warning");
              return;
            }

            try {
              const status = await DesktopBridge.authCheckOAuthStatus();
              if (status && status.success && status.session) {
                clearInterval(this._oauthPollInterval);
                this._oauthPollInterval = null;
                this.authSession = status.session;
                this.renderUserWidget();
                this.closeActiveModal();
                this.showToast(status.message || `Đăng nhập thành công! Chào mừng ${status.session.user?.full_name || 'bạn'}.`, "success");
              } else if (status && status.success === false && !status.pending) {
                clearInterval(this._oauthPollInterval);
                this._oauthPollInterval = null;
                if (btn) {
                  btn.disabled = false;
                  btn.style.opacity = "1";
                  btn.innerHTML = origHtml;
                }
                this.openAuthModal("signin", status.message || "Xác thực không thành công.");
              }
            } catch (e) {
              // Ignore interim poll errors
            }
          }, 1500);
        }
      } else {
        if (btn) {
          btn.disabled = false;
          btn.style.opacity = "1";
          btn.innerHTML = origHtml;
        }
        this.openAuthModal("signin", res ? res.message : "Đăng nhập OAuth không thành công.");
      }
    } catch (err) {
      if (btn) {
        btn.disabled = false;
        btn.style.opacity = "1";
        btn.innerHTML = origHtml;
      }
      this.openAuthModal("signin", "Lỗi kết nối OAuth: " + err.message);
    }
  },

  async handleSignIn(email, password) {
    if (!email || !password) {
      this.openAuthModal("signin", "Vui lòng nhập đầy đủ Email và Mật khẩu.");
      return;
    }
    const btn = document.getElementById("btn-submit-signin");
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span style="animation:spin 1s infinite linear;">↻</span><span>Đang xác thực...</span>`;
    }

    try {
      const res = await DesktopBridge.authSignIn({ email, password });
      if (res && res.success) {
        this.authSession = res.session;
        this.renderUserWidget();
        this.closeActiveModal();
        this.showToast(res.message, "success");
      } else {
        this.openAuthModal("signin", res ? res.message : "Đăng nhập không thành công.");
      }
    } catch (err) {
      this.openAuthModal("signin", "Lỗi kết nối: " + err.message);
    }
  },

  async handleSignUp(email, password, fullName) {
    if (!email || !password) {
      this.openAuthModal("signup", "Vui lòng điền Email và Mật khẩu.");
      return;
    }
    const btn = document.getElementById("btn-submit-signup");
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span style="animation:spin 1s infinite linear;">↻</span><span>Đang tạo tài khoản...</span>`;
    }

    try {
      const res = await DesktopBridge.authSignUp({ email, password, full_name: fullName });
      if (res && res.success) {
        if (res.session) {
          this.authSession = res.session;
          this.renderUserWidget();
          this.closeActiveModal();
          this.showToast(res.message, "success");
        } else if (res.requires_login) {
          this.openAuthModal("signin", "");
          const emailInput = document.getElementById("auth-signin-email");
          if (emailInput) emailInput.value = email;
          this.showToast(res.message, "info");
        } else {
          this.closeActiveModal();
          this.showToast(res.message, "success");
        }
      } else {
        this.openAuthModal("signup", res ? res.message : "Đăng ký không thành công.");
      }
    } catch (err) {
      this.openAuthModal("signup", "Lỗi: " + err.message);
    }
  },

  async handleSignOut() {
    try {
      const res = await DesktopBridge.authSignOut();
      this.authSession = { authenticated: false, user: null };
      this.renderUserWidget();
      this.showToast(res ? res.message : "Đã đăng xuất tài khoản an toàn.", "info");
    } catch (err) {
      this.showToast("Lỗi đăng xuất: " + err.message, "error");
    }
  },

  async handleSaveSupabaseConfig(url, anonKey, secretKey) {
    const btn = document.getElementById("btn-save-supabase-config");
    if (btn) btn.disabled = true;

    try {
      const res = await DesktopBridge.authSaveConfig({
        supabase_url: url,
        anon_key: anonKey,
        service_secret_key: secretKey
      });
      if (res && res.success) {
        this.supabaseConfig = res.config;
        this.showToast(res.message, "success");
        this.openAuthModal("config");
      } else {
        this.showToast(res ? res.message : "Lỗi lưu cấu hình.", "error");
      }
    } catch (err) {
      this.showToast("Lỗi lưu cấu hình: " + err.message, "error");
    }
  },

  switchWorkspace(workspace) {
    this.activeWorkspace = workspace;
    document.querySelectorAll(".nav-link").forEach(link => link.classList.remove("active"));
    document.querySelector(`.nav-link[data-nav='${workspace}']`)?.classList.add("active");

    const breadcrumb = document.getElementById("breadcrumb-current");
    const orgBanner = document.getElementById("org-banner-container");
    const filterBar = document.getElementById("catalog-filter-bar");
    const bentoGrid = document.getElementById("skills-bento-grid");
    const linearList = document.getElementById("skills-linear-list");
    const guideContainer = document.getElementById("guide-container");
    const studioContainer = document.getElementById("studio-container");
    const communityContainer = document.getElementById("community-container");
    const profileContainer = document.getElementById("profile-container");

    // Hide all view containers
    bentoGrid.style.display = "none";
    linearList.style.display = "none";
    if (guideContainer) guideContainer.style.display = "none";
    studioContainer.style.display = "none";
    communityContainer.style.display = "none";
    if (profileContainer) profileContainer.style.display = "none";

    if (workspace === "library" || workspace === "installed") {
      filterBar.style.display = "flex";
      breadcrumb.innerText = (workspace === "library") ? "Kho Kỹ Năng (Skill-AI Suite)" : "Kỹ Năng Đã Kích Hoạt";
      
      // Render or show org banner
      if (workspace === "library") {
        orgBanner.style.display = "block";
        this.renderOrgBanner();
      } else {
        orgBanner.style.display = "none";
      }

      if (this.activeViewMode === "bento") {
        bentoGrid.style.display = "grid";
      } else {
        linearList.style.display = "flex";
      }
      this.applyFilters();
    } else if (workspace === "guide") {
      orgBanner.style.display = "none";
      filterBar.style.display = "none";
      breadcrumb.innerText = "Cẩm Nang Sử Dụng A-Z";
      if (guideContainer) {
        guideContainer.style.display = "block";
        guideContainer.innerHTML = UIComponents.renderGuideView();
      }
    } else if (workspace === "studio") {
      orgBanner.style.display = "none";
      filterBar.style.display = "none";
      breadcrumb.innerText = "Xưởng Chế Tác Kỹ Năng";
      studioContainer.style.display = "block";
      this.renderStudioView();
    } else if (workspace === "community") {
      orgBanner.style.display = "none";
      filterBar.style.display = "none";
      breadcrumb.innerText = "Trung Tâm Đám Mây Cộng Đồng (Supabase RLS)";
      communityContainer.style.display = "block";
      if (!this.communitySchema) {
        this.renderCommunityView();
        this.loadCommunitySchema().then(() => this.renderCommunityView());
      } else {
        this.renderCommunityView();
      }
    } else if (workspace === "profile") {
      orgBanner.style.display = "none";
      filterBar.style.display = "none";
      breadcrumb.innerText = "Hồ Sơ Lập Trình Viên AI & Portfolio";
      if (profileContainer) {
        profileContainer.style.display = "block";
        this.renderProfileView();
      }
    }
  },

  async renderProfileView() {
    const container = document.getElementById("profile-container");
    if (!container) return;

    let stats = {
      installed_count: this.skills.filter(s => s.installed_targets && s.installed_targets.length > 0).length,
      total_skills: this.skills.length,
      favorites_count: this.skills.filter(s => s.is_favorite).length,
      contributed_count: 1,
      installed_skills: [],
      favorite_skills: [],
      contributed_skills: []
    };

    try {
      const statsRes = await DesktopBridge.authGetUserStats();
      if (statsRes && statsRes.success) {
        stats = { ...stats, ...statsRes };
      }
    } catch (err) {
      console.warn("User stats fetch warning:", err);
    }

    container.innerHTML = UIComponents.renderProfileView(this.authSession, stats);

    // 1. Preset avatar picker clicks
    container.querySelectorAll(".preset-avatar-option").forEach(opt => {
      opt.addEventListener("click", () => {
        container.querySelectorAll(".preset-avatar-option").forEach(o => o.classList.remove("selected"));
        opt.classList.add("selected");
        const avatarUrl = opt.getAttribute("data-avatar-url");
        const inputUrl = document.getElementById("profile-edit-avatar-url");
        if (inputUrl) inputUrl.value = avatarUrl;
      });
    });

    // 2. Save profile event
    document.getElementById("btn-save-profile")?.addEventListener("click", async () => {
      const btn = document.getElementById("btn-save-profile");
      const statusEl = document.getElementById("profile-save-status");
      const name = document.getElementById("profile-edit-name")?.value.trim();
      const bio = document.getElementById("profile-edit-bio")?.value.trim();
      const avatarUrl = document.getElementById("profile-edit-avatar-url")?.value.trim();

      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<span>Đang lưu...</span>`;
      }

      try {
        const res = await DesktopBridge.authUpdateProfile({
          full_name: name,
          bio: bio,
          avatar_url: avatarUrl
        });

        if (res && res.success) {
          if (res.session) {
            this.authSession = res.session;
          }
          this.renderUserWidget();
          this.showToast("✓ Cập nhật hồ sơ cá nhân thành công!", "success");
          if (statusEl) {
            statusEl.innerText = "✓ Đã lưu thay đổi vào hệ thống";
            setTimeout(() => { if (statusEl) statusEl.innerText = ""; }, 3000);
          }
          await this.renderProfileView();
        } else {
          this.showToast(res ? res.message : "Cập nhật thất bại.", "error");
        }
      } catch (err) {
        this.showToast("Lỗi lưu hồ sơ: " + err.message, "error");
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = `${Icons.check} <span>Lưu Thay Đổi Hồ Sơ</span>`;
        }
      }
    });

    // 3. Copy Token in Profile
    document.getElementById("btn-profile-copy-token")?.addEventListener("click", () => {
      this.copyUserAccessToken();
    });

    // 4. Signout in Profile
    document.getElementById("btn-profile-signout")?.addEventListener("click", async () => {
      await this.handleSignOut();
      await this.renderProfileView();
    });

    // 5. Open Studio from Profile
    document.getElementById("btn-profile-open-studio")?.addEventListener("click", () => {
      this.switchWorkspace("studio");
    });

    // 6. Guest buttons
    document.getElementById("btn-profile-guest-login")?.addEventListener("click", () => {
      this.openAuthModal("signin");
    });

    document.getElementById("btn-profile-guest-github")?.addEventListener("click", async () => {
      await this.handleSocialLogin("github");
      await this.renderProfileView();
    });
  },

  renderOrgBanner() {
    const orgBanner = document.getElementById("org-banner-container");
    if (!orgBanner) return;
    const targetSkills = this.activeSource === "all" 
      ? this.skills 
      : this.skills.filter(s => (s.source_group || "skill_ai") === this.activeSource);
    const count = targetSkills.length;
    const newCount = targetSkills.filter(s => !s.installed_targets || s.installed_targets.length === 0).length;
    const updateCount = targetSkills.filter(s => s.has_update).length;

    orgBanner.innerHTML = UIComponents.renderOrgBanner(count, 26, this.activeSource, newCount, updateCount);
    document.getElementById("btn-batch-install-all")?.addEventListener("click", () => this.handleBatchInstallAll());
    document.getElementById("btn-batch-review-updates")?.addEventListener("click", () => this.handleReviewFirstUpdate());
    document.getElementById("btn-trigger-quick-help")?.addEventListener("click", () => this.openQuickHelpModal());
    document.getElementById("btn-toggle-onboarding")?.addEventListener("click", () => this.toggleOnboarding());
    document.getElementById("btn-open-guide-link")?.addEventListener("click", () => this.switchWorkspace("guide"));

    // Hero Quick-Start Goal Action Tiles (v6.0 Beginner-First Hub)
    document.getElementById("hero-goal-ui")?.addEventListener("click", () => {
      this.activeCategory = "ui_ux";
      document.querySelectorAll(".filter-chip").forEach(c => {
        c.classList.toggle("active", c.getAttribute("data-cat") === "ui_ux");
      });
      this.applyFilters();
      const targetSkill = this.skills.find(s => s.id === "ui-ux-design-master");
      if (targetSkill) {
        this.openQuickTryout(targetSkill.id);
      }
    });

    document.getElementById("hero-goal-plan")?.addEventListener("click", () => {
      this.activeCategory = "plan_debug";
      document.querySelectorAll(".filter-chip").forEach(c => {
        c.classList.toggle("active", c.getAttribute("data-cat") === "plan_debug");
      });
      this.applyFilters();
      const targetSkill = this.skills.find(s => s.id === "strict-architect-coder");
      if (targetSkill) {
        this.openQuickTryout(targetSkill.id);
      }
    });

    document.getElementById("hero-goal-all")?.addEventListener("click", () => {
      this.handleBatchInstallAll();
    });
  },

  openQuickTryout(skillId) {
    const skill = this.skills.find(s => s.id === skillId) || this.skills[0];
    if (!skill) return;
    const root = document.getElementById("modal-root");
    if (!root) return;
    root.innerHTML = UIComponents.renderQuickTryoutModal(skill);
  },

  async copyTryoutPrompt() {
    const contentEl = document.getElementById("tryout-prompt-content");
    const btnText = document.getElementById("btn-copy-tryout-text");
    const promptText = contentEl ? contentEl.innerText.trim() : "";
    if (!promptText) return;

    try {
      await navigator.clipboard.writeText(promptText);
      if (btnText) btnText.innerText = "✓ Đã Chép! Dán Vào Khung Chat AI Của Bạn";
      this.showToast("✓ Đã sao chép câu lệnh! Dán (Ctrl+V) vào AI của bạn ngay.", "success");
      setTimeout(() => {
        if (btnText) btnText.innerText = "Sao Chép Câu Lệnh Này";
      }, 2500);
    } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = promptText;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      if (btnText) btnText.innerText = "✓ Đã Chép!";
      this.showToast("✓ Đã sao chép câu lệnh!", "success");
      setTimeout(() => {
        if (btnText) btnText.innerText = "Sao Chép Câu Lệnh Này";
      }, 2500);
    }
  },

  openQuickHelpModal() {
    const root = document.getElementById("modal-root");
    if (!root) return;
    root.innerHTML = UIComponents.renderQuickHelpModal();
  },

  async checkAppUpdates(isManual = false) {
    if (isManual) {
      this.showToast("Đang kiểm tra bản cập nhật mới từ máy chủ...", "info");
    }
    try {
      const res = await DesktopBridge.updaterCheck();
      if (res && res.success) {
        this.updateData = res;
        const topbarBadge = document.getElementById("btn-topbar-update");
        const topbarLabel = document.getElementById("topbar-update-label");

        // Rebuild notifications array
        this.notifications = [];

        // 1. Check for App Software Update
        if (res.has_app_update) {
          if (topbarBadge) {
            topbarBadge.classList.remove("hidden");
            if (topbarLabel) topbarLabel.innerText = `Bản mới v${res.latest_version}`;
          }
          this.notifications.push({
            id: `app-update-${res.latest_version}`,
            type: "app",
            title: `Bản cập nhật phần mềm v${res.latest_version}`,
            desc: res.release_title || "Có bản phát hành phần mềm mới với các tính năng cải tiến.",
            time: "Mới phát hành",
            unread: true,
            action: "open-update-modal",
            actionLabel: "Xem chi tiết"
          });
          if (isManual) {
            this.openUpdateModal(res);
          } else {
            this.showToast(`🚀 Đã có phiên bản mới v${res.latest_version}! Bấm để xem chi tiết.`, "info");
          }
        } else {
          if (topbarBadge) topbarBadge.classList.add("hidden");
          if (isManual) {
            this.openUpdateModal(res);
          }
        }

        // 2. Check for Minor Skills / Prompts Update
        if (res.has_skills_update) {
          this.notifications.push({
            id: `skills-update-${res.update_signature}`,
            type: "skills",
            title: "Có kỹ năng & câu lệnh mới",
            desc: res.skills_summary || "Phát hiện có kỹ năng mới từ Addy Osmani (Google) sẵn sàng nạp.",
            time: "Vừa kiểm tra",
            unread: true,
            action: "sync-skills",
            actionLabel: "Đồng bộ ngay (2s)"
          });

          // Check if user has muted minor banners or already dismissed this signature
          const isMuted = (localStorage.getItem("abyssalskillsd-mute-minor-banners") ?? localStorage.getItem("skillforge-mute-minor-banners")) === "true";
          const dismissedSig = localStorage.getItem("abyssalskillsd-dismissed-banner-sig") || localStorage.getItem("skillforge-dismissed-banner-sig");

          if (!isMuted && dismissedSig !== res.update_signature) {
            this.renderSkillsBanner(res);
          }
        } else {
          const bannerMount = document.getElementById("skills-notification-banner-mount");
          if (bannerMount && !res.has_skills_update) {
            bannerMount.innerHTML = "";
          }
        }

        this.updateNotificationBadge();
      } else if (isManual) {
        this.showToast("Không thể kết nối máy chủ kiểm tra cập nhật.", "warning");
      }
    } catch (e) {
      console.warn("Auto-update check error:", e);
      if (isManual) {
        this.showToast("Lỗi khi kiểm tra cập nhật. Vui lòng thử lại sau.", "error");
      }
    }
  },

  renderSkillsBanner(data) {
    const mount = document.getElementById("skills-notification-banner-mount");
    if (!mount) return;
    mount.innerHTML = UIComponents.renderSkillsUpdateBanner(
      data.skills_summary,
      data.update_signature,
      data.new_skills_count || 3
    );

    document.getElementById("btn-banner-sync-skills")?.addEventListener("click", async () => {
      await this.handleSyncFromBanner();
    });

    document.getElementById("btn-banner-dismiss")?.addEventListener("click", () => {
      this.dismissSkillsUpdateBanner(data.update_signature);
    });
  },

  dismissSkillsUpdateBanner(sig) {
    if (sig) {
      localStorage.setItem("abyssalskillsd-dismissed-banner-sig", sig);
    }
    const mount = document.getElementById("skills-notification-banner-mount");
    if (mount) {
      const banner = document.getElementById("skills-update-banner");
      if (banner) {
        banner.style.opacity = "0";
        banner.style.transform = "translateY(-6px)";
        banner.style.transition = "all 0.2s ease";
        setTimeout(() => {
          mount.innerHTML = "";
        }, 200);
      } else {
        mount.innerHTML = "";
      }
    }
    this.showToast("Đã ẩn thông báo cập nhật này.", "info");
  },

  async handleSyncFromBanner() {
    const btn = document.getElementById("btn-banner-sync-skills");
    const btnText = document.getElementById("btn-banner-sync-text");
    if (btn) btn.disabled = true;
    if (btnText) btnText.innerText = "Đang đồng bộ...";

    try {
      const res = await DesktopBridge.updaterSyncSkills();
      if (res && res.success) {
        if (btnText) btnText.innerText = "✓ Hoàn Tất";
        this.showToast(res.message || "Đồng bộ kỹ năng thành công!", "success");
        await this.loadSkills();
        setTimeout(() => {
          const mount = document.getElementById("skills-notification-banner-mount");
          if (mount) mount.innerHTML = "";
          this.notifications = this.notifications.filter(n => n.type !== "skills");
          this.updateNotificationBadge();
        }, 1200);
      } else {
        if (btnText) btnText.innerText = "Thử lại";
        if (btn) btn.disabled = false;
        this.showToast(res?.message || "Lỗi khi đồng bộ kỹ năng.", "error");
      }
    } catch (e) {
      if (btn) btn.disabled = false;
      this.showToast("Lỗi đồng bộ: " + e.message, "error");
    }
  },

  updateNotificationBadge() {
    const dot = document.getElementById("notification-unread-dot");
    if (!dot) return;
    const hasUnread = this.notifications.some(n => n.unread);
    if (hasUnread) {
      dot.classList.remove("hidden");
    } else {
      dot.classList.add("hidden");
    }
  },

  toggleNotificationTray() {
    if (this.isNotificationTrayOpen) {
      this.closeNotificationTray();
    } else {
      this.openNotificationTray();
    }
  },

  openNotificationTray() {
    const container = document.getElementById("notification-dropdown-container");
    if (!container) return;
    this.isNotificationTrayOpen = true;
    container.innerHTML = UIComponents.renderNotificationDropdown(this.notifications);

    // Bind item action buttons
    container.querySelectorAll(".notif-action-btn").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        const action = e.currentTarget.getAttribute("data-action");
        if (action === "sync-skills") {
          this.closeNotificationTray();
          await this.handleSyncSkills();
        } else if (action === "open-update-modal") {
          this.closeNotificationTray();
          this.openUpdateModal(this.updateData);
        }
      });
    });

    // Clear all
    document.getElementById("btn-clear-all-notifications")?.addEventListener("click", () => {
      this.clearAllNotifications();
    });

    // Full update modal
    document.getElementById("btn-open-full-update-modal")?.addEventListener("click", () => {
      this.closeNotificationTray();
      this.openUpdateModal(this.updateData);
    });

    // Preference checkbox toggle
    document.getElementById("pref-toggle-minor-banners")?.addEventListener("change", (e) => {
      const isChecked = e.target.checked;
      localStorage.setItem("abyssalskillsd-mute-minor-banners", isChecked ? "false" : "true");
      if (!isChecked) {
        const mount = document.getElementById("skills-notification-banner-mount");
        if (mount) mount.innerHTML = "";
      }
      this.showToast(isChecked ? "Đã bật thanh gợi ý cập nhật nhỏ." : "Đã tắt thanh gợi ý cập nhật nhỏ.", "info");
    });
  },

  closeNotificationTray() {
    const container = document.getElementById("notification-dropdown-container");
    if (container) container.innerHTML = "";
    this.isNotificationTrayOpen = false;
  },

  clearAllNotifications() {
    this.notifications.forEach(n => { n.unread = false; });
    this.updateNotificationBadge();
    const container = document.getElementById("notification-dropdown-container");
    if (container && this.isNotificationTrayOpen) {
      container.innerHTML = UIComponents.renderNotificationDropdown(this.notifications);
    }
    this.showToast("Đã đánh dấu tất cả thông báo là đã đọc.", "info");
  },

  openUpdateModal(data) {
    const root = document.getElementById("modal-root");
    if (!root) return;
    root.innerHTML = UIComponents.renderUpdateModal(data || this.updateData || {});
    this.bindUpdateModalEvents();
  },

  bindUpdateModalEvents() {
    document.getElementById("btn-action-sync-skills")?.addEventListener("click", async () => {
      await this.handleSyncSkills();
    });

    document.getElementById("btn-recheck-updates")?.addEventListener("click", async () => {
      await this.checkAppUpdates(true);
    });
  },

  async handleSyncSkills() {
    const btn = document.getElementById("btn-action-sync-skills");
    const btnText = document.getElementById("btn-sync-skills-text");
    const spinner = document.getElementById("sync-spinner");
    const progressBox = document.getElementById("update-progress-container");
    const progressFill = document.getElementById("update-progress-fill");
    const progressMsg = document.getElementById("update-progress-msg");

    if (btn) btn.disabled = true;
    if (spinner) spinner.style.display = "inline";
    if (btnText) btnText.innerText = "Đang đồng bộ...";
    if (progressBox) progressBox.style.display = "block";
    if (progressFill) progressFill.style.width = "40%";
    if (progressMsg) progressMsg.innerText = "Đang kết nối GitHub và tải các kỹ năng mới...";

    try {
      const res = await DesktopBridge.updaterSyncSkills();
      if (progressFill) progressFill.style.width = "100%";
      if (res && res.success) {
        if (progressMsg) progressMsg.innerText = res.message || "Đồng bộ thành công!";
        if (btnText) btnText.innerText = "✓ Hoàn Tất Đồng Bộ";
        this.showToast(res.message || "Đồng bộ kỹ năng thành công!", "success");
        await this.loadSkills();
        setTimeout(() => {
          this.closeActiveModal();
          this.notifications = this.notifications.filter(n => n.type !== "skills");
          this.updateNotificationBadge();
          const bannerMount = document.getElementById("skills-notification-banner-mount");
          if (bannerMount) bannerMount.innerHTML = "";
        }, 1800);
      } else {
        if (progressMsg) progressMsg.innerText = res?.message || "Đồng bộ thất bại.";
        if (btnText) btnText.innerText = "Thử lại";
        if (btn) btn.disabled = false;
        this.showToast(res?.message || "Lỗi khi đồng bộ kỹ năng.", "error");
      }
    } catch (e) {
      if (progressMsg) progressMsg.innerText = "Lỗi kết nối ngoại lệ.";
      if (btn) btn.disabled = false;
      this.showToast("Lỗi khi đồng bộ: " + e.message, "error");
    }
  },

  toggleOnboarding() {
    this.isOnboardingCollapsed = !this.isOnboardingCollapsed;
    localStorage.setItem("abyssalskillsd-onboarding-collapsed", this.isOnboardingCollapsed ? "true" : "false");
    this.renderOrgBanner();
  },

  applyFilters() {
    if (this.activeWorkspace !== "library" && this.activeWorkspace !== "installed") return;

    let result = [...this.skills];

    if (this.activeWorkspace === "installed") {
      result = result.filter(s => s.installed_targets && s.installed_targets.length > 0);
    }

    if (this.activeSource && this.activeSource !== "all") {
      result = result.filter(s => (s.source_group || "skill_ai") === this.activeSource);
    }

    if (this.activeCategory !== "all") {
      const active = this.activeCategory.toLowerCase();
      result = result.filter(s => {
        const cat = (s.category || "").toLowerCase();
        const grp = (s.use_case_group || "").toLowerCase();
        return cat === active || grp === active;
      });
    }

    if (this.searchQuery.trim()) {
      const q = this.searchQuery.toLowerCase().trim();
      result = result.filter(s => {
        const title = (s.display_title || s.name || "").toLowerCase();
        const desc = (s.description || "").toLowerCase();
        const cat = (s.category || "").toLowerCase();
        const tags = (s.tags || []).join(" ").toLowerCase();
        const body = (s.skill_content || "").toLowerCase();
        return title.includes(q) || desc.includes(q) || cat.includes(q) || tags.includes(q) || body.includes(q);
      });
    }

    this.filteredSkills = result;
    this.renderSkills();
  },

  renderSkills() {
    const bentoGrid = document.getElementById("skills-bento-grid");
    const linearList = document.getElementById("skills-linear-list");

    if (this.filteredSkills.length === 0) {
      const emptyHtml = UIComponents.renderEmptyIllustration();
      if (bentoGrid) bentoGrid.innerHTML = emptyHtml;
      if (linearList) linearList.innerHTML = emptyHtml;
      return;
    }

    if (bentoGrid) {
      bentoGrid.innerHTML = this.filteredSkills.map(s => 
        UIComponents.renderBentoCard(s, s.id === this.selectedSkillId)
      ).join("");
    }

    if (linearList) {
      linearList.innerHTML = this.filteredSkills.map(s => 
        UIComponents.renderLinearRow(s, s.id === this.selectedSkillId)
      ).join("");
    }

    this.bindCardEvents();
  },

  bindCardEvents() {
    document.querySelectorAll(".bento-card, .linear-row").forEach(el => {
      el.addEventListener("click", () => {
        const id = el.getAttribute("data-id");
        this.selectSkill(id);
      });
    });

    document.querySelectorAll(".btn-card-open, .btn-card-pro-settings").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const id = btn.getAttribute("data-id");
        this.selectSkill(id, "pro_settings");
      });
    });

    document.querySelectorAll(".btn-card-tryout").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const id = btn.getAttribute("data-id");
        this.openQuickTryout(id);
      });
    });

    document.querySelectorAll(".btn-card-verify, .badge-ai-active").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const id = btn.getAttribute("data-id");
        if (id) this.openVerificationModal(id);
      });
    });

    document.querySelectorAll(".btn-copy-card").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const id = btn.getAttribute("data-id");
        this.copySkillPrompt(id);
      });
    });
  },

  selectSkill(skillId, initialDocId = "pro_settings") {
    this.selectedSkillId = skillId;
    this.activeDocId = initialDocId;

    document.querySelectorAll(".bento-card, .linear-row").forEach(el => {
      el.classList.toggle("selected", el.getAttribute("data-id") === skillId);
    });

    const skill = this.skills.find(s => s.id === skillId);
    if (!skill) return;

    const drawer = document.getElementById("inspector-drawer");
    if (drawer) {
      drawer.style.display = "flex";
      drawer.innerHTML = UIComponents.renderInspector(skill, this.activeDocId);
      this.bindInspectorEvents(skill);
    }
  },

  bindInspectorEvents(skill) {
    const drawer = document.getElementById("inspector-drawer");
    if (!drawer) return;

    drawer.querySelectorAll(".outline-item").forEach(item => {
      item.addEventListener("click", () => {
        const docId = item.getAttribute("data-doc");
        this.activeDocId = docId;
        drawer.innerHTML = UIComponents.renderInspector(skill, docId);
        this.bindInspectorEvents(skill);
      });
    });

    drawer.querySelectorAll(".btn-copy-prompt").forEach(btn => {
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const promptText = btn.getAttribute("data-prompt");
        if (promptText) {
          this.copyStarterPrompt(promptText, btn);
        }
      });
    });

    document.getElementById("btn-close-inspector")?.addEventListener("click", () => {
      this.closeInspector();
    });

    document.getElementById("btn-inspector-apply")?.addEventListener("click", () => {
      this.handleApplyInstall(skill.id);
    });

    drawer.querySelector(".btn-inspector-open-explorer")?.addEventListener("click", () => {
      this.handleOpenSkillFolder(skill.id);
    });

    drawer.querySelector(".btn-inspector-verify-ai")?.addEventListener("click", () => {
      this.openVerificationModal(skill.id);
    });

    drawer.querySelector(".btn-inspector-uninstall")?.addEventListener("click", () => {
      this.openUninstallModal(skill.id);
    });

    document.getElementById("btn-inspector-action-uninstall")?.addEventListener("click", () => {
      this.openUninstallModal(skill.id);
    });

    drawer.querySelectorAll(".btn-inspector-customize, .btn-inspector-action-customize").forEach(btn => {
      btn.addEventListener("click", () => {
        this.handleCustomizeInStudio(skill.id);
      });
    });

    document.getElementById("btn-inspector-copy-all")?.addEventListener("click", () => {
      this.copySkillPrompt(skill.id);
    });

    document.getElementById("btn-inspector-git-sync")?.addEventListener("click", (e) => {
      const repo = e.currentTarget.getAttribute("data-repo");
      if (repo) this.handleGitHubSync(repo);
    });

    // Pro Settings Panel: Custom Workspace & Target Sync
    document.getElementById("btn-apply-pro-workspace")?.addEventListener("click", async () => {
      const inputEl = document.getElementById("pro-custom-workspace-input");
      const customPath = inputEl ? inputEl.value.trim() : "";
      const btn = document.getElementById("btn-apply-pro-workspace");

      const targets = [];
      if (document.getElementById("pro-sw-cursor")?.checked) targets.push("cursor");
      if (document.getElementById("pro-sw-windsurf")?.checked) targets.push("windsurf");
      if (document.getElementById("pro-sw-claude")?.checked) targets.push("claude");
      if (document.getElementById("pro-sw-antigravity")?.checked) targets.push("antigravity");
      if (document.getElementById("pro-sw-copilot")?.checked) targets.push("copilot");
      if (customPath) targets.push("workspace");
      if (targets.length === 0) targets.push("workspace");

      if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<span>Đang lưu...</span>`;
      }

      try {
        const res = await DesktopBridge.installSkill({
          skill_id: skill.id,
          targets: targets,
          workspace_path: customPath || null,
          enable_always_on: true,
          with_graphify: false
        });

        if (res && res.success) {
          this.showToast(`✓ Đã cấu hình và lưu quy tắc cho "${skill.display_title || skill.name}"!`, "success");
          await this.loadSkills();
          this.selectSkill(skill.id, "pro_settings");
        } else {
          this.showToast(res ? res.message : "Cài đặt thất bại.", "error");
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = `${Icons.download} <span>Lưu & Đồng Bộ</span>`;
          }
        }
      } catch (err) {
        this.showToast("Lỗi cấu hình: " + err.message, "error");
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = `${Icons.download} <span>Lưu & Đồng Bộ</span>`;
        }
      }
    });
  },

  async copyStarterPrompt(promptText, btnElement) {
    try {
      await navigator.clipboard.writeText(promptText);
    } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = promptText;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    this.showToast("✓ Đã chép câu lệnh mẫu! Hãy dán vào khung chat AI.", "success");
    if (btnElement) {
      const origText = btnElement.innerHTML;
      btnElement.classList.add("copied");
      btnElement.innerHTML = `${Icons.check}<span>Đã chép!</span>`;
      setTimeout(() => {
        btnElement.classList.remove("copied");
        btnElement.innerHTML = origText;
      }, 2000);
    }
  },

  closeInspector() {
    const drawer = document.getElementById("inspector-drawer");
    if (drawer) drawer.style.display = "none";
    this.selectedSkillId = null;
    document.querySelectorAll(".bento-card, .linear-row").forEach(el => el.classList.remove("selected"));
  },

  openActivationModal(skill, targets = ["antigravity"], state = {}) {
    const root = document.getElementById("modal-root");
    if (!root) return;
    root.innerHTML = UIComponents.renderActivationModal(skill, targets, state);

    document.getElementById("btn-open-explorer-from-modal")?.addEventListener("click", (e) => {
      const id = e.currentTarget.getAttribute("data-id") || (skill ? skill.id : "");
      this.handleOpenSkillFolder(id);
    });

    document.getElementById("btn-copy-activation-prompt")?.addEventListener("click", (e) => {
      const prompt = e.currentTarget.getAttribute("data-prompt") || "";
      this.copyStarterPrompt(prompt, e.currentTarget);
    });
  },

  async openVerificationModal(skillId) {
    const skill = this.skills.find(s => s.id === skillId) || { id: skillId, name: skillId };
    try {
      const report = await DesktopBridge.verifySkillActive({ skill_id: skillId });
      const root = document.getElementById("modal-root");
      if (!root) return;
      root.innerHTML = UIComponents.renderVerificationModal(skill, report || {});

      root.querySelectorAll(".btn-open-target-dir, #btn-open-explorer-bottom").forEach(btn => {
        btn.addEventListener("click", (e) => {
          const target = e.currentTarget.getAttribute("data-target") || "antigravity";
          this.handleOpenSkillFolder(skillId, target);
        });
      });

      document.getElementById("btn-copy-verify-prompt")?.addEventListener("click", (e) => {
        const prompt = e.currentTarget.getAttribute("data-prompt") || "";
        this.copyStarterPrompt(prompt, e.currentTarget);
      });
    } catch (e) {
      this.showToast("Không thể tải thông tin kiểm chứng: " + e.message, "error");
    }
  },

  async handleOpenSkillFolder(skillId, target = "antigravity") {
    try {
      const res = await DesktopBridge.openSkillFolder({ skill_id: skillId, target: target });
      if (res && res.success) {
        this.showToast(res.message || "Đã mở thư mục trong Windows Explorer.", "info");
      } else {
        this.showToast(res ? res.message : "Chưa tìm thấy thư mục trên máy.", "warning");
      }
    } catch (e) {
      this.showToast("Lỗi mở thư mục: " + e.message, "error");
    }
  },

  async handleApplyInstall(skillId) {
    const skill = this.skills.find(s => s.id === skillId) || { id: skillId, name: skillId };
    const targets = [];
    if (document.getElementById("sw-antigravity")?.checked) targets.push("antigravity");
    if (document.getElementById("sw-claude")?.checked) targets.push("claude");
    if (document.getElementById("sw-cursor")?.checked) targets.push("cursor");
    if (document.getElementById("sw-windsurf")?.checked) targets.push("windsurf");
    if (document.getElementById("sw-copilot")?.checked) targets.push("copilot");
    if (document.getElementById("sw-workspace")?.checked) targets.push("workspace");
    if (targets.length === 0) targets.push("antigravity", "cursor");

    const enableAlwaysOn = document.getElementById("sw-always-on")?.checked ?? true;
    const withGraphify = document.getElementById("sw-graphify")?.checked ?? true;

    // 1. Launch Neural Stream Modal - Step 1: Packing Playbooks
    this.openActivationModal(skill, targets, {
      stepIndex: 1,
      progressPct: 28,
      isComplete: false
    });

    await new Promise(r => setTimeout(r, 380));

    // 2. Advance to Step 2: Injecting Rules
    this.openActivationModal(skill, targets, {
      stepIndex: 2,
      progressPct: 68,
      isComplete: false
    });

    try {
      const res = await DesktopBridge.installSkill({
        skill_id: skillId,
        targets: targets,
        enable_always_on: enableAlwaysOn,
        with_graphify: withGraphify
      });

      if (res && res.success) {
        await new Promise(r => setTimeout(r, 350));
        const verifyRes = await DesktopBridge.verifySkillActive({ skill_id: skillId });

        // 3. Step 3: Complete & Render Proof
        this.openActivationModal(skill, targets, {
          stepIndex: 3,
          progressPct: 100,
          isComplete: true,
          testPrompt: verifyRes ? verifyRes.test_prompt : null,
          verifiedData: verifyRes
        });

        await this.loadSkills();
        if (this.selectedSkillId === skillId) {
          this.selectSkill(skillId, this.activeDocId);
        }
      } else {
        this.closeActiveModal();
        this.showToast(res ? res.message : "Cài đặt thất bại.", "error");
      }
    } catch (err) {
      this.closeActiveModal();
      this.showToast("Lỗi cài đặt: " + err.message, "error");
    }
  },

  async handleBatchInstallAll(forceAll = false) {
    const targetSkills = this.activeSource === "all" 
      ? this.skills 
      : this.skills.filter(s => (s.source_group || "skill_ai") === this.activeSource);
    
    // Only install skills that are NEW (uninstalled)
    // Updated skills require user review in Diff Modal to protect personal edits!
    const newSkills = targetSkills.filter(s => !s.installed_targets || s.installed_targets.length === 0);
    const updateSkills = targetSkills.filter(s => s.has_update);

    if (newSkills.length === 0 && !forceAll) {
      if (updateSkills.length > 0) {
        this.showToast(`🛡️ Toàn bộ kỹ năng mới đã được kích hoạt. Có ${updateSkills.length} kỹ năng có bản cập nhật mới, vui lòng kiểm tra bảng so sánh trước khi ghi đè!`, "warning");
        this.openDiffReviewModal(updateSkills[0].id);
      } else {
        this.showToast("✓ Toàn bộ kỹ năng đều đang ở trạng thái mới nhất và đã được kích hoạt đầy đủ trên máy!", "success");
      }
      return;
    }

    const toInstall = forceAll ? targetSkills : newSkills;
    const count = toInstall.length;

    const collectiveSkill = {
      id: "batch-all",
      display_title: `Trọn Bộ ${count} Kỹ Năng Mới`,
      name: `Trọn Bộ ${count} Kỹ Năng Mới`,
      category: "Suite Chuyên Gia"
    };

    const targets = ["antigravity", "cursor", "claude"];

    // 1. Neural Stream Step 1
    this.openActivationModal(collectiveSkill, targets, {
      stepIndex: 1,
      progressPct: 30,
      isComplete: false
    });

    await new Promise(r => setTimeout(r, 450));

    // 2. Neural Stream Step 2
    this.openActivationModal(collectiveSkill, targets, {
      stepIndex: 2,
      progressPct: 70,
      isComplete: false
    });

    try {
      const payload = {
        targets: ["antigravity", "claude"],
        enable_always_on: true,
        with_graphify: true,
        workspace_path: this.activeWorkspaceProject,
        skill_ids: toInstall.map(s => s.id)
      };
      const res = await DesktopBridge.installAllSkills(payload);

      if (res && res.success) {
        await new Promise(r => setTimeout(r, 400));
        this.openActivationModal(collectiveSkill, targets, {
          stepIndex: 3,
          progressPct: 100,
          isComplete: true,
          testPrompt: "Hãy lập kế hoạch thiết kế và lập trình giao diện chuẩn /plan"
        });

        await this.loadSkills();
        await this.updateSystemStatus();
        this.showToast(`🎉 ${res.message}`, "success");
      } else {
        this.closeActiveModal();
        this.showToast(res ? res.message : "Có lỗi khi cài đặt kỹ năng mới.", "error");
      }
    } catch (e) {
      this.closeActiveModal();
      this.showToast("Lỗi batch install: " + e.message, "error");
    }
  },

  handleReviewFirstUpdate() {
    const targetSkills = this.activeSource === "all" 
      ? this.skills 
      : this.skills.filter(s => (s.source_group || "skill_ai") === this.activeSource);
    const updateSkill = targetSkills.find(s => s.has_update) || this.skills.find(s => s.has_update);
    if (updateSkill) {
      this.openDiffReviewModal(updateSkill.id);
    } else {
      this.showToast("Không có kỹ năng nào cần cập nhật.", "info");
    }
  },

  async openDiffReviewModal(skillId) {
    const root = document.getElementById("modal-root");
    if (!root) return;
    try {
      const diff = await DesktopBridge.getSkillDiff(skillId, this.activeWorkspaceProject);
      root.innerHTML = UIComponents.renderDiffReviewModal(diff);

      // Button Keep Local
      document.getElementById("btn-diff-keep-local")?.addEventListener("click", () => {
        this.closeActiveModal();
        this.showToast("🛡️ Đã giữ lại bản tùy biến của bạn trên máy (không thay đổi).", "info");
      });

      // Button Accept Update
      document.getElementById("btn-diff-apply-update")?.addEventListener("click", async () => {
        const btn = document.getElementById("btn-diff-apply-update");
        if (btn) {
          btn.disabled = true;
          btn.innerHTML = `<span>Đang cập nhật & sao lưu .bak...</span>`;
        }
        try {
          const installPayload = {
            skill_id: skillId,
            targets: (diff.targets && diff.targets.length > 0) ? diff.targets : ["antigravity"],
            workspace_path: this.activeWorkspaceProject,
            enable_always_on: true,
            with_graphify: false
          };
          const res = await DesktopBridge.installSkill(installPayload);
          if (res && res.success) {
            this.closeActiveModal();
            this.showToast(`✓ Đã cập nhật thành công kỹ năng "${diff.display_title}"! (Bản cũ đã được lưu tại SKILL.md.bak)`, "success");
            await this.loadSkills();
            await this.updateSystemStatus();
          } else {
            this.showToast(res ? res.message : "Lỗi khi cập nhật kỹ năng.", "error");
            if (btn) btn.disabled = false;
          }
        } catch (e) {
          this.showToast("Lỗi cập nhật: " + e.message, "error");
          if (btn) btn.disabled = false;
        }
      });
    } catch (err) {
      this.showToast("Lỗi mở so sánh kỹ năng: " + err.message, "error");
    }
  },

  async copySkillPrompt(skillId) {
    const skill = this.skills.find(s => s.id === skillId);
    if (!skill) return;

    let text = `# ${skill.display_title || skill.name}\n\n${skill.skill_content}`;
    if (skill.references && skill.references.length > 0) {
      text += `\n\n## Sổ tay tham khảo:\n`;
      skill.references.forEach(r => {
        text += `\n### ${r.title}\n${r.content}\n`;
      });
    }

    try {
      await navigator.clipboard.writeText(text);
      this.showToast("Đã sao chép câu lệnh chỉ dẫn vào bộ nhớ tạm!", "success");
    } catch (e) {
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      this.showToast("Đã sao chép câu lệnh chỉ dẫn!", "success");
    }
  },

  studioPresets: {
    "spec-driven": {
      title: "Spec-Driven Development Master",
      id: "spec-driven-development",
      category: "Architecture & Code",
      desc: "Bắt buộc mô hình AI viết bản đặc tả kỹ thuật (Spec / PRD) và làm rõ các biên giới kiến trúc trước khi bắt đầu viết mã.",
      content: `---
name: spec-driven-development
description: Use when building new features, refactoring non-trivial components, or clarifying user requirements before writing code.
phase: define-and-plan
---

# Spec-Driven Development Standard (Addy Osmani Architecture)

> **Luật cốt lõi:** Không bao giờ gõ một dòng mã nguồn nào trước khi người dùng đồng thuận bản đặc tả kỹ thuật!

## 1. Quy Trình 4 Bước Của Senior Engineer
1. **Làm rõ mục tiêu (Intent & Scope):** Đặt tối đa 2 câu hỏi làm rõ vấn đề có kèm sẵn phương án gợi ý \`(Recommended)\`.
2. **Ma trận trạng thái UI (5-State UI Matrix):**
   - *Idle (Chờ)*
   - *Loading / Submitting (Đang tải)*
   - *Success (Thành công)*
   - *Empty State (Trống rỗng)*
   - *Error Recovery (Xử lý lỗi)*
3. **Danh sách tệp tin nằm trong vùng ảnh hưởng (File Whitelist):**
   - Tuyệt đối không chạm vào các tệp ngoài phạm vi đã cam kết.
4. **Kế hoạch xác minh (Verification Strategy):**
   - Viết rõ các lệnh kiểm thử tự động (\`pytest\`, \`vitest\`, \`playwright\`) để nghiệm thu.

## 2. Bảng Chống Ngụy Biện (Anti-Rationalization Table)
| Lời ngụy biện thường gặp của AI | Hành động bắt buộc phải thực hiện |
| :--- | :--- |
| *"Tính năng này đơn giản, để tôi code luôn cho nhanh"* | **CHẶN LẠI:** Vẫn phải viết tối thiểu 3 gạch đầu dòng về phạm vi và tệp sửa đổi. |
| *"Người dùng đang vội, không cần hỏi thêm đâu"* | **CHẶN LẠI:** Đưa ra phương án mặc định \`(Recommended)\` và xin xác nhận 1 chạm. |
| *"Viết spec sau khi code xong cũng được"* | **CHẶN LẠI:** Không có spec thì không có chuẩn mực để nghiệm thu kết quả. |

## 3. Cổng Nghiệm Thu (Quality Gate)
- [ ] Khách hàng / Người dùng đã duyệt bản kế hoạch.
- [ ] Danh sách tệp tin không làm ảnh hưởng đến các God Node của hệ thống.`
    },
    "test-driven": {
      title: "Test-Driven Development (TDD) Artisan",
      id: "test-driven-development",
      category: "Testing & QA",
      desc: "Áp dụng vòng lặp Red-Green-Refactor nghiêm ngặt: Viết bài kiểm thử tự động thất bại trước khi viết mã nguồn thực tế.",
      content: `---
name: test-driven-development
description: Use when implementing complex business logic, calculation engines, API endpoints, or bug fixes.
phase: build-and-verify
---

# Test-Driven Development (TDD) Senior Engineering Standard

> **Quy tắc vàng:** Chỉ viết mã nguồn mới khi và chỉ khi có một bài kiểm thử tự động đang bị THẤT BẠI (Red Stage)!

## 1. Vòng Lặp 3 Bước Red-Green-Refactor
1. **Red (Đỏ):** Viết một unit test hoặc integration test mô tả chính xác yêu cầu mới. Chạy bài test và quan sát nó thất bại đúng như dự kiến.
2. **Green (Xanh):** Viết lượng code tối thiểu cần thiết để bài test chuyển sang màu xanh (PASS). Không viết thừa!
3. **Refactor (Tối ưu):** Dọn dẹp mã nguồn, tối ưu hiệu năng và loại bỏ trùng lặp mà không làm bài test bị đỏ.

## 2. Bảng Chống Ngụy Biện (Anti-Rationalization Table)
| Lời ngụy biện của AI | Hành động bắt buộc |
| :--- | :--- |
| *"Code xong tôi sẽ viết test bù sau"* | **CHẶN LẠI:** Test viết sau thường bị thiên kiến xác nhận, chỉ test case đúng và bỏ lọt lỗi biên. |
| *"Tính năng này khó viết test tự động lắm"* | **CHẶN LẠI:** Chia nhỏ thành các hàm thuần túy (pure functions) dễ kiểm thử. |
| *"Test đang pass rồi, không cần refactor nữa"* | **CHẶN LẠI:** Dọn sạch technical debt ngay khi test đang bảo vệ an toàn. |

## 3. Tiêu Chuẩn Nghiệm Thu
- [ ] Chạy lệnh kiểm thử tự động đạt 100% exit code 0.
- [ ] Không có assertion giả định (\`assert True\`).`
    },
    "code-review": {
      title: "5-Axis Code Review & Quality Gate",
      id: "code-review-and-quality",
      category: "Review & Security",
      desc: "Kiểm tra mã nguồn trên 5 trục nghiêm ngặt: Tính đúng đắn, Kiến trúc, Bảo mật, Hiệu năng và Khả năng đọc hiểu.",
      content: `---
name: code-review-and-quality
description: Use before merging PRs, completing major features, or auditing existing codebases.
phase: review-and-audit
---

# 5-Axis Code Review & Quality Gate (Addy Osmani Standard)

> **Mục tiêu:** Bảo đảm không có nợ kỹ thuật (technical debt), lỗ hổng bảo mật hay bẫy hiệu năng nào lọt vào nhánh chính.

## 1. Năm Trục Đánh Giá Toàn Diện (5-Axis Audit)
1. **Tính đúng đắn (Correctness):**
   - Mã nguồn có xử lý đầy đủ các trường hợp biên (\`null\`, \`undefined\`, \`empty array\`, \`network timeout\`)?
2. **Kiến trúc (Architecture & Blast Radius):**
   - Có tuân thủ nguyên lý Single Responsibility? Có làm phình to các God Node không?
3. **Bảo mật (Security & Hardening):**
   - Có kiểm tra đầu vào (Zod / Pydantic)? Có ngăn chặn SQL Injection / XSS? Secret keys có được che giấu?
4. **Hiệu năng (Performance & Resources):**
   - Có vòng lặp lồng nhau $O(n^2)$ không? Có hiện tượng waterfall re-fetch data không?
5. **Khả năng bảo trì & Đọc hiểu (Readability):**
   - Đặt tên biến và hàm có rõ nghĩa? Có ghi chú thích ở các logic phức tạp?

## 2. Bảng Chống Ngụy Biện
| Lời ngụy biện | Hành động bắt buộc |
| :--- | :--- |
| *"Code chạy được là được rồi, review làm gì"* | **CHẶN LẠI:** Code chạy được chỉ là điều kiện cần; khả năng bảo trì mới là điều kiện đủ. |
| *"Hàm này hơi dài nhưng tiện tay gom vào một chỗ"* | **CHẶN LẠI:** Tách hàm nếu vượt quá 50 dòng hoặc làm hơn 2 nhiệm vụ. |`
    },
    "root-cause-debug": {
      title: "Root-Cause Debugging & Error Recovery",
      id: "debugging-and-error-recovery",
      category: "Testing & QA",
      desc: "Phương pháp truy vết nguyên nhân gốc rễ, cô lập lỗi và tạo bài kiểm thử tự động ngăn chặn tái diễn lỗi vĩnh viễn.",
      content: `---
name: debugging-and-error-recovery
description: Use when diagnosing bug reports, runtime crashes, race conditions, or unexplained regressions.
phase: verify-and-debug
---

# Root-Cause Debugging & Error Recovery Protocol

> **Luật bất thành văn:** Không bao giờ đoán mò hay sửa chữa theo kiểu 'thử vận may' (Shotgun Debugging)!

## 1. Quy Trình 5 Bước Khắc Phục Lỗi
1. **Tái hiện ổn định (Stable Reproduction):** Tạo kịch bản kiểm thử tối thiểu để kích hoạt lỗi 100% các lần chạy.
2. **Cô lập nguyên nhân gốc rễ (Root-Cause Isolation):** Dùng công cụ ghi vết, log và breakpoint để xác định đúng dòng mã gây lỗi.
3. **Hình thành giả thuyết (Hypothesis Testing):** Đưa ra giải thích khoa học vì sao lỗi xảy ra và vì sao giải pháp này sẽ khắc phục được.
4. **Sửa chữa tối thiểu & chính xác (Surgical Fix):** Chỉ sửa đúng điểm lỗi, không làm xáo trộn các đoạn mã xung quanh.
5. **Kiểm thử chống tái diễn (Regression Prevention):** Thêm bài kiểm thử tự động mô phỏng đúng trường hợp lỗi vừa sửa.

## 2. Bảng Chống Ngụy Biện
| Lời ngụy biện | Hành động bắt buộc |
| :--- | :--- |
| *"Bọc try-catch vào là hết văng lỗi ngay"* | **CHẶN LẠI:** Tuyệt đối không giấu lỗi bằng try-catch rỗng (Silent Error Swallow). |
| *"Chắc do thư viện bên ngoài lỗi thôi"* | **CHẶN LẠI:** Kiểm tra kỹ input truyền vào trước khi đổ lỗi cho upstream library. |`
    },
    "ui-ux-artisan": {
      title: "Frontend UI/UX Artisan & Design Integrity",
      id: "frontend-ui-engineering",
      category: "UI/UX Design",
      desc: "Thiết kế giao diện chống slop, tuân thủ Vercel Web Interface Guidelines, hiệu ứng vật lý dưới 250ms và bố cục chống tràn.",
      content: `---
name: frontend-ui-engineering
description: Use when building screens, forms, responsive layouts, motion effects, and accessible UI components.
phase: build-and-polish
---

# Frontend UI/UX Artisan Standard (Vercel & shadcn Quality)

> **Tiêu chuẩn thẩm mỹ:** Tinh tế, nhất quán, không lỗi tràn bố cục, phản hồi tức thì và tôn trọng tâm lý học người dùng!

## 1. Bốn Trụ Cột Vàng Của Giao Diện Cao Cấp
1. **Tâm lý học UX (UX Psychology):**
   - Tuyệt đối không có hành động mù (Zero Blind Actions). Mọi nút bấm đều có trạng thái Hover, Active, và Loading Spinner.
2. **Vercel Web Interface Guidelines:**
   - Bo góc đồng nhất (\`radius-sm\`, \`radius-md\`), khoảng cách chuẩn bội số của 4/8px.
3. **Bố cục chống tràn (Anti-Overflow Layout Safety):**
   - Luôn sử dụng \`min-w-0\`, \`min-h-0\` trong flex/grid containers; thanh hành động luôn được neo cố định.
4. **Hiệu ứng chuyển động vật lý (Physics Motion):**
   - Thời gian chuyển động dưới 250ms (\`cubic-bezier(0.16, 1, 0.3, 1)\`), tạo cảm giác mượt mà không gây giật lag.`
    }
  },

  renderStudioView() {
    const container = document.getElementById("studio-container");
    if (!container) return;

    container.innerHTML = UIComponents.renderStudioView();

    const titleInput = document.getElementById("studio-title");
    const idInput = document.getElementById("studio-id");
    const categorySelect = document.getElementById("studio-category");
    const descInput = document.getElementById("studio-desc");
    const contentInput = document.getElementById("studio-content");
    const previewPane = document.getElementById("studio-preview-pane");
    const charCount = document.getElementById("studio-char-count");

    const updateLivePreview = () => {
      const text = contentInput?.value || "";
      if (charCount) {
        charCount.innerText = `${text.length} ký tự (~${Math.round(text.length / 4)} tokens)`;
      }
      if (previewPane) {
        previewPane.innerHTML = text.trim() 
          ? MarkdownRenderer.render(text) 
          : `<p style="color:var(--text-muted);">Bấm chọn một mẫu Addy Osmani ở trên hoặc gõ nội dung vào cột trái để xem trước định dạng tại đây...</p>`;
      }
    };

    // Preset Buttons Click Listeners
    container.querySelectorAll(".preset-chip-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        container.querySelectorAll(".preset-chip-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        const presetKey = btn.getAttribute("data-preset");
        if (presetKey === "blank") {
          titleInput.value = "";
          idInput.value = "";
          idInput.dataset.manual = "";
          descInput.value = "";
          contentInput.value = "";
        } else if (this.studioPresets[presetKey]) {
          const p = this.studioPresets[presetKey];
          titleInput.value = p.title;
          idInput.value = p.id;
          idInput.dataset.manual = "true";
          descInput.value = p.desc;
          contentInput.value = p.content;
          if (categorySelect) categorySelect.value = p.category;
          this.showToast(`✓ Đã nạp mẫu chuẩn Addy Osmani: ${p.title}`, "success");
        }
        updateLivePreview();
      });
    });

    titleInput?.addEventListener("input", (e) => {
      if (!idInput.dataset.manual) {
        idInput.value = e.target.value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
      }
    });

    idInput?.addEventListener("input", () => {
      idInput.dataset.manual = "true";
    });

    contentInput?.addEventListener("input", () => {
      updateLivePreview();
    });

    document.getElementById("btn-studio-save")?.addEventListener("click", async () => {
      const title = titleInput.value.trim();
      const id = idInput.value.trim();
      const category = categorySelect?.value || "Developer Tools";
      const desc = descInput?.value.trim() || "";
      const content = contentInput.value.trim();

      if (!title || !id) {
        this.showToast("Vui lòng nhập Tên và Mã định danh (ID) cho kỹ năng.", "error");
        return;
      }

      try {
        const res = await DesktopBridge.saveSkill({
          id: id,
          name: id,
          display_title: title,
          category: category,
          description: desc,
          skill_content: content,
          version: "1.0.0",
          author: "Tôi (Addy Osmani Standard)",
          tags: [category]
        });

        if (res && res.success) {
          this.showToast("🎉 Đã lưu kỹ năng vào Thư viện thành công!", "success");
          await this.loadSkills();
          this.switchWorkspace("library");
          this.selectSkill(id);
        } else {
          this.showToast(res ? res.message : "Lỗi lưu kỹ năng.", "error");
        }
      } catch (err) {
        this.showToast("Lỗi: " + err.message, "error");
      }
    });

    document.getElementById("btn-publish-to-community")?.addEventListener("click", async () => {
      const title = titleInput.value.trim();
      const id = idInput.value.trim();
      const category = categorySelect?.value || "Developer Tools";
      const desc = descInput?.value.trim() || "";
      const content = contentInput.value.trim();

      if (!title || !id) {
        this.showToast("Vui lòng nhập Tên và Mã định danh (ID) trước khi đăng lên Chợ Cloud.", "error");
        return;
      }

      const publishBtn = document.getElementById("btn-publish-to-community");
      if (publishBtn) {
        publishBtn.disabled = true;
        publishBtn.innerHTML = `<span>Đang đăng tải...</span>`;
      }

      try {
        const res = await DesktopBridge.communityPublishSkill({
          id: id,
          title: title,
          category: category,
          description: desc,
          content: content,
          author: this.authSession?.user?.email ? this.authSession.user.email.split('@')[0] : "Kỹ Sư Cộng Đồng"
        });

        if (res && res.success) {
          this.showToast(res.message || "✓ Đã đăng tải kỹ năng lên Chợ Cộng Đồng!", "success");
          await this.loadCommunitySkills();
          this.switchWorkspace("community");
        } else {
          this.showToast(res ? res.message : "Đăng tải thất bại.", "error");
        }
      } catch (err) {
        this.showToast("Lỗi đăng tải: " + err.message, "error");
      } finally {
        if (publishBtn) {
          publishBtn.disabled = false;
          publishBtn.innerHTML = `${Icons.uploadCloud} <span>Đăng Lên Chợ Cloud</span>`;
        }
      }
    });
  },

  async loadCommunitySkills() {
    try {
      const res = await DesktopBridge.communityGetSkills();
      if (res && res.success) {
        this.communitySkills = res.skills || [];
      }
    } catch (e) {
      console.warn("loadCommunitySkills error:", e);
    }
  },

  async renderCommunityView() {
    const container = document.getElementById("community-container");
    if (!container) return;

    if (this.communitySkills.length === 0) {
      await this.loadCommunitySkills();
    }

    container.innerHTML = UIComponents.renderCommunityCloudView(
      this.communitySchema,
      this.communitySkills,
      {
        activeTab: this.communitySubTab,
        activeCat: this.communityFilterCat,
        query: this.communitySearchQuery
      }
    );

    document.getElementById("btn-subtab-marketplace")?.addEventListener("click", () => {
      this.communitySubTab = "marketplace";
      this.renderCommunityView();
    });

    document.getElementById("btn-subtab-schema")?.addEventListener("click", () => {
      this.communitySubTab = "schema";
      this.renderCommunityView();
    });

    container.querySelectorAll(".comm-cat-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        this.communityFilterCat = chip.getAttribute("data-comm-cat") || "all";
        this.renderCommunityView();
      });
    });

    const searchInput = document.getElementById("community-search-input");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.communitySearchQuery = e.target.value;
        clearTimeout(this._commSearchTimer);
        this._commSearchTimer = setTimeout(() => this.renderCommunityView(), 220);
      });
    }

    container.querySelectorAll(".btn-view-community-skill").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        this.openCommunityDetailModal(id);
      });
    });

    container.querySelectorAll(".btn-install-community-skill").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        this.openCommunityDetailModal(id);
      });
    });

    document.getElementById("btn-copy-community-sql")?.addEventListener("click", async () => {
      if (this.communitySchema?.sql) {
        try {
          await navigator.clipboard.writeText(this.communitySchema.sql);
          this.showToast("Đã sao chép Supabase SQL Schema vào bộ nhớ tạm!", "success");
        } catch (e) {
          this.showToast("Đã sao chép SQL Schema!", "success");
        }
      }
    });
  },

  resetCommunityFilters() {
    this.communityFilterCat = "all";
    this.communitySearchQuery = "";
    this.renderCommunityView();
  },

  openCommunityDetailModal(skillId) {
    const skill = this.communitySkills.find(s => s.id === skillId);
    if (!skill) return;
    const root = document.getElementById("modal-root");
    if (!root) return;

    root.innerHTML = UIComponents.renderCommunitySkillDetailModal(skill, this.activeWorkspaceProject);

    root.querySelector(".btn-confirm-comm-install")?.addEventListener("click", async () => {
      const checkedBoxes = Array.from(root.querySelectorAll(".comm-target-checkbox:checked"));
      const selectedTargets = checkedBoxes.map(cb => cb.value);
      if (selectedTargets.length === 0) {
        this.showToast("Vui lòng chọn ít nhất một nền tảng để cài đặt.", "warning");
        return;
      }

      const installBtn = root.querySelector(".btn-confirm-comm-install");
      if (installBtn) {
        installBtn.disabled = true;
        installBtn.innerHTML = `<span>Đang cài đặt...</span>`;
      }

      try {
        const res = await DesktopBridge.communityInstallSkill({
          skill_id: skill.id,
          targets: selectedTargets,
          workspace_path: this.activeWorkspaceProject || null
        });

        if (res && res.success) {
          this.closeActiveModal();
          this.showToast(res.message || `✓ Đã cài đặt kỹ năng "${skill.display_title || skill.name}"!`, "success");
          await this.loadSkills();
          await this.loadCommunitySkills();
        } else {
          this.showToast(res ? res.message : "Cài đặt thất bại.", "error");
        }
      } catch (err) {
        this.showToast("Lỗi: " + err.message, "error");
      }
    });
  },

  async openDiagnosticsModal() {
    const root = document.getElementById("modal-root");
    if (!root) return;

    try {
      const res = await DesktopBridge.getDiagnosticLogs(120);
      const data = res && res.success ? res : {};
      root.innerHTML = UIComponents.renderDiagnosticModal(data);

      document.getElementById("btn-export-diagnostics")?.addEventListener("click", async () => {
        const btn = document.getElementById("btn-export-diagnostics");
        if (btn) {
          btn.disabled = true;
          btn.innerHTML = `<span>Đang xuất...</span>`;
        }
        try {
          const exportRes = await DesktopBridge.exportDiagnosticLogs();
          if (exportRes && exportRes.success) {
            this.showToast(`✓ ${exportRes.message}`, "success");
          } else {
            this.showToast(exportRes ? exportRes.message : "Lỗi xuất báo cáo.", "error");
          }
        } catch (e) {
          this.showToast("Lỗi: " + e.message, "error");
        } finally {
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = `${Icons.download} <span>Xuất File ZIP Chẩn Đoán</span>`;
          }
        }
      });

      document.getElementById("btn-open-log-folder")?.addEventListener("click", async () => {
        try {
          await DesktopBridge.openLogsFolder();
        } catch (e) {
          this.showToast("Không thể mở thư mục: " + e.message, "error");
        }
      });

      // Submit Cloud Error Telemetry with Anti-Spam Cooldown & Zero-Trust Sanitization
      document.getElementById("btn-submit-cloud-error")?.addEventListener("click", async () => {
        const btn = document.getElementById("btn-submit-cloud-error");
        const COOLDOWN_MS = 180 * 1000;
        const lastSentStr = localStorage.getItem("abyssalskillsd-last-error-submit");
        if (lastSentStr) {
          const lastSent = parseInt(lastSentStr, 10);
          const elapsed = Date.now() - lastSent;
          if (elapsed < COOLDOWN_MS) {
            const remSec = Math.ceil((COOLDOWN_MS - elapsed) / 1000);
            this.showToast(`🛡️ Vui lòng chờ ${remSec}s trước khi gửi báo cáo tiếp theo (chống spam flood).`, "warning");
            return;
          }
        }

        if (btn) {
          btn.disabled = true;
          btn.innerHTML = `<span>Đang gửi báo cáo an toàn...</span>`;
        }

        try {
          const logsList = data.logs || [];
          let lastErrorLine = "Người dùng chủ động gửi chẩn đoán hệ thống";
          let moduleName = "app_runtime";
          let lineNum = 0;

          for (let i = logsList.length - 1; i >= 0; i--) {
            const l = logsList[i];
            if (l.includes("[ERROR]") || l.includes("Traceback") || l.includes("Error:") || l.includes("Exception")) {
              lastErrorLine = l;
              break;
            }
          }

          const payload = {
            error_message: lastErrorLine,
            error_type: lastErrorLine.includes("Error") ? "SystemError" : "DiagnosticTelemetry",
            stack_trace: logsList.slice(-15).join("\n"),
            module_name: moduleName,
            line_number: lineNum,
            metadata: {
              app_version: "2.4.0",
              os: data.system_info?.os || "Windows",
              active_workspace: data.system_info?.active_workspace || ""
            }
          };

          const reportRes = await DesktopBridge.reportSystemError(payload);
          if (reportRes && reportRes.success) {
            localStorage.setItem("abyssalskillsd-last-error-submit", Date.now().toString());
            this.showToast(`✓ ${reportRes.message || "Báo cáo lỗi đã được gửi an toàn!"}`, "success");
            if (btn) {
              btn.innerHTML = `<span>✓ Đã tiếp nhận (${reportRes.occurrences || 1} lần)</span>`;
            }
          } else {
            this.showToast(reportRes ? reportRes.message : "Không thể gửi báo cáo lỗi.", "error");
            if (btn) {
              btn.disabled = false;
              btn.innerHTML = `<span>🚀 Gửi Báo Cáo Lên Cloud</span>`;
            }
          }
        } catch (e) {
          this.showToast("Lỗi gửi báo cáo: " + e.message, "error");
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = `<span>🚀 Gửi Báo Cáo Lên Cloud</span>`;
          }
        }
      });
    } catch (err) {
      this.showToast("Lỗi tải thông tin chẩn đoán: " + err.message, "error");
    }
  },

  // Command Palette Methods
  openCommandPalette() {
    this.isCommandPaletteOpen = true;
    this.commandPaletteIndex = 0;
    const root = document.getElementById("modal-root");
    root.innerHTML = UIComponents.renderCommandPalette(this.skills, this.commandPaletteIndex, "");

    const input = document.getElementById("command-search-input");
    input?.focus();

    input?.addEventListener("input", (e) => {
      const q = e.target.value;
      root.innerHTML = UIComponents.renderCommandPalette(this.skills, 0, q);
      const refreshedInput = document.getElementById("command-search-input");
      refreshedInput?.focus();
      refreshedInput?.setSelectionRange(q.length, q.length);
      this.bindCommandPaletteList();
    });

    this.bindCommandPaletteList();
  },

  bindCommandPaletteList() {
    document.querySelectorAll(".command-item").forEach((item, idx) => {
      item.addEventListener("click", () => {
        this.executeCommandItem(item);
      });
    });
  },

  executeCommandItem(item) {
    const action = item.getAttribute("data-action");
    const skillId = item.getAttribute("data-id");
    this.closeCommandPalette();

    if (action === "batch-install") {
      this.handleBatchInstallAll();
    } else if (action === "toggle-theme") {
      this.toggleTheme();
    } else if (action === "open-guide") {
      this.switchWorkspace("guide");
    } else if (action === "open-auth") {
      this.openAuthModal("signin");
    } else if (action === "open-auth-config") {
      this.openAuthModal("config");
    } else if (action === "open-diagnostics") {
      this.openDiagnosticsModal();
    } else if (action === "open-skill" && skillId) {
      this.switchWorkspace("library");
      this.selectSkill(skillId);
    }
  },

  closeCommandPalette(event) {
    if (event && event.target && !event.target.classList.contains("command-backdrop")) {
      return;
    }
    const root = document.getElementById("modal-root");
    if (root) root.innerHTML = "";
    this.isCommandPaletteOpen = false;
  },

  toggleToolsDropdown() {
    const container = document.getElementById("tools-dropdown-container");
    if (!container) return;

    if (container.innerHTML.trim()) {
      container.innerHTML = "";
      return;
    }

    container.innerHTML = UIComponents.renderToolsDropdown();

    document.getElementById("btn-tool-scan")?.addEventListener("click", () => {
      this.closeToolsDropdown();
      this.triggerNativeFolderPicker();
    });

    document.getElementById("btn-tool-github")?.addEventListener("click", () => {
      this.closeToolsDropdown();
      this.openGitHubModal();
    });

    document.getElementById("btn-tool-studio")?.addEventListener("click", () => {
      this.closeToolsDropdown();
      this.switchWorkspace("studio");
    });

    document.getElementById("btn-tool-batch-sync")?.addEventListener("click", () => {
      this.closeToolsDropdown();
      this.handleBatchInstallAll();
    });

    document.getElementById("btn-tool-check-updates")?.addEventListener("click", () => {
      this.closeToolsDropdown();
      this.checkAppUpdates(true);
    });

    document.getElementById("btn-tool-theme")?.addEventListener("click", () => {
      this.closeToolsDropdown();
      this.toggleTheme();
    });
  },

  closeToolsDropdown() {
    const container = document.getElementById("tools-dropdown-container");
    if (container) container.innerHTML = "";
  },

  openGitHubModal() {
    const root = document.getElementById("modal-root");
    root.innerHTML = UIComponents.renderGitHubModal();

    document.getElementById("btn-confirm-github-clone")?.addEventListener("click", () => {
      const url = document.getElementById("input-github-url")?.value.trim();
      if (url) this.handleGitHubSync(url);
    });
  },

  async handleGitHubSync(repoUrl) {
    const statusBox = document.getElementById("github-sync-status");
    const statusText = document.getElementById("github-sync-text");
    const confirmBtn = document.getElementById("btn-confirm-github-clone");

    if (statusBox) statusBox.style.display = "block";
    if (statusText) statusText.innerText = "Đang kết nối và tải kho từ GitHub...";
    if (confirmBtn) confirmBtn.disabled = true;

    try {
      const res = await DesktopBridge.importFromGitHub(repoUrl);
      if (res && res.success) {
        this.showToast(res.message, "success");
        await this.loadSkills();
        this.closeActiveModal();
      } else {
        this.showToast(res ? res.message : "Tải từ GitHub thất bại.", "error");
        if (statusBox) statusBox.style.display = "none";
        if (confirmBtn) confirmBtn.disabled = false;
      }
    } catch (err) {
      this.showToast("Lỗi đồng bộ GitHub: " + err.message, "error");
      if (statusBox) statusBox.style.display = "none";
      if (confirmBtn) confirmBtn.disabled = false;
    }
  },

  async triggerNativeFolderPicker() {
    this.showToast("Đang mở hộp thoại chọn thư mục...", "info");
    try {
      const res = await DesktopBridge.pickFolderDialog();
      if (res && res.success && res.path) {
        this.showToast(`Đang quét thư mục: ${res.path}`, "info");
        const scanRes = await DesktopBridge.scanLocalFolder(res.path);
        if (scanRes && scanRes.success) {
          this.showToast(scanRes.message, "success");
          await this.loadSkills();
        } else {
          this.showToast(scanRes ? scanRes.message : "Không tìm thấy file SKILL.md", "error");
        }
      } else if (res && res.message && !res.message.includes("hủy")) {
        this.showToast(res.message, "error");
      }
    } catch (e) {
      this.showToast("Lỗi mở hộp thoại: " + e.message, "error");
    }
  },

  closeActiveModal(event) {
    if (event && event.target && !event.target.classList.contains("modal-backdrop")) {
      return;
    }
    const root = document.getElementById("modal-root");
    if (root) root.innerHTML = "";
  },

  showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `
      <div style="color: ${type === 'success' ? 'var(--led-success)' : (type === 'error' ? 'var(--led-danger)' : 'var(--led-info)')};">
        ${type === 'success' ? Icons.check : (type === 'error' ? Icons.x : Icons.sparkles)}
      </div>
      <div>${UIComponents.escape(message)}</div>
    `;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(6px)";
      toast.style.transition = "all 150ms ease";
      setTimeout(() => toast.remove(), 150);
    }, 2600);
  },

  resetFilters() {
    this.activeCategory = "all";
    this.searchQuery = "";
    const input = document.getElementById("global-search-input");
    if (input) input.value = "";
    document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
    document.querySelector(".filter-chip[data-cat='all']")?.classList.add("active");
    this.applyFilters();
  },

  bindEvents() {
    // Navigation items
    document.querySelectorAll(".nav-link").forEach(link => {
      link.addEventListener("click", () => {
        const nav = link.getAttribute("data-nav");
        if (nav) this.switchWorkspace(nav);
      });
    });

    // Theme toggle button
    document.getElementById("btn-toggle-theme")?.addEventListener("click", () => {
      this.toggleTheme();
    });

    // Notification Center Bell click
    document.getElementById("btn-notification-bell")?.addEventListener("click", (e) => {
      e.stopPropagation();
      this.toggleNotificationTray();
    });

    // Topbar update badge click
    document.getElementById("btn-topbar-update")?.addEventListener("click", () => {
      this.checkAppUpdates(true);
    });

    // Brand Logo trigger (replays intro anytime)
    document.getElementById("brand-logo-trigger")?.addEventListener("click", () => {
      this.showIntro();
    });

    // View mode switchers (Bento vs Linear)
    document.getElementById("btn-view-bento")?.addEventListener("click", () => {
      this.activeViewMode = "bento";
      document.getElementById("btn-view-bento").classList.add("active");
      document.getElementById("btn-view-linear").classList.remove("active");
      document.getElementById("skills-bento-grid").style.display = "grid";
      document.getElementById("skills-linear-list").style.display = "none";
    });

    document.getElementById("btn-view-linear")?.addEventListener("click", () => {
      this.activeViewMode = "linear";
      document.getElementById("btn-view-linear").classList.add("active");
      document.getElementById("btn-view-bento").classList.remove("active");
      document.getElementById("skills-bento-grid").style.display = "none";
      document.getElementById("skills-linear-list").style.display = "flex";
    });

    // Category chips
    document.querySelectorAll(".filter-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        this.activeCategory = chip.getAttribute("data-cat");
        this.applyFilters();
      });
    });

    // Source chips (Skill-AI Suite vs Addy Osmani Suite)
    document.querySelectorAll(".source-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".source-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        this.activeSource = chip.getAttribute("data-source") || "all";
        this.renderOrgBanner();
        this.applyFilters();
      });
    });

    // Search command input with 150ms debounce
    const searchInput = document.getElementById("global-search-input");
    let debounceTimer;
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          this.searchQuery = e.target.value;
          this.applyFilters();
        }, 150);
      });
    }

    // Command palette trigger
    document.getElementById("trigger-command-palette")?.addEventListener("click", (e) => {
      if (e.target !== searchInput) {
        this.openCommandPalette();
      }
    });

    // Dynamic Active Workspace Project Selector
    document.getElementById("btn-change-workspace")?.addEventListener("click", () => {
      this.handleSelectWorkspaceProject();
    });

    // 1-Click Multi-AI Global Sync & Rules Generator
    document.getElementById("btn-sync-all-ais")?.addEventListener("click", () => {
      this.openSyncAllModal();
    });

    document.getElementById("btn-generate-project-rules")?.addEventListener("click", () => {
      this.openGenerateRulesModal();
    });

    document.getElementById("btn-open-diagnostics")?.addEventListener("click", () => {
      this.openDiagnosticsModal();
    });

    // Delegated click for .btn-card-customize across cards & lists
    document.addEventListener("click", (e) => {
      const btn = e.target.closest(".btn-card-customize");
      if (btn) {
        e.stopPropagation();
        const skillId = btn.getAttribute("data-id");
        if (skillId) this.handleCustomizeInStudio(skillId);
      }
    });

    // Delegated click for .btn-card-review-diff across cards
    document.addEventListener("click", (e) => {
      const btn = e.target.closest(".btn-card-review-diff");
      if (btn) {
        e.stopPropagation();
        const skillId = btn.getAttribute("data-id");
        if (skillId) this.openDiffReviewModal(skillId);
      }
    });

    // Top action buttons
    document.getElementById("btn-open-studio")?.addEventListener("click", () => {
      this.switchWorkspace("studio");
    });

    document.getElementById("btn-open-scan-folder")?.addEventListener("click", () => {
      this.triggerNativeFolderPicker();
    });

    document.getElementById("btn-open-github-modal")?.addEventListener("click", () => {
      this.openGitHubModal();
    });

    // Consolidated Tools Dropdown Trigger
    document.getElementById("btn-tools-dropdown")?.addEventListener("click", (e) => {
      e.stopPropagation();
      this.toggleToolsDropdown();
    });

    // Close user and tools dropdown menus when clicking outside
    window.addEventListener("click", (e) => {
      const panel = document.getElementById("user-dropdown-panel");
      if (panel && !panel.contains(e.target) && !document.getElementById("btn-user-profile-menu")?.contains(e.target)) {
        this.closeUserMenu();
      }

      const toolsMenu = document.getElementById("tools-dropdown-menu");
      if (toolsMenu && !toolsMenu.contains(e.target) && !document.getElementById("btn-tools-dropdown")?.contains(e.target)) {
        this.closeToolsDropdown();
      }

      const notifMenu = document.getElementById("notification-dropdown-menu");
      if (notifMenu && !notifMenu.contains(e.target) && !document.getElementById("btn-notification-bell")?.contains(e.target)) {
        this.closeNotificationTray();
      }
    });

    // Keyboard shortcuts
    window.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        this.openCommandPalette();
      }

      if (e.key === "Escape") {
        if (this.isCommandPaletteOpen) {
          this.closeCommandPalette();
        } else {
          const root = document.getElementById("modal-root");
          if (root && root.innerHTML.trim() !== "") {
            this.closeActiveModal();
          } else if (this.selectedSkillId) {
            this.closeInspector();
          }
        }
      }

      // Command palette arrow keys
      if (this.isCommandPaletteOpen) {
        const items = document.querySelectorAll(".command-item");
        if (items.length > 0) {
          if (e.key === "ArrowDown") {
            e.preventDefault();
            this.commandPaletteIndex = (this.commandPaletteIndex + 1) % items.length;
            items.forEach((it, i) => it.classList.toggle("active", i === this.commandPaletteIndex));
            items[this.commandPaletteIndex]?.scrollIntoView({ block: "nearest" });
          } else if (e.key === "ArrowUp") {
            e.preventDefault();
            this.commandPaletteIndex = (this.commandPaletteIndex - 1 + items.length) % items.length;
            items.forEach((it, i) => it.classList.toggle("active", i === this.commandPaletteIndex));
            items[this.commandPaletteIndex]?.scrollIntoView({ block: "nearest" });
          } else if (e.key === "Enter") {
            e.preventDefault();
            const activeItem = items[this.commandPaletteIndex];
            if (activeItem) this.executeCommandItem(activeItem);
          }
        }
      }
    });
  },

  showShimmer() {
    const grid = document.getElementById("skills-bento-grid");
    if (!grid) return;
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-muted);">
        <div style="font-size: 13px; font-weight: 500;">Khởi tạo không gian làm việc AbyssalSkillsD Suite...</div>
      </div>
    `;
  }
};

window.App = App;
document.addEventListener("DOMContentLoaded", () => App.init());
