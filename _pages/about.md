---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

I'm a first-year Ph.D. student in <a href="https://gaplab.cuhk.edu.cn/">GAP Lab</a>, CUHK(SZ), supervised by <a href="https://scholar.google.com/citations?user=z-rqsR4AAAAJ&hl=zh-CN">Prof.Xiaoguang Han</a>. 

My research interest includes multimodal generation. Please email me if you want to collaborate for academic research or have any questions.

{% include_relative includes/news.md %}
{% include_relative includes/pub.md %}