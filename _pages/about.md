---
permalink: /
title: "Damien Robert"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

<p>
    As a postdoctoral researcher at the <a href="https://dm3l.uzh.ch/en/wegner">EcoVision</a> lab at 
    <a href="https://www.uzh.ch/en.html">University of Zurich</a>, I collaborate with 
    <a href="https://dm3l.uzh.ch/wegner/group-leader">Jan Dirk Wegner</a> to design deep learning methods for remote 
    sensing and environmental applications.
    Before joining UZH, I completed my PhD on <i>"Efficient Learning on Large-Scale 3D Point Clouds"</i> at 
    <a href="https://www.ign.fr">IGN</a> and <a href="https://www.engie.com">ENGIE</a>, under the supervision of 
    <a href="https://loiclandrieu.com/">Loïc Landrieu</a> and 
    <a href="https://www.umr-lastig.fr/bruno-vallet/">Bruno Vallet</a>.
    <br><br>
    You like point clouds ☁️? You like trees 🌳? You like satellites 🛰️? You like me 🤗
</p>

{% if site.news %}
News
------
{% for post in site.news reversed %}
    {% include archive-single-news.html %}
{% endfor %}
{% endif %}

{% if site.publications %}
Publications
------
{% for post in site.publications reversed %}
    {% include archive-single-publication.html %}
{% endfor %}
{% endif %}
