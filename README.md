![Made-love][made-love-shield]
[![LinkedIn][linkedin-shield]][linkedin-url]

# Deoldify-image-coloring
[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1OpIIpDUA-M9QD-PExdYzXY3FJ8qG3l9i?usp=sharing)

![Coloring result][product-screenshot]

Google colab notebook for coloring black and white images by means of the use of DeOldify's trained network.

For coloring images, go to Google colab and introduce the following link: https://github.com/davertor/Deoldify-image-coloring

## Description

DeOldify is a tool that colors digitalized black and white photos. At this moment, DeOldify represents the state of the art in image coloring.

This tool was developed by Jason Antic, who trained an AI based on a GAN architecture, called NoGan, with a collection of color photos and their corresponding black and white version. 

While black and white photos are a combination of grayscale pixels that can take a value between 0-255; in color photos each pixel is a combination of three values, red, green and blue where each of them can take a value from 0 to 255. Therefore, the NoGan network has to achieve triple the information it has on the photo to get a color photo.The result is that the network has learned to color black and white photos; filling in the missing information.

## Instructions
For working with this notebook, clone repo and execute it in your favourite Notebook environment, or open Google's colab and introduce the following link: https://github.com/davertor/Deoldify-image-coloring

## References
* [Deoldify](https://deoldify.ai/)

## Contact
* [@davertor](https://github.com/davertor) 

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/di_stefano_merged.png
[linkedin-url]: https://linkedin.com/daniel-verdu-torres

[made-love-shield]: https://img.shields.io/badge/-Made%20with%20love%20❤️-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/badge/License-GNU-brightgreen.svg?style=for-the-badge
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-darkblue.svg?style=for-the-badge&logo=linkedin
[twitter-shield]: https://img.shields.io/badge/-Twitter-blue.svg?style=for-the-badge&logo=twitter


