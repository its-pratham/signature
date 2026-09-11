"""
Orbrick Email Signature Generator
----------------------------------
Edit the variables in the CONFIG section below, then run:
    python generate_signature.py

Output: orbrick_signature.html  (ready to paste into Outlook)

Requirements:
    pip install Pillow
"""

import base64
import io
import os
from pathlib import Path
from PIL import Image

# ─────────────────────────────────────────────
#  CONFIG  –  change these values as needed
# ─────────────────────────────────────────────

IMAGE_PATH   = "imagee.png"
FULL_NAME    = "Brix Stir Orbronaut"
DESIGNATION  = "Consulting Genius"
PHONE        = "+91 9997773627"

# Company URLs
COMPANY_WEBSITE = "http://www.orbrick.com"
LINKEDIN_URL    = "https://in.linkedin.com/company/orbrick"
INSTAGRAM_URL   = "https://www.instagram.com/orbrick"
BLOG_URL        = "https://www.orbrick.com/blog"

# Company images (hosted)
COMPANY_LOGO_URL = "https://orbrick.com/wp-content/uploads/2024/08/Main-logoTransparent.png"

# Social icon URLs
LINKEDIN_ICON_URL  = "https://orbrick.com/wp-content/uploads/2024/08/LinkedIn_logo_initials.png"
INSTAGRAM_ICON_URL = "igs.png"
BLOG_ICON_URL      = "https://orbrick.com/wp-content/uploads/2024/08/rss-round-color-icon-2.png"

# Brand colours
COLOR_NAME        = "#5A2B86"   # purple – name & phone
COLOR_DESIGNATION = "#f08519"   # orange – designation

OUTPUT_FILE = "orbrick_signature.html"
OUTPUT_FILE1 = "orbrick_signature_v1.html"
OUTPUT_FILE2 = "orbrick_signature_v2.html"
OUTPUT_FILE3 = "orbrick_signature_v3.html"
# Photo dimensions – portrait crop like the reference signatures
# Width is fixed; height is proportionally taller for a natural portrait feel
PHOTO_WIDTH  = 150
PHOTO_HEIGHT = 170   # slightly taller than wide, matches Khushali/Niyam style

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def image_to_base64(path):
    """
    Open the photo, crop to PHOTO_WIDTH x PHOTO_HEIGHT (centred),
    and return a base64 PNG data-URI.

    Cropping is done here in Python so Outlook receives an image that
    is already the exact right size — no CSS resizing needed.
    Returns None if the file is not found.
    """
    p = Path(path)
    if not p.exists():
        print(f"[WARNING] Image not found: {path}. Placeholder will be used.")
        return None

    with Image.open(p) as img:
        img = img.convert("RGB")
        orig_w, orig_h = img.size

        # Scale the image so the shorter side fits our target,
        # then centre-crop to exact PHOTO_WIDTH x PHOTO_HEIGHT.
        scale = max(PHOTO_WIDTH / orig_w, PHOTO_HEIGHT / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)

        left = (new_w - PHOTO_WIDTH)  // 2
        top  = (new_h - PHOTO_HEIGHT) // 2
        img  = img.crop((left, top, left + PHOTO_WIDTH, top + PHOTO_HEIGHT))

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    return f"data:image/png;base64,{b64}"


def build_signature(name, designation, phone, photo_src):
    """
    Total table width = PHOTO_WIDTH + 30 (spacer) + 240 (details)
    Photo and details are both top-aligned (valign=top), which gives the
    clean, professional look seen in the reference signatures.
    """

    details_width = 240
    total_width   = PHOTO_WIDTH + 30 + details_width

    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
  <TITLE>Orbrick Email Signature</TITLE>
  <META content="text/html; charset=utf-8" http-equiv="Content-Type">
</HEAD>
<BODY style="font-size:10pt; font-family:Tahoma,sans-serif; margin:0; padding:0;">

<table width="{total_width}" cellpadding="0" cellspacing="0"
       style="font-family:Tahoma,sans-serif; background:transparent;">
  <tbody>
    <tr>

      <!-- Photo cell — top-aligned so it sits flush with the name row -->
      <td width="{PHOTO_WIDTH}"
          style="width:{PHOTO_WIDTH}px; padding:0; vertical-align:top;"
          valign="top">
        <img src="{photo_src}"
             width="{PHOTO_WIDTH}" height="{PHOTO_HEIGHT}" border="0"
             style="width:{PHOTO_WIDTH}px; height:{PHOTO_HEIGHT}px;
                    border:0; display:block;">
      </td>

      <!-- 30px spacer — dedicated column, never stripped by Outlook -->
      <td width="30" style="width:30px; padding:0;" >&nbsp;</td>

      <!-- Details column -->
      <td width="{details_width}" style="padding:0; vertical-align:top;" valign="top">
        <table width="{details_width}" cellpadding="0" cellspacing="0"
               style="font-family:Tahoma,sans-serif; background:transparent;">
          <tbody>

            <!-- Name -->
            <tr>
              <td style="padding:0 0 2px 0; vertical-align:top;" valign="top">
                <strong>
                  <span style="font-family:Tahoma,sans-serif;
                               color:{COLOR_NAME}; font-size:14pt;">
                    {name}
                  </span>
                </strong>
              </td>
            </tr>

            <!-- Designation -->
            <tr>
              <td style="padding:0 0 10px 0; vertical-align:top;" valign="top">
                <span style="font-family:Tahoma,sans-serif;
                             color:{COLOR_DESIGNATION}; font-size:10pt;
                             line-height:18px;">
                  {designation}
                </span>
              </td>
            </tr>

            <!-- Phone -->
            <tr>
              <td style="padding:0 0 10px 0; vertical-align:top; line-height:18px;"
                  valign="top">
                <span style="font-family:Tahoma,sans-serif;
                             color:{COLOR_NAME}; font-size:10pt;">
                  <b>M:</b> {phone}
                </span>
              </td>
            </tr>

            <!-- Company logo -->
            <tr>
              <td style="padding:0 0 8px 0; vertical-align:top;" valign="top">
                <a href="{COMPANY_WEBSITE}" target="_blank" rel="noopener"
                   style="text-decoration:none;">
                  <img src="{COMPANY_LOGO_URL}" width="190" border="0"
                       style="border:0; display:block;">
                </a>
              </td>
            </tr>

           <!-- Social icons: LinkedIn | Instagram | Blog -->
           <tr>
           <td style="padding:0; vertical-align:top;" valign="top">

    <a href="{LINKEDIN_URL}" target="_blank" rel="noopener"
       style="text-decoration:none; border:0; display:inline-block; line-height:0;">
      <img src="{LINKEDIN_ICON_URL}" width="28" height="28" border="0"
           style="border:0; width:28px; height:28px; margin-right:5px; display:block;">
    </a>

    <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener"
       style="text-decoration:none; border:0; display:inline-block; line-height:0;">
      <img src="{INSTAGRAM_ICON_URL}" width="28" height="28" border="0"
           style="border:0; width:28px; height:28px; margin-right:5px; display:block;">
    </a>

    <a href="{BLOG_URL}" target="_blank" rel="noopener"
       style="text-decoration:none; border:0; display:inline-block; line-height:0;">
      <img src="{BLOG_ICON_URL}" width="28" height="28" border="0"
           style="border:0; width:28px; height:28px; display:block;">
    </a>

  </td>
</tr>

          </tbody>
        </table>
      </td>
      <!-- end details -->

    </tr>
  </tbody>
</table>

</BODY>
</HTML>
"""

 
def build_signature_a(name, designation, phone, photo_src):
    """
    Dark Luxe variant.
 
    Layout  : Circular photo (gold ring) | gradient divider | details
    Theme   : Deep navy-purple (#1A1033) background, white serif name,
              gold designation, purple-to-gold vertical gradient divider.
    Photo   : Circular, PHOTO_WIDTH x PHOTO_HEIGHT, gold border ring.
    Details : Serif name -> gold uppercase designation -> phone ->
              company logo -> social icon pills (rounded squares).
    """
 
    details_width = 300
    divider_width = 2
    spacer_width  = 22      # gap on each side of the divider column
    total_width   = PHOTO_WIDTH + spacer_width + divider_width + spacer_width + details_width
 
    circle_radius = PHOTO_WIDTH // 2
 
    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
  <TITLE>Orbrick Email Signature — Dark Luxe</TITLE>
  <META content="text/html; charset=utf-8" http-equiv="Content-Type">
</HEAD>
<BODY style="margin:0; padding:0; font-family:Tahoma,sans-serif; font-size:10pt;">
 
<table width="{total_width}" cellpadding="0" cellspacing="0"
       style="font-family:Tahoma,sans-serif; background:#1A1033;
              border-radius:14px;">
  <tbody>
    <tr>
 
      <!-- Photo cell — circular with gold ring -->
      <td width="{PHOTO_WIDTH}"
          style="width:{PHOTO_WIDTH}px; padding:22px 0 22px 22px;
                 vertical-align:middle;"
          valign="middle">
        <div style="width:{PHOTO_WIDTH}px; height:{PHOTO_HEIGHT}px;
                    border-radius:{circle_radius}px;
                    border:3px solid #F5A623;
                    overflow:hidden; display:block;
                    line-height:0; font-size:0;">
          <img src="{photo_src}"
               width="{PHOTO_WIDTH}" height="{PHOTO_HEIGHT}" border="0"
               style="width:{PHOTO_WIDTH}px; height:{PHOTO_HEIGHT}px;
                      border-radius:{circle_radius}px; display:block; border:0;">
        </div>
      </td>
 
      <!-- Left spacer -->
      <td width="{spacer_width}" style="width:{spacer_width}px; padding:0;">&nbsp;</td>
 
      <!-- Gradient divider column -->
      <td width="{divider_width}"
          style="width:{divider_width}px; padding:16px 0; vertical-align:top;"
          valign="top">
        <!--[if !mso]><!-->
        <div style="width:{divider_width}px; height:80px;
                    background:linear-gradient(to bottom,#F5A623,#C46FD4);
                    font-size:0; line-height:0;">&nbsp;</div>
        <!--<![endif]-->
        <!--[if mso]>
        <v:rect xmlns:v="urn:schemas-microsoft-com:vml"
                style="width:{divider_width}pt; height:80pt;" filled="true" stroked="false">
          <v:fill type="gradient" color="#F5A623" color2="#C46FD4" angle="270"/>
        </v:rect>
        <![endif]-->
      </td>
 
      <!-- Right spacer -->
      <td width="{spacer_width}" style="width:{spacer_width}px; padding:0;">&nbsp;</td>
 
      <!-- Details column -->
      <td width="{details_width}"
          style="padding:22px 22px 22px 0; vertical-align:middle;"
          valign="middle">
        <table width="{details_width}" cellpadding="0" cellspacing="0"
               style="font-family:Georgia,serif; background:transparent;">
          <tbody>
 
            <!-- Name -->
            <tr>
              <td style="padding:0 0 4px 0; vertical-align:top;" valign="top">
                <strong>
                  <span style="font-family:Georgia,serif;
                               color:#FFFFFF; font-size:16pt;
                               letter-spacing:0.3px;">
                    {name}
                  </span>
                </strong>
              </td>
            </tr>
 
            <!-- Designation -->
            <tr>
              <td style="padding:0 0 12px 0; vertical-align:top;" valign="top">
                <span style="font-family:Tahoma,sans-serif;
                             color:{COLOR_DESIGNATION}; font-size:8pt;
                             font-weight:bold; letter-spacing:2px;
                             text-transform:uppercase;">
                  {designation}
                </span>
              </td>
            </tr>
 
            <!-- Phone -->
            <tr>
              <td style="padding:0 0 14px 0; vertical-align:top; line-height:18px;"
                  valign="top">
                <span style="font-family:Tahoma,sans-serif;
                             color:#B8A9D4; font-size:10pt;">
                  <b style="color:#F5A623;">M:</b> {phone}
                </span>
              </td>
            </tr>
 
            <!-- Company logo -->
            <tr>
              <td style="padding:0 0 14px 0; vertical-align:top;" valign="top">
                <a href="{COMPANY_WEBSITE}" target="_blank" rel="noopener"
                   style="text-decoration:none;">
                  <img src="{COMPANY_LOGO_URL}" width="160" border="0"
                       style="border:0; display:block;">
                </a>
              </td>
            </tr>
 
            <!-- Social icons -->
            <tr>
              <td style="padding:0; vertical-align:top;" valign="top">
                <table cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                  <tbody>
                    <tr>
                      <td style="padding:0 6px 0 0; vertical-align:top;" valign="top">
                        <a href="{LINKEDIN_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{LINKEDIN_ICON_URL}"
                               width="28" height="28" border="0"
                               style="border:0; width:28px; height:28px;
                                      border-radius:6px; display:block;">
                        </a>
                      </td>
                      <td style="padding:0 6px 0 0; vertical-align:top;" valign="top">
                        <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{INSTAGRAM_ICON_URL}"
                               width="28" height="28" border="0"
                               style="border:0; width:28px; height:28px;
                                      border-radius:6px; display:block;">
                        </a>
                      </td>
                      <td style="padding:0; vertical-align:top;" valign="top">
                        <a href="{BLOG_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{BLOG_ICON_URL}"
                               width="28" height="28" border="0"
                               style="border:0; width:28px; height:28px;
                                      border-radius:6px; display:block;">
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
 
          </tbody>
        </table>
      </td>
 
    </tr>
  </tbody>
</table>
 
</BODY>
</HTML>
"""
 
 
# ── Option B — Clean Minimal ──────────────────────────────────────────────────
 
def build_signature_b(name, designation, phone, photo_src):
    """
    Clean Minimal variant.
 
    Layout  : Accent bar | rounded-square photo | spacer | details
    Theme   : White card, 4px purple-to-gold left accent bar,
              hairline separator between name block and contact block.
    Photo   : PHOTO_WIDTH x PHOTO_HEIGHT, border-radius 10px.
    Details : Bold name -> gold designation -> hairline separator ->
              phone -> logo + social icons on the same row.
    """
 
    accent_width  = 4
    photo_pad     = 22
    spacer_width  = 18
    details_width = 300
    total_width   = accent_width + PHOTO_WIDTH + (photo_pad * 2) + spacer_width + details_width
 
    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
  <TITLE>Orbrick Email Signature — Clean Minimal</TITLE>
  <META content="text/html; charset=utf-8" http-equiv="Content-Type">
</HEAD>
<BODY style="margin:0; padding:0; font-family:Tahoma,sans-serif; font-size:10pt;">
 
<table width="{total_width}" cellpadding="0" cellspacing="0"
       style="font-family:Tahoma,sans-serif; background:#FFFFFF;
              border-radius:14px; border:1px solid #E8E3F0;">
  <tbody>
    <tr>
 
      <!-- Purple-to-gold accent bar — leftmost 4px column -->
      <td width="{accent_width}"
          style="width:{accent_width}px; padding:0;
                 vertical-align:top; border-radius:14px 0 0 14px;"
          valign="top">
        <!--[if !mso]><!-->
        <div style="width:{accent_width}px; height:130px;
                    background:linear-gradient(to bottom,#6B4FA0,#F5A623);
                    border-radius:14px 0 0 14px;
                    font-size:0; line-height:0;">&nbsp;</div>
        <!--<![endif]-->
        <!--[if mso]>
        <v:rect xmlns:v="urn:schemas-microsoft-com:vml"
                style="width:{accent_width}pt; height:130pt;"
                filled="true" stroked="false">
          <v:fill type="gradient" color="#6B4FA0" color2="#F5A623" angle="270"/>
        </v:rect>
        <![endif]-->
      </td>
 
      <!-- Photo cell -->
      <td width="{PHOTO_WIDTH}"
          style="width:{PHOTO_WIDTH}px;
                 padding:{photo_pad}px {photo_pad}px;
                 vertical-align:middle;"
          valign="middle">
        <img src="{photo_src}"
             width="{PHOTO_WIDTH}" height="{PHOTO_HEIGHT}" border="0"
             style="width:{PHOTO_WIDTH}px; height:{PHOTO_HEIGHT}px;
                    border-radius:10px; display:block; border:0;">
      </td>
 
      <!-- Spacer -->
      <td width="{spacer_width}" style="width:{spacer_width}px; padding:0;">&nbsp;</td>
 
      <!-- Details column -->
      <td width="{details_width}"
          style="padding:20px 20px 20px 0; vertical-align:middle;"
          valign="middle">
        <table width="{details_width}" cellpadding="0" cellspacing="0"
               style="font-family:Tahoma,sans-serif; background:transparent;">
          <tbody>
 
            <!-- Name -->
            <tr>
              <td style="padding:0 0 3px 0; vertical-align:top;" valign="top">
                <strong>
                  <span style="font-family:Tahoma,sans-serif;
                               color:{COLOR_NAME}; font-size:14pt;
                               letter-spacing:0.2px;">
                    {name}
                  </span>
                </strong>
              </td>
            </tr>
 
            <!-- Designation -->
            <tr>
              <td style="padding:0 0 10px 0; vertical-align:top;" valign="top">
                <span style="font-family:Tahoma,sans-serif;
                             color:{COLOR_DESIGNATION}; font-size:10pt;
                             font-weight:bold;">
                  {designation}
                </span>
              </td>
            </tr>
 
            <!-- Hairline separator -->
            <tr>
              <td style="padding:0 0 0 0; height:1px; font-size:0; line-height:0;
                         border-bottom:1px solid #E8E3F0;"
                  valign="top">&nbsp;</td>
            </tr>
 
            <!-- Phone -->
            <tr>
              <td style="padding:10px 0 14px 0; vertical-align:top; line-height:18px;"
                  valign="top">
                <span style="font-family:Tahoma,sans-serif;
                             color:#5C5C7A; font-size:10pt;">
                  <b style="color:{COLOR_NAME};">M:</b> {phone}
                </span>
              </td>
            </tr>
 
            <!-- Logo + social icons on the same row -->
            <tr>
              <td style="padding:0; vertical-align:middle;" valign="middle">
                <table cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                  <tbody>
                    <tr>
                      <td style="padding:0 16px 0 0; vertical-align:middle;"
                          valign="middle">
                        <a href="{COMPANY_WEBSITE}" target="_blank" rel="noopener"
                           style="text-decoration:none;">
                          <img src="{COMPANY_LOGO_URL}" width="130" border="0"
                               style="border:0; display:block;">
                        </a>
                      </td>
                      <td style="padding:0 6px 0 0; vertical-align:middle;"
                          valign="middle">
                        <a href="{LINKEDIN_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{LINKEDIN_ICON_URL}"
                               width="26" height="26" border="0"
                               style="border:0; width:26px; height:26px;
                                      border-radius:5px; display:block;">
                        </a>
                      </td>
                      <td style="padding:0 6px 0 0; vertical-align:middle;"
                          valign="middle">
                        <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{INSTAGRAM_ICON_URL}"
                               width="26" height="26" border="0"
                               style="border:0; width:26px; height:26px;
                                      border-radius:5px; display:block;">
                        </a>
                      </td>
                      <td style="padding:0; vertical-align:middle;"
                          valign="middle">
                        <a href="{BLOG_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{BLOG_ICON_URL}"
                               width="26" height="26" border="0"
                               style="border:0; width:26px; height:26px;
                                      border-radius:5px; display:block;">
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
 
          </tbody>
        </table>
      </td>
 
    </tr>
  </tbody>
</table>
 
</BODY>
</HTML>
"""
 
 
# ── Option C — Split Block ────────────────────────────────────────────────────
 
def build_signature_c(name, designation, phone, photo_src):
    """
    Split Block variant.
 
    Layout  : Purple sidebar (photo + social icons) | white right panel (details)
    Theme   : Deep purple (#5B3A9E) left panel, off-white (#FAFAFA) right panel,
              gold uppercase designation, circular photo with translucent white ring.
    Photo   : PHOTO_WIDTH x PHOTO_HEIGHT, circular (border-radius 50%),
              semi-transparent white border.
    Details : Bold name -> gold uppercase designation ->
              bullet-dot + phone -> company logo.
    Socials : Sit inside the purple sidebar below the photo.
    """
 
    sidebar_width = 130
    details_width = 290
    total_width   = sidebar_width + details_width
    circle_radius = PHOTO_WIDTH // 2
 
    return f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
  <TITLE>Orbrick Email Signature — Split Block</TITLE>
  <META content="text/html; charset=utf-8" http-equiv="Content-Type">
</HEAD>
<BODY style="margin:0; padding:0; font-family:Tahoma,sans-serif; font-size:10pt;">
 
<table width="{total_width}" cellpadding="0" cellspacing="0"
       style="font-family:Tahoma,sans-serif;
              border-radius:14px; overflow:hidden;
              border:1px solid #E2D9F3;">
  <tbody>
    <tr>
 
      <!-- Purple sidebar -->
      <td width="{sidebar_width}"
          style="width:{sidebar_width}px; background:#5B3A9E;
                 padding:24px 12px; vertical-align:middle;
                 border-radius:14px 0 0 14px;"
          valign="middle">
        <table width="106" cellpadding="0" cellspacing="0"
               style="margin:0 auto;">
          <tbody>
 
            <!-- Circular photo -->
            <tr>
              <td style="padding:0 0 14px 0; text-align:center;"
                  align="center" valign="top">
                <div style="width:{PHOTO_WIDTH}px; height:{PHOTO_HEIGHT}px;
                            border-radius:{circle_radius}px;
                            border:3px solid rgba(255,255,255,0.30);
                            overflow:hidden; display:inline-block;
                            line-height:0; font-size:0;">
                  <img src="{photo_src}"
                       width="{PHOTO_WIDTH}" height="{PHOTO_HEIGHT}" border="0"
                       style="width:{PHOTO_WIDTH}px; height:{PHOTO_HEIGHT}px;
                              border-radius:{circle_radius}px;
                              display:block; border:0;">
                </div>
              </td>
            </tr>
 
            <!-- Social icons in sidebar -->
            <tr>
              <td style="padding:0; text-align:center;"
                  align="center" valign="top">
                <table cellpadding="0" cellspacing="0"
                       style="margin:0 auto; border-collapse:collapse;">
                  <tbody>
                    <tr>
                      <td style="padding:0 5px 0 0; vertical-align:top;"
                          valign="top">
                        <a href="{LINKEDIN_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{LINKEDIN_ICON_URL}"
                               width="24" height="24" border="0"
                               style="border:0; width:24px; height:24px;
                                      border-radius:5px;
                                      background:rgba(255,255,255,0.15);
                                      display:block;">
                        </a>
                      </td>
                      <td style="padding:0 5px 0 0; vertical-align:top;"
                          valign="top">
                        <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{INSTAGRAM_ICON_URL}"
                               width="24" height="24" border="0"
                               style="border:0; width:24px; height:24px;
                                      border-radius:5px;
                                      background:rgba(255,255,255,0.15);
                                      display:block;">
                        </a>
                      </td>
                      <td style="padding:0; vertical-align:top;" valign="top">
                        <a href="{BLOG_URL}" target="_blank" rel="noopener"
                           style="text-decoration:none; border:0;
                                  display:inline-block; line-height:0;">
                          <img src="{BLOG_ICON_URL}"
                               width="24" height="24" border="0"
                               style="border:0; width:24px; height:24px;
                                      border-radius:5px;
                                      background:rgba(255,255,255,0.15);
                                      display:block;">
                        </a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
 
          </tbody>
        </table>
      </td>
      <!-- end sidebar -->
 
      <!-- White right panel -->
      <td width="{details_width}"
          style="width:{details_width}px; background:#FAFAFA;
                 padding:22px 24px; vertical-align:middle;
                 border-radius:0 14px 14px 0;"
          valign="middle">
        <table width="{details_width - 48}" cellpadding="0" cellspacing="0"
               style="font-family:Tahoma,sans-serif; background:transparent;">
          <tbody>
 
            <!-- Name -->
            <tr>
              <td style="padding:0 0 3px 0; vertical-align:top;" valign="top">
                <strong>
                  <span style="font-family:Tahoma,sans-serif;
                               color:#1C0F40; font-size:15pt;
                               letter-spacing:-0.3px;">
                    {name}
                  </span>
                </strong>
              </td>
            </tr>
 
            <!-- Designation -->
            <tr>
              <td style="padding:0 0 14px 0; vertical-align:top;" valign="top">
                <span style="font-family:Tahoma,sans-serif;
                             color:{COLOR_DESIGNATION}; font-size:8pt;
                             font-weight:bold; letter-spacing:2px;
                             text-transform:uppercase;">
                  {designation}
                </span>
              </td>
            </tr>
 
            <!-- Phone with bullet dot -->
            <tr>
              <td style="padding:0 0 16px 0; vertical-align:middle;"
                  valign="middle">
                <table cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                  <tbody>
                    <tr>
                      <td style="padding:0 7px 0 0; vertical-align:middle;"
                          valign="middle">
                        <div style="width:7px; height:7px;
                                    border-radius:4px;
                                    background:#5B3A9E;
                                    font-size:0; line-height:0;">&nbsp;</div>
                      </td>
                      <td style="padding:0; vertical-align:middle;"
                          valign="middle">
                        <span style="font-family:Tahoma,sans-serif;
                                     color:#6A6280; font-size:10pt;
                                     line-height:18px;">
                          {phone}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </td>
            </tr>
 
            <!-- Company logo -->
            <tr>
              <td style="padding:0; vertical-align:top;" valign="top">
                <a href="{COMPANY_WEBSITE}" target="_blank" rel="noopener"
                   style="text-decoration:none;">
                  <img src="{COMPANY_LOGO_URL}" width="150" border="0"
                       style="border:0; display:block;">
                </a>
              </td>
            </tr>
 
          </tbody>
        </table>
      </td>
      <!-- end right panel -->
 
    </tr>
  </tbody>
</table>
 
</BODY>
</HTML>
"""

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    photo_src = image_to_base64(IMAGE_PATH)

    if photo_src is None:
        # Fallback to the original hosted placeholder
        photo_src = "https://orbrick.com/wp-content/uploads/2024/08/sigImage.png"

    html = build_signature(
        name        = FULL_NAME,
        designation = DESIGNATION,
        phone       = PHONE,
        photo_src   = photo_src,
    )
    html1 = build_signature_a(
            name        = FULL_NAME,
            designation = DESIGNATION,
            phone       = PHONE,
            photo_src   = photo_src,
        )
    html2 = build_signature_b(
            name        = FULL_NAME,
            designation = DESIGNATION,
            phone       = PHONE,
            photo_src   = photo_src,
        )
    html3 = build_signature_c(
            name        = FULL_NAME,
            designation = DESIGNATION,
            phone       = PHONE,
            photo_src   = photo_src,
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    with open(OUTPUT_FILE1, "w", encoding="utf-8") as f:
            f.write(html1)
    with open(OUTPUT_FILE2, "w", encoding="utf-8") as f:
            f.write(html2)
    with open(OUTPUT_FILE3, "w", encoding="utf-8") as f:
            f.write(html3)

    print(f"Signature saved to: {os.path.abspath(OUTPUT_FILE)}")
    print("Open in a browser to preview, then paste into Outlook.")


if __name__ == "__main__":
    main()