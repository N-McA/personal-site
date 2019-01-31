---
title: "Enforcing spatial regularity in CPPNs"
date: 2019-01-31
draft: false
math: true
tags: ["#diffentiable-programming", "#cnns", "#art"]
---

Some readers may be familiar with [this work](https://distill.pub/2018/differentiable-parameterizations/) on differentiable image parameterisations. It's really, very cool, producing incredible images like the following:

![Pretty CNN Visualisation](enforcing-spatial-regularity.example.jpeg)

These images are not only pretty, but offer some great insights into how neural networks work. In this post I'll briefly outline how they work before illustrating some simple extensions that allow you to create arbitrary geometric patterns, tilings and moving images.

## What's a CPPN?

So CPPN is apparently a "Compositional Pattern Producing Network". I'm not a fan of the name. Essentially, a CPPN is a function from 2D coordinates into a color space. For example the function

```py
def silly_cppn(x: float, y: float, theta: float):
	# return 0-1 RGB
	redness = sigmoid(x * theta)
	return redness, 0, 0
```

Is a CPPN. But it's not very expressive, and it doesn't do anything exciting (fun game: what does this one look like?).

In the excellent distill post above, they note that you can have an arbitrary multi-layer perceptron as your CPPN, provided the input is 2D and the output is 3D. Further, suppose you have a CNN which takes 3D tensor input with two spatial dimensions and one color dimension - you can apply your CPPN at every point in the spatial grid in order to get a 2D image of the appropriate size, and then feed this directly into the CNN.

![CPPN_Stack](enforcing-spatial-regularity.CPPN_Stack.svg)