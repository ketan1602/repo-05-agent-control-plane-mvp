from __future__ import annotations


def propagation_time_svg(seconds: float) -> str:
    label = f"{seconds}s"
    width = 320
    fill_w = min(int(seconds / 60 * width), width)
    return f"""<svg viewBox="0 0 320 80" xmlns="http://www.w3.org/2000/svg">
  <rect width="320" height="80" fill="#1a1d27" rx="8"/>
  <text x="16" y="22" fill="#6b7280" font-size="11" font-family="sans-serif"
        font-weight="600" letter-spacing="0.06em" text-transform="uppercase">
    POLICY PROPAGATION TIME
  </text>
  <text x="16" y="56" fill="#22c55e" font-size="36" font-family="sans-serif" font-weight="700">
    {label}
  </text>
  <rect x="16" y="64" width="{fill_w}" height="4" fill="#22c55e" rx="2"/>
  <rect x="{16 + fill_w}" y="64" width="{width - fill_w}" height="4" fill="#2a2d3a" rx="2"/>
  <text x="304" y="72" fill="#6b7280" font-size="10" font-family="sans-serif" text-anchor="end">
    60s max
  </text>
</svg>"""


def fleet_visibility_svg(pct: float, total: int) -> str:
    bar_w = int(pct / 100 * 288)
    return f"""<svg viewBox="0 0 320 80" xmlns="http://www.w3.org/2000/svg">
  <rect width="320" height="80" fill="#1a1d27" rx="8"/>
  <text x="16" y="22" fill="#6b7280" font-size="11" font-family="sans-serif"
        font-weight="600" letter-spacing="0.06em">FLEET VISIBILITY</text>
  <text x="16" y="52" fill="#e2e8f0" font-size="30" font-family="sans-serif" font-weight="700">
    {pct}%
  </text>
  <text x="160" y="52" fill="#6b7280" font-size="13" font-family="sans-serif">
    ({total}/{total} agents)
  </text>
  <rect x="16" y="60" width="288" height="6" fill="#2a2d3a" rx="3"/>
  <rect x="16" y="60" width="{bar_w}" height="6" fill="#6366f1" rx="3"/>
</svg>"""


def comparison_table_svg(cp_seconds: float, manual_minutes: float) -> str:
    return f"""<svg viewBox="0 0 320 100" xmlns="http://www.w3.org/2000/svg">
  <rect width="320" height="100" fill="#1a1d27" rx="8"/>
  <text x="16" y="22" fill="#6b7280" font-size="11" font-family="sans-serif"
        font-weight="600" letter-spacing="0.06em">OPERATIONAL LEVERAGE</text>
  <rect x="16" y="32" width="132" height="52" fill="#0f1117" rx="6"/>
  <text x="82" y="52" fill="#22c55e" font-size="22" font-family="sans-serif"
        font-weight="700" text-anchor="middle">{cp_seconds}s</text>
  <text x="82" y="72" fill="#6b7280" font-size="11" font-family="sans-serif"
        text-anchor="middle">Control Plane</text>
  <rect x="172" y="32" width="132" height="52" fill="#0f1117" rx="6"/>
  <text x="238" y="52" fill="#ef4444" font-size="22" font-family="sans-serif"
        font-weight="700" text-anchor="middle">{manual_minutes}m</text>
  <text x="238" y="72" fill="#6b7280" font-size="11" font-family="sans-serif"
        text-anchor="middle">Manual (7 agents)</text>
</svg>"""
