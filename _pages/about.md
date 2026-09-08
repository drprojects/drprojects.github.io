---
permalink: /
title: "Damien Robert"
author_profile: true
---

{% comment %}
  Everything here is rendered from _data/. The intro in profile.yml is the same
  one the PDF CV uses, so there is a single source for it.
{% endcomment %}
{% assign p = site.data.profile %}
{% include base_path %}

<p>
  {{ p.summary | markdownify | remove: "<p>" | remove: "</p>" }}
  <br><br>
  My research interests cover
  {% for i in p.interests_web %}{{ i.label }}&nbsp;{{ i.emoji }}{% if forloop.last %}.{% elsif forloop.rindex == 2 %}, and {% else %}, {% endif %}{% endfor %}
</p>

{% comment %} ---------- distinctions: pulled from _data/awards.yml ---------- {% endcomment %}
{% if site.data.awards %}
<div class="awards-strip">
  {% assign featured = site.data.awards | sort: 'weight' | reverse %}
  {% for a in featured %}
    <div class="award-card">
      <div class="award-card__year">{{ a.year }}</div>
      <div class="award-card__title">{{ a.title }}</div>
      {% if a.venue %}<div class="award-card__venue">{{ a.venue }}</div>{% endif %}
      {% if a.description %}<div class="award-card__note">{{ a.description }}</div>{% endif %}
    </div>
  {% endfor %}
</div>
{% endif %}

{% comment %} ---------------- stats: all computed from _data ---------------- {% endcomment %}
{% capture country_list %}{% for t in site.data.talks %}{% if t.location and t.location != "Virtual" and t.location != "YouTube" %}{{ t.location | split: ", " | last }}|{% endif %}{% endfor %}{% endcapture %}
{% assign countries = country_list | split: "|" | uniq %}
{% assign star_total = 0 %}
{% for pair in site.data.github_stars %}
  {% if pair[0] != "_fetched" %}{% assign star_total = star_total | plus: pair[1].stars %}{% endif %}
{% endfor %}

<div class="stats-band">
  <a class="stat" href="{{ base_path }}/publications/">
    <span class="stat__num">{{ site.data.publications | size }}</span>
    <span class="stat__label">publications</span>
  </a>
  <a class="stat" href="{{ base_path }}/talks/">
    <span class="stat__num">{{ site.data.talks | size }}</span>
    <span class="stat__label">talks given</span>
  </a>
  {% if star_total > 0 %}
  <a class="stat" href="{{ base_path }}/code/">
    <span class="stat__num">{{ star_total }}</span>
    <span class="stat__label">GitHub stars</span>
  </a>
  {% endif %}
  <span class="stat">
    <span class="stat__num">{{ countries | size }}</span>
    <span class="stat__label">countries presented in</span>
  </span>
</div>

{% comment %} ------------------------------- news --------------------------- {% endcomment %}
{% if site.data.news %}
<h2 class="home-heading">News</h2>
{% for item in site.data.news limit: 8 %}
  {% include archive-single-news.html item=item %}
{% endfor %}

<p class="more-link-wrap">
  <a class="more-link" href="{{ base_path }}/news/">Browse all {{ site.data.news | size }} news items</a>
</p>
{% endif %}
