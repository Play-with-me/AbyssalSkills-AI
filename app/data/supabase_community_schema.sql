-- ==========================================================================
-- AbyssalSkillsD - Community Cloud Architecture (Supabase & PostgreSQL)
-- Standard: supabase-backend-architect (RLS Security, Granular Policies & GIN Index)
-- ==========================================================================

-- 1. User Profiles & Roles
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE NOT NULL,
  display_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  role TEXT DEFAULT 'creator' CHECK (role IN ('creator', 'curator', 'admin')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public profiles are viewable by everyone."
  ON public.profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can insert their own profile."
  ON public.profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update their own profile."
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);

-- 2. Skills Registry Table
CREATE TABLE IF NOT EXISTS public.skills (
  id TEXT PRIMARY KEY,
  author_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  name TEXT NOT NULL,
  display_title TEXT NOT NULL,
  version TEXT DEFAULT '1.0.0',
  description TEXT NOT NULL,
  category TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  skill_content TEXT NOT NULL,
  yaml_frontmatter JSONB DEFAULT '{}'::jsonb,
  repo_url TEXT,
  has_graphify BOOLEAN DEFAULT false,
  downloads_count INTEGER DEFAULT 0,
  stars_count INTEGER DEFAULT 0,
  is_verified BOOLEAN DEFAULT false,
  is_public BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on skills
ALTER TABLE public.skills ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public skills are viewable by everyone."
  ON public.skills FOR SELECT
  USING (is_public = true OR auth.uid() = author_id);

CREATE POLICY "Authenticated users can create skills."
  ON public.skills FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = author_id);

CREATE POLICY "Authors and admins can update their skills."
  ON public.skills FOR UPDATE
  TO authenticated
  USING (
    auth.uid() = author_id 
    OR EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
  );

CREATE POLICY "Authors and admins can delete their skills."
  ON public.skills FOR DELETE
  TO authenticated
  USING (
    auth.uid() = author_id 
    OR EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
  );

-- 3. Skill References Table
CREATE TABLE IF NOT EXISTS public.skill_references (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id TEXT REFERENCES public.skills(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  filename TEXT NOT NULL,
  content TEXT NOT NULL,
  category TEXT DEFAULT 'reference',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.skill_references ENABLE ROW LEVEL SECURITY;

CREATE POLICY "References of public skills are viewable by everyone."
  ON public.skill_references FOR SELECT
  USING (EXISTS (SELECT 1 FROM public.skills WHERE id = skill_references.skill_id AND (is_public = true OR auth.uid() = author_id)));

CREATE POLICY "Authors can manage references for their skills."
  ON public.skill_references FOR ALL
  TO authenticated
  USING (EXISTS (SELECT 1 FROM public.skills WHERE id = skill_references.skill_id AND auth.uid() = author_id));

-- 4. Full-Text Search Optimization (GIN Index)
CREATE INDEX IF NOT EXISTS idx_skills_fts ON public.skills 
USING GIN (to_tsvector('english', display_title || ' ' || description || ' ' || category));

CREATE INDEX IF NOT EXISTS idx_skills_category ON public.skills(category);
CREATE INDEX IF NOT EXISTS idx_skills_author ON public.skills(author_id);

-- 5. Enterprise Error Telemetry & Anti-Spam Reporting Table (Phase 4 Security)
CREATE TABLE IF NOT EXISTS public.system_error_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  fingerprint TEXT NOT NULL,
  error_type TEXT NOT NULL,
  error_message TEXT NOT NULL,
  module_name TEXT NOT NULL,
  line_number INTEGER DEFAULT 0,
  app_version TEXT NOT NULL DEFAULT '1.0.0',
  os_info TEXT NOT NULL DEFAULT 'win32',
  occurrences INTEGER NOT NULL DEFAULT 1,
  status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'investigating', 'resolved')),
  first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  sanitized_traceback TEXT,
  CONSTRAINT uq_error_fingerprint_version UNIQUE (fingerprint, app_version)
);

ALTER TABLE public.system_error_reports ENABLE ROW LEVEL SECURITY;

-- Policy 1: Client apps (anon or authenticated) can submit error reports
CREATE POLICY "Clients can report errors"
  ON public.system_error_reports FOR INSERT
  WITH CHECK (true);

-- Policy 2: Only administrators can view error reports (Zero-Trust Information Disclosure Defense)
CREATE POLICY "Only admins can view error reports"
  ON public.system_error_reports FOR SELECT
  TO authenticated
  USING (
    EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
  );

CREATE INDEX IF NOT EXISTS idx_error_fingerprint ON public.system_error_reports(fingerprint);
CREATE INDEX IF NOT EXISTS idx_error_status ON public.system_error_reports(status);
