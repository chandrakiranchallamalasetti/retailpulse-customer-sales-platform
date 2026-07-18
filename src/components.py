from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
        [data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.22); border-radius: 16px; padding: 14px;}
        .rp-eyebrow {font-size:.78rem; letter-spacing:.08em; text-transform:uppercase; opacity:.65; margin-bottom:.2rem;}
        .rp-hero {padding: 1.35rem 1.5rem; border:1px solid rgba(128,128,128,.24); border-radius:22px; margin-bottom:1rem;}
        .rp-card {padding:1rem; border:1px solid rgba(128,128,128,.20); border-radius:16px; height:100%;}
        .rp-small {font-size:.9rem; opacity:.76;}
        .rp-pill {display:inline-block; padding:.25rem .6rem; border-radius:999px; background:rgba(128,128,128,.14); margin:.15rem .2rem .15rem 0; font-size:.82rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "Retail analytics portfolio project") -> None:
    st.markdown(
        f"""
        <section class="rp-hero">
          <div class="rp-eyebrow">{eyebrow}</div>
          <h1 style="margin:.1rem 0 .45rem 0;">{title}</h1>
          <div class="rp-small">{subtitle}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_card(title: str, body: str) -> None:
    st.markdown(f'<div class="rp-card"><h3>{title}</h3><div class="rp-small">{body}</div></div>', unsafe_allow_html=True)
