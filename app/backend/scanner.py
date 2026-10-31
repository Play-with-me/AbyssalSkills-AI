"""
AbyssalSkillsD - Scanner & Parser
Parses SKILL.md, YAML frontmatter, references/, rules/, and Graphify reports.
Supports both Skill-AI-private Suite and Addy Osmani's Production-Grade Monorepo.
"""
import os
import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from .models import SkillItem, ReferenceDoc, RuleDoc

class SkillScanner:
    # Mapping for Skill-AI-private Official Suite
    OFFICIAL_METADATA = {
        "strict-architect-coder": {
            "title": "Kiến Trúc Sư & Lập Kế Hoạch Chuẩn (Strict Architect v4.0)",
            "category": "Architecture & Code",
            "use_case_group": "plan_debug",
            "source_group": "skill_ai",
            "when_to_use": "Dùng khi bắt đầu dự án mới, cần lập kế hoạch 2 lớp chi tiết, hỏi đáp làm rõ ý tưởng, hoặc sửa lỗi tìm nguyên nhân gốc rễ.",
            "description": "Quy trình lập trình chuẩn mực: Phỏng vấn làm rõ ý tưởng trước khi code, phân tích điểm trọng yếu (God Nodes), và giải quyết lỗi tận gốc.",
            "icon": "cpu",
            "repo": "https://github.com/Skill-AI-private/Strict-architect-coder.git",
            "author": "Skill-AI Organization",
            "starter_prompts": [
                {
                    "title": "Khởi tạo dự án & Hỏi đáp làm rõ ý tưởng",
                    "prompt": "Tôi muốn làm một ứng dụng [mô tả ngắn ý tưởng], hãy hỏi tôi từng bước bằng tiếng Việt để làm rõ yêu cầu và lập bản kế hoạch chi tiết trước khi code /plan /grill-me"
                },
                {
                    "title": "Bổ sung tính năng mới an toàn",
                    "prompt": "Hãy kiểm tra cấu trúc mã nguồn hiện tại và lập bản kế hoạch bổ sung tính năng [tên tính năng] sao cho không ảnh hưởng code cũ /plan"
                },
                {
                    "title": "Tìm nguyên nhân gốc rễ và sửa dứt điểm lỗi",
                    "prompt": "Ứng dụng đang gặp lỗi [mô tả chi tiết lỗi], hãy phân tích nguyên nhân gốc rễ và đề xuất phương án xử lý triệt để /strict-architect-coder"
                }
            ]
        },
        "ui-ux-design-master": {
            "title": "Chuyên Gia Thiết Kế Giao Diện (UI/UX Design Master)",
            "category": "UI/UX Design",
            "use_case_group": "ui_ux",
            "source_group": "skill_ai",
            "when_to_use": "Dùng khi giao diện còn đại trà, thô sơ hoặc quá 'AI', muốn nâng cấp lên chuẩn Designer chuyên nghiệp, chống tràn khung và hiệu ứng mượt mà.",
            "description": "Bộ quy chuẩn 16-trong-1 kết hợp 118 quy tắc chống giao diện đại trà, thiết kế bảng màu DESIGN.md, hiệu ứng mượt dưới 250ms và bố cục chống tràn.",
            "icon": "palette",
            "repo": "https://github.com/Skill-AI-private/ui-ux-design-master.git",
            "author": "Skill-AI Organization",
            "starter_prompts": [
                {
                    "title": "Nâng cấp giao diện lên chuẩn Designer",
                    "prompt": "Giao diện hiện tại nhìn còn đại trà và quá AI, hãy áp dụng quy chuẩn UI/UX Master để thiết kế lại cho chuyên nghiệp, hiện đại và chuẩn xác /plan"
                },
                {
                    "title": "Kiểm tra và sửa lỗi tràn khung hình",
                    "prompt": "Hãy kiểm tra toàn bộ giao diện và khắc phục triệt để các lỗi tràn chữ, vỡ khung (min-h-0, min-w-0) trên mọi độ phân giải"
                },
                {
                    "title": "Xây dựng bảng màu và tài liệu DESIGN.md",
                    "prompt": "Hãy xây dựng hệ thống quy chuẩn màu sắc, phông chữ và khoảng cách trong tệp DESIGN.md cho dự án"
                }
            ]
        },
        "shadcn-tailwind-artisan": {
            "title": "Nghệ Nhân shadcn/ui & Tailwind CSS",
            "category": "UI/UX Design",
            "use_case_group": "ui_ux",
            "source_group": "skill_ai",
            "when_to_use": "Dùng khi bạn muốn xây dựng các khối giao diện nút bấm, bảng biểu, hộp thoại, thanh điều hướng đẹp chuẩn shadcn và Tailwind v4.",
            "description": "Chế tác linh kiện giao diện shadcn/ui tinh xảo, phối màu Tailwind v4 chuẩn Semantic Tokens, hỗ trợ phím tắt và chế độ Sáng / Tối.",
            "icon": "tailwind",
            "repo": "https://github.com/Skill-AI-private/shadcn-tailwind-artisan.git",
            "author": "Skill-AI Organization",
            "starter_prompts": [
                {
                    "title": "Tạo linh kiện giao diện chuẩn shadcn",
                    "prompt": "Hãy tạo cho tôi linh kiện [tên linh kiện, ví dụ: Bảng thống kê / Hộp thoại] chuẩn phong cách shadcn/ui và Tailwind CSS"
                },
                {
                    "title": "Tích hợp chế độ Sáng / Tối (Dark / Light Mode)",
                    "prompt": "Hãy thiết lập hệ thống chuyển đổi màu sắc Giao diện Sáng và Tối (Dark/Light Mode) hoàn chỉnh bằng biến CSS"
                },
                {
                    "title": "Tối ưu khả năng dùng bàn phím (Accessibility)",
                    "prompt": "Hãy tối ưu khả năng truy cập WAI-ARIA và phím tắt (Tab, ESC, Mũi tên) cho các menu và hộp thoại trong app"
                }
            ]
        },
        "web-assets-creative-vault": {
            "title": "Thư Viện Tài Nguyên Đồ Họa & Icon (Creative Vault)",
            "category": "Design & Assets",
            "use_case_group": "design_assets",
            "source_group": "skill_ai",
            "when_to_use": "Dùng khi bạn cần icon vector SVG sắc nét, logo chính hãng các thương hiệu công nghệ, hoặc hình vẽ minh họa không bản quyền.",
            "description": "Thư viện tổng hợp icon SVG Lucide, Simple Icons (Google, Claude, GitHub...) và hình minh họa unDraw linh hoạt màu sắc.",
            "icon": "sparkles",
            "repo": "https://github.com/Skill-AI-private/web-assets-creative-vault.git",
            "author": "Skill-AI Organization",
            "starter_prompts": [
                {
                    "title": "Tìm và nhúng icon vector SVG",
                    "prompt": "Tôi cần các icon SVG sắc nét nét mảnh (1.5px) cho [danh sách chức năng, ví dụ: Tải xuống, Cài đặt, Tìm kiếm]"
                },
                {
                    "title": "Lấy logo công nghệ chính hãng Simple Icons",
                    "prompt": "Hãy cung cấp mã SVG chính hãng chuẩn vector cho logo của [Google, Next.js, Supabase, Tailwind, GitHub]"
                },
                {
                    "title": "Tạo minh họa khi không có dữ liệu (Empty State)",
                    "prompt": "Hãy tạo một hình minh họa vector unDraw tuyệt đẹp để hiển thị khi người dùng chưa có dữ liệu hoặc tìm kiếm không thấy"
                }
            ]
        },
        "nextjs-fullstack-master": {
            "title": "Chuyên Gia Next.js Full-Stack (App Router)",
            "category": "Full-Stack Web",
            "use_case_group": "web_db",
            "source_group": "skill_ai",
            "when_to_use": "Dùng khi xây dựng ứng dụng web hiện đại với Next.js 15+, React 19 Server Components, tải song song loại bỏ độ trễ.",
            "description": "Kiến trúc Next.js App Router chuẩn mực: Tải dữ liệu song song không chờ đợi (Zero-Waterfall), Server Actions bảo mật và tối ưu SEO.",
            "icon": "nextjs",
            "repo": "https://github.com/Skill-AI-private/nextjs-fullstack-master.git",
            "author": "Skill-AI Organization",
            "starter_prompts": [
                {
                    "title": "Tối ưu hóa Server Components song song",
                    "prompt": "Hãy tái cấu trúc trang [tên trang] để tải song song các khối dữ liệu bằng Promise.all() và Streaming Suspense"
                },
                {
                    "title": "Tạo Server Action bảo mật với Zod",
                    "prompt": "Hãy tạo một Server Action xử lý form [tên form] có kiểm tra dữ liệu đầu vào bằng Zod và xử lý lỗi an toàn"
                },
                {
                    "title": "Kiểm tra và loại bỏ tình trạng tải chậm (Waterfall)",
                    "prompt": "Hãy kiểm tra mã nguồn trang này và tái cấu trúc để loại bỏ hiện tượng gọi API tuần tự làm chậm thời gian tải trang"
                }
            ]
        },
        "supabase-backend-architect": {
            "title": "Kiến Trúc Sư Cơ Sở Dữ Liệu Supabase & RLS",
            "category": "Database & Backend",
            "use_case_group": "web_db",
            "source_group": "skill_ai",
            "when_to_use": "Dùng khi thiết kế cơ sở dữ liệu PostgreSQL trên Supabase, bảo mật Row Level Security (RLS), hoặc cần schema chia sẻ cộng đồng.",
            "description": "Thiết kế cơ sở dữ liệu Supabase PostgreSQL: Phân quyền Row Level Security (RLS) tuyệt đối, tìm kiếm toàn văn Full-Text Search và kết nối SSR an toàn.",
            "icon": "supabase",
            "repo": "https://github.com/Skill-AI-private/supabase-backend-architect.git",
            "author": "Skill-AI Organization",
            "starter_prompts": [
                {
                    "title": "Thiết kế bảng dữ liệu và phân quyền RLS",
                    "prompt": "Hãy thiết kế bảng PostgreSQL [tên bảng] trên Supabase kèm các chính sách bảo mật Row Level Security (RLS) chuẩn mực"
                },
                {
                    "title": "Tạo hàm tìm kiếm nhanh Full-Text Search",
                    "prompt": "Hãy viết câu lệnh SQL tạo chỉ mục GIN và hàm tìm kiếm tiếng Việt toàn văn (Full-Text Search) cho bảng này"
                },
                {
                    "title": "Viết mã kết nối Supabase an toàn trong SSR",
                    "prompt": "Hãy viết mã kết nối và truy vấn dữ liệu từ Supabase client trên Next.js Server Components đảm bảo xác thực cookie"
                }
            ]
        },
        "playwright-web-tester": {
            "title": "Kỹ Sư Kiểm Thử Tự Động (Playwright QA Tester)",
            "category": "Testing & QA",
            "use_case_group": "testing_qa",
            "source_group": "skill_ai",
            "when_to_use": "Dùng khi bạn muốn viết kịch bản tự động kiểm tra xem website có bị lỗi không, chụp ảnh so sánh giao diện và chạy QA trước khi xuất bản.",
            "description": "Kiểm thử tự động End-to-End với Playwright: Giả lập người dùng thật, tự động bấm nút, kiểm tra lỗi giao diện và hỗ trợ đa thiết bị.",
            "icon": "playwright",
            "repo": "https://github.com/Skill-AI-private/playwright-web-tester.git",
            "author": "Skill-AI Organization",
            "starter_prompts": [
                {
                    "title": "Viết kịch bản kiểm thử luồng người dùng",
                    "prompt": "Hãy viết kịch bản Playwright E2E để tự động kiểm tra toàn bộ luồng [đăng nhập / tìm kiếm / cài đặt kỹ năng]"
                },
                {
                    "title": "Kiểm tra độ phản hồi trên điện thoại & máy tính",
                    "prompt": "Hãy viết bài test Playwright kiểm tra giao diện trên cả màn hình di động (iPhone/Android) và máy tính để bàn"
                },
                {
                    "title": "Chẩn đoán nguyên nhân bài test bị trượt",
                    "prompt": "Kịch bản kiểm thử Playwright đang báo lỗi tại bước [tên bước], hãy tìm nguyên nhân và sửa lại cho ổn định"
                }
            ]
        }
    }

    # Metadata for Addy Osmani's 25 Skills + 4 Personas Suite
    ADDY_OSMANI_METADATA = {
        "using-agent-skills": {
            "title": "Agent Skills Meta-Router",
            "category": "Meta",
            "use_case_group": "plan_debug",
            "icon": "command",
            "when_to_use": "Use when starting a session or deciding which skill workflow to apply to incoming tasks.",
            "description": "Maps incoming engineering tasks to the right skill workflow and defines shared operating rules.",
            "starter_prompts": [
                {"title": "Route Task to Optimal Skill", "prompt": "/using-agent-skills Analyze my incoming task and recommend the best engineering workflow."},
                {"title": "Check Active SDLC Quality Gates", "prompt": "/using-agent-skills Audit active quality gates and anti-rationalization guidelines for this session."},
                {"title": "Recommend Development Workflow", "prompt": "/using-agent-skills Suggest the optimal lifecycle path from spec to ship for [feature name]."}
            ]
        },
        "interview-me": {
            "title": "Interview Me (Requirements Discovery)",
            "category": "Define",
            "use_case_group": "plan_debug",
            "icon": "sparkles",
            "when_to_use": "Use when requirements are ambiguous, underspecified, or when invoking 'interview me' or 'grill me'.",
            "description": "One-question-at-a-time interview that extracts true requirements until ~95% confidence before coding.",
            "starter_prompts": [
                {"title": "Interrogate Project Scope", "prompt": "/agent-skills:interview-me Ask me one question at a time to clarify the scope of [feature name]."},
                {"title": "Challenge Design Assumptions", "prompt": "/agent-skills:interview-me Grill me on edge cases, user roles, and system constraints for this architecture."},
                {"title": "Extract Technical PRD Essentials", "prompt": "/agent-skills:interview-me Interview me step-by-step until we reach 95% confidence on technical specs."}
            ]
        },
        "idea-refine": {
            "title": "Idea Refinement",
            "category": "Define",
            "use_case_group": "plan_debug",
            "icon": "sparkles",
            "when_to_use": "Use when you have a rough concept that needs structured exploration into a concrete proposal.",
            "description": "Structured divergent and convergent thinking framework to turn rough concepts into concrete proposals.",
            "starter_prompts": [
                {"title": "Brainstorm and Refine Idea", "prompt": "/agent-skills:idea-refine Help me turn my rough concept [idea description] into a structured proposal."},
                {"title": "Explore Architectural Trade-offs", "prompt": "/agent-skills:idea-refine Analyze alternative approaches, pros, and cons for [proposed solution]."},
                {"title": "Converge on Concrete Proposal", "prompt": "/agent-skills:idea-refine Synthesize our brainstorming into an actionable technical proposal."}
            ]
        },
        "spec-driven-development": {
            "title": "Spec-Driven Development (PRD)",
            "category": "Define",
            "use_case_group": "plan_debug",
            "icon": "fileText",
            "when_to_use": "Use when starting a new project, feature, or significant change and no specification exists yet.",
            "description": "Write a structured PRD covering objectives, commands, structure, code style, testing, and boundaries before coding.",
            "starter_prompts": [
                {"title": "Draft Feature Specification", "prompt": "/agent-skills:spec-driven-development Draft a comprehensive PRD and technical spec document for [new feature]."},
                {"title": "Decompose Capability Map", "prompt": "/agent-skills:spec-driven-development Create a capability map of modules before specifying implementation details."},
                {"title": "Define Boundaries & Acceptance", "prompt": "/agent-skills:spec-driven-development Specify input boundaries, error semantics, and verification exit criteria."}
            ]
        },
        "constraint-driven-development": {
            "title": "Constraint-Driven Development",
            "category": "Define",
            "use_case_group": "testing_qa",
            "icon": "lock",
            "when_to_use": "Use when no quality standards are written down, or to catch agents silencing checks or skipping tests.",
            "description": "Interviews for a quality bar with sane default thresholds, writes CONSTRAINTS.md, and catches silenced checks.",
            "starter_prompts": [
                {"title": "Establish Project Quality Bar", "prompt": "/agent-skills:constraint-driven-development Interview me and write CONSTRAINTS.md for this repo."},
                {"title": "Enforce Test Thresholds", "prompt": "/agent-skills:constraint-driven-development Verify all quality gates and ensure no tests or linter checks are silenced."},
                {"title": "Audit Project Constraints", "prompt": "/agent-skills:constraint-driven-development Audit code against our established architectural constraints."}
            ]
        },
        "planning-and-task-breakdown": {
            "title": "Planning & Task Breakdown",
            "category": "Plan",
            "use_case_group": "plan_debug",
            "icon": "layers",
            "when_to_use": "Use when you have a spec and need to break it down into small, verifiable, dependency-ordered tasks.",
            "description": "Decomposes specs into small, verifiable tasks with clear acceptance criteria and dependency ordering.",
            "starter_prompts": [
                {"title": "Decompose Spec into Tasks", "prompt": "/agent-skills:planning-and-task-breakdown Break down the approved spec into atomic tasks under 100 lines each."},
                {"title": "Map Dependency Build Order", "prompt": "/agent-skills:planning-and-task-breakdown Order implementation tasks by dependency direction with zero cycles."},
                {"title": "Define Task Verification Criteria", "prompt": "/agent-skills:planning-and-task-breakdown Define exact automated verification commands for each task."}
            ]
        },
        "incremental-implementation": {
            "title": "Incremental Implementation",
            "category": "Build",
            "use_case_group": "web_db",
            "icon": "cpu",
            "when_to_use": "Use for any code change touching multiple files: build thin vertical slices with feature flags and safe defaults.",
            "description": "Thin vertical slices — implement, test, verify, commit. Emphasizes rollback-friendly changes and safe defaults.",
            "starter_prompts": [
                {"title": "Implement Thin Vertical Slice", "prompt": "/agent-skills:incremental-implementation Build task 1 as an atomic vertical slice and verify immediately."},
                {"title": "Add Feature Flag Guard", "prompt": "/agent-skills:incremental-implementation Wrap new functionality in a safe feature flag with default-off behavior."},
                {"title": "Step-by-Step Verified Execution", "prompt": "/agent-skills:incremental-implementation Execute the next planned task with commit-as-save-point discipline."}
            ]
        },
        "test-driven-development": {
            "title": "Test-Driven Development (TDD)",
            "category": "Build",
            "use_case_group": "testing_qa",
            "icon": "check",
            "when_to_use": "Use when implementing logic, fixing bugs (Prove-It pattern), or changing any behavior.",
            "description": "Red-Green-Refactor loop, test pyramid (80/15/5), test sizes, DAMP over DRY, and the Beyonce Rule.",
            "starter_prompts": [
                {"title": "Start Red-Green-Refactor", "prompt": "/agent-skills:test-driven-development Write a failing test first to prove the missing behavior."},
                {"title": "Reproduce Bug with Test", "prompt": "/agent-skills:test-driven-development Write an automated test reproducing the reported bug before fixing."},
                {"title": "Refactor with Passing Tests", "prompt": "/agent-skills:test-driven-development Clean up implementation while ensuring all existing tests stay green."}
            ]
        },
        "context-engineering": {
            "title": "Context Engineering",
            "category": "Build",
            "use_case_group": "plan_debug",
            "icon": "layers",
            "when_to_use": "Use when starting a session, switching tasks, or when agent output quality drops due to context pollution.",
            "description": "Feeds agents the right information at the right time using rules files, context packing, and MCP integrations.",
            "starter_prompts": [
                {"title": "Pack Relevant Context", "prompt": "/agent-skills:context-engineering Clean context window and summarize key architectural anchors for next task."},
                {"title": "Optimize Rules & Instructions", "prompt": "/agent-skills:context-engineering Structure project rules for minimal token overhead and maximal adherence."},
                {"title": "Prepare Task Workspace Context", "prompt": "/agent-skills:context-engineering Gather only the necessary source files and schemas for [task name]."}
            ]
        },
        "source-driven-development": {
            "title": "Source-Driven Development",
            "category": "Build",
            "use_case_group": "web_db",
            "icon": "fileText",
            "when_to_use": "Use when making framework/library decisions and you want authoritative, source-cited code from official docs.",
            "description": "Grounds every framework decision in official documentation — verify, cite sources, and flag unverified assumptions.",
            "starter_prompts": [
                {"title": "Ground in Official Docs", "prompt": "/agent-skills:source-driven-development Verify the latest API patterns for [library name] against official documentation."},
                {"title": "Cite Authoritative Sources", "prompt": "/agent-skills:source-driven-development Provide working code with exact documentation links and citations."},
                {"title": "Audit Deprecated API Usage", "prompt": "/agent-skills:source-driven-development Check if any library methods used in [file] are outdated or deprecated."}
            ]
        },
        "doubt-driven-development": {
            "title": "Doubt-Driven Development",
            "category": "Build",
            "use_case_group": "testing_qa",
            "icon": "lock",
            "when_to_use": "Use when stakes are high (production, security, irreversible changes) or working in unfamiliar code.",
            "description": "Adversarial fresh-context review of non-trivial decisions: CLAIM -> EXTRACT -> DOUBT -> RECONCILE -> STOP.",
            "starter_prompts": [
                {"title": "Adversarial Decision Audit", "prompt": "/agent-skills:doubt-driven-development Challenge every assumption in our migration plan with fresh context."},
                {"title": "Stress-Test Security Boundary", "prompt": "/agent-skills:doubt-driven-development Act as an adversary and probe for edge-case vulnerabilities in this auth flow."},
                {"title": "Reconcile Competing Designs", "prompt": "/agent-skills:doubt-driven-development Formulate rigorous counter-arguments against [proposed architecture]."}
            ]
        },
        "frontend-ui-engineering": {
            "title": "Frontend UI Engineering",
            "category": "Build",
            "use_case_group": "ui_ux",
            "icon": "palette",
            "when_to_use": "Use when building or modifying user-facing interfaces, component architecture, state management, or accessibility.",
            "description": "Component architecture, design systems, state management, responsive design, and WCAG 2.1 AA accessibility.",
            "starter_prompts": [
                {"title": "Build Accessible UI Component", "prompt": "/agent-skills:frontend-ui-engineering Craft [component name] with keyboard navigation and ARIA semantics."},
                {"title": "Audit Responsive Layout", "prompt": "/agent-skills:frontend-ui-engineering Ensure multi-breakpoint responsiveness and eliminate overflow bugs."},
                {"title": "Refactor UI State Flow", "prompt": "/agent-skills:frontend-ui-engineering Simplify state flow and decouple business logic from presentation."}
            ]
        },
        "api-and-interface-design": {
            "title": "API & Interface Design",
            "category": "Build",
            "use_case_group": "web_db",
            "icon": "database",
            "when_to_use": "Use when designing APIs, module boundaries, public interfaces, or contracts between services.",
            "description": "Contract-first design, Hyrum's Law, One-Version Rule, error semantics, and boundary validation.",
            "starter_prompts": [
                {"title": "Design REST/GraphQL Contract", "prompt": "/agent-skills:api-and-interface-design Design a backward-compatible API interface for [service name]."},
                {"title": "Validate Boundary Semantics", "prompt": "/agent-skills:api-and-interface-design Define strict input schemas, error responses, and status codes."},
                {"title": "Apply Hyrum's Law Check", "prompt": "/agent-skills:api-and-interface-design Audit public interfaces to ensure internal implementation details are not leaked."}
            ]
        },
        "browser-testing-with-devtools": {
            "title": "Browser Testing with DevTools",
            "category": "Verify",
            "use_case_group": "testing_qa",
            "icon": "sparkles",
            "when_to_use": "Use when building or debugging anything running in a browser using Chrome DevTools MCP.",
            "description": "Chrome DevTools MCP integration for live runtime data: DOM inspection, console logs, network traces, and profiling.",
            "starter_prompts": [
                {"title": "Inspect Live DOM & Styles", "prompt": "/agent-skills:browser-testing-with-devtools Inspect the active page DOM and diagnose styling discrepancies."},
                {"title": "Trace Network Requests", "prompt": "/agent-skills:browser-testing-with-devtools Analyze runtime API payloads, headers, and slow network responses."},
                {"title": "Audit Console Logs & Errors", "prompt": "/agent-skills:browser-testing-with-devtools Capture runtime browser errors and exceptions during user interaction."}
            ]
        },
        "debugging-and-error-recovery": {
            "title": "Debugging & Error Recovery",
            "category": "Verify",
            "use_case_group": "plan_debug",
            "icon": "bug",
            "when_to_use": "Use when tests fail, builds break, or application behavior is unexpected.",
            "description": "Five-step triage: reproduce, localize, reduce, fix, guard. Stop-the-line rule and safe fallbacks.",
            "starter_prompts": [
                {"title": "Triage Unexpected Error", "prompt": "/agent-skills:debugging-and-error-recovery Follow the 5-step triage process to find root cause of [error]."},
                {"title": "Isolate Minimal Reproduction", "prompt": "/agent-skills:debugging-and-error-recovery Reduce complex failure down to a minimal reproducible script."},
                {"title": "Create Regression Guard", "prompt": "/agent-skills:debugging-and-error-recovery Fix the root cause and add an automated guard test to prevent recurrence."}
            ]
        },
        "code-review-and-quality": {
            "title": "Code Review & Quality",
            "category": "Review",
            "use_case_group": "testing_qa",
            "icon": "fileText",
            "when_to_use": "Use before merging any change: five-axis review (correctness, readability, architecture, security, performance).",
            "description": "Five-axis review, change sizing (~100 lines), severity labels (Nit/Optional/FYI), and splitting strategies.",
            "starter_prompts": [
                {"title": "Five-Axis Pre-Merge Review", "prompt": "/agent-skills:code-review-and-quality Review the diff against correctness, readability, architecture, security, and perf."},
                {"title": "Label Review Feedback", "prompt": "/agent-skills:code-review-and-quality Categorize feedback using standard severity labels (Blocker, Nit, FYI)."},
                {"title": "Check Change Sizing", "prompt": "/agent-skills:code-review-and-quality Audit PR size and propose splitting strategies if over 200 lines."}
            ]
        },
        "code-simplification": {
            "title": "Code Simplification",
            "category": "Review",
            "use_case_group": "plan_debug",
            "icon": "cpu",
            "when_to_use": "Use when code works but is harder to read, maintain, or understand than it should be.",
            "description": "Chesterton's Fence, Rule of 500, reduce cognitive complexity while preserving exact runtime behavior.",
            "starter_prompts": [
                {"title": "Simplify Complex Module", "prompt": "/agent-skills:code-simplification Refactor [module name] to reduce cognitive complexity while keeping tests green."},
                {"title": "Apply Chesterton's Fence", "prompt": "/agent-skills:code-simplification Understand why existing logic was built before removing or refactoring it."},
                {"title": "De-nest Deeply Nested Logic", "prompt": "/agent-skills:code-simplification Flatten nested loops and conditionals into clear guard clauses."}
            ]
        },
        "security-and-hardening": {
            "title": "Security & Hardening",
            "category": "Review",
            "use_case_group": "testing_qa",
            "icon": "lock",
            "when_to_use": "Use when handling user input, authentication, data storage, or external integrations.",
            "description": "OWASP Top 10 prevention, auth patterns, secrets management, dependency auditing, and three-tier boundaries.",
            "starter_prompts": [
                {"title": "OWASP Top 10 Security Scan", "prompt": "/agent-skills:security-and-hardening Audit codebase for injection, XSS, CSRF, and broken access controls."},
                {"title": "Harden Authentication Flow", "prompt": "/agent-skills:security-and-hardening Review session handling, token storage, and password reset security."},
                {"title": "Audit Third-Party Dependencies", "prompt": "/agent-skills:security-and-hardening Scan project dependencies for known CVEs and supply chain risks."}
            ]
        },
        "performance-optimization": {
            "title": "Performance Optimization",
            "category": "Review",
            "use_case_group": "web_db",
            "icon": "refresh",
            "when_to_use": "Use when performance requirements exist or you suspect runtime regressions.",
            "description": "Measure-first approach: Core Web Vitals targets, profiling workflows, bundle analysis, and anti-pattern detection.",
            "starter_prompts": [
                {"title": "Profile Core Web Vitals", "prompt": "/agent-skills:performance-optimization Measure LCP, INP, and CLS and identify the critical bottlenecks."},
                {"title": "Optimize Bundle Size", "prompt": "/agent-skills:performance-optimization Analyze JavaScript bundle size and eliminate unused dependencies."},
                {"title": "Eliminate Runtime Waterfalls", "prompt": "/agent-skills:performance-optimization Refactor sequential data queries into parallel fetches."}
            ]
        },
        "git-workflow-and-versioning": {
            "title": "Git Workflow & Versioning",
            "category": "Ship",
            "use_case_group": "web_db",
            "icon": "gitBranch",
            "when_to_use": "Use when making any code change: trunk-based development, atomic commits, commit-as-save-point pattern.",
            "description": "Trunk-based development, atomic commits, change sizing (~100 lines), and commit-as-save-point pattern.",
            "starter_prompts": [
                {"title": "Commit Atomic Save Point", "prompt": "/agent-skills:git-workflow-and-versioning Create a descriptive atomic commit for the verified changes."},
                {"title": "Format Semantic Commit Message", "prompt": "/agent-skills:git-workflow-and-versioning Generate conventional commit message with clear rationale."},
                {"title": "Prepare Clean Pull Request", "prompt": "/agent-skills:git-workflow-and-versioning Rebase and organize commits for clear peer review."}
            ]
        },
        "ci-cd-and-automation": {
            "title": "CI/CD & Automation",
            "category": "Ship",
            "use_case_group": "testing_qa",
            "icon": "download",
            "when_to_use": "Use when setting up or modifying build, test, and deployment pipelines.",
            "description": "Shift Left, Faster is Safer, feature flags, quality gate pipelines, and rapid failure feedback loops.",
            "starter_prompts": [
                {"title": "Setup GitHub Actions Pipeline", "prompt": "/agent-skills:ci-cd-and-automation Create an automated CI workflow with linting, testing, and build gates."},
                {"title": "Optimize Pipeline Execution Speed", "prompt": "/agent-skills:ci-cd-and-automation Cache dependencies and parallelize test runs to achieve sub-5m CI."},
                {"title": "Implement Staging Quality Gates", "prompt": "/agent-skills:ci-cd-and-automation Configure automated pre-deployment smoke tests and rollback triggers."}
            ]
        },
        "deprecation-and-migration": {
            "title": "Deprecation & Migration",
            "category": "Ship",
            "use_case_group": "plan_debug",
            "icon": "layers",
            "when_to_use": "Use when removing old systems, migrating users/APIs, or sunsetting features (treating code as liability).",
            "description": "Code-as-liability mindset, compulsory vs advisory deprecation, migration patterns, and zombie code removal.",
            "starter_prompts": [
                {"title": "Plan API Deprecation Lifecycle", "prompt": "/agent-skills:deprecation-and-migration Formulate a phased deprecation strategy with clear migration paths."},
                {"title": "Remove Zombie Code", "prompt": "/agent-skills:deprecation-and-migration Safely identify and delete unused functions, dead flags, and stale imports."},
                {"title": "Execute Zero-Downtime Migration", "prompt": "/agent-skills:deprecation-and-migration Design zero-downtime expand-and-contract migration for [database table]."}
            ]
        },
        "documentation-and-adrs": {
            "title": "Documentation & ADRs",
            "category": "Ship",
            "use_case_group": "plan_debug",
            "icon": "fileText",
            "when_to_use": "Use when making architectural decisions, changing public APIs, or shipping major features.",
            "description": "Architecture Decision Records (ADRs), API docs, and inline documentation standards — document the 'why'.",
            "starter_prompts": [
                {"title": "Draft Architecture Decision Record", "prompt": "/agent-skills:documentation-and-adrs Write an ADR recording context, options, decision, and consequences."},
                {"title": "Document Public API Methods", "prompt": "/agent-skills:documentation-and-adrs Write clean, accurate docstrings with code examples for [module]."},
                {"title": "Create Onboarding Guide", "prompt": "/agent-skills:documentation-and-adrs Update README with quickstart instructions, environment setup, and architecture overview."}
            ]
        },
        "observability-and-instrumentation": {
            "title": "Observability & Instrumentation",
            "category": "Ship",
            "use_case_group": "testing_qa",
            "icon": "refresh",
            "when_to_use": "Use when adding telemetry, structured logging, RED metrics, or shipping production workloads.",
            "description": "Structured logging, RED metrics, OpenTelemetry distributed tracing, and symptom-based alerting.",
            "starter_prompts": [
                {"title": "Instrument Structured Logging", "prompt": "/agent-skills:observability-and-instrumentation Add contextual JSON logs with correlation IDs to [service]."},
                {"title": "Define RED/USE Metrics", "prompt": "/agent-skills:observability-and-instrumentation Instrument Rate, Errors, and Duration metrics for critical API endpoints."},
                {"title": "Setup OpenTelemetry Tracing", "prompt": "/agent-skills:observability-and-instrumentation Configure distributed spans across frontend and backend calls."}
            ]
        },
        "shipping-and-launch": {
            "title": "Shipping & Launch",
            "category": "Ship",
            "use_case_group": "testing_qa",
            "icon": "sparkles",
            "when_to_use": "Use when preparing to deploy to production: pre-launch checklists, staged rollouts, and rollback readiness.",
            "description": "Pre-launch checklists, feature flag lifecycle, staged rollouts, rollback procedures, and monitoring setup.",
            "starter_prompts": [
                {"title": "Execute Pre-Launch Checklist", "prompt": "/agent-skills:shipping-and-launch Audit Definition of Done, backups, DNS, and rollback procedures."},
                {"title": "Configure Staged Rollout", "prompt": "/agent-skills:shipping-and-launch Set up canary deployment thresholds (1% -> 10% -> 100%) with automated alerts."},
                {"title": "Prepare Rollback Action Plan", "prompt": "/agent-skills:shipping-and-launch Document step-by-step emergency rollback procedure for [deployment]."}
            ]
        },
        # 4 Specialist Personas
        "code-reviewer": {
            "title": "Senior Code Reviewer",
            "category": "Personas",
            "use_case_group": "testing_qa",
            "icon": "fileText",
            "is_persona": True,
            "when_to_use": "Use for thorough code review before merging changes to verify correctness, readability, architecture, and security.",
            "description": "Senior Staff Engineer persona conducting five-axis code reviews with 'would a staff engineer approve this?' standard.",
            "starter_prompts": [
                {"title": "Staff Engineer Code Review", "prompt": "Review these changes as a Senior Staff Engineer against correctness, architecture, and maintainability."},
                {"title": "Probe Edge Cases & Race Conditions", "prompt": "Identify subtle bugs, off-by-one errors, or concurrency issues in this implementation."},
                {"title": "Evaluate Architectural Fit", "prompt": "Evaluate whether this new abstraction aligns with existing architectural conventions."}
            ]
        },
        "security-auditor": {
            "title": "Security Auditor",
            "category": "Personas",
            "use_case_group": "testing_qa",
            "icon": "lock",
            "is_persona": True,
            "when_to_use": "Use when reviewing authentication, secrets, input validation, or sensitive operations for security vulnerabilities.",
            "description": "Specialist Security Engineer persona evaluating threat models, OWASP vulnerabilities, and data exposure.",
            "starter_prompts": [
                {"title": "Threat Modeling Audit", "prompt": "Act as a Security Auditor and perform threat modeling on this authentication and session architecture."},
                {"title": "Audit Input Validation & Injection", "prompt": "Probe for potential SQL injection, XSS, SSRF, or privilege escalation vectors in these endpoints."},
                {"title": "Verify Secrets & Crypto Practices", "prompt": "Verify that secrets, hashing algorithms, and encryption keys are handled safely."}
            ]
        },
        "test-engineer": {
            "title": "QA Test Engineer",
            "category": "Personas",
            "use_case_group": "testing_qa",
            "icon": "check",
            "is_persona": True,
            "when_to_use": "Use when designing test strategies, evaluating test coverage, or implementing the Prove-It pattern.",
            "description": "Specialist QA Engineer persona enforcing test strategy, pyramid balance, and comprehensive behavioral proof.",
            "starter_prompts": [
                {"title": "Design QA Test Matrix", "prompt": "Create a comprehensive test plan covering unit, integration, and E2E layers for [feature]."},
                {"title": "Analyze Test Coverage Gaps", "prompt": "Identify critical untested paths and edge cases in the current test suite."},
                {"title": "Enforce Prove-It Pattern", "prompt": "Review this bug fix to ensure an automated test conclusively reproduces the issue before patching."}
            ]
        },
        "web-performance-auditor": {
            "title": "Web Performance Auditor",
            "category": "Personas",
            "use_case_group": "web_db",
            "icon": "sun",
            "is_persona": True,
            "when_to_use": "Use when analyzing Core Web Vitals, diagnosing slow rendering, or profiling browser frontend performance.",
            "description": "Web Performance Engineer persona conducting Core Web Vitals audits with metric-honesty rules via /webperf.",
            "starter_prompts": [
                {"title": "Audit Core Web Vitals", "prompt": "Perform a Core Web Vitals audit and diagnose causes of high LCP, poor INP, or layout shifts."},
                {"title": "Detect Layout Shifts (CLS)", "prompt": "Identify dynamic elements causing Cumulative Layout Shift and provide stabilizing CSS fixes."},
                {"title": "Analyze Main Thread Blocking", "prompt": "Profile JavaScript execution and recommend code-splitting or web worker offloading."}
            ]
        }
    }

    @staticmethod
    def parse_markdown_with_frontmatter(file_path: Path) -> Tuple[Dict[str, Any], str]:
        """Extracts YAML frontmatter and markdown body from a file."""
        if not file_path.exists():
            return {}, ""
        content = file_path.read_text(encoding="utf-8", errors="replace")
        frontmatter = {}
        body = content

        pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
        match = re.match(pattern, content, re.DOTALL)
        if match:
            fm_text, body = match.groups()
            try:
                parsed = yaml.safe_load(fm_text)
                if isinstance(parsed, dict):
                    frontmatter = parsed
            except Exception:
                pass
        return frontmatter, body.strip()

    @classmethod
    def scan_skill_directory(cls, dir_path: Path, repo_url: Optional[str] = None) -> List[SkillItem]:
        """Scans a directory for skills, supporting flat, nested, and Monorepo structures."""
        dir_path = Path(dir_path)
        if not dir_path.exists() or not dir_path.is_dir():
            return []

        skills: List[SkillItem] = []

        # 1. Check if folder contains "skills" subfolder (Monorepo structure e.g. agent-skills)
        skills_sub = dir_path / "skills"
        if skills_sub.exists() and skills_sub.is_dir():
            for child in sorted(skills_sub.iterdir()):
                if child.is_dir() and not child.name.startswith("."):
                    sf = child / "SKILL.md"
                    if sf.exists():
                        s = cls._build_skill_from_folder(child, sf, repo_url=repo_url or "https://github.com/addyosmani/agent-skills", parent_repo_dir=dir_path)
                        if s and not any(existing.id == s.id for existing in skills):
                            skills.append(s)

        # 2. Check if folder contains "agents" subfolder (Personas e.g. code-reviewer.md)
        agents_sub = dir_path / "agents"
        if agents_sub.exists() and agents_sub.is_dir():
            for persona_file in sorted(agents_sub.glob("*.md")):
                p = cls._build_persona_from_file(persona_file, parent_repo_dir=dir_path, repo_url=repo_url or "https://github.com/addyosmani/agent-skills")
                if p and not any(existing.id == p.id for existing in skills):
                    skills.append(p)

        # 3. Check if folder itself is a skill
        main_skill_file = dir_path / "SKILL.md"
        if main_skill_file.exists():
            skill = cls._build_skill_from_folder(dir_path, main_skill_file, repo_url)
            if skill and not any(existing.id == skill.id for existing in skills):
                skills.append(skill)

        # 4. Check direct subdirectories (excluding internal references/rules or hidden dirs)
        for sub_dir in sorted(dir_path.iterdir()):
            if sub_dir.is_dir() and not sub_dir.name.startswith(".") and sub_dir.name not in ["references", "rules", "scripts", "skills", "agents", "docs", "evals", "hooks"]:
                sub_skill_file = sub_dir / "SKILL.md"
                if sub_skill_file.exists() and sub_dir != dir_path:
                    sub_skill = cls._build_skill_from_folder(sub_dir, sub_skill_file, repo_url, parent_repo_dir=dir_path)
                    if sub_skill and not any(s.id == sub_skill.id for s in skills):
                        skills.append(sub_skill)

        return skills

    @classmethod
    def _build_skill_from_folder(cls, folder: Path, skill_file: Path, repo_url: Optional[str] = None, parent_repo_dir: Optional[Path] = None) -> Optional[SkillItem]:
        fm, body = cls.parse_markdown_with_frontmatter(skill_file)
        skill_id = fm.get("name") or folder.name

        # Check metadata from either official suite or Addy Osmani suite
        meta = cls.OFFICIAL_METADATA.get(skill_id)
        is_addy = False

        if not meta and skill_id in cls.ADDY_OSMANI_METADATA:
            meta = cls.ADDY_OSMANI_METADATA[skill_id]
            is_addy = True
        elif meta:
            is_addy = False
        else:
            # Check if parent or repo indicates Addy Osmani
            if (parent_repo_dir and "agent-skills" in parent_repo_dir.name.lower()) or (repo_url and "addyosmani" in repo_url.lower()):
                is_addy = True

        title = (meta.get("title") if meta else None) or fm.get("name") or skill_id.replace("-", " ").title()
        category = (meta.get("category") if meta else None) or fm.get("category") or "Developer Tools"
        icon = (meta.get("icon") if meta else None) or "sparkles"
        final_repo = repo_url or (meta.get("repo") if meta else None) or ("https://github.com/addyosmani/agent-skills" if is_addy else None)
        author = (meta.get("author") if meta else None) or ("Addy Osmani" if is_addy else fm.get("author") or "Skill-AI")
        source_group = "addy_osmani" if is_addy else (meta.get("source_group") if meta else "skill_ai")
        license_str = "MIT"

        when_to_use = (meta.get("when_to_use") if meta else "") or fm.get("when_to_use", "")
        use_case_group = (meta.get("use_case_group") if meta else "all") or "all"
        starter_prompts = (meta.get("starter_prompts") if meta else []) or []

        description = (meta.get("description") if meta else None) or fm.get("description", "")
        if not description:
            for line in body.splitlines():
                clean = line.strip("# \t-")
                if len(clean) > 20:
                    description = clean
                    break
            if not description:
                description = f"AI capability skill for {title}"

        # If when_to_use or starter_prompts still empty, generate sensible defaults
        if not when_to_use:
            when_to_use = f"Use when working on {title} or applying the {skill_id} engineering workflow."
        if len(starter_prompts) < 3:
            cmd = f"/agent-skills:{skill_id}" if is_addy else f"/{skill_id}"
            starter_prompts = [
                {"title": f"Activate {title}", "prompt": f"{cmd} execute workflow for current task"},
                {"title": f"Verify with {title}", "prompt": f"{cmd} verify requirements and adherence"},
                {"title": f"Inspect {title} guidelines", "prompt": f"{cmd} review active constraints and patterns"}
            ]

        # References
        references: List[ReferenceDoc] = []
        ref_dirs = []
        if (folder / "references").exists() and (folder / "references").is_dir():
            ref_dirs.append(folder / "references")
        if parent_repo_dir and (parent_repo_dir / "references").exists() and (parent_repo_dir / "references").is_dir():
            ref_dirs.append(parent_repo_dir / "references")

        seen_refs = set()
        for r_dir in ref_dirs:
            for ref_file in sorted(r_dir.glob("*.md")):
                if ref_file.stem not in seen_refs:
                    seen_refs.add(ref_file.stem)
                    ref_content = ref_file.read_text(encoding="utf-8", errors="replace")
                    ref_title = ref_file.stem.replace("-", " ").title()
                    ref_title = re.sub(r"^\d+\s*", "", ref_title).strip()
                    references.append(ReferenceDoc(
                        id=ref_file.stem,
                        title=ref_title,
                        filename=ref_file.name,
                        content=ref_content,
                        category="reference"
                    ))

        # Rules
        rules: List[RuleDoc] = []
        rule_dir = folder / "rules"
        if not rule_dir.exists() and parent_repo_dir:
            rule_dir = parent_repo_dir / "rules"

        if rule_dir.exists() and rule_dir.is_dir():
            for rule_file in sorted(rule_dir.glob("*.md")):
                rule_content = rule_file.read_text(encoding="utf-8", errors="replace")
                rules.append(RuleDoc(
                    id=rule_file.stem,
                    name=rule_file.stem.replace("-", " ").title(),
                    filename=rule_file.name,
                    content=rule_content,
                    rule_type="always_on"
                ))

        has_graphify = (
            "graphify" in body.lower() or 
            any("graphify" in r.content.lower() for r in references) or
            (folder / "graphify-out").exists() or
            skill_id == "strict-architect-coder"
        )

        tags = [t.strip() for t in fm.get("tags", [])] if isinstance(fm.get("tags"), list) else []
        if category not in tags:
            tags.append(category)
        if has_graphify and "Graphify" not in tags:
            tags.append("Graphify AST")
        if is_addy and "Addy Osmani" not in tags:
            tags.append("Addy Osmani")

        installed_targets = cls.detect_installed_targets(skill_id)
        always_on = cls.detect_always_on_enabled()

        return SkillItem(
            id=skill_id,
            name=skill_id,
            display_title=title,
            version=fm.get("version", "0.6.14" if is_addy else "1.0.0"),
            description=description,
            category=category,
            tags=tags,
            author=author,
            repo_url=final_repo,
            skill_content=body,
            yaml_frontmatter=fm,
            references=references,
            rules=rules,
            has_graphify=has_graphify,
            installed_targets=installed_targets,
            always_on_enabled=always_on,
            icon=icon,
            when_to_use=when_to_use,
            use_case_group=use_case_group,
            starter_prompts=starter_prompts,
            source_group=source_group,
            is_persona=False,
            license=license_str
        )

    @classmethod
    def _build_persona_from_file(cls, persona_file: Path, parent_repo_dir: Optional[Path] = None, repo_url: Optional[str] = None) -> Optional[SkillItem]:
        fm, body = cls.parse_markdown_with_frontmatter(persona_file)
        persona_id = fm.get("name") or persona_file.stem

        meta = cls.ADDY_OSMANI_METADATA.get(persona_id, {})
        title = meta.get("title") or persona_id.replace("-", " ").title()
        category = "Personas"
        icon = meta.get("icon") or "user"
        final_repo = repo_url or "https://github.com/addyosmani/agent-skills"
        author = "Addy Osmani"
        source_group = "addy_osmani"
        license_str = "MIT"

        when_to_use = meta.get("when_to_use") or f"Use as a specialist reviewer for {title}."
        use_case_group = meta.get("use_case_group", "testing_qa")
        starter_prompts = meta.get("starter_prompts", [])
        description = meta.get("description") or fm.get("description", f"Specialist AI persona: {title}")

        if len(starter_prompts) < 3:
            starter_prompts = [
                {"title": f"Run {title} Review", "prompt": f"Act as {title} and evaluate the current changes."},
                {"title": f"Audit edge cases with {title}", "prompt": f"Inspect code and identify subtle failure modes as {title}."},
                {"title": f"Check compliance as {title}", "prompt": f"Ensure all quality gates are satisfied according to {title} guidelines."}
            ]

        # References from parent repo
        references: List[ReferenceDoc] = []
        if parent_repo_dir and (parent_repo_dir / "references").exists():
            for ref_file in sorted((parent_repo_dir / "references").glob("*.md")):
                ref_content = ref_file.read_text(encoding="utf-8", errors="replace")
                ref_title = ref_file.stem.replace("-", " ").title()
                references.append(ReferenceDoc(
                    id=ref_file.stem,
                    title=ref_title,
                    filename=ref_file.name,
                    content=ref_content,
                    category="reference"
                ))

        tags = ["Personas", "Addy Osmani", "Specialist"]
        installed_targets = cls.detect_installed_targets(persona_id)
        always_on = cls.detect_always_on_enabled()

        return SkillItem(
            id=persona_id,
            name=persona_id,
            display_title=title,
            version="0.6.14",
            description=description,
            category=category,
            tags=tags,
            author=author,
            repo_url=final_repo,
            skill_content=body,
            yaml_frontmatter=fm,
            references=references,
            rules=[],
            has_graphify=False,
            installed_targets=installed_targets,
            always_on_enabled=always_on,
            icon=icon,
            when_to_use=when_to_use,
            use_case_group=use_case_group,
            starter_prompts=starter_prompts,
            source_group=source_group,
            is_persona=True,
            license=license_str
        )

    @classmethod
    def get_installed_targets_and_paths(cls, workspace_path: Optional[str] = None) -> Tuple[Dict[str, List[str]], Dict[str, Path]]:
        """
        Fast-path bulk scanner: Quét toàn bộ thư mục công cụ trong 1 lượt,
        trả về cả danh sách targets lẫn đường dẫn tệp SKILL.md thực tế trên ổ đĩa.
        """
        home = Path.home()
        antigravity_set = set()
        paths_map = {}

        # 1. Antigravity targets
        for base in [home / ".gemini" / "config" / "skills", home / ".gemini" / "antigravity" / "skills"]:
            if base.exists() and base.is_dir():
                try:
                    for p in base.iterdir():
                        if p.is_dir() and (p / "SKILL.md").exists():
                            antigravity_set.add(p.name)
                            if p.name not in paths_map:
                                paths_map[p.name] = p / "SKILL.md"
                except Exception:
                    pass

        # 2. Claude targets
        claude_set = set()
        claude_base = home / ".claude" / "skills"
        if claude_base.exists() and claude_base.is_dir():
            try:
                for p in claude_base.iterdir():
                    if p.is_dir() and (p / "SKILL.md").exists():
                        claude_set.add(p.name)
                        if p.name not in paths_map:
                            paths_map[p.name] = p / "SKILL.md"
            except Exception:
                pass

        # 3. Copilot targets
        copilot_set = set()
        copilot_base = home / ".copilot" / "skills"
        if copilot_base.exists() and copilot_base.is_dir():
            try:
                for p in copilot_base.iterdir():
                    if p.is_dir() and (p / "SKILL.md").exists():
                        copilot_set.add(p.name)
                        if p.name not in paths_map:
                            paths_map[p.name] = p / "SKILL.md"
            except Exception:
                pass

        # 4. Active Workspace targets (highest priority for paths)
        ws_set = set()
        active_ws = Path(workspace_path) if workspace_path else Path.cwd()
        ws_base = active_ws / ".agents" / "skills"
        if ws_base.exists() and ws_base.is_dir():
            try:
                for p in ws_base.iterdir():
                    if p.is_dir() and (p / "SKILL.md").exists():
                        ws_set.add(p.name)
                        paths_map[p.name] = p / "SKILL.md"
            except Exception:
                pass

        all_skill_ids = antigravity_set | claude_set | copilot_set | ws_set
        targets_result = {}
        for s_id in all_skill_ids:
            targets = []
            if s_id in ws_set:
                targets.append("workspace")
            if s_id in antigravity_set:
                targets.append("antigravity")
            if s_id in claude_set:
                targets.append("claude")
            if s_id in copilot_set:
                targets.append("copilot")
            targets_result[s_id] = targets

        return targets_result, paths_map

    @classmethod
    def get_installed_targets_map(cls, workspace_path: Optional[str] = None) -> Dict[str, List[str]]:
        """Backwards-compatible wrapper returning only targets map."""
        targets, _ = cls.get_installed_targets_and_paths(workspace_path)
        return targets

    @classmethod
    def _legacy_get_installed_targets_map(cls, workspace_path: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Fast-path bulk scanner: Quét toàn bộ thư mục công cụ trong 1 lượt (4 directory reads),
        thay vì lặp 500+ lượt kiểm tra file riêng lẻ làm nghẽn I/O khi khởi động.
        Hỗ trợ workspace_path động để người dùng chọn dự án làm việc linh hoạt.
        """
        home = Path.home()
        antigravity_set = set()
        for base in [home / ".gemini" / "config" / "skills", home / ".gemini" / "antigravity" / "skills"]:
            if base.exists() and base.is_dir():
                try:
                    for p in base.iterdir():
                        if p.is_dir() and (p / "SKILL.md").exists():
                            antigravity_set.add(p.name)
                except Exception:
                    pass

        claude_set = set()
        claude_base = home / ".claude" / "skills"
        if claude_base.exists() and claude_base.is_dir():
            try:
                for p in claude_base.iterdir():
                    if p.is_dir() and (p / "SKILL.md").exists():
                        claude_set.add(p.name)
            except Exception:
                pass

        copilot_set = set()
        copilot_base = home / ".copilot" / "skills"
        if copilot_base.exists() and copilot_base.is_dir():
            try:
                for p in copilot_base.iterdir():
                    if p.is_dir() and (p / "SKILL.md").exists():
                        copilot_set.add(p.name)
            except Exception:
                pass

        ws_set = set()
        active_ws = Path(workspace_path) if workspace_path else Path.cwd()
        ws_base = active_ws / ".agents" / "skills"
        if ws_base.exists() and ws_base.is_dir():
            try:
                for p in ws_base.iterdir():
                    if p.is_dir() and (p / "SKILL.md").exists():
                        ws_set.add(p.name)
            except Exception:
                pass

        all_skill_ids = antigravity_set | claude_set | copilot_set | ws_set
        result = {}
        for s_id in all_skill_ids:
            targets = []
            if s_id in antigravity_set:
                targets.append("antigravity")
            if s_id in claude_set:
                targets.append("claude")
            if s_id in copilot_set:
                targets.append("copilot")
            if s_id in ws_set:
                targets.append("workspace")
            result[s_id] = targets
        return result

    @classmethod
    def detect_installed_targets(cls, skill_id: str, workspace_path: Optional[str] = None) -> List[str]:
        """Detects which tools currently have this skill installed."""
        targets = []
        home = Path.home()

        # 1. Antigravity Global
        antigravity_paths = [
            home / ".gemini" / "config" / "skills" / skill_id,
            home / ".gemini" / "antigravity" / "skills" / skill_id,
        ]
        if any(p.exists() and (p / "SKILL.md").exists() for p in antigravity_paths):
            targets.append("antigravity")

        # 2. Claude Code
        claude_path = home / ".claude" / "skills" / skill_id
        if claude_path.exists() and (claude_path / "SKILL.md").exists():
            targets.append("claude")

        # 3. Copilot CLI
        copilot_path = home / ".copilot" / "skills" / skill_id
        if copilot_path.exists() and (copilot_path / "SKILL.md").exists():
            targets.append("copilot")

        # 4. Current Workspace (Hỗ trợ đường dẫn động)
        active_ws = Path(workspace_path) if workspace_path else Path.cwd()
        ws_path = active_ws / ".agents" / "skills" / skill_id
        if ws_path.exists() and (ws_path / "SKILL.md").exists():
            targets.append("workspace")

        return targets

    @classmethod
    def detect_always_on_enabled(cls) -> bool:
        """Checks if always-on-autopilot rule is active in Antigravity or Claude."""
        home = Path.home()
        candidates = [
            home / ".gemini" / "config" / "rules" / "always-on-autopilot.md",
            home / ".gemini" / "GEMINI.md",
            home / ".gemini" / "config" / "GEMINI.md",
            home / ".claude" / "CLAUDE.md",
            Path.cwd() / "GEMINI.md",
            Path.cwd() / ".agents" / "rules" / "always-on-autopilot.md",
        ]
        return any(c.exists() for c in candidates)
