---
permalink: /
title: "Damien Robert"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% comment %}
  Bio and interests come from _data/profile.yml, which also feeds the PDF CV.
{% endcomment %}
{% assign p = site.data.profile %}

<p>
  {{ p.summary.web }}
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

<p style="margin-top:1em;"><a href="{{ base_path }}/news/">All news →</a></p>
{% endif %}
