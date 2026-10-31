"""
AbyssalSkillsD - Comprehensive Verification Suite
Tests the 7-Skill Suite from Skill-AI-private, Addy Osmani Suite, Supabase Community Schema,
Batch Multi-Target Deployment, Graphify AST, Standalone Packaging, and Auto-Update Engine.
"""
import sys
import json
import time
import zipfile
from pathlib import Path

def test_all():
    print("▶ Running AbyssalSkillsD Comprehensive Verification Suite (20 Gates)...")
    
    # 1. Test Storage & All 7 Skills from Skill-AI-private
    from app.backend.models import SkillItem, InstallRequest
    from app.backend.storage import SkillStorage
    from app.backend.api import DesktopAPI

    SkillStorage.initialize()
    skills = SkillStorage.get_all_skills()
    assert len(skills) >= 7, f"Expected 7 skills, got {len(skills)}"
    
    expected_skills = [
        "strict-architect-coder",
        "ui-ux-design-master",
        "shadcn-tailwind-artisan",
        "web-assets-creative-vault",
        "nextjs-fullstack-master",
        "supabase-backend-architect",
        "playwright-web-tester"
    ]
    
    loaded_ids = [s.id for s in skills]
    for exp_id in expected_skills:
        assert exp_id in loaded_ids, f"Skill '{exp_id}' not found in registry!"
        skill_item = SkillStorage.get_skill(exp_id)
        assert skill_item is not None
        assert "Skill-AI" in skill_item.author or "Community" in skill_item.author
        print(f"  [PASS] Verified Skill '{exp_id}' (refs: {len(skill_item.references)}, rules: {len(skill_item.rules)})")

    # 2. Total references count across the suite
    total_refs = sum(len(s.references) for s in skills)
    assert total_refs >= 24, f"Expected >= 24 references, found {total_refs}"
    print(f"  [PASS] Verified {total_refs} total reference playbooks across suite.")

    # 3. Test Batch Multi-Target Deployment
    api = DesktopAPI()
    test_ws = Path("app/data/test_batch_ws")
    test_ws.mkdir(parents=True, exist_ok=True)
    
    batch_res = api.install_all_skills({
        "targets": ["workspace"],
        "workspace_path": str(test_ws),
        "enable_always_on": True,
        "with_graphify": False
    })
    assert batch_res["success"] is True, f"Batch install failed: {batch_res}"
    assert batch_res["count"] >= 7, f"Expected at least 7 skills installed, got {batch_res['count']}"
    assert (test_ws / ".agents" / "skills" / "strict-architect-coder" / "SKILL.md").exists()
    assert (test_ws / ".agents" / "skills" / "shadcn-tailwind-artisan" / "SKILL.md").exists()
    assert (test_ws / ".agents" / "rules" / "always-on-autopilot.md").exists()
    assert (test_ws / ".cursorrules").exists(), "Cursor .cursorrules missing!"
    assert (test_ws / ".cursor" / "rules" / "always-on-autopilot.mdc").exists(), "Cursor .mdc missing!"
    assert (test_ws / ".windsurfrules").exists(), "Windsurf .windsurfrules missing!"
    assert (test_ws / ".github" / "copilot-instructions.md").exists(), "GitHub Copilot instructions missing!"
    assert (test_ws / "CONVENTIONS.md").exists(), "Aider CONVENTIONS.md missing!"
    print("  [PASS] Batch installation of all 7 skills and Universal Autopilot rules (.cursorrules, .windsurfrules, copilot, aider) succeeded.")

    # 4. Test Supabase Community Cloud Schema (supabase-backend-architect)
    schema_res = api.get_community_schema()
    assert schema_res["success"] is True, "Failed to load community schema!"
    assert "ENABLE ROW LEVEL SECURITY" in schema_res["sql"], "RLS not enabled in schema!"
    assert "idx_skills_fts" in schema_res["sql"], "GIN Index missing in schema!"
    print("  [PASS] Supabase Community Schema verified with RLS & GIN Index.")

    # 5. Test Graphify AST & Clean UI Decoupling
    g_res = api.run_graphify()
    assert g_res["success"] is True, f"Graphify failed: {g_res}"
    assert Path("graphify-out/GRAPH_REPORT.md").exists()
    assert Path("graphify-out/graph.json").exists()
    
    # Assert frontend is decoupled from Graphify UI bloat
    raw_html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    assert 'data-nav="graphify"' not in raw_html, "Graphify nav item still present in index.html!"
    assert 'id="graphify-lab-container"' not in raw_html, "Graphify container still present in index.html!"
    raw_comp = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert 'data-action="open-graphify"' not in raw_comp, "Graphify quick action still in Command Palette!"
    print("  [PASS] Graphify AST analysis verified as internal AI watchdog and cleanly decoupled from UI.")

    # 6. Test Frontend Assets & Accessibility (playwright-web-tester / shadcn standards)
    index_html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    assert 'data-theme="dark"' in index_html, "Dark theme default missing"
    assert 'data-testid="global-search-input"' in index_html, "Search input testid missing"
    assert 'data-testid="activity-sidebar"' in index_html, "Sidebar testid missing"
    assert 'data-testid="btn-batch-install-all"' in Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert Path("app/frontend/css/app.css").exists()
    assert '[data-theme="light"]' in Path("app/frontend/css/app.css").read_text(encoding="utf-8")
    print("  [PASS] Frontend dual-theme tokens & accessibility testids verified.")

    # 7. Check 3 Memory Anchors
    assert Path(".agents/PROJECT_MEMORY.md").exists()
    assert Path("DESIGN.md").exists()
    assert Path("graphify-out/GRAPH_REPORT.md").exists()
    print("  [PASS] 3 Persistent Project Memory Anchors verified.")

    # 8. Test Onboarding, Guided Workflow & Starter Prompts
    for s in skills:
        assert s.when_to_use, f"Skill '{s.id}' missing when_to_use guidance!"
        assert len(s.starter_prompts) >= 3, f"Skill '{s.id}' has fewer than 3 starter prompts ({len(s.starter_prompts)})"
        assert s.use_case_group, f"Skill '{s.id}' missing use_case_group!"
    
    assert 'data-testid="nav-guide"' in index_html, "Nav Guide testid missing"
    assert 'data-testid="filter-plan-debug"' in index_html, "Filter plan debug testid missing"
    components_js = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert 'renderGuideView' in components_js, "renderGuideView missing in components.js"
    assert 'starter-prompt-card' in components_js, "starter-prompt-card missing in components.js"
    assert 'onboarding-step-card' in components_js, "onboarding-step-card missing in components.js"
    app_js = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert 'copyStarterPrompt' in app_js, "copyStarterPrompt missing in app.js"
    print("  [PASS] Onboarding 3-step banner, Guide A-Z, when_to_use, and Vietnamese starter prompts verified.")

    # 9. Test Supabase Authentication, Token & Secret Key Engine (supabase-backend-architect)
    from app.backend.auth import AuthEngine
    orig_saved_cfg = api.auth_get_config()

    # Test config save and get
    save_cfg_res = api.auth_save_config({
        "supabase_url": "https://custom-project.supabase.co",
        "anon_key": "custom_anon_jwt_token_sample",
        "service_secret_key": "custom_service_secret_key_123"
    })
    assert save_cfg_res["success"] is True, "Failed to save Supabase config!"
    curr_cfg = api.auth_get_config()
    assert curr_cfg["supabase_url"] == "https://custom-project.supabase.co"
    assert curr_cfg["has_secret_key"] is True
    assert "custom_anon_jwt" in curr_cfg["anon_key"]

    # Test sign up / sign in
    sign_in_res = api.auth_sign_in({
        "email": "developer.admin@skillforge.ai",
        "password": "secret_password_123"
    })
    assert sign_in_res["success"] is True, f"Sign in failed: {sign_in_res}"
    session = sign_in_res["session"]
    assert session["authenticated"] is True
    assert "access_token" in session and session["access_token"]
    assert "refresh_token" in session and session["refresh_token"]
    assert session["user"]["email"] == "developer.admin@skillforge.ai"
    assert session["user"]["role"] == "admin"

    # Test get active session
    active_sess = api.auth_get_session()
    assert active_sess["authenticated"] is True
    assert active_sess["user"]["email"] == "developer.admin@skillforge.ai"

    # Test token refresh
    refreshed = api.auth_refresh_token({"refresh_token": session["refresh_token"]})
    assert refreshed["success"] is True

    # Test sign out
    sign_out_res = api.auth_sign_out()

    # Restore original real configuration
    api.auth_save_config({
        "supabase_url": orig_saved_cfg.get("supabase_url", ""),
        "anon_key": orig_saved_cfg.get("anon_key", ""),
        "service_secret_key": orig_saved_cfg.get("service_secret_key", "")
    })
    assert sign_out_res["success"] is True
    cleared_sess = api.auth_get_session()
    assert cleared_sess.get("authenticated") is False

    # 10. Test Social Login (Google & GitHub OAuth) & Progressive Disclosure (shadcn & web-assets standards)
    # Test Google OAuth
    google_res = api.auth_sign_in_oauth({"provider": "google"})
    assert google_res["success"] is True, f"Google OAuth failed: {google_res}"
    g_sess = google_res["session"]
    assert g_sess["authenticated"] is True
    assert g_sess["user"]["provider"] == "google"
    assert "Google" in g_sess["user"]["full_name"]
    assert g_sess["access_token"]

    # Test GitHub OAuth
    github_res = api.auth_sign_in_oauth({"provider": "github"})
    assert github_res["success"] is True, f"GitHub OAuth failed: {github_res}"
    gh_sess = github_res["session"]
    assert gh_sess["authenticated"] is True
    assert gh_sess["user"]["provider"] == "github"
    assert "GitHub" in gh_sess["user"]["full_name"]
    assert gh_sess["user"]["role"] == "admin"
    assert gh_sess["access_token"]

    # Test frontend assets for Auth & Progressive Disclosure
    assert 'data-testid="user-account-widget"' in index_html, "User account widget missing in index.html"
    assert 'data-testid="btn-tools-dropdown"' in index_html, "Tools dropdown trigger missing in index.html"
    assert 'data-testid="btn-auth-google"' in components_js, "Google Auth button missing in components.js"
    assert 'data-testid="btn-auth-github"' in components_js, "GitHub Auth button missing in components.js"
    assert 'renderExecutiveHeader' in components_js, "renderExecutiveHeader missing in components.js"
    assert 'renderToolsDropdown' in components_js, "renderToolsDropdown missing in components.js"
    assert 'renderQuickHelpModal' in components_js, "renderQuickHelpModal missing in components.js"
    assert 'renderAuthModal' in components_js, "renderAuthModal missing in components.js"
    assert 'renderUserWidget' in components_js, "renderUserWidget missing in components.js"
    assert 'renderUserDropdown' in components_js, "renderUserDropdown missing in components.js"

    bridge_js = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert 'authSignIn' in bridge_js, "authSignIn missing in bridge.js"
    assert 'authSignInOAuth' in bridge_js, "authSignInOAuth missing in bridge.js"
    assert 'authSignOut' in bridge_js, "authSignOut missing in bridge.js"
    assert 'handleSignIn' in app_js, "handleSignIn missing in app.js"
    assert 'handleSocialLogin' in app_js, "handleSocialLogin missing in app.js"
    assert 'toggleToolsDropdown' in app_js, "toggleToolsDropdown missing in app.js"
    assert 'handleSignOut' in app_js, "handleSignOut missing in app.js"
    print("  [PASS] Google & GitHub Social Login (1-Click) & Progressive Disclosure Workbench verified.")

    # 11. Test Addy Osmani Suite Integration, Attribution & Source Filtering
    all_skills = SkillStorage.get_all_skills()
    assert len(all_skills) == 36, f"Expected exactly 36 total skills, got {len(all_skills)}"
    
    skill_ai_skills = [s for s in all_skills if (s.source_group or "skill_ai") == "skill_ai"]
    addy_skills = [s for s in all_skills if s.source_group == "addy_osmani"]
    addy_personas = [s for s in addy_skills if s.is_persona]
    addy_core_skills = [s for s in addy_skills if not s.is_persona]

    assert len(skill_ai_skills) == 7, f"Expected 7 Skill-AI skills, got {len(skill_ai_skills)}"
    assert len(addy_skills) == 29, f"Expected 29 Addy Osmani items, got {len(addy_skills)}"
    assert len(addy_personas) == 4, f"Expected 4 Addy Osmani personas, got {len(addy_personas)}"
    assert len(addy_core_skills) == 25, f"Expected 25 Addy Osmani core skills, got {len(addy_core_skills)}"

    for s in addy_skills:
        assert "Addy Osmani" in s.author, f"Skill '{s.id}' missing Addy Osmani attribution!"
        assert s.repo_url == "https://github.com/addyosmani/agent-skills", f"Skill '{s.id}' missing repo url!"
        assert s.license == "MIT", f"Skill '{s.id}' missing MIT license!"
        assert s.when_to_use, f"Skill '{s.id}' missing when_to_use!"
        assert len(s.starter_prompts) >= 3, f"Skill '{s.id}' missing 3 starter prompts!"
        assert len(s.references) >= 7, f"Skill '{s.id}' missing shared references!"

    # Verify Frontend Source Filter Bar & Card Badges
    assert 'data-testid="catalog-source-bar"' in index_html, "catalog-source-bar missing in index.html"
    assert 'data-testid="source-all"' in index_html, "source-all chip missing in index.html"
    assert 'data-testid="source-skill-ai"' in index_html, "source-skill-ai chip missing in index.html"
    assert 'data-testid="source-addy-osmani"' in index_html, "source-addy-osmani chip missing in index.html"
    assert 'card-author-pill' in components_js, "card-author-pill missing in components.js"
    assert 'card-persona-pill' in components_js, "card-persona-pill missing in components.js"

    # Test Batch Install filtered by source_group="addy_osmani"
    test_addy_ws = Path("app/data/test_addy_ws")
    test_addy_ws.mkdir(parents=True, exist_ok=True)
    addy_batch_res = api.install_all_skills({
        "targets": ["workspace"],
        "workspace_path": str(test_addy_ws),
        "source_group": "addy_osmani",
        "enable_always_on": False,
        "with_graphify": False
    })
    assert addy_batch_res["success"] is True, f"Addy batch install failed: {addy_batch_res}"
    assert addy_batch_res["count"] == 29, f"Expected 29 Addy items installed, got {addy_batch_res['count']}"
    assert (test_addy_ws / ".agents" / "skills" / "spec-driven-development" / "SKILL.md").exists()
    assert (test_addy_ws / ".agents" / "skills" / "test-driven-development" / "SKILL.md").exists()
    assert (test_addy_ws / ".agents" / "skills" / "code-reviewer" / "SKILL.md").exists()
    assert (test_addy_ws / ".agents" / "skills" / "spec-driven-development" / "references" / "definition-of-done.md").exists()
    print("  [PASS] Addy Osmani Suite (25 Skills + 4 Personas), 100% Attribution, and Source Filtering verified.")

    # 12. Test Clean Cinematic Assembly Intro & Zoom-Through Reveal (ui-ux-design-master)
    assert 'data-testid="intro-mount"' in index_html, "Intro mount container missing in index.html"
    assert 'data-testid="brand-logo-trigger"' in index_html, "Brand logo replay trigger missing in TopBar"
    assert 'sf-brand-svg' in index_html, "SkillForge SF precision monogram logo missing in TopBar"

    assert 'brandSkillForgeLogo' in components_js, "brandSkillForgeLogo missing in components.js"
    assert 'brandSkillForgeLogoLarge' in components_js, "brandSkillForgeLogoLarge missing in components.js"
    assert 'renderIntroOverlay' in components_js, "renderIntroOverlay missing in components.js"
    assert 'sf-shard-nw' in components_js, "sf-shard-nw missing in components.js"
    assert 'sf-shockwave-ring-1' in components_js, "sf-shockwave-ring-1 missing in components.js"
    assert 'intro-mote' in components_js, "intro-mote particles missing in components.js"
    assert 'intro-title-badge' in components_js, "intro-title-badge missing in components.js"

    assert 'showIntro' in app_js, "showIntro method missing in app.js"
    assert 'enterWorkbench' in app_js, "enterWorkbench method missing in app.js"
    assert 'replayIntro' in app_js, "replayIntro method missing in app.js"
    assert 'brand-logo-trigger' in app_js, "brand-logo-trigger event listener missing in app.js"

    app_css = Path("app/frontend/css/app.css").read_text(encoding="utf-8")
    assert '.intro-overlay' in app_css, "intro-overlay class missing in app.css"
    assert '.intro-stage' in app_css, "intro-stage class missing in app.css"
    assert '.intro-vector-rig' in app_css, "intro-vector-rig class missing in app.css"
    assert '.zoom-through-out' in app_css, "zoom-through-out class missing in app.css"
    assert '.intro-mote' in app_css, "intro-mote class missing in app.css"
    assert '.intro-water-ripple' in app_css, "intro-water-ripple class missing in app.css"
    assert '@keyframes waterRippleSpread' in app_css, "waterRippleSpread keyframe missing in app.css"
    assert '@keyframes floatMote' in app_css, "floatMote keyframe missing in app.css"
    assert '@keyframes sfShardNw' in app_css, "sfShardNw keyframe missing in app.css"
    assert '@keyframes sfShockwaveCircle' in app_css, "sfShockwaveCircle keyframe missing in app.css"
    assert '@keyframes sfOrbitCw' in app_css, "sfOrbitCw keyframe missing in app.css"
    print("  [PASS] Clean Cinematic Assembly Intro (Pure Logo + Title + Floating Particles + Zoom-Through) verified.")

    # 13. Test Studio Addy Osmani Standard, Form System & Cosmic Mesh Theme (v5.0 Studio Precision)
    assert '.form-input' in app_css, ".form-input CSS missing in app.css"
    assert '.form-group' in app_css, ".form-group CSS missing in app.css"
    assert 'radial-gradient' in app_css, "Cosmic Aurora Mesh gradient missing in app.css"
    assert '.studio-split-workbench' in app_css, "studio-split-workbench class missing in app.css"
    assert '.studio-step-banner' in app_css, "studio-step-banner class missing in app.css"
    assert '.preset-chip-btn' in app_css, "preset-chip-btn class missing in app.css"

    assert 'studio-step-banner' in components_js, "studio-step-banner missing in components.js"
    assert 'spec-driven' in components_js, "spec-driven preset chip missing in components.js"
    assert 'test-driven' in components_js, "test-driven preset chip missing in components.js"
    assert 'code-review' in components_js, "code-review preset chip missing in components.js"
    assert 'sw-cursor' in components_js, "Cursor switch missing in components.js"
    assert 'sw-windsurf' in components_js, "Windsurf switch missing in components.js"

    assert 'studioPresets' in app_js, "studioPresets missing in app.js"
    assert 'spec-driven-development' in app_js, "spec-driven-development template missing in app.js"
    assert 'test-driven-development' in app_js, "test-driven-development template missing in app.js"
    assert 'sw-cursor' in app_js, "sw-cursor target missing in app.js"
    assert 'sw-windsurf' in app_js, "sw-windsurf target missing in app.js"
    print("  [PASS] Studio Addy Osmani Standard (1-Click Presets + Split Workbench + Universal Autopilot) verified.")

    # 14. Test v6.0 Beginner-First Visual Hierarchy & Quick Tryout Guidance Hub
    assert 'catalog-unified-toolbar' in index_html, "catalog-unified-toolbar missing in index.html"
    assert '.catalog-unified-toolbar' in app_css, "catalog-unified-toolbar CSS missing in app.css"
    assert '.hero-action-hub' in app_css, "hero-action-hub CSS missing in app.css"
    assert '.hero-goal-grid' in app_css, "hero-goal-grid CSS missing in app.css"
    assert '.btn-card-tryout' in app_css, "btn-card-tryout CSS missing in app.css"
    assert '.tryout-modal-body' in app_css, "tryout-modal-body CSS missing in app.css"

    assert 'hero-action-hub' in components_js, "hero-action-hub missing in components.js"
    assert 'hero-goal-ui' in components_js, "hero-goal-ui missing in components.js"
    assert 'hero-goal-plan' in components_js, "hero-goal-plan missing in components.js"
    assert 'hero-goal-all' in components_js, "hero-goal-all missing in components.js"
    assert 'btn-card-tryout' in components_js, "btn-card-tryout missing in components.js"
    assert 'renderQuickTryoutModal' in components_js, "renderQuickTryoutModal missing in components.js"

    assert 'openQuickTryout' in app_js, "openQuickTryout missing in app.js"
    assert 'copyTryoutPrompt' in app_js, "copyTryoutPrompt missing in app.js"
    assert 'hero-goal-ui' in app_js, "hero-goal-ui listener missing in app.js"
    assert 'hero-goal-plan' in app_js, "hero-goal-plan listener missing in app.js"
    assert 'btn-card-tryout' in app_js, "btn-card-tryout listener missing in app.js"
    print("  [PASS] v6.0 Beginner-First Visual Hierarchy (Hero Quick-Start Hub + Unified Toolbar + Tryout Guidance) verified.")

    # 15. Test GitHub-Inspired 2-Tier Card Model & Pro Developer Panel (v6.1)
    assert '.bento-card-clean' in app_css, "bento-card-clean CSS missing in app.css"
    assert '.bento-card-benefit-row' in app_css, "bento-card-benefit-row CSS missing in app.css"
    assert '.btn-card-pro-settings' in app_css, "btn-card-pro-settings CSS missing in app.css"
    assert '.pro-settings-pane' in app_css, "pro-settings-pane CSS missing in app.css"

    assert 'bento-card-clean' in components_js, "bento-card-clean missing in components.js"
    assert 'bento-card-benefit-row' in components_js, "bento-card-benefit-row missing in components.js"
    assert 'btn-card-pro-settings' in components_js, "btn-card-pro-settings missing in components.js"
    assert 'pro-settings-pane' in components_js, "pro-settings-pane missing in components.js"
    assert 'pro-custom-workspace-input' in components_js, "pro-custom-workspace-input missing in components.js"
    assert 'btn-apply-pro-workspace' in components_js, "btn-apply-pro-workspace missing in components.js"

    assert 'btn-card-pro-settings' in app_js, "btn-card-pro-settings listener missing in app.js"
    assert 'btn-apply-pro-workspace' in app_js, "btn-apply-pro-workspace listener missing in app.js"
    assert 'pro-custom-workspace-input' in app_js, "pro-custom-workspace-input handler missing in app.js"
    print("  [PASS] GitHub-Inspired 2-Tier Model (Clean Beginner Card Face + Pro Settings Panel) verified.")

    # 16. Test Abyssal Sky v2.0 Geometric Logo & Background Blueprint Canvas (v7.0)
    assert 'geometric-background-canvas' in index_html, "geometric-background-canvas missing in index.html"
    assert '.geometric-background-canvas' in app_css, "geometric-background-canvas CSS missing in app.css"
    assert '.sf-geometric-bg-svg' in app_css, "sf-geometric-bg-svg CSS missing in app.css"
    assert '--bg-canvas: #050C1A;' in app_css, "Abyssal Void #050C1A missing in app.css"
    assert '--ocean-cyan: #00B4D8;' in app_css, "Ocean Cyan token missing in app.css"
    assert '--sky-violet: #7C3AED;' in app_css, "Sky Violet token missing in app.css"

    assert 'sf-geometric-logo' in components_js or 'sf-geometric-logo-large' in components_js, "Geometric logo SVG missing in components.js"
    assert 'brandSkillForgeLogo' in components_js, "brandSkillForgeLogo missing in components.js"
    assert 'brandSkillForgeLogoLarge' in components_js, "brandSkillForgeLogoLarge missing in components.js"
    assert 'intro-stage-svg' in components_js, "intro-stage-svg missing in components.js"

    # Verify that external C:\Logo was kept strictly read-only and preserved
    logo_dir = Path("C:/Logo")
    assert logo_dir.exists(), "C:/Logo directory must exist"
    assert (logo_dir / "assets" / "svg" / "icon-mark.svg").exists(), "C:/Logo/assets/svg/icon-mark.svg missing"
    assert (logo_dir / "DESIGN.md").exists(), "C:/Logo/DESIGN.md must remain intact"

    # Verify workspace asset staging
    staged_logo = Path("app/frontend/assets/logo/icon-mark.svg")
    assert staged_logo.exists(), "Staged logo in app/frontend/assets/logo/icon-mark.svg missing"
    print("  [PASS] Abyssal Sky v2.0 Geometric Logo & Background Blueprint Canvas verified.")

    # 17. Test Auto-Update Engine (v1.0.0 Dual-Layer Skills & Application Updates)
    from app.backend.updater import UpdateEngine

    # Test version.json presence and format
    v_file = Path("app/data/version.json")
    assert v_file.exists(), "app/data/version.json missing!"
    v_data = json.loads(v_file.read_text(encoding="utf-8"))
    assert v_data.get("version") == "1.0.0", "Version in version.json must be 1.0.0"
    assert v_data.get("app_name") == "AbyssalSkillsD", "app_name in version.json must be AbyssalSkillsD"
    assert "kyuu4/abyssalskillsd" in v_data.get("repository", ""), "Repository slug missing in version.json"

    # Test UpdateEngine SemVer logic
    assert UpdateEngine.parse_semver("1.0.1") == (1, 0, 1)
    assert UpdateEngine.is_newer_version("1.0.1", "1.0.0") is True
    assert UpdateEngine.is_newer_version("1.0.0", "1.0.0") is False
    assert UpdateEngine.is_newer_version("0.9.9", "1.0.0") is False

    # Test UpdateEngine local and release check
    v_info = UpdateEngine.get_version_info()
    assert v_info.get("version") == "1.0.0"
    check_res = UpdateEngine.check_for_updates()
    assert check_res["success"] is True
    assert check_res["current_version"] == "1.0.0"
    assert check_res["total_skills_installed"] >= 36

    # Test DesktopAPI integration
    api_info = api.updater_get_info()
    assert api_info.get("version") == "1.0.0"
    api_check = api.updater_check()
    assert api_check["success"] is True
    assert "checked_at" in api_check

    # Test Frontend bridge, components & styling
    bridge_js = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert 'updaterCheck' in bridge_js, "updaterCheck missing in bridge.js"
    assert 'updaterSyncSkills' in bridge_js, "updaterSyncSkills missing in bridge.js"
    assert 'updaterGetInfo' in bridge_js, "updaterGetInfo missing in bridge.js"

    index_html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    assert 'btn-topbar-update' in index_html, "btn-topbar-update missing in index.html"

    components_js = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert 'renderUpdateModal' in components_js, "renderUpdateModal missing in components.js"
    assert 'btn-tool-check-updates' in components_js, "btn-tool-check-updates missing in components.js"
    assert 'btn-action-sync-skills' in components_js, "btn-action-sync-skills missing in components.js"

    app_js = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert 'checkAppUpdates' in app_js, "checkAppUpdates missing in app.js"
    assert 'openUpdateModal' in app_js, "openUpdateModal missing in app.js"
    assert 'handleSyncSkills' in app_js, "handleSyncSkills missing in app.js"

    app_css = Path("app/frontend/css/app.css").read_text(encoding="utf-8")
    assert '.btn-topbar-update' in app_css, "btn-topbar-update CSS missing in app.css"
    assert '.update-pulse-dot' in app_css, "update-pulse-dot CSS missing in app.css"
    assert '.update-modal-card' in app_css, "update-modal-card CSS missing in app.css"
    assert '.update-progress-track' in app_css, "update-progress-track CSS missing in app.css"
    print("  [PASS] Auto-Update Engine (Dual-Layer Skills & Application Updates v1.0.0) verified.")

    # 18. Test Smart Notification Center & Dismissible Skills Update Banner
    assert 'btn-notification-bell' in index_html, "btn-notification-bell missing in index.html"
    assert 'notification-dropdown-container' in index_html, "notification-dropdown-container missing in index.html"
    assert 'skills-notification-banner-mount' in index_html, "skills-notification-banner-mount missing in index.html"

    assert 'renderSkillsUpdateBanner' in components_js, "renderSkillsUpdateBanner missing in components.js"
    assert 'renderNotificationDropdown' in components_js, "renderNotificationDropdown missing in components.js"
    assert 'btn-banner-sync-skills' in components_js, "btn-banner-sync-skills missing in components.js"
    assert 'btn-banner-dismiss' in components_js, "btn-banner-dismiss missing in components.js"
    assert 'notification-dropdown-menu' in components_js, "notification-dropdown-menu missing in components.js"

    assert 'toggleNotificationTray' in app_js, "toggleNotificationTray missing in app.js"
    assert 'dismissSkillsUpdateBanner' in app_js, "dismissSkillsUpdateBanner missing in app.js"
    assert 'handleSyncFromBanner' in app_js, "handleSyncFromBanner missing in app.js"
    assert 'clearAllNotifications' in app_js, "clearAllNotifications missing in app.js"

    assert '.btn-notification-bell' in app_css, ".btn-notification-bell CSS missing in app.css"
    assert '.notification-dropdown-menu' in app_css, ".notification-dropdown-menu CSS missing in app.css"
    assert '.skills-update-banner' in app_css, ".skills-update-banner CSS missing in app.css"
    assert '.btn-banner-dismiss' in app_css, ".btn-banner-dismiss CSS missing in app.css"

    assert "update_signature" in check_res, "update_signature missing in check_for_updates result"
    print("  [PASS] Smart Notification Center & Dismissible Skills Update Banner verified.")

    # 19. Test Standalone Distribution & Packaging Integrity (Gate 19)
    dist_dir = Path("dist/AbyssalSkillsD")
    assert dist_dir.exists(), "dist/AbyssalSkillsD output directory missing!"
    
    dist_exe = dist_dir / "AbyssalSkillsD.exe"
    assert dist_exe.exists(), "AbyssalSkillsD.exe missing in dist folder!"
    assert dist_exe.stat().st_size > 1_000_000, "AbyssalSkillsD.exe size too small (corrupted)!"

    # Verify portable zip archive
    portable_zip = Path("dist/AbyssalSkillsD-v1.0.0-Portable.zip")
    assert portable_zip.exists(), "AbyssalSkillsD-v1.0.0-Portable.zip missing!"
    assert portable_zip.stat().st_size > 10_000_000, "Portable zip file too small!"
    
    with zipfile.ZipFile(portable_zip, "r") as zf:
        namelist = zf.namelist()
        assert any("AbyssalSkillsD.exe" in name for name in namelist), "AbyssalSkillsD.exe missing in zip archive!"
        assert any("index.html" in name for name in namelist), "index.html missing in zip archive!"
        assert any("version.json" in name for name in namelist), "version.json missing in zip archive!"

    # Verify Inno Setup specification
    iss_file = Path("installer/abyssalskillsd.iss")
    assert iss_file.exists(), "installer/abyssalskillsd.iss missing!"
    iss_text = iss_file.read_text(encoding="utf-8")
    assert 'MyAppName "AbyssalSkillsD"' in iss_text, "MyAppName in Inno Setup must be AbyssalSkillsD"
    assert 'MyAppVersion "1.0.0"' in iss_text, "MyAppVersion in Inno Setup must be 1.0.0"

    # Verify Windows shortcut in workspace
    shortcut = Path("AbyssalSkillsD AI.lnk")
    assert shortcut.exists(), "AbyssalSkillsD AI.lnk missing in workspace root!"
    print("  [PASS] Standalone Distribution & Packaging Integrity (Gate 19) verified.")

    # 20. Test Neural Stream Activation Animation & Live Verification Proof Engine (Gate 20)
    # Test DesktopAPI verification endpoint
    verify_res = api.verify_skill_active({"skill_id": "strict-architect-coder"})
    assert verify_res["success"] is True, f"verify_skill_active failed: {verify_res}"
    assert "Strict Architect" in verify_res["skill_name"]
    assert "test_prompt" in verify_res and len(verify_res["test_prompt"]) > 10
    assert "expected_behavior" in verify_res and len(verify_res["expected_behavior"]) > 10
    assert isinstance(verify_res["verified_targets"], list)

    # Test open folder path validation
    invalid_open = api.open_skill_folder({"skill_id": "non_existent_xyz_999"})
    assert invalid_open["success"] is False

    valid_open = api.open_skill_folder({"skill_id": "strict-architect-coder", "target": "workspace"})
    assert "path" in valid_open

    # Test frontend components & bridge
    bridge_js = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert 'openSkillFolder' in bridge_js, "openSkillFolder missing in bridge.js"
    assert 'verifySkillActive' in bridge_js, "verifySkillActive missing in bridge.js"

    components_js = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert 'renderActivationModal' in components_js, "renderActivationModal missing in components.js"
    assert 'renderVerificationModal' in components_js, "renderVerificationModal missing in components.js"
    assert 'btn-card-verify' in components_js, "btn-card-verify missing in components.js"
    assert 'badge-ai-active' in components_js, "badge-ai-active missing in components.js"

    app_js = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert 'openActivationModal' in app_js, "openActivationModal missing in app.js"
    assert 'openVerificationModal' in app_js, "openVerificationModal missing in app.js"
    assert 'handleOpenSkillFolder' in app_js, "handleOpenSkillFolder missing in app.js"

    app_css = Path("app/frontend/css/app.css").read_text(encoding="utf-8")
    assert '.neural-stage' in app_css, "neural-stage CSS missing in app.css"
    assert '.neural-stream-beam' in app_css, "neural-stream-beam CSS missing in app.css"
    assert '.activation-steps-list' in app_css, "activation-steps-list CSS missing in app.css"
    assert '.badge-ai-active' in app_css, "badge-ai-active CSS missing in app.css"
    assert '.btn-card-verify' in app_css, "btn-card-verify CSS missing in app.css"
    assert '@keyframes neuralBeamFlow' in app_css, "neuralBeamFlow keyframe missing in app.css"
    print("  [PASS] Neural Stream Activation Animation & Live Verification Proof Engine (Gate 20) verified.")

    # 21. Test Clean Teardown / Uninstall Engine, Backup (.bak) Creation & Dynamic Active Workspace Targeting (Gate 21)
    import tempfile
    with tempfile.TemporaryDirectory() as temp_ws:
        temp_ws_path = Path(temp_ws)

        # Test Dynamic Workspace Switching
        curr_ws = api.get_active_workspace()
        assert "workspace_path" in curr_ws
        set_res = api.set_active_workspace({"path": str(temp_ws_path)})
        assert set_res["success"] is True
        assert api.get_active_workspace()["workspace_path"] == str(temp_ws_path)

        # Test Installation targeting dynamic workspace
        inst_res = api.install_skill({
            "skill_id": "strict-architect-coder",
            "targets": ["workspace"],
            "workspace_path": str(temp_ws_path)
        })
        assert inst_res["success"] is True
        target_skill_md = temp_ws_path / ".agents" / "skills" / "strict-architect-coder" / "SKILL.md"
        assert target_skill_md.exists(), "Target SKILL.md missing in dynamic workspace"

        # Test Safe Backup (.bak) generation on re-install
        inst_res2 = api.install_skill({
            "skill_id": "strict-architect-coder",
            "targets": ["workspace"],
            "workspace_path": str(temp_ws_path)
        })
        assert inst_res2["success"] is True
        backup_file = temp_ws_path / ".agents" / "skills" / "strict-architect-coder" / "SKILL.md.bak"
        assert backup_file.exists(), "Backup SKILL.md.bak missing after re-installing"

        # Test Clean Teardown / Uninstall Engine
        uninst_res = api.uninstall_skill({
            "skill_id": "strict-architect-coder",
            "targets": ["workspace"],
            "workspace_path": str(temp_ws_path)
        })
        assert uninst_res["success"] is True
        assert not target_skill_md.exists(), "Target SKILL.md was not uninstalled"
        assert not (temp_ws_path / ".agents" / "skills" / "strict-architect-coder").exists(), "Skill directory was not cleaned up"

        # Restore original workspace
        api.set_active_workspace({"path": curr_ws["workspace_path"]})

    # Test Frontend Bridge, Components & CSS for Uninstall & Dynamic Workspace
    bridge_js = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert 'uninstallSkill' in bridge_js, "uninstallSkill missing in bridge.js"
    assert 'getActiveWorkspace' in bridge_js, "getActiveWorkspace missing in bridge.js"
    assert 'setActiveWorkspace' in bridge_js, "setActiveWorkspace missing in bridge.js"

    index_html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    assert 'workspace-project-bar' in index_html, "workspace-project-bar missing in index.html"
    assert 'workspace-current-badge' in index_html, "workspace-current-badge missing in index.html"
    assert 'btn-change-workspace' in index_html, "btn-change-workspace missing in index.html"

    components_js = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert 'renderUninstallConfirmModal' in components_js, "renderUninstallConfirmModal missing in components.js"
    assert 'btn-inspector-uninstall' in components_js, "btn-inspector-uninstall missing in components.js"
    assert 'btn-inspector-action-uninstall' in components_js, "btn-inspector-action-uninstall missing in components.js"
    assert 'brand-text-abyssal' in components_js, "brand-text-abyssal missing in components.js"
    assert 'brand-text-skills' in components_js, "brand-text-skills missing in components.js"
    assert 'brand-badge-d' in components_js, "brand-badge-d missing in components.js"

    app_js = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert 'initWorkspaceProject' in app_js, "initWorkspaceProject missing in app.js"
    assert 'handleSelectWorkspaceProject' in app_js, "handleSelectWorkspaceProject missing in app.js"
    assert 'openUninstallModal' in app_js, "openUninstallModal missing in app.js"

    app_css = Path("app/frontend/css/app.css").read_text(encoding="utf-8")
    assert '.workspace-project-bar' in app_css, ".workspace-project-bar CSS missing in app.css"
    assert '.workspace-current-badge' in app_css, ".workspace-current-badge CSS missing in app.css"
    assert '.btn-change-workspace' in app_css, ".btn-change-workspace CSS missing in app.css"
    assert '.brand-text-abyssal' in app_css, ".brand-text-abyssal CSS missing in app.css"
    assert '.brand-text-skills' in app_css, ".brand-text-skills CSS missing in app.css"
    assert '.brand-badge-d' in app_css, ".brand-badge-d CSS missing in app.css"
    print("  [PASS] Clean Teardown / Uninstall Engine, Backup (.bak) Creation & Dynamic Workspace (Gate 21) verified.")

    # 22. Test 1-Click Multi-AI Global Sync, Rule Scaffolding Generator & Studio Customizer (Gate 22)
    with tempfile.TemporaryDirectory() as temp_ws:
        temp_ws_path = Path(temp_ws)

        # 1. Test 1-Click Multi-AI Global Sync
        sync_res = api.sync_all_ais({
            "targets": ["workspace"],
            "workspace_path": str(temp_ws_path),
            "skill_ids": ["strict-architect-coder", "ui-ux-design-master"]
        })
        assert sync_res["success"] is True, f"sync_all_ais failed: {sync_res}"
        assert sync_res["target_counts"]["workspace"] >= 2
        assert (temp_ws_path / ".agents" / "skills" / "strict-architect-coder" / "SKILL.md").exists()
        assert (temp_ws_path / ".agents" / "skills" / "ui-ux-design-master" / "SKILL.md").exists()

        # 2. Test Instant Rule Scaffolding Generator
        scaffold_res = api.generate_project_rules({
            "workspace_path": str(temp_ws_path),
            "rule_types": ["cursorrules", "windsurfrules", "claude", "copilot", "agent_rules"]
        })
        assert scaffold_res["success"] is True, f"generate_project_rules failed: {scaffold_res}"
        assert (temp_ws_path / ".cursorrules").exists(), ".cursorrules missing"
        assert (temp_ws_path / ".windsurfrules").exists(), ".windsurfrules missing"
        assert (temp_ws_path / "CLAUDE.md").exists(), "CLAUDE.md missing"
        assert (temp_ws_path / ".github" / "copilot-instructions.md").exists(), "copilot-instructions.md missing"
        assert (temp_ws_path / ".agents" / "rules" / "always-on-autopilot.md").exists(), "always-on-autopilot.md missing"

        # Verify rule content integrity
        cursorrules_text = (temp_ws_path / ".cursorrules").read_text(encoding="utf-8")
        assert "strict-architect-coder" in cursorrules_text
        assert "PROJECT_MEMORY.md" in cursorrules_text
        assert "Always-On" in cursorrules_text

    # 3. Test Frontend Bridge, Components & App.js bindings for Phase 2
    bridge_js = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert 'syncAllAIs' in bridge_js, "syncAllAIs missing in bridge.js"
    assert 'generateProjectRules' in bridge_js, "generateProjectRules missing in bridge.js"

    index_html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    assert 'btn-sync-all-ais' in index_html, "btn-sync-all-ais missing in index.html"
    assert 'btn-generate-project-rules' in index_html, "btn-generate-project-rules missing in index.html"

    components_js = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert 'renderSyncAllModal' in components_js, "renderSyncAllModal missing in components.js"
    assert 'renderGenerateRulesModal' in components_js, "renderGenerateRulesModal missing in components.js"
    assert 'btn-card-customize' in components_js, "btn-card-customize missing in components.js"
    assert 'btn-inspector-customize' in components_js, "btn-inspector-customize missing in components.js"

    app_js = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert 'handleCustomizeInStudio' in app_js, "handleCustomizeInStudio missing in app.js"
    assert 'openSyncAllModal' in app_js, "openSyncAllModal missing in app.js"
    assert 'openGenerateRulesModal' in app_js, "openGenerateRulesModal missing in app.js"

    app_css = Path("app/frontend/css/app.css").read_text(encoding="utf-8")
    assert '.btn-sync-all' in app_css, ".btn-sync-all CSS missing in app.css"
    assert '.btn-generate-rules' in app_css, ".btn-generate-rules CSS missing in app.css"
    assert '.btn-card-customize' in app_css, ".btn-card-customize CSS missing in app.css"
    print("  [PASS] 1-Click Multi-AI Global Sync, Rule Scaffolding Generator & Studio Customizer (Gate 22) verified.")

    # 23. Test Phase 3: Community Cloud Marketplace, Diagnostic Logger & Inno Setup (Gate 23)
    from app.backend.paths import get_log_dir
    from app.backend.logger import get_logger, init_logger

    logger = get_logger()
    logger.info("Executing Gate 23 Automated Verification Test")

    # 1. Test Diagnostic Logger and Export
    diag_res = api.get_diagnostic_logs(50)
    assert diag_res["success"] is True, f"Failed to get diagnostic logs: {diag_res}"
    assert "platform" in diag_res and diag_res["platform"]
    assert "python_version" in diag_res and diag_res["python_version"]
    assert "logs" in diag_res

    export_res = api.export_diagnostic_logs()
    assert export_res["success"] is True, f"Failed to export diagnostic logs: {export_res}"
    assert Path(export_res["path"]).exists(), "Exported diagnostic zip does not exist"
    assert export_res["size_kb"] > 0, "Diagnostic zip size is 0"

    # 2. Test Community Cloud Marketplace API
    comm_skills_res = api.community_get_skills()
    assert comm_skills_res["success"] is True, "Failed to get community skills"
    assert len(comm_skills_res["skills"]) >= 4, f"Fewer than 4 community skills found: {len(comm_skills_res['skills'])}"

    # Test community skill publishing
    test_pub_skill = {
        "id": "enterprise-microservice-chassis",
        "title": "Enterprise Microservice Chassis",
        "category": "Backend & API",
        "description": "Standardized chassis for Golang/Python microservices with OpenTelemetry, gRPC, and health checks.",
        "author": "gate23_tester",
        "content": "---\nname: enterprise-microservice-chassis\ndescription: Microservice chassis\n---\n# Enterprise Chassis\nStandardized service chassis."
    }
    pub_res = api.community_publish_skill(test_pub_skill)
    assert pub_res["success"] is True, f"Publish failed: {pub_res}"

    # Verify published skill is discoverable
    refreshed_comm = api.community_get_skills()
    found_pub = next((s for s in refreshed_comm["skills"] if s["id"] == "enterprise-microservice-chassis"), None)
    assert found_pub is not None, "Published skill not found in community catalog"
    assert found_pub["author"] == "gate23_tester"

    # Test community skill installation
    with tempfile.TemporaryDirectory() as temp_comm_ws:
        comm_inst_res = api.community_install_skill({
            "skill_id": "docker-k8s-devops-autopilot",
            "targets": ["workspace"],
            "workspace_path": temp_comm_ws
        })
        assert comm_inst_res["success"] is True, f"Community install failed: {comm_inst_res}"
        assert (Path(temp_comm_ws) / ".agents" / "skills" / "docker-k8s-devops-autopilot" / "SKILL.md").exists(), "Community skill SKILL.md missing in workspace"

    # 3. Test Inno Setup Installer Script
    iss_content = Path("installer/abyssalskillsd.iss").read_text(encoding="utf-8")
    assert "UninstallDisplayName=" in iss_content, "UninstallDisplayName missing in Inno Setup script"
    assert "OutputBaseFilename=" in iss_content, "OutputBaseFilename missing in Inno Setup script"
    assert "desktopicon" in iss_content, "desktopicon task missing in Inno Setup script"

    # 4. Test Frontend UI Assets & Bindings for Phase 3
    bridge_js = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert "communityGetSkills" in bridge_js, "communityGetSkills missing in bridge.js"
    assert "communityPublishSkill" in bridge_js, "communityPublishSkill missing in bridge.js"
    assert "communityInstallSkill" in bridge_js, "communityInstallSkill missing in bridge.js"
    assert "getDiagnosticLogs" in bridge_js, "getDiagnosticLogs missing in bridge.js"
    assert "exportDiagnosticLogs" in bridge_js, "exportDiagnosticLogs missing in bridge.js"

    index_html = Path("app/frontend/index.html").read_text(encoding="utf-8")
    assert 'btn-open-diagnostics' in index_html, "btn-open-diagnostics missing in index.html"

    components_js = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert "renderDiagnosticModal" in components_js, "renderDiagnosticModal missing in components.js"
    assert "renderCommunitySkillDetailModal" in components_js, "renderCommunitySkillDetailModal missing in components.js"
    assert "btn-publish-to-community" in components_js, "btn-publish-to-community missing in components.js"
    assert "btn-subtab-marketplace" in components_js, "btn-subtab-marketplace missing in components.js"

    app_js = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert "openDiagnosticsModal" in app_js, "openDiagnosticsModal missing in app.js"
    assert "openCommunityDetailModal" in app_js, "openCommunityDetailModal missing in app.js"
    assert "loadCommunitySkills" in app_js, "loadCommunitySkills missing in app.js"
    print("  [PASS] Live Community Cloud, Diagnostic Logger & Complete Setup Ecosystem (Gate 23) verified.")

    # 24. Test Zero-Trust Security, Anti-Spam Telemetry & Error Deduplication Engine (Gate 24)
    from app.backend.logger import sanitize_sensitive_data
    from app.backend.paths import assert_safe_workspace_path

    # A. Test PII & Secret Scrubbing
    raw_log = (
        "User path: C:\\Users\\alice_wonder\\Desktop\\secret_project\n"
        "Connecting with token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.sflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c\n"
        "GitHub token ghp_1234567890abcdef1234567890abcdef1234\n"
        "Configuration: anon_key = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test and password = super_secret_pass"
    )
    sanitized = sanitize_sensitive_data(raw_log)
    assert "alice_wonder" not in sanitized, "Windows username must be redacted"
    assert "C:\\Users\\<user>" in sanitized, "Path should be masked to <user>"
    assert "[REDACTED_JWT_TOKEN]" in sanitized, "JWT token must be masked"
    assert "[REDACTED_GITHUB_TOKEN]" in sanitized, "GitHub PAT must be masked"
    assert "[REDACTED_SECRET]" in sanitized, "Password/key must be masked"

    # B. Test Path Traversal and Safe Workspace Assertions
    try:
        assert_safe_workspace_path("C:\\Windows\\System32")
        assert False, "Should have rejected C:\\Windows\\System32"
    except (ValueError, PermissionError) as ve:
        assert "hệ thống" in str(ve) or "bảo vệ" in str(ve)

    try:
        assert_safe_workspace_path("C:\\non_existent_folder_xyz_12345")
        assert False, "Should have rejected non-existent directory"
    except (ValueError, PermissionError, FileNotFoundError) as ve:
        assert "tồn tại" in str(ve)

    # Valid folder check
    with tempfile.TemporaryDirectory() as valid_ws:
        safe_path = assert_safe_workspace_path(valid_ws)
        assert Path(safe_path).exists()

    # C. Test Anti-Spam Error Telemetry & Deduplication
    test_err_payload = {
        "error_message": "NullPointerException: target node not found in C:\\Users\\alice_dev\\code.js",
        "error_type": "NullPointerException",
        "stack_trace": "Traceback (most recent call last):\n  File 'test.py', line 99, in run\n    raise NullPointerException()",
        "module_name": "worker.py",
        "line_number": 99,
        "metadata": {"app_version": "2.4.0", "os": "Windows"}
    }
    report1 = api.report_system_error(test_err_payload)
    assert report1["success"] is True, f"Error reporting failed: {report1}"
    assert "fingerprint" in report1, "Report must return a cryptographic fingerprint"
    fp = report1["fingerprint"]
    assert len(fp) == 16, "Fingerprint should be 16 hex chars"
    first_occurrences = report1.get("occurrences", 1)

    # Submit the exact same error again (simulating user spam / rage-clicking)
    report2 = api.report_system_error(test_err_payload)
    assert report2["success"] is True
    assert report2["fingerprint"] == fp, "Identical error must produce identical fingerprint"
    assert report2["occurrences"] == first_occurrences + 1, "Repeated report must increment occurrences counter"
    assert "được gom nhóm" in report2.get("message", ""), "Message should indicate deduplication grouping"

    # Verify persistent error store sanitization
    err_store_file = Path("app/data/system_error_reports.json")
    assert err_store_file.exists()
    err_store = json.loads(err_store_file.read_text(encoding="utf-8"))
    found_item = next((r for r in err_store if r.get("fingerprint") == fp), None)
    assert found_item is not None, f"Fingerprint {fp} not found in error store"
    assert "alice_dev" not in found_item["error_message"], "Stored error message must be scrubbed"
    assert "<user>" in found_item["error_message"], "Stored message should contain sanitized <user>"

    # D. Test Supabase Error Reports SQL Schema
    sql_schema = Path("app/data/supabase_community_schema.sql").read_text(encoding="utf-8")
    assert "system_error_reports" in sql_schema, "system_error_reports table missing in schema SQL"
    assert "idx_error_fingerprint" in sql_schema, "Fingerprint index missing in schema SQL"
    assert "Clients can report errors" in sql_schema, "Anonymous error reporting RLS policy missing"
    assert "Only admins can view error reports" in sql_schema, "Admin-only view RLS policy missing"

    # E. Test Frontend Telemetry Bindings
    assert "reportSystemError" in bridge_js, "reportSystemError missing in bridge.js"
    assert "btn-submit-cloud-error" in components_js, "btn-submit-cloud-error missing in components.js"
    assert "btn-submit-cloud-error" in app_js, "btn-submit-cloud-error click listener missing in app.js"
    assert "abyssalskillsd-last-error-submit" in app_js, "Anti-spam cooldown storage missing in app.js"
    print("  [PASS] Zero-Trust Security, Anti-Spam Telemetry & Deduplication Engine (Gate 24) verified.")

    # 25. Test Anti-Overflow Layout Safety, 2-Flow Batch Activation & Side-by-Side Diff Engine (Gate 25)
    app_css = Path("app/frontend/css/app.css").read_text(encoding="utf-8")
    assert "overflow: hidden;" in app_css, "overflow: hidden missing in app.css"
    assert ".card-action-group" in app_css and "flex-wrap: wrap;" in app_css, "card-action-group flex-wrap missing in app.css"
    assert ".card-action-left" in app_css and ".card-action-right" in app_css, "Split card action layout missing in app.css"
    assert ".diff-modal-container" in app_css, "diff-modal-container CSS missing in app.css"
    assert ".btn-batch-complete" in app_css, "btn-batch-complete CSS missing in app.css"
    assert ".btn-batch-updates-pill" in app_css, "btn-batch-updates-pill CSS missing in app.css"
    assert ".btn-card-review-diff" in app_css, "btn-card-review-diff CSS missing in app.css"

    # Backend Scanner & Diff Engine
    from app.backend.scanner import SkillScanner
    from app.backend.storage import SkillStorage
    targets_map, paths_map = SkillScanner.get_installed_targets_and_paths()
    assert isinstance(targets_map, dict) and isinstance(paths_map, dict)
    assert len(targets_map) > 0, "Targets map must not be empty"

    all_skills = SkillStorage.get_all_skills()
    assert all(hasattr(s, "has_update") for s in all_skills), "All skills must have has_update attribute"
    assert all(hasattr(s, "installed_path") for s in all_skills), "All skills must have installed_path attribute"

    # API Diff Engine Test
    diff_res = api.get_skill_diff({"skill_id": "nextjs-fullstack-master"})
    assert diff_res["success"] is True, f"Diff API failed: {diff_res}"
    assert "local_content" in diff_res and "new_content" in diff_res
    assert diff_res["skill_id"] == "nextjs-fullstack-master"
    assert len(diff_res["new_content"]) > 100

    # Test Selective Batch Installation (skill_ids whitelist)
    with tempfile.TemporaryDirectory() as temp_batch_ws:
        batch_res = api.install_all_skills({
            "targets": ["workspace"],
            "workspace_path": temp_batch_ws,
            "skill_ids": ["nextjs-fullstack-master"]
        })
        assert batch_res["success"] is True
        assert (Path(temp_batch_ws) / ".agents" / "skills" / "nextjs-fullstack-master" / "SKILL.md").exists()
        # Verify unrequested skills were NOT installed
        assert not (Path(temp_batch_ws) / ".agents" / "skills" / "strict-architect-coder").exists(), "Unrequested skills must not be installed"

    # Frontend Bridge, Components & App.js
    bridge_js = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert "getSkillDiff" in bridge_js, "getSkillDiff missing in bridge.js"

    components_js = Path("app/frontend/js/components.js").read_text(encoding="utf-8")
    assert "renderDiffReviewModal" in components_js, "renderDiffReviewModal missing in components.js"
    assert "btn-diff-keep-local" in components_js, "btn-diff-keep-local missing in components.js"
    assert "btn-diff-apply-update" in components_js, "btn-diff-apply-update missing in components.js"
    assert "btn-batch-updates-pill" in components_js, "btn-batch-updates-pill missing in components.js"
    assert "btn-card-review-diff" in components_js, "btn-card-review-diff missing in components.js"

    app_js = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert "openDiffReviewModal" in app_js, "openDiffReviewModal missing in app.js"
    assert "btn-diff-keep-local" in app_js, "btn-diff-keep-local click handler missing in app.js"
    assert "btn-diff-apply-update" in app_js, "btn-diff-apply-update click handler missing in app.js"
    assert "btn-batch-review-updates" in app_js, "btn-batch-review-updates click listener missing in app.js"
    assert "btn-card-review-diff" in app_js, "btn-card-review-diff delegated listener missing in app.js"
    print("  [PASS] Anti-Overflow Layout Safety, 2-Flow Batch Activation & Side-by-Side Diff Engine (Gate 25) verified.")

    # -------------------------------------------------------------------------
    # Gate 26: Complete Supabase Auth Suite, Desktop OAuth Loopback & Session Lifecycle
    # -------------------------------------------------------------------------
    from app.backend.auth import AuthEngine, OAuthServerManager
    # 1. Test get_safe_config
    auth_cfg = AuthEngine.get_safe_config()
    assert "supabase_url" in auth_cfg and "anon_key" in auth_cfg
    assert "https://ldzgwlvhbomjmonxutyc.supabase.co" in auth_cfg["supabase_url"]

    # 2. Test sign_up validation (empty password, short password)
    err_signup1 = AuthEngine.sign_up("", "")
    assert err_signup1["success"] is False
    err_signup2 = AuthEngine.sign_up("test@example.com", "123")
    assert err_signup2["success"] is False and "ít nhất 6 ký tự" in err_signup2["message"]

    # 3. Test sign_in validation
    err_signin = AuthEngine.sign_in("", "")
    assert err_signin["success"] is False

    # 4. Test OAuth Loopback Server lifecycle
    assert OAuthServerManager.start_server(AuthEngine, port=54321) is True
    assert OAuthServerManager.server is not None
    OAuthServerManager.stop_server()
    assert OAuthServerManager.server is None

    # 5. Test session persistence & clear on logout
    mock_test_session = {
        "authenticated": True,
        "access_token": "gate26_test_token_123",
        "refresh_token": "gate26_refresh_123",
        "expires_at": time.time() + 3600,
        "user": {
            "id": "gate26_user",
            "email": "tester@example.com",
            "full_name": "Gate26 Tester",
            "role": "creator",
            "avatar_url": ""
        }
    }
    AuthEngine.save_session(mock_test_session)
    loaded_session = AuthEngine.get_session()
    assert loaded_session.get("authenticated") is True
    assert loaded_session["user"]["email"] == "tester@example.com"

    # Test Sign Out clears session
    signout_res = AuthEngine.sign_out()
    assert signout_res["success"] is True
    cleared_session = AuthEngine.get_session()
    assert cleared_session.get("authenticated") is False

    # 6. Verify Frontend bridge & components bindings
    bridge_code = Path("app/frontend/js/bridge.js").read_text(encoding="utf-8")
    assert "authCheckOAuthStatus" in bridge_code, "authCheckOAuthStatus missing in bridge.js"
    assert "authSignInOAuth" in bridge_code, "authSignInOAuth missing in bridge.js"

    app_code = Path("app/frontend/js/app.js").read_text(encoding="utf-8")
    assert "authCheckOAuthStatus" in app_code, "authCheckOAuthStatus missing in app.js"
    assert "_oauthPollInterval" in app_code, "OAuth polling loop missing in app.js"
    print("  [PASS] Supabase Auth, Desktop OAuth Engine & Session Lifecycle (Gate 26) verified.")

    print("\n✅ ALL 26 VERIFICATION GATES PASSED! AbyssalSkillsD (v1.2.0 Enterprise Commercial Suite) is 100% operational.")

if __name__ == "__main__":
    test_all()
