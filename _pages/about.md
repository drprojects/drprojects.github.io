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

<ul class="mb-0" style="list-style-type:none;padding-left:0;">
  <li><span class="label label-info">11/2024</span> Defending my <a href="#theses">habilitation thesis</a>, and using the opportunity to organize <a href="./hdr/index.html">a workshop on Nov 21</a>.</li>
  <li><span class="label label-info">01/2024</span> Busy with <a href="https://eccv2024.ecva.net/">ECCV'24</a> Program Chairing... Update: Done as of 10/2024!</li>
  <li><span class="label label-warning">05/2023</span> Received a <a href="https://research.google/outreach/research-scholar-program/recipients/?category=2023">Google Research Scholar</a> award.</li>
  <li><span class="label label-warning">04/2023</span> Spent two wonderful weeks in <a href="https://ps.is.tuebingen.mpg.de/">MPI</a> Tübingen.</li>
</ul>


<ul class="mb-0" style="list-style-type:none;padding-left:0;">
  <li><span class="label label-primary">Fall&emsp; 2024</span> <a href="teaching/recvis24">Object recognition and computer vision</a>, Main Lecturer - MVA Masters</li>
  <li><span class="label label-success">Fall&emsp; 2023</span> <a href="teaching/recvis23">Object recognition and computer vision</a>, Main Lecturer - MVA Masters</li>
  <li><span class="label label-success">Fall&emsp; 2023</span> <a href="https://moodle.psl.eu/course/view.php?id=13982">Introduction to computer vision</a>, Lecturer - M1, École normale supérieure </li>
</ul>


<!-- New style rendering if publication categories are defined -->
{% for post in site.publications reversed %}
    {% include archive-single-publication.html %}
{% endfor %}