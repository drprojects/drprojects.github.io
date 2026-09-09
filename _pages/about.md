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

<p>
  {{ p.summary | markdownify | remove: "<p>" | remove: "</p>" }}
  <br><br>
  My research interests cover
  {% for i in p.interests_web %}{{ i.label }}&nbsp;{{ i.emoji }}{% if forloop.last %}.{% elsif forloop.rindex == 2 %}, and {% else %}, {% endif %}{% endfor %}
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
