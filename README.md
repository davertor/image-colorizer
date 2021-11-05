![Made-love][made-love-shield]
[![LinkedIn][linkedin-shield]][linkedin-url]

# Image colorizer
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/your_user/your_space)
[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1OpIIpDUA-M9QD-PExdYzXY3FJ8qG3l9i?usp=sharing)

![Coloring result][product-screenshot]

Streamlit app and google colab notebook have been developed for coloring black and white images by means of the use of DeOldify's trained networks. You can check original implementation at the following [Github](https://github.com/jantic/DeOldify)

For coloring images, you have two options
* Click on Hugging face spaces button above of the image and upload your images
* Click on Google colab button and execute the cells

## About the tool

DeOldify is a tool that colors digitalized black and white photos. At this moment, DeOldify represents the state of the art in image coloring.

This tool was developed by Jason Antic, who trained an AI based on a GAN architecture, called NoGan, with a collection of color photos and their corresponding black and white version. 

While black and white photos are a combination of grayscale pixels that can take a value between 0-255; in color photos each pixel is a combination of three values, red, green and blue where each of them can take a value from 0 to 255. Therefore, the NoGan network has to achieve triple the information it has on the photo to get a color photo.The result is that the network has learned to color black and white photos; filling in the missing information.

## Contact
* Author - Daniel Verdú Torres
* Linkedin - [Linkedin](https://linkedin.com/daniel-verdu-torres) 
* Github - [@davertor](https://github.com/davertor)

## References
* [Deoldify](https://deoldify.ai/)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/di_stefano_merged.png
[linkedin-url]: https://linkedin.com/daniel-verdu-torres
[github-url]: https://github.com/davertor

[made-love-shield]: https://img.shields.io/badge/-Made%20with%20love%20❤️-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/badge/License-GNU-brightgreen.svg?style=for-the-badge
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-darkblue.svg?style=for-the-badge&logo=linkedin
[github-shield]: https://img.shields.io/badge/-Github-black.svg?style=for-the-badge&logo=github
[twitter-shield]: https://img.shields.io/badge/-Twitter-blue.svg?style=for-the-badge&logo=twitter


