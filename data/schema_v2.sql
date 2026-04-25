-- ============================================================
-- Freedom and Dignity Project — Policy Catalog v2
-- ID format: ^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$
-- e.g. HLTH-COVR-0001
-- ============================================================

CREATE TABLE IF NOT EXISTS domains (
  code        TEXT PRIMARY KEY CHECK(length(code) = 4),
  name        TEXT NOT NULL,
  pillar_id   TEXT,        -- data.js pillar id (null for XDOM)
  html_file   TEXT,        -- docs/pillars/*.html relative path (null for XDOM)
  is_cross_domain INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS subdomains (
  code        TEXT NOT NULL CHECK(length(code) = 4),
  domain      TEXT NOT NULL REFERENCES domains(code),
  name        TEXT NOT NULL,
  PRIMARY KEY (code, domain)
);

CREATE TABLE IF NOT EXISTS positions (
  id              TEXT PRIMARY KEY CHECK(id GLOB '[A-Z][A-Z][A-Z][A-Z]-[A-Z][A-Z][A-Z][A-Z]-[0-9][0-9][0-9][0-9]'),
  domain          TEXT NOT NULL REFERENCES domains(code),
  subdomain       TEXT NOT NULL,
  seq             INTEGER NOT NULL CHECK(seq BETWEEN 1 AND 9999),
  short_title     TEXT NOT NULL CHECK(length(short_title) <= 120),
  full_statement  TEXT NOT NULL,
  plain_language  TEXT,            -- plain-language summary (~8th grade); NULL = data gap
  is_cross_domain INTEGER NOT NULL DEFAULT 0,
  status          TEXT NOT NULL DEFAULT 'CANONICAL' CHECK(status IN ('CANONICAL','PROPOSED','DEPRECATED','REVIEW')),
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (subdomain, domain) REFERENCES subdomains(code, domain)
);

CREATE TABLE IF NOT EXISTS position_pillar_appearances (
  position_id    TEXT NOT NULL REFERENCES positions(id),
  pillar_domain  TEXT NOT NULL REFERENCES domains(code),
  section_name   TEXT,
  display_order  INTEGER,
  PRIMARY KEY (position_id, pillar_domain)
);

CREATE TABLE IF NOT EXISTS legacy_id_map (
  old_id    TEXT PRIMARY KEY,
  new_id    TEXT NOT NULL REFERENCES positions(id),
  source    TEXT NOT NULL CHECK(source IN ('db','html','both')),
  notes     TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_positions_domain ON positions(domain);
CREATE INDEX IF NOT EXISTS idx_positions_subdomain ON positions(domain, subdomain);
CREATE INDEX IF NOT EXISTS idx_positions_status ON positions(status);
CREATE INDEX IF NOT EXISTS idx_appearances_pillar ON position_pillar_appearances(pillar_domain);
CREATE INDEX IF NOT EXISTS idx_legacy_new_id ON legacy_id_map(new_id);
