---
permalink: /
title: "Damien Robert"
author_profile: true
---

{% comment %}
  The intro comes from _data/profile.yml and is the same paragraph the PDF CV
  uses, so there is a single source for it.
{% endcomment %}
{% assign p = site.data.profile %}
{% include base_path %}

<p>{{ p.summary | markdownify | remove: "<p>" | remove: "</p>" }}</p>

{% comment %}
  Research interests as "methods FOR applications". Laid out in normal inline
  flow, not flex, so the line breaks where the text would: the connector is
  glued to the first application chip, which means a break can happen *before*
  "for" but never after it. No media query — it stays on one line whenever it
  fits, and only splits when the viewport actually demands it.
{% endcomment %}
{% assign methods = p.interests_web | where: "group", "methods" %}
{% assign applications = p.interests_web | where: "group", "applications" %}
<p class="interests">
  {%- for i in methods -%}
    <span class="interests__chip">{{ i.emoji }}&nbsp;{{ i.short | default: i.label }}</span>
  {%- endfor -%}
  {%- for i in applications -%}
    {%- if forloop.first -%}
      <span class="interests__join"><span class="interests__for">for</span><span class="interests__chip">{{ i.emoji }}&nbsp;{{ i.short | default: i.label }}</span></span>
    {%- else -%}
      <span class="interests__chip">{{ i.emoji }}&nbsp;{{ i.short | default: i.label }}</span>
    {%- endif -%}
  {%- endfor -%}
</p>

{% if site.data.news %}
News
------
{% for item in site.data.news limit: 8 %}
  {% include archive-single-news.html item=item %}
{% endfor %}

<p class="more-link-wrap">
  <a class="more-link" href="{{ base_path }}/news/">All news items</a>
</p>
{% endif %}
