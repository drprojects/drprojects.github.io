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

<p class="intro">{{ p.summary | markdownify | remove: "<p>" | remove: "</p>" }}</p>

{% comment %}
  Research interests as "methods / for / applications", on three lines. Each
  row wraps on its own if the viewport is narrow, so the connector always sits
  between the two groups and can never strand at the end of a line.
{% endcomment %}
{% assign methods = p.interests_web | where: "group", "methods" %}
{% assign applications = p.interests_web | where: "group", "applications" %}
<div class="interests">
  <div class="interests__row">
    {%- for i in methods -%}
      <span class="interests__chip">{{ i.emoji }}&nbsp;{{ i.short | default: i.label }}</span>
    {%- endfor -%}
  </div>
  <div class="interests__for">for</div>
  <div class="interests__row">
    {%- for i in applications -%}
      <span class="interests__chip">{{ i.emoji }}&nbsp;{{ i.short | default: i.label }}</span>
    {%- endfor -%}
  </div>
</div>

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
